################### Use AriParti
FROM smt-comp-ariparti:common AS builder
USER root

################### Extract AriParti in run stage
FROM satcomp-infrastructure:leader AS ariparti_liaison
WORKDIR /
# Copy AriParti and solver scripts

COPY --from=builder --chown=ecs-user /AriParti /competition/AriParti

COPY --chown=ecs-user resources/init_solver.sh /competition
COPY --chown=ecs-user resources/solver /competition

USER ecs-user

RUN python3 -m pip install mpi4py

RUN chmod +x /competition/AriParti/AriParti.py
RUN chmod +x /competition/init_solver.sh
RUN chmod +x /competition/solver


##//linxi-test
USER ecs-user
COPY --chown=ecs-user resources/test-files /test-files
RUN mkdir /competition/rundir
COPY resources/test-files /test-files

# ##//linxi-test
# USER root
# RUN apt-get update
# RUN apt-get -y --no-install-recommends install \
#     vim

# ENTRYPOINT /competition/init_solver.sh ; exec bash