__author__ = 'Yaacov'

import action
import dice
import verbose as v

verbose_msg=True


class TargetedAction(action.Action):
    def __init__(self, combat, combatant, time, action_type, parameters, log_message):
        action.Action.__init__(self, combat, combatant, time, action_type, parameters, log_message)
        self.target = parameters['target']
