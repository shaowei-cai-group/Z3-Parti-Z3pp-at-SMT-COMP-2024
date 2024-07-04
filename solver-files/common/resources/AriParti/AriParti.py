#!/usr/bin/python3

from mpi4py import MPI
import argparse
import APLeader
import APWorker

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--file', type=str, required=True,
                            help='input instance file path')
    arg_parser.add_argument('--partitioner', type=str, required=True,
                            help='partitioner path')
    arg_parser.add_argument('--solver', type=str, required=True,
                            help='solver path')
    arg_parser.add_argument('--max-running-tasks', type=int, required=True,
                            help='maximum number of tasks running simultaneously')
    arg_parser.add_argument('--time-limit', type=int, default=0,
                            help='time limit, 0 means no limit')
    arg_parser.add_argument('--temp-dir', type=str,
                            help='temp dir path')
    arg_parser.add_argument('--output-dir', type=str, default=None,
                            help='output dir path')
    
    arg_parser.add_argument('--run-mode', type=str,
                            help='run mode')
    cmd_args = arg_parser.parse_args()
    # print(f'cmd_args.temp_dir: {cmd_args.temp_dir}')
    comm_world = MPI.COMM_WORLD
    rank = comm_world.Get_rank()
    if rank == 0:
        ap_leader = APLeader.Leader()
        ap_leader(comm_world, cmd_args)
    else:
        ap_worker = APWorker.Worker()
        ap_worker(comm_world, rank, cmd_args)
    
'''

'''

