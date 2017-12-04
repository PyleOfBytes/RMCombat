__author__ = 'Yaacov'

import tkinter as tk
import tkinter.ttk as ttk
import attackframe, moveframe, castspellframe, performskillframe
import verbose as v

verbose_msg=True

class ChooseActionNtbk(ttk.Notebook):
    def __init__(self, parent, combat, guy):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent
        self.combat = combat
        self.combatant = guy
        self.attack_frame = None
        self.cast_spell_frame = None
        self.move_frame = None
        self.perform_skill_frame = None
        self.initialize()

    def initialize(self):
        self.attack_frame = attackframe.AttackFrame(self, self.combat, self.combatant)
        self.add( self.attack_frame, text="Attack")
        self.cast_spell_frame = castspellframe.CastSpellFrame(self, self.combat, self.combatant)
        self.add(self.cast_spell_frame, text="Cast Spell")
        self.move_frame = moveframe.MoveFrame(self, self.combat, self.combatant)
        self.add(self.move_frame, text="Move")
        self.perform_skill_frame = performskillframe.PerformSkillFrame(self, self.combat, self.combatant)
        self.add(self.perform_skill_frame, text="Perform Skill")

        self.select(self.attack_frame)