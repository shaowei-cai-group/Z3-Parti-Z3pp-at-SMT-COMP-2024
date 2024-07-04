# Z3-Parti-Z3++ at SMT-COMP 2024

We intend to participate in the forthcoming SMT-COMP 2024 by submitting **Z3-Parti-Z3++** for **the Parallel Track** and **the Cloud Track** categories.

**Z3-Parti-Z3++** is a **derived** tool from Z3 and intend for **QF_RDL, QF_IDL, QF_LRA, QF_LIA, QF_NRA, and QF_NIA**. The authors of **Z3-Parti-Z3++** are **Mengyu Zhao and Shaowei Cai**.

The system description is named `Z3_Parti_Z3pp_at_SMT_COMP_2024.pdf`.

As per the submission rule, we are providing the pseudo-random 32-bit unsigned number **998244353**.

Zenodo DOI: 10.5281/zenodo.11627838

## Variable-level Partitioning for Distributed SMT Solving

Z3-Parti-Z3++ is the practical implementations of our innovative concept of **Var**iable-level **Parti**tioning, which is applied to the Arithmetic theories. This technique is introduced for the first time in our recently published paper at CAV 2024, titled *Distributed SMT Solving Based on Dynamic Variable-level Partitioning*.

Within Arithmetic theories, each time VarParti picks a variable and partitions the problem by dividing the feasible domain of the variable, leading to sub-problems, which can be further simplified via constraint propagation.

Our proposed variable-level partitioning permits robust, comprehensive partitioning. Regardless of the Boolean structure of any given instance, our partitioning algorithm can keep partitioning to the last moment of the solving process.

## Prerequisites

Docker should be installed on the machine.

Clone this repository need Git LFS (Large File Storage).

The VarParti docker images are built on top of the base containers satcomp-infrastructure:common, satcomp-infrastructure:leader and satcomp-infrastructure:worker.

The process of building these base images (as well as many other aspects of building solvers for SAT-Comp) is described in the README.md file in the [SAT-Comp and SMT-Comp Parallel and Cloud Track Instructions](https://github.com/aws-samples/aws-batch-comp-infrastructure-sample) repository.
Please follow the steps in this repository up to the point at which the base containers have been built.

## How to Build and Test

Here is an example illustrating how to build and test our solver:

Build the dockers:

```bash
cd solver-files
bash build-cloud-docker-images.sh
```

Create a docker network:

```bash
docker network create smt-comp-ap-test
```

Run the leader docker:

```bash
docker run \
    -i --shm-size=32g \
    --name leader \
    --network smt-comp-ap-test \
    --rm \
    --user ecs-user \
    -t smt-comp-ariparti:leader
```

Run the worker docker:

```bash
docker run \
    -i --shm-size=32g \
    --name worker \
    --network smt-comp-ap-test \
    --rm \
    --user ecs-user \
    -t smt-comp-ariparti:worker
```

Test in the leader docker:

```bash
python3 /test-files/scripts/run-parallel.py /test-files/instances/lia-sat-10.4.smt2
```

It will output as follows format:
The first line is the solving result, and the second is the run time.

A possible output:

```bash
sat
96.96219038963318
total cost time (start MPI and clean up):
100.5447518825531
```
