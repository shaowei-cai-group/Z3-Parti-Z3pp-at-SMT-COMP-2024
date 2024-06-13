#!/bin/bash
pkill -SIGTERM mpi
echo "mpi killed"
pkill -SIGTERM orted
echo "orted killed"
pkill -SIGTERM AriParti.py
echo "AriParti killed"
pkill -SIGTERM partitioner-bin
echo "partitioner killed"
pkill -SIGTERM $1
echo "base_solver killed"
rm -rf $2
echo "temp folder cleaned"