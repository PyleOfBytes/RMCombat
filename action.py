__author__ = 'Yaacov'

import combatant
import dice
import verbose as v

verbose_msg=True


class Action:
    def __init__(self, combat, combatant, time, action_type, parameters, log_message):
        self.combat = combat
        self.combatant = combatant
        self.time = time
        self.duration = 0
        self.end_time = 0
        self.action_type = action_type
        self.exh_cost = 0
        self.parameters = parameters
        self.log_message = log_message