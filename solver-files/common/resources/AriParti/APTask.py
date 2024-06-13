
# Task maintained by the Master
class Task():
    def __init__(self, p, id, parent, make_time):
        self.p = p
        self.id = id
        self.parent = parent
        self.time_infos = {'make': make_time}
        # waiting running sat unsat unknown
        # waiting -> running BY (run task)
        #         -> unsat   BY (ancester, children, partitioner)
        #         -> unknown BY (children)
        # running -> sat BY (solver)
        #         -> unsat BY (solver, ancester, children, partitioner)
        #         -> unknown BY (solver, children)
        self.state = 'waiting'
        self.reason = -3
        self.subtasks = []
        
    def __str__(self) -> str:
        pid = -1
        if (self.parent != None):
            pid = self.parent.id
        ret = f'id: {self.id}'
        ret += f', parent: {pid}'
        ret += f', state: {self.state}'
        if self.reason != -3:
            ret += f', reason: {self.reason}'
        if len(self.subtasks) > 0:
            stid = [self.subtasks[0].id, self.subtasks[1].id]
            ret += f', subtasks: {stid}'
        ret += f'\ntime-infos: {self.time_infos}\n'
        return ret
