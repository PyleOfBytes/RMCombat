__author__ = 'Yaacov'

import tkinter as tk
import tkinter.ttk as ttk
import verbose as v


class MoveFrame(tk.Frame):
    def __init__(self, parent, combat, guy):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.combat = combat
        self.combatant = guy
        self.pace = tk.StringVar()
        self.pace_list = self.combat.possible_paces
        self.initialize()

    def initialize(self):
        self.grid()
        r = 0
        self.choose_pace_label = ttk.Label(self, text="Choose Pace: ")
        self.choose_pace_label.grid(row=r, column=0, sticky=tk.W)
        self.choose_pace_entry = ttk.OptionMenu(self, self.pace, self.pace.get(), *self.pace_list )
        self.choose_pace_entry.grid(row=r, column=1, sticky=tk.W)