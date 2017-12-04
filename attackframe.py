import tkinter as tk
import tkinter.ttk as ttk
import verbose as v
import targetedactionframe as taf

__author__ = 'Yaacov'

verbose_msg = True


class AttackFrame(taf.TargetedActionFrame):
    def __init__(self, parent, combat, guy):
        taf.TargetedActionFrame.__init__(self, parent, combat, guy)
        self.attacks_list = []
        self.attack = tk.StringVar()
        self.parry_percentage = tk.IntVar(0)
        self.initialize()

    def initialize(self):
        self.grid()

        r = 0
        self.choose_attack_label = ttk.Label(self, text="Choose Attack: ")
        self.choose_attack_label.grid(row=r, column=0)
        self.choose_attack_optmenu = ttk.OptionMenu(self, self.attack, self.attack.get(), *self.attacks_list)
        self.choose_attack_optmenu.grid(row=r, column=1, sticky=tk.W)
        r += 1
        self.choose_target_label = ttk.Label(self, text="Choose Target: ")
        self.choose_target_label.grid(row=r, column=0)
        self.choose_target_optmenu.grid(row=r, column=1, sticky=tk.W)
        r += 1
        self.choose_parry_label = ttk.Label(self, text="Choose Parry %: ")
        self.choose_parry_label.grid(row=r, column=0)
        self.choose_parry_optmenu = ttk.OptionMenu(self, self.parry_percentage, self.parry_percentage.get(), *[0, 25, 50, 75, 100])
        self.choose_parry_optmenu.grid(row=r, column=1, sticky=tk.W)

        self.update_attacks_list()

    def update_attacks_list(self):
        self.attacks_list = []
        for item in self.combatant.attacks_list:
            self.attacks_list.append(str(item))
        v.p(verbose_msg, "      Updating attacks list for " + self.combatant.name + " to " + str(self.attacks_list))
        self.choose_attack_optmenu['menu'].delete(0, tk.END)
        if not self.attacks_list:
            self.attack.set("None")
            self.choose_attack_optmenu['menu'].add_command(label="None", command=tk._setit(self.attack, "None"))
        else:
            for item in self.attacks_list:
                self.choose_attack_optmenu['menu'].add_command(label=item, command=tk._setit(self.attack, item))
            self.attack.set(self.attacks_list[0])
