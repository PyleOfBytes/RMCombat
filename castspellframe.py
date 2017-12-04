__author__ = 'Yaacov'

import tkinter as tk
import tkinter.ttk as ttk
import targetedactionframe as taf
import verbose as v

verbose_msg= True

class CastSpellFrame(taf.TargetedActionFrame):
    def __init__(self, parent, combat, guy):
        taf.TargetedActionFrame.__init__(self, parent, combat, guy)
        self.spell_list = tk.StringVar()
        self.spell_level = tk.IntVar()
        self.initialize()

    def initialize(self):
        self.grid()
        r = 0
        self.choose_spell_list_label = ttk.Label(self, text="Choose Spell List: ")
        self.choose_spell_list_label.grid(row=r, column=0, sticky= tk.W)
        self.choose_spell_list_optmenu = ttk.OptionMenu(self, self.spell_list, *['None'])
        self.choose_spell_list_optmenu.grid(row=r, column=1, sticky=tk.W)
        r+=1
        self.choose_spell_level_label = ttk.Label(self, text="Choose Spell Level: ")
        self.choose_spell_level_label.grid(row=r, column=0, sticky= tk.W)
        self.choose_spell_level_optmenu = ttk.OptionMenu(self, self.spell_level, *self.combat.spell_levels_list)
        self.choose_spell_level_optmenu.grid(row=r, column=1, sticky = tk.W)
        r += 1
        self.choose_target_label = ttk.Label(self, text="Choose Target: ")
        self.choose_target_label.grid(row=r, column=0, sticky=tk.W)
        self.choose_target_optmenu = ttk.OptionMenu(self, self.target, *['None'])
        self.choose_target_optmenu.grid(row=r, column=1, sticky=tk.W)