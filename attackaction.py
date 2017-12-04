__author__ = 'Yaacov'

import targetedaction
import math
import dice
import verbose as v

verbose_msg=True


class AttackAction(targetedaction.TargetedAction):
    def __init__(self, combat, combatant, time, action_type, parameters, log_message):
        targetedaction.TargetedAction.__init__(self, combat, combatant, time, action_type, parameters, log_message)
        self.duration = 10
        self.end_time = time + self.duration
        self.attack_type = parameters['attack'].name
        self.attack_table = parameters['attack'].table
        self.parry_percentage = parameters['parry_percentage']
        self.parry_DB = math.ceil(parameters['parry_percentage']*parameters['attack'].OB/100)
        self.attack_OB = math.floor((100-parameters['parry_percentage'])*parameters['attack'].OB/100)
        self.attack_ranged = parameters['attack'].ranged
        self.attack_ranges = parameters['attack'].ranges


        if self.attack_ranged:
            self.exh_cost = 1/6
        else:
            self.exh_cost = 1/2

    def __str__(self):
        return self.combatant.name + " attacks with a " + self.attack_type