################### Use AriParti
FROM smt-comp-ariparti:common AS builder
USER root

################### Extract AriParti in run stage
FROM satcomp-infrastructure:worker AS ariparti_liaison
WORKDIR /
# Copy AriParti and solver scripts

COPY --from=builder --chown=ecs-user /AriParti /competition/AriParti

COPY --chown=ecs-user resources/init_solver.sh /competition
COPY --chown=ecs-user resources/worker /competition

USER ecs-user

RUN python3 -m pip install mpi4py

RUN chmod +x /competition/AriParti/AriParti.py
RUN chmod +x /competition/init_solver.sh
RUN chmod +x /competition/worker

##//linxi-test
RUN mkdir /competition/rundir

ENTRYPOINT /competition/init_solver.sh ; exec bash