import editattackwindow
import combatantframe
import combatant
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
import verbose as v

__author__ = 'Yaacov'

verbose_msg = True


class EditCombatantWindow(tk.Toplevel):
    def __init__(self, parent, combat, guy=None, frame=None):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.combat = combat
        if guy:
            self.combatant = guy
        else:
            self.combatant = combatant.Combatant(combat, {})

        self.frame = frame

        self.name = tk.StringVar(self, self.combatant.name)
        self.max_hits = tk.IntVar(self, self.combatant.max_hits)
        self.hits = tk.IntVar(self, self.combatant.hits)
        self.status = tk.StringVar(self, self.combatant.status)
        self.max_PP = tk.IntVar(self, self.combatant.max_PP)
        self.PP = tk.IntVar(self, self.combatant.PP)
        self.AT = tk.IntVar(self, self.combatant.AT)
        self.DB_melee = tk.IntVar(self, self.combatant.DB_melee)
        self.DB_ranged = tk.IntVar(self, self.combatant.DB_ranged)
        self.max_exhpts = tk.IntVar(self, self.combatant.max_exhpts)
        self.exhpts = tk.IntVar(self, self.combatant.exhpts)
        self.initiative_bonus = tk.IntVar(self, self.combatant.initiative_bonus)
        self.attacks = self.combatant.attacks_list
        self.geometry("+" + str(self.parent.winfo_x()) + "+" + str(self.parent.winfo_y()))
        self.initialize()

    def initialize(self):
        self.grid()
        if self.frame is None:
            verb = "Add"
        else:
            verb = "Edit"
        self.title(verb + " Combatant")
        r = 0
        self.name_label = ttk.Label(self, text='Combatant Name:')
        self.name_label.grid(column=0, row=r, sticky="E")
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.state(['focus'])
        self.name_entry.grid(column=1, row=r)
        self.attacks_label = ttk.Label(self, text="Attacks")
        self.attacks_label.grid(row=r, column=2)
        r += 1
        self.max_hits_label = ttk.Label(self, text="Max Hit Points:")
        self.max_hits_label.grid(row=r, column=0)
        self.max_hits_entry = ttk.Entry(self, textvariable=self.max_hits)
        self.max_hits_entry.grid(row=r, column=1)
        r += 1
        self.hits_label = ttk.Label(self, text="Hit Points:")
        self.hits_label.grid(row=r, column=0)
        self.hits_entry = ttk.Entry(self, textvariable=self.hits)
        self.hits_entry.grid(row=r, column=1)
        r += 1
        self.max_PP_label = ttk.Label(self, text="Max Power Points:")
        self.max_PP_label.grid(row=r, column=0)
        self.max_PP_entry = ttk.Entry(self, textvariable=self.max_PP)
        self.max_PP_entry.grid(row=r, column=1)
        r += 1
        self.PP_label = ttk.Label(self, text="Power Points:")
        self.PP_label.grid(row=r, column=0)
        self.PP_entry = ttk.Entry(self, textvariable=self.PP)
        self.PP_entry.grid(row=r, column=1)
        r += 1
        self.AT_label = ttk.Label(self, text='AT:')
        self.AT_label.grid(row=r, column=0)
        self.AT_entry = ttk.Entry(self, textvariable=self.AT)
        self.AT_entry.grid(row=r, column=1)
        r += 1
        self.DB_melee_label = ttk.Label(self, text="Melee DB:")
        self.DB_melee_label.grid(row=r, column=0)
        self.DB_melee_entry = ttk.Entry(self, textvariable=self.DB_melee)
        self.DB_melee_entry.grid(row=r, column=1)
        r += 1
        self.DB_ranged_label = ttk.Label(self, text="Ranged DB:")
        self.DB_ranged_label.grid(row=r, column=0)
        self.DB_ranged_entry = ttk.Entry(self, textvariable=self.DB_ranged)
        self.DB_ranged_entry.grid(row=r, column=1)
        r += 1
        self.max_exh_label = ttk.Label(self, text="Max Exh. Points:")
        self.max_exh_label.grid(row=r, column=0)
        self.max_exh_entry = ttk.Entry(self, textvariable=self.max_exhpts)
        self.max_exh_entry.grid(row=r, column=1)
        r += 1
        self.exh_label = ttk.Label(self, text="Current Exh. Points:")
        self.exh_label.grid(row=r, column=0)
        self.exh_entry = ttk.Entry(self, textvariable=self.exhpts)
        self.exh_entry.grid(row=r, column=1)

        self.attacks_lbox = tk.Listbox(self)
        self.attacks = self.combatant.attacks_list
        for item in self.attacks:
            self.attacks_lbox.insert(tk.END, str(item))
        self.attacks_lbox.grid(row=1, column=2, rowspan=r)
        r += 1
        self.initiative_bonus_label = ttk.Label(self, text="Initiative Bonus:")
        self.initiative_bonus_label.grid(row=r, column=0)
        self.initiative_bonus_entry = ttk.Entry(self, textvariable=self.initiative_bonus)
        self.initiative_bonus_entry.grid(row=r, column=1)

        self.attacks_btn = ttk.Button(self, text="Add Attack", command=self.add_attack)
        self.attacks_btn.grid(row=r, column=2)
        r += 1
        self.submit_btn = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=r, column=0)
        self.cancel_btn = ttk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_btn.grid(row=r, column=1)

    def add_attack(self):
        self.edit_attack_win = editattackwindow.EditAttackWin(self, self.combat, self.combatant)

    def submit(self):
        if self.name.get() in self.combat.get_combatant_names() and \
                        self.combatant != self.combat.get_combatant(self.name.get()):
            self.duplicate_mb = tkmb.showwarning("Duplicate Name",
                                                 "A combatant with that name already exists. Please change the name.")
        else:
            if self.frame is None:
                self.combatant.update_info(self.name.get(),
                                           self.max_hits.get(),
                                           self.hits.get(),
                                           self.combatant.status,
                                           self.max_PP.get(),
                                           self.PP.get(),
                                           self.AT.get(),
                                           self.DB_melee.get(),
                                           self.DB_ranged.get(),
                                           self.max_exhpts.get(),
                                           self.exhpts.get(),
                                           self.initiative_bonus.get())
                self.combatant.update_status()
                self.combat.add_combatant(self.combatant)
                self.frame = combatantframe.CombatantFrame(self.parent, self.combat, self.combatant)
                if self.combat.num_of_combatants == 1:
                    self.frame.grid(row=1, column=0, columnspan=2)
                else:
                    self.frame.grid(column=0, columnspan=2)
                self.parent.combatant_frames.append(self.frame)
                self.parent.combat_log_msg.grid(rowspan=len(self.parent.combatant_frames)+1)

            else:
                self.combat.update_combatant(self.combatant,
                                             self.name.get(),
                                             self.max_hits.get(),
                                             self.hits.get(),
                                             self.combatant.status,
                                             self.max_PP.get(),
                                             self.PP.get(),
                                             self.AT.get(),
                                             self.DB_melee.get(),
                                             self.DB_ranged.get(),
                                             self.max_exhpts.get(),
                                             self.exhpts.get(),
                                             self.initiative_bonus.get())
                self.combatant.update_status()
                v.p(verbose_msg, "Updating combatant: " + self.name.get())

            self.frame.update_info()
            self.parent.update_combatants_list()
            self.parent.update_target_lists()

            self.destroy()

    def close_window(self):
        self.destroy()
