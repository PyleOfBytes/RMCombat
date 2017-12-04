__author__ = 'Yaacov'

import tkinter as tk
import tkinter.ttk as ttk
import verbose as v

verbose_msg = True


class PerformSkillFrame(tk.Frame):
    def __init__(self, parent, combat, guy):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.combat = combat
        self.combatant = guy
        self.initialize()

    def initialize(self):
        self.grid()
        r = 0
        self.choose_skill_label = ttk.Label(self, text="Choose Skill: ")
        self.choose_skill_label.grid(row=r, column=0)
