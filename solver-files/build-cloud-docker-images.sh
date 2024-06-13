#!/bin/bash

cd common
docker build -t smt-comp-ariparti:common .
cd ../leader
docker build -t smt-comp-ariparti:leader .
cd ../worker
docker build -t smt-comp-ariparti:worker .

