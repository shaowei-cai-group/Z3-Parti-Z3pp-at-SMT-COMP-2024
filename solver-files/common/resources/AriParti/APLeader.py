
import os
import time
import logging
import subprocess
from datetime import datetime
from mpi4py import MPI
from APTask import Task

class Leader():
    def get_current_time(self):
        return time.time() - self.start_time
    
    def init_params(self, cmd_args):
        self.input_file_path: str = cmd_args.file
        self.partitioner_path: str = cmd_args.partitioner
        self.solver_path: str = cmd_args.solver
        self.max_running_tasks: int = cmd_args.max_running_tasks
        self.time_limit: int = cmd_args.time_limit
        self.temp_folder_path = cmd_args.temp_dir
        self.output_dir_path: str = cmd_args.output_dir
        self.run_mode = cmd_args.run_mode
        
        assert(self.run_mode in ['parallel', 'distributed'])
        
        if not os.path.exists(self.input_file_path):
            print('file-not-found')
            assert(False)
        
        self.instance_name: str = self.input_file_path[ \
            self.input_file_path.rfind('/') + 1: self.input_file_path.find('.smt2')]
    
    def init_logging(self):
        if self.output_dir_path != None:
            logging.basicConfig(format='%(relativeCreated)d - %(levelname)s - %(message)s', 
                    filename=f'{self.output_dir_path}/log', level=logging.INFO)
        self.start_time = time.time()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.write_line_to_log(f'start-time {formatted_time} ({self.start_time})')

    def init_partitioner_comm(self):
        self.need_communicate = True
        
        write_pipe_path = f'{self.temp_folder_path}/master-to-partitioner'
        read_pipe_path = f'{self.temp_folder_path}/partitioner-to-master'
        
        temp_file = open(read_pipe_path, "w")
        temp_file.close()
        
        self.write_pipe = open(write_pipe_path, 'w')
        self.read_pipe = open(read_pipe_path, 'r')
        
        self.start_time = time.time()
        self.write_line_to_partitioner(f"start-time {self.start_time}")
    
    def write_line_to_log(self, data: str):
        logging.info(data)
        
    def write_line_to_partitioner(self, data: str):
        curr_time: int = int(time.time() - self.start_time)
        line: str = f'{curr_time} {data}\n'
        self.write_pipe.write(line)
        self.write_pipe.flush()
        self.write_line_to_log(data)
    
    def read_line_from_partitioner(self):
        res = self.read_pipe.readline().strip('\n')
        return res
    
    def init(self, comm_world: MPI.COMM_WORLD, cmd_args):
        
        self.comm_world = comm_world
        self.num_processes = comm_world.Get_size()
        self.idle_workers = set(range(1, self.num_processes))
        self.init_params(cmd_args)
        self.state_tasks_dict = {
            'waiting': [],
            'solving': [],
            'ended': [],
        }
        self.task_head = 0
        self.id2task = {}
        self.tasks = []
        self.result = 'undefined'
        self.reason = -3
        self.done = False
        
        self.max_unended_tasks = self.max_running_tasks + self.max_running_tasks // 3 + 1
        
        self.base_run_cnt = 0
        # self.solve_ori_flag = False
        self.solve_ori_flag = True
        
        if not os.path.exists(self.temp_folder_path):
            os.system(f'mkdir -p {self.temp_folder_path}')
            os.system(f'mkdir -p {self.temp_folder_path}/tasks')
        
        # ##//linxi debug
        # print(self.temp_folder_path)
        # print(f'{self.output_dir_path}/log')
        
        if self.output_dir_path != None:
            if not os.path.exists(self.output_dir_path):
                os.system(f'mkdir -p {self.output_dir_path}')
        
        self.init_logging()
        logging.info(f'temp_folder_path: {self.temp_folder_path}')
        
        self.init_partitioner_comm()
        
    def make_task(self, id, pid, is_unsat):
        
        parent: Task = None
        if (pid != -1):
            parent = self.id2task[pid]
        t = Task(None, id, parent, self.get_current_time())
        
        if is_unsat:
            self.update_task_state(t, 'unsat')
            t.reason = -1
            if parent != None:
                self.push_up(parent, t.id)
        else:
            self.update_task_state(t, 'waiting')
        
        if parent != None:
            if t.state != 'unsat' and parent.state == 'unsat':
                self.propagate_unsat(t, parent.reason)
            parent.subtasks.append(t)
        
        # self.write_line_to_log(f'make-task {t}')
        
        self.id2task[id] = t
        self.tasks.append(t)
    
    def parse_line(self, line: str):
        words = line.split(' ')
        op = words[1]
        if op == 'debug-info':
            remains = " ".join(words[2: ])
            self.write_line_to_log(f'partitioner-debug-info {remains}')
        elif op in ['new-task', 'unsat-task']:
            id = int(words[2])
            pid = int(words[3])
            if op == 'new-task':
                is_unsat = False
            else:
                is_unsat = True
            self.make_task(id, pid, is_unsat)
        else:
            assert(False)

    def read_parse_line(self):
        line = self.read_line_from_partitioner()
        if line == "":
            return False
        self.parse_line(line)
        return True
        
    def communicate_with_partitioner(self):
        while self.read_parse_line():
            pass
        if self.partitioner.state != 'solving':
            self.write_line_to_log(f'partitioner-done {self.partitioner.state}')
            self.need_communicate = False
    
    def terminate(self, wid):
        self.comm_world.send(None, dest=wid, tag=1)
    
    def propagate_unsat(self, t: Task, reason):
        assert(t.state != 'unsat')
        self.update_task_state(t, 'unsat')
        t.reason = reason
        self.write_line_to_partitioner(f'unsat-node {t.id}')
    
    def push_up(self, t: Task, reason):
        # only 'unsat' 'unknown' need push up
        if t.state == 'unsat':
            return
        if len(t.subtasks) == 2 and \
           t.subtasks[0].state == 'unsat' and \
           t.subtasks[1].state == 'unsat':
            self.propagate_unsat(t, reason)
            self.write_line_to_log(f'unsat-by-children {t.id} {t.subtasks[0].id} {t.subtasks[1].id}')
            if t.parent != None:
                self.push_up(t.parent, reason)
    
    def push_down(self, t: Task, reason):
        # only 'unsat' need push up
        if t.state == 'unsat':
            return
        self.propagate_unsat(t, reason)
        self.write_line_to_log(f'unsat-by-ancestor {t.id} {reason}')
        for st in t.subtasks:
            self.push_down(st, reason)

    def need_terminate(self, t: Task):
        if t.id <= 0:
            return False
        num_st = len(t.subtasks)
        st_end = 0
        if num_st > 0 and t.subtasks[0].state in ['solving', 'unsat', 'terminated']:
            st_end += 1
        if num_st > 1 and t.subtasks[1].state in ['solving', 'unsat', 'terminated']:
            st_end += 1
        
        if st_end == 0:
            return False
        if st_end == 1 and self.get_current_time() - t.time_infos['solving'] < 200.0:
            return False
        if st_end == 2 and self.get_current_time() - t.time_infos['solving'] < 100.0:
            return False
        return True
    
    def free_worker(self, id):
        # while self.comm_world.Iprobe(source=id):
        #     self.comm_world.recv(source=id)
        self.idle_workers.add(id)
    
    def update_task_state(self, t: Task, new_state: str):
        self.write_line_to_log(f'update-state {t.id} {new_state}')
        t.state = new_state
        if new_state == 'unsat':
            if t.p != None:
                self.write_line_to_log(f'terminate (task-{t.id}, {t.state}) to worker-{t.p}')
                self.terminate(t.p)
                self.free_worker(t.p)
                t.p = None
        
        if new_state in ['sat', 'unsat', 'unknown', 'terminated']:
            new_state = 'ended'
        self.state_tasks_dict[new_state].append(t)
        t.time_infos[new_state] = self.get_current_time()
    
    def check_process_state(self, wid, tid, running_state):
        while self.comm_world.Iprobe(source=wid):
            data = self.comm_world.recv(source=wid)
            cur_tid, result, logs = data
            self.write_line_to_log(f'### check_process_state ###')
            self.write_line_to_log(f'worker-{wid}')
            self.write_line_to_log(f'task-{tid}, current-{cur_tid}')
            self.write_line_to_log(f'running_state: {running_state}')
            self.write_line_to_log(f'result {result}')
            for log in logs:
                self.write_line_to_log(f'logs: {log}')
            if cur_tid == tid:
                self.write_line_to_log(f'result accepted!')
                return result
            else:
                self.write_line_to_log(f'result rejected!')
        return running_state
    
    def terminate_task(self, t: Task):
        t.state = 'terminated'
        if t.p != None:
            self.terminate(t.p)
            self.free_worker(t.p)
            t.p = None
        self.write_line_to_partitioner(f'terminate-node {t.id}')
    
    # True for still running
    def check_solving_state(self, t: Task):
        if t.state in ['unsat', 'unknown', 'terminated']:
            return False

        sta = self.check_process_state(t.p, t.id, 'solving')
        
        if sta == 'solving':
            return True
            # if self.need_terminate(t):
            #     self.update_task_state(t, 'terminated')
            #     self.terminate_task(t)
            #     return False
            # else:
            #     return True
        
        self.free_worker(t.p)
        t.p = None
        
        if sta == 'sat':
            self.result = 'sat'
            self.reason = t.id
            self.done = True
            self.write_line_to_log(f'sat-task {t.id}')
            return False
        
        t.reason = t.id
        if sta == 'unsat':
            self.update_task_state(t, 'unsat')
            self.write_line_to_partitioner(f'unsat-node {t.id}')
            if t.parent != None:
                self.push_up(t.parent, t.id)
            root_task: Task = self.tasks[0]
            if root_task.state == 'unsat':
                self.result = 'unsat'
                self.reason = root_task.reason
                self.done = True
                self.write_line_to_log(f'unsat-root-task {root_task.reason}')
                return False
            for st in t.subtasks:
                self.push_down(st, t.id)
        else:
            self.update_task_state(t, 'unknown')
            self.write_line_to_partitioner(f'unknown-node {t.id} {sta}')
        
        return False
    
    def assign_task(self, task_id, instance_data):
        worker_id = self.idle_workers.pop()
        self.write_line_to_log(f'assign task-{task_id} to worker-{worker_id}')
        send_data = (task_id, instance_data)
        self.comm_world.send(send_data, dest=worker_id, tag=0)
        return worker_id
    
    def solve_task(self, t: Task):
        instance_path = f'{self.temp_folder_path}/tasks/task-{t.id}.smt2'
        cmd =  [self.solver_path,
                instance_path,
            ]
        self.write_line_to_log('exec-command {}'.format(' '.join(cmd)))
        
        if self.run_mode == 'parallel':
            instance_data = None
        else:
            with open(instance_path, 'br') as file:
                instance_data = file.read()
        
        t.p = self.assign_task(t.id, instance_data)
        
        self.update_task_state(t, 'solving')
        self.write_line_to_log(f'run-task {t.id}')
        
    def check_partitioner_state(self):
        p = self.partitioner.p
        rc = p.poll()
        if rc == None:
            return 'solving'
        out_data, err_data = p.communicate()
        ret: str = out_data.strip('\n').strip(' ')
        # print(rc)
        # print(f'out_data: {out_data}, err_data: {err_data}')
        # assert(rc == 0)
        if rc != 0:
            ret = 'non-zero-return'
        self.write_line_to_log(f'partitioner-done {ret}')
        return ret
    
    def check_runnings_state(self):
        if self.solve_ori_flag and self.ori_task.state == 'solving':
            sta = self.check_process_state(self.ori_task.p, -1, 'solving')
            if sta != 'solving':
                if sta in ['sat', 'unsat']:
                    self.result = sta
                    self.done = True
                    self.write_line_to_log(f'solved-by-original {sta}')
                    return
                self.ori_task.state = sta
                self.base_run_cnt -= 1
        
        if self.partitioner.state == 'solving':
            sta = self.check_partitioner_state()
            if sta != 'solving':
                if sta in ['sat', 'unsat']:
                    self.result = sta
                    self.done = True
                    self.write_line_to_log(f'solved-by-partitioner {sta}')
                    return
                self.partitioner.state = sta
        
        still_solvings = []
        for t in self.state_tasks_dict['solving']:
            t: Task
            if t.state != 'solving':
                continue
            if self.check_solving_state(t):
                still_solvings.append(t)
            else:
                if self.done:
                    return
        
        if len(self.tasks) > 0:
            root_task: Task = self.tasks[0]
            if root_task.state == 'unsat':
                self.result = 'unsat'
                self.reason = root_task.reason
                self.done = True
                self.write_line_to_log(f'unsat-root-task {root_task.reason}')
                return
        
        self.state_tasks_dict['solving'] = still_solvings
        
        if self.partitioner.state != 'solving' and \
            len(self.state_tasks_dict['solving']) == 0 and \
            self.result not in ['sat', 'unsat']:
            self.result = 'unknown'
            self.reason = -3
            self.done = True
            if self.solve_ori_flag:
                if self.ori_task.state == 'solving':
                    self.write_line_to_log(f'unknown partitioner bug')
                else:
                    self.write_line_to_log(f'unknown instance bug')
            return
    
    def get_running_num(self):
        return len(self.state_tasks_dict['solving']) \
             + self.base_run_cnt
    
    def get_unended_num(self):
        return len(self.tasks) \
             - len(self.state_tasks_dict['ended'])
    
    # run waitings by:
    # currently: generation order
    # can be easily change to: priority select
    def run_waiting_tasks(self):
        sz = len(self.tasks)
        cnt = 0
        while self.task_head < sz:
            if len(self.idle_workers) == 0:
                return
            t: Task = self.tasks[self.task_head]
            self.task_head += 1
            if t.state == 'waiting':
                self.solve_task(t)
                self.write_line_to_log(f'running: {self.get_running_num()}, unended: {self.get_unended_num()}')
                cnt += 1
                if cnt >= 10:
                    return
    
    # run the partitioner and build the communication
    def run_partitioner(self):
        cmd =  [self.partitioner_path,
                f'{self.temp_folder_path}/tasks/task-0-ori.smt2',
                f"-outputdir:{self.temp_folder_path}",
                f"-partmrt:{self.max_running_tasks}"
            ]
        self.write_line_to_log(f'exec-command {" ".join(cmd)}')
        p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        self.partitioner = Task(p, -2, None, self.get_current_time())
        self.partitioner.state = 'solving'
        self.partitioner.time_infos['solving'] = self.get_current_time()
    
    # solver original task without BICP simplification
    def solve_ori_task(self):
        # run original task
        instance_path = f'{self.temp_folder_path}/tasks/task-0-ori.smt2'
        cmd =  [self.solver_path,
                instance_path
            ]
        self.write_line_to_log('exec-command {}'.format(' '.join(cmd)))
        
        with open(instance_path, 'br') as file:
            instance_data = file.read()
        
        p = self.assign_task(-1, instance_data)
        self.ori_task = Task(p, -1, None, self.get_current_time())
        
        self.ori_task.state = 'solving'
        self.ori_task.time_infos['solving'] = self.get_current_time()
        self.base_run_cnt += 1
    
    def init_root_task(self):
        os.system(f'cp {self.input_file_path} {self.temp_folder_path}/tasks/task-0-ori.smt2')
    
    def solve(self):
        self.init_root_task()
        if self.solve_ori_flag:
            self.solve_ori_task()
        
        self.run_partitioner()
        while True:
            if self.need_communicate:
                self.communicate_with_partitioner()
            self.check_runnings_state()
            if self.done:
                return
            self.run_waiting_tasks()
            if self.time_limit != 0 and self.get_current_time() >= self.time_limit:
                raise TimeoutError()
            if len(self.idle_workers) == 0 or (not self.need_communicate):
                time.sleep(0.1)
    
    def terminate_partitioner(self):
        if self.partitioner.state == 'solving':
            self.partitioner.p.terminate()
        
    def __call__(self, comm_world: MPI.COMM_WORLD, cmd_args):
        self.init(comm_world, cmd_args)
        try:
            self.solve()
        except TimeoutError:
            self.result = 'timeout'
            self.write_line_to_log('timeout')
        # except AssertionError as ae:
        #     self.result = 'AssertionError'
        #     # print(f'AssertionError: {ae}')
        #     # self.write_line_to_log(f'AssertionError: {ae}')
        # except Exception as e:
        #     self.result = 'Exception'
        #     # print(f'Exception: {e}')
        #     # self.write_line_to_log(f'Exception: {e}')
        
        end_time = time.time()
        execution_time = end_time - self.start_time
        print(self.result)
        print(execution_time)
        
        self.terminate_partitioner()
        
        if self.output_dir_path != None:
            with open(f'{self.output_dir_path}/result.txt', 'w') as f:
                f.write(f'{self.result}\n{execution_time}\n')
        
        comm_world.Abort()

