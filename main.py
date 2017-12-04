import pickle
from functools import partial
import rmcombat
import attackaction
import castspellaction
import moveaction
import performskillaction
import spell
import editcombatantwindow
import combatantframe
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
import verbose as v

__author__ = 'Yaacov'

verbose_msg = True


class RMCombatApp(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.combat = rmcombat.RMCombat()
        self.combatant_frames = []
        self.combat_log = tk.StringVar()
        self.menu_bar = None
        self.filemenu = None
        self.savemenu = None
        self.time = 0
        self.action_dict = self.combat.possible_actions
        self.paces_dict = self.combat.possible_paces
        self.initialize()

    def initialize(self):
        self.menu_bar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menu_bar, tearoff=0)
        self.filemenu.add_command(label="Save Combat", accelerator='^S', command=self.saveCombat)
        self.filemenu.add_command(label="Load Combat", accelerator='^L', command=self.loadCombat)
        self.filemenu.add_command(label="Add Combatant", accelerator='^A', command=self.addCombatant)
        self.filemenu.add_command(label="Load Combatant", accelerator='^L', command=self.loadCombatant)
        self.savemenu = tk.Menu(self.filemenu, tearoff=0)
        self.filemenu.add_cascade(menu=self.savemenu, label="Save Combatants")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", accelerator='^Q', command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menu_bar)

        self.grid()
        r = 0
        self.combatants_list_label = ttk.Label(self, text='Combatants: ')
        self.combatants_list_label.grid(column=0, row=r)
        self.add_combatant_btn = ttk.Button(self, text='Add', command=self.addCombatant)
        self.add_combatant_btn.grid(column=1, row=r)

        self.rounds_label = ttk.Label(self, text="Combat Log")
        self.rounds_label.grid(column=7, row=r)
        self.begin_combat_btn = ttk.Button(self, text="Play Actions", command=self.begin_combat)
        self.begin_combat_btn.grid(row=r, column=8)
        r += 1
        self.combat_log_msg = tkst.ScrolledText(self,
                                                height=2,
                                                relief="flat",
                                                borderwidth=0,
                                                width=100)
        self.combat_log_msg.grid(row=r, column=7, columnspan=3, sticky=tk.NW + tk.SE)

    def update_combatants_list(self):
        combatants_list = self.combat.get_combatant_names()
        combatants_list.sort()

        if not combatants_list:
            self.savemenu.delete(0, tk.END)
        else:
            for name in combatants_list:
                self.savemenu.add_command(label=name, command=partial(self.saveCombatant, name))

    def saveCombat(self):
        filename = tkfd.asksaveasfilename(initialdir="./Combats", title="Select file", defaultextension='.rmc',
                                                filetypes=(("Rolemaster Combat files", "*.rmc"), ("all files", "*.*")))
        save_file = open(filename, 'wb')
        pickle.dump(self.combat, save_file)
        save_file.close()

    def loadCombat(self):
        filename = tkfd.askopenfilename(title="Select file", defaultextension='.rmc',
                                          filetypes=(("Rolemaster Combat files", "*.rmc"), ("all files", "*.*")))
        load_file= open(filename, 'rb')
        self.combat = pickle.load(load_file)
        load_file.close()

        v.p(verbose_msg, "Combat loaded. Combatants: " + str([self.combat.combatants[guy].name for guy in self.combat.combatants]))

        for combatant in self.combat.combatants:
            new_frame = combatantframe.CombatantFrame(self, self.combat, self.combat.combatants[combatant])
            if self.combat.num_of_combatants == 1:
                new_frame.grid(row=1, column=0, columnspan=7)
            else:
                new_frame.grid(column=0, columnspan=7)
            self.combatant_frames.append(new_frame)
            new_frame.update_targets()
        self.combat_log_msg.grid(rowspan=len(self.combatant_frames)+1)

        for i in self.combat.log:
            self.combat_log_msg.insert(tk.END, i)

        self.update_combatants_list()

    def saveCombatant(self, combatant):
        filename = tkfd.asksaveasfilename(initialdir="./Combatants", title="Select file", defaultextension='.cbt',
                                                filetypes=(("Rolemaster Combatant files", "*.cbt"), ("all files", "*.*")))
        save_file = open(filename, 'wb')
        pickle.dump(self.combat.combatants[combatant], save_file)
        save_file.close()

    def loadCombatant(self):
        filename = tkfd.askopenfilename(title="Select file", defaultextension='.cbt',
                                          filetypes=(("Rolemaster Combatant files", "*.cbt"), ("all files", "*.*")))
        load_file= open(filename, 'rb')
        combatant = pickle.load(load_file)
        load_file.close()

        proceed = True
        if combatant.name in self.combat.get_combatant_names():
            proceed = tkmb.askokcancel("Overwrite Combatant?", combatant.name +
                                   " already exists in this combat. Continuing will overwrite the current combatant.")
            if proceed:
                for frame in self.combatant_frames:
                    if frame.combatant.name == combatant.name:
                        self.combatant_frames.remove(frame)
                self.combat.combatants.pop(combatant.name)

        if proceed:
            self.combat.add_combatant(combatant)
            new_frame = combatantframe.CombatantFrame(self, self.combat, self.combat.combatants[combatant.name])
            if self.combat.num_of_combatants == 1:
                new_frame.grid(row=1, column=0, columnspan=4)
            else:
                new_frame.grid(column=0, columnspan=4)
            self.combatant_frames.append(new_frame)

        self.update_target_lists()

        v.p(verbose_msg, "Combatant loaded: " + combatant.name )
        self.combat_log_msg.grid(rowspan=len(self.combatant_frames)+1)

    def addCombatant(self):
        edit_combatant_win = editcombatantwindow.EditCombatantWindow(self, self.combat, None, None)

    def update_target_lists(self):
        for item in self.combatant_frames:
            item.update_targets()

    def begin_combat(self):
        for item in self.combatant_frames:
            action_num = item.choose_actions_ntbk.index(item.choose_actions_ntbk.select())
            action_desc = self.action_dict[action_num]
            parameters = {}

            # if action is an attack
            if action_num == 0:
                target = item.choose_actions_ntbk.attack_frame.target.get()
                parameters['target'] = self.combat.get_combatant(target)
                parameters['attack'] = item.combatant.get_attack(item.choose_actions_ntbk.attack_frame.attack.get())
                parameters['parry_percentage'] = item.choose_actions_ntbk.attack_frame.parry_percentage.get()
                target_text = " " + target + " with a " + item.choose_actions_ntbk.attack_frame.attack.get()
                log_message = item.combatant.name + " " + action_desc + target_text
                action = attackaction.AttackAction(self.combat, item.combatant, self.combat.time, action_num,
                                                   parameters, log_message)

            # if action is a spell cast
            elif action_num == 1:
                target = item.choose_actions_ntbk.cast_spell_frame.target.get()

                if target and target != "None":
                    parameters['target'] = self.combat.get_combatant(target)
                else:
                    parameters['target'] = None

                spell_to_cast = spell.Spell(item.choose_actions_ntbk.cast_spell_frame.spell_list.get(),
                                            item.choose_actions_ntbk.cast_spell_frame.spell_level.get())
                parameters['spell'] = spell_to_cast
                target_text = " at " + target
                log_message = item.combatant.name + " " + action_desc + target_text

                action = castspellaction.CastSpellAction(self.combat,
                                                         item.combatant,
                                                         self.combat.time,
                                                         action_num,
                                                         parameters, log_message)

            elif action_num == 2:
                parameters['pace'] = item.choose_actions_ntbk.move_frame.pace.get()
                log_message = item.combatant.name + " " + action_desc

                action = moveaction.MoveAction(self.combat, item.combatant, self.combat.time, action_num, parameters,
                                               log_message)

            elif action_num == 3:
                parameters = []
                log_message = item.combatant.name + " " + action_desc

                action = performskillaction.PerformSkillAction(self.combat,
                                                               item.combatant,
                                                               self.combat.time,
                                                               action_num,
                                                               parameters, log_message)

            else:
                raise(NotImplementedError, "This action type is not implemented yet.")

            self.combat.add_action(action)
            item.combatant.current_action = action
            v.p(verbose_msg, "Action put in list: " + action.log_message + " at time " + str(action.end_time))

        prior_log_length = len(self.combat.log)

        # Call the routine to carry out the actions
        self.combat.act()

        for item in self.combatant_frames:
            item.update_info()

        for i in range(prior_log_length, len(self.combat.log)):
            self.combat_log_msg.insert(tk.END, self.combat.log[i])

if __name__ == "__main__":
    app = RMCombatApp(None)
    app.title('Rolemaster Combat')
    app.mainloop()
