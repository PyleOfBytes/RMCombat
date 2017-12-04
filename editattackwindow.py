import attack
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkm

__author__ = 'Yaacov'


class EditAttackWin(tk.Toplevel):
    def __init__(self, parent, combat, combatant, cur_attack=None, cur_attack_index=None):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.combat = combat
        self.combatant = combatant
        self.attack_index = cur_attack_index
        self.attack = cur_attack
        self.name = tk.StringVar()
        self.table = tk.StringVar()
        self.ob = tk.IntVar()
        self.ranged = tk.IntVar()
        self.ranges = []
        if cur_attack:
            self.name.set(cur_attack.name)
            self.table.set(cur_attack.table)
            self.ob.set(cur_attack.OB)
            self.ranged.set(cur_attack.ranged)
            self.ranges = cur_attack.ranges
        else:
            self.name.set("")
            # the next two lines exists merely to speed up testing
            self.table.set("Broadsword")
            self.ob.set(35)
            self.ranged.set(0)

        self.geometry("+" + str(self.parent.winfo_x()) + "+" + str(self.parent.winfo_y()))
        self.initialize()

    def initialize(self):
        self.grid()
        self.title("Add Attack")
        r = 0
        self.name_label = ttk.Label(self, text="Attack Name:")
        self.name_label.grid(row=r, column=0)
        self.name_entry = ttk.Entry(self, textvariable=self.name)
        self.name_entry.grid(row=r, column=1)
        r += 1
        self.table_label = ttk.Label(self, text="Attack Table:")
        self.table_label.grid(row=r, column=0)
        attacks = sorted(list(self.combat.attack_tables.keys()))
        self.table_optmenu = ttk.OptionMenu(self, self.table, self.table.get(), *attacks, command=self.set_ranged)
        self.table_optmenu.grid(row=r, column=1, sticky=tk.W)
        self.table_optmenu.focus_set()
        r += 1
        self.ob_label = ttk.Label(self, text="OB:")
        self.ob_label.grid(row=r, column=0)
        self.ob_entry = ttk.Entry(self, textvariable=self.ob)
        self.ob_entry.grid(row=r, column=1)
        r += 1
        self.ranged_label = ttk.Label(self, text="Ranged?")
        self.ranged_label.grid(row=r, column=0)
        self.ranged_chkbox = ttk.Checkbutton(self, variable=self.ranged)
        self.ranged_chkbox.grid(row=r, column=1)
        r += 1
        self.submit_btn = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=r, column=0)
        self.cancel_btn = ttk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_btn.grid(row=r, column=1)

    def submit(self):
        if self.name_entry.get() == "":
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.table.get())
        if self.name_entry.get() in self.combatant.get_attack_names():
            self.name_duplicate_mb = tkm.showwarning("Duplicate Name",
                                                     "An attack with that name already exists. Please change the name.")
        else:
            if self.attack:
                self.attack.update_attack(self.name_entry.get(),
                                          self.table.get(),
                                          int(self.ob_entry.get()),
                                          self.ranged.get(),
                                          # Need to code button for getting ranges with window, etc.
                                          [])
                self.parent.attacks_lbox.delete(self.attack_index)
                self.parent.attacks_lbox.insert(self.attack_index, str(self.attack))
            else:
                self.attack = attack.Attack(self.name_entry.get(),
                                            self.table.get(),
                                            int(self.ob_entry.get()),
                                            self.ranged.get(),
                                            # Need to code button for getting ranges with window, etc.
                                            [])
                self.parent.combatant.add_attack(self.attack)
                self.parent.attacks_lbox.insert(tk.END, str(self.attack))
            self.destroy()

    def set_ranged(self, value):
        if self.combat.attack_tables[value].hands == "Missile":
            self.ranged.set(1)
            self.ranged_chkbox.state(['disabled'])
        else:
            self.ranged_chkbox.state(['!disabled'])

    def close_window(self):
        self.destroy()
