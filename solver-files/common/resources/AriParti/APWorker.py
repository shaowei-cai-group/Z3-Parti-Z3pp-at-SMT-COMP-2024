from mpi4py import MPI
import subprocess
import time
import os

class Worker():
    
    def write_line_to_log(self, info: str):
        self.logs.append(info)
     
    def check_solving_process(self, id, p: subprocess.Popen):
        rc = p.poll()
        if rc == None:
            return 'solving'
        out_data, err_data = p.communicate()
        
        ret: str = out_data.strip('\n').strip(' ')
        ret = 'unknown'
        lines = out_data.split('\n')
        self.write_line_to_log(f'solving-result id {id}')
        for line in lines:
            words = line.split(' ')
            if len(words) <= 0:
                continue
            if ret == 'unknown' and words[0] != 'c':
                ret = line
            self.write_line_to_log(f'solving-result {line}')
        # # debug
        # if True:
        #     print(rc)
        #     print(f'out_data: {out_data}, err_data: {err_data}')
        # self.write_line_to_log(f'return-code {rc}')
        # if rc != 0:
        #     ret = 'non-zero-return'
        #     raise AssertionError()
        self.write_line_to_log(f'task-solved {id} {ret}')
        return ret
    
    def __call__(self, comm_world: MPI.COMM_WORLD, wid, cmd_args):
        status = 'idle'
        recv_data = None
        
        temp_folder_path = cmd_args.temp_dir
        solver_path = cmd_args.solver
        run_mode = cmd_args.run_mode
        
        if not os.path.exists(temp_folder_path):
            os.system(f'mkdir -p {temp_folder_path}')
            os.system(f'mkdir -p {temp_folder_path}/tasks')
            
        # print(temp_folder_path)
        while True:
            if status == 'running':
                self.logs = []
                result = self.check_solving_process(task_id, p)
                if result != 'solving':
                    send_data = (task_id, result, self.logs)
                    comm_world.send(send_data, dest=0)
                    status = 'idle'
                time.sleep(0.2)
            
            if not comm_world.Iprobe(source=0):
                time.sleep(0.1)
                continue
            
            msg_status = MPI.Status()
            recv_data = comm_world.recv(source=0, status=msg_status)
            status_tag = msg_status.Get_tag()
            
            if status_tag == 0:
                task_id, instance_data = recv_data
                
                if status != 'idle':
                    assert(False)
                if task_id == -1:
                    instance_path = f'{temp_folder_path}/tasks/task-0-ori.smt2'
                else:
                    instance_path = f'{temp_folder_path}/tasks/task-{task_id}.smt2'
                cmd =  [solver_path,
                        instance_path,
                    ]
                
                if run_mode == 'distributed':
                    if not os.path.exists(instance_path):
                        with open(instance_path, 'bw') as file:
                            file.write(instance_data)

                if os.path.exists(instance_path):
                    status = 'running'
                    p = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                else:
                    assert(False)
            elif status_tag == 1:
                p: subprocess.Popen
                if status == 'running':
                    p.terminate()
                status = 'idle'
            else:
                assert(False)

