import os
import re
import sys
import json
import time
import string
import random
import concurrent
import concurrent.futures
import subprocess
import multiprocessing

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_logic(file):
    with open(file, "r") as f:
        content = f.read()
        m = re.search("set-logic ([A-Z_]+)", content) 
        if m: 
            return m[1]
    return None

def select_solver_for_logic(logic: str):
    return 'z3pp-at-smt-comp-2023-bin'
    if logic == 'QF_LRA':
        return 'opensmt-2.5.2-bin'
    elif logic == 'QF_LIA':
        return 'opensmt-2.5.2-bin'
    elif logic == 'QF_NRA':
        return 'cvc5-1.0.8-bin'
    elif logic == 'QF_NIA':
        return 'z3-4.12.1-bin'
    else:
        assert(False)

def cmd_runner(cmd_paras):
    cmd = ' '.join(cmd_paras)
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result

if __name__ == '__main__':
    
    start_time = time.time()
    
    request_directory = sys.argv[1]
    with open(f'{request_directory}/input.json', 'r') as file:
        config_data: dict = json.load(file)

    formula_file = config_data['formula_file']
    timeout_seconds: int = config_data['timeout_seconds']
    worker_node_ips = config_data['worker_node_ips']
    worker_node_cores = config_data.get('worker_node_cores', None)
    
    formula_logic = get_logic(formula_file)
    
    base_solver = select_solver_for_logic(formula_logic)
    
    output_dir = request_directory
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    
    # ##//linxi-test
    # print(f'script_path: {script_path}')
        
    node_number = len(worker_node_ips)
    host_core_number = multiprocessing.cpu_count()

    
    if not os.path.exists(output_dir):
        os.system(f'mkdir -p {output_dir}')

    if node_number > 1:
        run_mode = 'distributed'
        core_number_sumup = 0
        with open(f'{output_dir}/hostfile', 'w') as file:
            for i in range(node_number):
                node_ip = worker_node_ips[i]
                if worker_node_cores == None:
                    slot = host_core_number
                else:
                    slot = worker_node_cores[i]
                file.write(f'{node_ip} slots={slot}\n')
                # ##//linxi-test
                # print(f'{node_ip} slots={slot}\n')
                core_number_sumup += slot
    else:
        run_mode = 'parallel'
        core_number_sumup = host_core_number

    temp_folder_name = generate_random_string(16)
    
    # ##//linxi-test
    # temp_folder_name = 'ap-test'
    # print(temp_folder_name)
    
    temp_folder_path = f'/tmp/ap-files/{temp_folder_name}'
    
    # ##//linxi-test
    # print(temp_folder_path)
    
    if run_mode == 'distributed':
        fs = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for node_ip in worker_node_ips:
                cmd_paras = [
                    'ssh', node_ip,
                    'mkdir', '-p', f'{temp_folder_path}/tasks'
                ]
                f = executor.submit(cmd_runner, cmd_paras)
                fs[f] = cmd_paras
            
            # ##//linxi-test
            # for future in concurrent.futures.as_completed(fs):
            #     cmd_paras = fs[future]
            #     cmd = ' '.join(cmd_paras)
            #     print(f"command: {cmd}")
            #     result = future.result()
            #     print(f'result: {result}')
            #     print(f'stdout:')
            #     print(result.stdout.decode("utf-8"))
            #     print(f'stderr:')
            #     print(result.stderr.decode("utf-8"))
    else:
        cmd_paras = [
            'mkdir', '-p', f'{temp_folder_path}/tasks'
        ]
        cmd_runner(cmd_paras)
    
    assert(timeout_seconds > 10)
    
    solving_time_limit = timeout_seconds - 10
    
    cmd_paras = [
        'mpiexec',
        ### COMP-UPDATE ###
        '--mca btl_tcp_if_include eth0',
        # '--mca btl_tcp_if_include enp1s0f1',
        '--allow-run-as-root',
        '--use-hwthread-cpus',
        '--bind-to none', '--report-bindings',
        f'-np {core_number_sumup}',
    ]
    
    if run_mode == 'distributed':
        cmd_paras.append(f'--hostfile {output_dir}/hostfile')

    cmd_paras.extend([
        f'{script_dir}/AriParti.py',
        f'--file {formula_file}',
        f'--output-dir {output_dir}',
        f'--temp-dir {temp_folder_path}',
        f'--max-running-tasks {core_number_sumup}',
        f'--time-limit {solving_time_limit}',
        f'--partitioner {script_dir}/binary-files/partitioner-bin',
        f'--solver {script_dir}/binary-files/{base_solver}',
        f'--run-mode {run_mode}',
    ])
    cmd = ' '.join(cmd_paras)
    
    # ##//linxi-test
    # print(f"command:\n{cmd}")
    
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # ##//linxi-test
    # print(f'stdout:')
    # print(result.stdout.decode("utf-8"))
    # print(f'stderr:')
    # print(result.stderr.decode("utf-8"))
    
    sys.stdout.write(result.stdout.decode("utf-8"))
    # sys.stderr.write(result.stderr.decode("utf-8"))
    
    # ##//linxi-test
    # print('Cleaning up: Killing all processes')
    
    if run_mode == 'distributed':
        fs = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for node_ip in worker_node_ips:
                cmd_paras = [
                    'ssh', node_ip,
                    'bash', f'{script_dir}/AriParti-cleanup.sh', base_solver, temp_folder_path
                ]
                f = executor.submit(cmd_runner, cmd_paras)
                fs[f] = cmd_paras

            # ##//linxi-test
            # for future in concurrent.futures.as_completed(fs):
            #     cmd_paras = fs[future]
            #     cmd = ' '.join(cmd_paras)
            #     print(f"command: {cmd}")
            #     result = future.result()
            #     print(f'result: {result}')
            #     print(f'stdout:')
            #     print(result.stdout.decode("utf-8"))
            #     print(f'stderr:')
            #     print(result.stderr.decode("utf-8"))
    else:
        cmd_paras = [
            'bash', f'{script_dir}/AriParti-cleanup.sh', base_solver, temp_folder_path
        ]
        cmd_runner(cmd_paras)
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f'total cost time (start MPI and clean up):\n{execution_time}')
    