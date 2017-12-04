__author__ = 'Yaacov'

import action
import dice
import verbose as v

verbose_msg=True


class MoveAction(action.Action):
    def __init__(self, combat, combatant, time, action_type, parameters, log_message):
        action.Action.__init__(self, combat, combatant, time, action_type, parameters, log_message)
        self.duration = 10
        self.end_time = time + self.duration
        self.pace = parameters['pace']
