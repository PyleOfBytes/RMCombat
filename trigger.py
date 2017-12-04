import verbose as v

verbose_msg=True


class Trigger:
    def __init__(self, name, target, end_time, parameters = None):
        self.name = name
        self.target = target
        self.end_time = end_time
        self.parameters = parameters
