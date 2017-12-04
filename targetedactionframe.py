import tkinter as tk
import tkinter.ttk as ttk
import verbose as v
__author__ = 'Yaacov'

verbose_msg = False


class TargetedActionFrame(tk.Frame):
    def __init__(self, parent, combat, guy):
        tk.Frame.__init__(self, parent)
        v.p(verbose_msg, "Init Targeted Action Frame")
        self.parent = parent
        self.combat = combat
        self.combatant = guy
        self.targets_list = []
        self.target = tk.StringVar()
        self.choose_target_optmenu = ttk.OptionMenu(self, self.target, *['None'])

    def update_targets_list(self):
        self.targets_list = []
        self.targets_list = [x for x in self.combat.get_combatant_names() if x != self.combatant.name]
        self.targets_list.sort()
        self.choose_target_optmenu['menu'].delete(0, tk.END)

        if not self.targets_list:
            self.target.set("None")
            self.choose_target_optmenu['menu'].add_command(label="None", command=tk._setit(self.target, "None"))
        else:
            for item in self.targets_list:
                self.choose_target_optmenu['menu'].add_command(label=item, command=tk._setit(self.target, item))
            self.target.set(self.targets_list[0])
