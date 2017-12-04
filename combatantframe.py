
import chooseactionsnotebook
import editcombatantwindow
import tkinter.ttk as ttk, verbose as v
import tkinter as tk
verbose_msg=True


class CombatantFrame(ttk.LabelFrame):
    def __init__(self, parent, combat, guy):
        ttk.LabelFrame.__init__(self, parent, text=guy.name)
        self.parent = parent
        self.combat = combat
        self.combatant = guy
        self.choose_actions_ntbk = None
        self.hits_PP = tk.StringVar()
        self.status = tk.StringVar()
        self.AT_DB = tk.StringVar()
        self.exh = tk.StringVar()
        self.init_bonus = tk.StringVar()
        self.initialize()

    def initialize(self):
        v.p(verbose_msg, "Creating the combatant frame for " + self.combatant.name)
        r = 0
        self.hits_and_PP_label = ttk.Label(self, textvariable=self.hits_PP)
        self.hits_and_PP_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.status_label = ttk.Label(self, textvariable=self.status)
        self.status_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.AT_and_DB_label = ttk.Label(self, textvariable=self.AT_DB)
        self.AT_and_DB_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.exh_label = ttk.Label(self, textvariable=self.exh)
        self.exh_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.init_bonus_label = ttk.Label(self, textvariable=self.init_bonus)
        self.init_bonus_label.grid(row=r, column=0, sticky="w")
        r += 1
        self.edit_combatant_btn = ttk.Button(self, text="Edit", command=self.edit)
        self.edit_combatant_btn.grid(row=r, column=0)

        self.choose_actions_ntbk = chooseactionsnotebook.ChooseActionNtbk(self, self.combat, self.combatant)
        self.choose_actions_ntbk.grid(row=0, column=1, rowspan=r+1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.update_info()

    def edit(self):
        self.parent.edit_combatant_win = editcombatantwindow.EditCombatantWindow(self.parent, self.combat, self.combatant, self)

    def update_info(self):
        self.configure(text=self.combatant.name)
        self.choose_actions_ntbk.attack_frame.update_attacks_list()
        self.hits_PP.set('HP: ' + str(self.combatant.hits) + "/" + str(self.combatant.max_hits) + "    PP: " + str(self.combatant.PP) + "/" + str(self.combatant.max_PP))
        self.status.set('Status: ' + self.combatant.status)
        if self.combatant.status == "Unconscious":
            self.status_label.configure(foreground="blue")
        elif self.combatant.status == "Critically Injured":
            self.status_label.configure(foreground="red")
        elif self.combatant.status == "Seriously Injured":
            self.status_label.configure(foreground="orange")
        elif self.combatant.status == "Injured":
            self.status_label.configure(foreground="lawn green")
        elif self.combatant.status == "Normal":
            self.status_label.configure(foreground="green")
        elif self.combatant.status == "Stunned, No Parry":
            self.status_label.configure(foreground="purple")

        self.AT_DB.set('AT: ' + str(self.combatant.AT) + "    " + "DB: " + str(self.combatant.DB_melee) + "/" + str(self.combatant.DB_ranged))
        self.exh.set("Exh. Pts: " + str(self.combatant.exhpts) + "/" + str(self.combatant.max_exhpts))
        self.init_bonus.set("Init Bonus: " + str(self.combatant.initiative_bonus))

    def update_targets(self):
        v.p(verbose_msg, "      Updating Targets in " + self.combatant.name + "'s frame.")
        self.choose_actions_ntbk.attack_frame.update_targets_list()
        self.choose_actions_ntbk.cast_spell_frame.update_targets_list()

