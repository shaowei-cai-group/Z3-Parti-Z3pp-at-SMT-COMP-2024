

import os
import sys
import json

input_path = sys.argv[1]

rundir = '/competition/rundir'
input_dict = {
    'formula_file': input_path,
    'timeout_seconds': 200,
    # 'worker_node_ips': ['leader'],
    # 'worker_node_cores': [10]
    'worker_node_ips': ['leader', 'worker'],
    'worker_node_cores': [10, 10]
}

with open(f'{rundir}/input.json', 'w') as file:
    json.dump(input_dict, file)
    
os.system(f'python3 /competition/AriParti/run-AriParti-json.py {rundir}')


        