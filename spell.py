__author__ = 'Yaacov'

import combatant
import dice
import verbose as v

verbose_msg=True


class Spell:
    def __init__(self, spell_list, spell_level=1, spell_type='U'):
        self.spell_list = spell_list
        self.spell_level = spell_level
        self.spell_type = spell_type