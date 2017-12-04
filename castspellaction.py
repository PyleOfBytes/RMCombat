__author__ = 'Yaacov'

import targetedaction
import verbose as v

verbose_msg=True


class CastSpellAction(targetedaction.TargetedAction):
    def __init__(self, combat, combatant, time, action_type, parameters, log_message):
        targetedaction.TargetedAction.__init__(self, combat, combatant, time, action_type, parameters, log_message)
        self.duration = 10
        self.end_time = time + self.duration
        self.spell_list = parameters['spell'].spell_list
        self.spell_level = parameters['spell'].spell_level
        self.spell_type = parameters['spell'].spell_type
