import os
import attacktable
import criticaltable
import trigger
import dice
import verbose as v

__author__ = 'Yaacov'

verbose_msg = True


class RMCombat:

    def __init__(self):
        self.combatants = {}
        self.action_list = {}
        self.recurring_trigger_list = {}
        self.trigger_list = {}
        self.time = float(0)
        self.attack_tables = {}
        self.critical_tables = {}
        self.read_data()
        self.log = []

    @property
    def num_of_combatants(self):
        return len(self.combatants)

    @property
    def possible_actions(self):
        actions = {0: "attacks", 1: "casts a spell", 2: "moves", 3: "performs a skill"}
        return actions

    @property
    def possible_paces(self):
        paces = {0: "Walk", 1: "Jog", 2: "Run", 3: "Sprint", 4: "Fast Sprint", 5: "Dash"}
        return paces

    @property
    def hits_statuses(self):
        states = [[0, "Unconscious"], [0.25, "Critically Injured"], [0.5, "Seriously Injured"],
                  [0.75, "Injured"], [1, "Normal"]]
        return states

    def calc_penalties(self, hits, max_hits, exh, max_exh):
        hits_percentage = float(hits) / float(max_hits)
        i = 0
        while hits_percentage > self.hits_penalties[i][0]:
            i += 1
        hits_penalty = self.hits_penalties[i][1]

        exh_percentage = float(exh) / float(max_exh)
        i = 0
        while exh_percentage >= self.exh_penalties[i][0]:
            i += 1
        exh_penalty = self.exh_penalties[i][1]

        return [hits_penalty + exh_penalty, hits_penalty, exh_penalty]

    @property
    def hits_penalties(self):
        penalties = [[0.25, -30], [0.5, -20], [0.75, -10], [1, 0]]
        return penalties


    @property
    def exh_penalties(self):
        penalties = [[0, -100], [0.10, -60], [0.25, -30], [0.50, -20], [0.75, -10], [100, 0]]
        return penalties

    @property
    def spell_levels_list(self):
        spell_levels_list = list(range(1, 21)) + list(range(25, 105, 5))
        return spell_levels_list

    def read_data(self):
        attack_table_files = os.listdir("RM_Standard/Attack_Tables")
        for i in attack_table_files:
            new_attack_table = attacktable.AttackTable("RM_Standard/Attack_Tables/" + i)
            self.attack_tables[new_attack_table.name] = new_attack_table

        critical_table_files = os.listdir("RM_Standard/Critical_Tables")
        for i in critical_table_files:
            new_critical_table = criticaltable.CriticalTable("RM_Standard/Critical_Tables/" + i)
            self.critical_tables[new_critical_table.name] = new_critical_table

    def get_combatant(self, name):
        try:
            return self.combatants[name]
        except KeyError:
            return None

    def get_combatant_names(self):
        return list(self.combatants.keys())

    def add_combatant(self, guy):
        if guy.name not in self.combatants:
            self.combatants[guy.name] = guy
        else:
            raise NameError('Another combatant already has this name.')
        v.p(verbose_msg, "Added combatant: " + guy.name)

    def update_combatant(self, guy, name, max_hits, hits, status, max_PP, PP, AT, DB_melee, DB_ranged, max_exhpts,
                         exhpts, init_bonus):
        del self.combatants[guy.name]
        guy.update_info(name, max_hits, hits, status, max_PP, PP, AT, DB_melee, DB_ranged, max_exhpts, exhpts, init_bonus)
        guy.name = name
        guy.max_hits = max_hits
        guy.hits = hits
        guy.max_PP = max_PP
        guy.PP = PP
        guy.AT = AT
        guy.DB_melee = DB_melee
        guy.DB_ranged = DB_ranged
        guy.max_exhpts = max_exhpts
        guy.exhpts = exhpts
        guy.initiative_bonus = init_bonus
        self.combatants[guy.name] = guy

    def add_to_log(self, message):
        self.log.append(message + "\n")

    def roll_initiative(self, action_list):
        init_list = []
        for action in action_list:
            initiative = dice.Dice.roll(2, 10) + action.combatant.initiative_bonus
            init_list.append([initiative, action])

        init_list = sorted(init_list, key=lambda item: item[0])
        return [row[1] for row in init_list]

    def add_trigger(self, trig):
        if self.trigger_list.get(trig.end_time):
            self.trigger_list[trig.end_time].append(trig)
        else:
            self.trigger_list[trig.end_time] = [trig]

    def add_recurring_trigger(self, rtrigger):
        if self.recurring_trigger_list.get(rtrigger.end_time):
            self.recurring_trigger_list[rtrigger.end_time].append(rtrigger)
        else:
            self.recurring_trigger_list[rtrigger.end_time] = [rtrigger]

    def add_action(self, action):
        if self.action_list.get(action.end_time):
            self.action_list[action.end_time].append(action)
        else:
            self.action_list[action.end_time] = [action]

    def act(self):
        triggers_to_resolve = self.trigger_list.get(self.time)
        recurring_triggers_to_resolve = self.recurring_trigger_list.get(self.time)
        actions_to_resolve = self.action_list.get(self.time)
        v.p(verbose_msg, "Actions to resolve: " + str(actions_to_resolve))

        while not actions_to_resolve and not triggers_to_resolve and not recurring_triggers_to_resolve:
            self.time += 0.5
            triggers_to_resolve = self.trigger_list.get(self.time)
            recurring_triggers_to_resolve = self.recurring_trigger_list.get(self.time)
            actions_to_resolve = self.action_list.get(self.time)

        v.p(verbose_msg, "Time is " + str(self.time))
        self.add_to_log("    Time is " + str(self.time))

        if recurring_triggers_to_resolve:
            v.p(verbose_msg, "---Resolving recurring triggers at " + str(self.time) + " seconds")
            for rtrigger in recurring_triggers_to_resolve:
                self.resolve_recurring_trigger(rtrigger)
                rtrigger.end_time += 10
                self.add_recurring_trigger(rtrigger)
            self.recurring_trigger_list[self.time] = []

        if actions_to_resolve:
            v.p(verbose_msg, "---Resolving actions at " + str(self.time) + " seconds")
            if len(actions_to_resolve) > 1:
                actions_to_resolve = self.roll_initiative(actions_to_resolve)
            for action in actions_to_resolve:
                self.resolve_action(action)
            self.action_list[self.time] = []

        if triggers_to_resolve:
            v.p(verbose_msg, "---Resolving triggers at " + str(self.time) + " seconds")
            for item in triggers_to_resolve:
                self.resolve_trigger(item)
            self.trigger_list[self.time] = []

    def resolve_trigger(self, trig):
        v.p(verbose_msg, "Resolving trigger: " + trig.name + " for " + trig.target.name)
        print(self.trigger_list)
        if trig.name == "Stun No Parry":
            if trig.target.stun_ends_at > self.time:
                new_trig = trigger.Trigger("Stun", trig.target, trig.target.stun_ends_at)
                self.add_trigger(new_trig)

        else:
            v.p(verbose_msg, "Not actually doing anything with this trigger: " + trig.name)
        trig.target.update_status()

    def resolve_recurring_trigger(self, rtrigger):
        if rtrigger.name == "Bleeding":
            rtrigger.target.hits += -rtrigger.parameters['damage']
            self.add_to_log(rtrigger.target.name + " bled " + str(rtrigger.parameters['damage']) + " hits.")
        else:
            v.p(verbose_msg, "Not actually doing anything with recurring trigger: " + rtrigger.name)
        rtrigger.target.update_status()

    def resolve_action(self, action):
        if action.action_type == 0:
            if action.combatant.status in ["Unconscious", "Stunned, No Parry"]:
                self.add_to_log(action.combatant.name + " is " + action.combatant.status.lower() + " and can't attack.")
            else:
                self.add_to_log(action.log_message)
                self.resolve_attack(action)
        else:
            self.add_to_log(action.log_message)

        action.combatant.exhpts += -action.exh_cost
        self.action_list[self.time].remove(action)

    def resolve_attack(self, action):
        roll = dice.oehighroll()
        table = self.attack_tables[action.attack_table]
        if roll <= table.fumble:
            v.p(verbose_msg, "Attack roll is fumbled: " + str(roll))
            self.add_to_log(action.combatant.name + " fumbled the attack.")
        else:
            penalties = self.calc_penalties(action.combatant.hits, action.combatant.max_hits,
                                            action.combatant.exhpts, action.combatant.max_exhpts)
            if action.target.current_action.action_type == 0 and \
                            action.target.current_action.target == action.combatant:
                target_parry = action.target.current_action.parry_DB
            else:
                target_parry = 0

            if action.attack_ranged:
                # need to deal with parrying ranged attacks
                adjusted_roll = roll + action.attack_OB + penalties[0] - action.target.DB_ranged
            else:
                adjusted_roll = roll + action.attack_OB + penalties[0] - action.target.DB_melee - target_parry

            v.p(verbose_msg, "Roll: " + str(roll) + "OB: " + str(action.attack_OB) + " Pen: " + str(penalties[0]) +
                " DBs: " + str(action.target.DB_melee) + "/" + str(action.target.DB_ranged) + " Parried by: " +
                str(target_parry) + " Final: " + str(adjusted_roll))

            for item in table.results:
                if adjusted_roll < int(item[0]):
                    pass
                else:
                    result = item[22-action.target.AT]
                    v.p(verbose_msg, "Attack result: " + result)
                    if result == "-":
                        self.add_to_log(action.combatant.name + " missed " + action.target.name)
                    else:
                        if result[len(result)-1].isdigit():
                            damage = int(result)
                            self.add_to_log(action.combatant.name + " did " + str(
                                damage) + " hits to " + action.target.name)
                        else:
                            i = 0
                            while result[i].isdigit():
                                i += 1
                            damage = int(result[0:i])
                            critical_level = result[i:]
                            self.add_to_log(action.combatant.name + " did " + str(
                                damage) + " hits and a " + critical_level + " critical to " + action.target.name)

                            critical_table = self.critical_tables[self.attack_tables[action.attack_table].critical_type]
                            critical_column = critical_table.columns[critical_level]
                            i = 0
                            critical_roll = dice.Dice.d100()
                            while critical_column[i][2] < critical_roll:
                                i += 1
                            crit = critical_column[i]
                            log_message = "Crit: " + str(critical_roll) + " " + crit[3] + "\n   "

                            #Next four lines are for testing purposes:
                            crit[8] = "1~0"
                            crit[7] = "2~0"
                            crit[6] = "1~0"

                            if crit[4] != 0:
                                damage += crit[4]
                                log_message = log_message + " Hits: " + str(crit[4])
                            if crit[5] != 0:
                                rtrigger = trigger.Trigger("Bleeding", action.target, self.time + 10,
                                                           {"damage": crit[5]})
                                self.add_recurring_trigger(rtrigger)
                                log_message = log_message + " Bleeding: " + str(crit[5])
                            if crit[8] != "0~0":
                                snp = crit[8].split("~")
                                num_of_rounds = int(snp[0])
                                penalty = int(snp[1])
                                stun_duration = 0
                                if action.target.stun_no_parry_ends_at > self.time:
                                    end_time = action.target.stun_no_parry_ends_at + 10*num_of_rounds
                                    for i in self.trigger_list[action.target.stun_no_parry_ends_at]:
                                        if i.name == "Stun No Parry" and i.target == action.target:
                                            self.trigger_list[action.target.stun_no_parry_ends_at].remove(i)
                                    if action.target.stun_ends_at > action.target.stun_no_parry_ends_at:
                                        stun_duration = action.target.stun_ends_at - action.target.stun_no_parry_ends_at
                                        for i in self.trigger_list[action.target.stun_ends_at]:
                                            if i.name == "Stun" and i.target == action.target:
                                                self.trigger_list[action.target.stun_ends_at].remove(i)
                                else:
                                    end_time = self.time + 10*num_of_rounds
                                    if action.target.stun_ends_at > self.time:
                                        stun_duration = action.target.stun_ends_at - self.time
                                action.target.stun_no_parry_ends_at = end_time
                                action.target.stun_ends_at = end_time + stun_duration
                                trig = trigger.Trigger("Stun No Parry", action.target, end_time)
                                self.add_trigger(trig)
                                log_message = log_message + " Stun No Parry: " + snp[0]
                            if crit[7] != "0~0":
                                snp = crit[7].split("~")
                                num_of_rounds = int(snp[0])
                                penalty = int(snp[1])
                                must_parry_duration = 0
                                if action.target.stun_ends_at > self.time:
                                    end_time = action.target.stun_ends_at + 10*num_of_rounds
                                    for i in self.trigger_list[action.target.stun_ends_at]:
                                        if i.name == "Stun" and i.target == action.target:
                                            self.trigger_list[action.target.stun_ends_at].remove(i)
                                    if action.target.must_parry_ends_at > action.target.stun_ends_at:
                                        must_parry_duration = action.target.must_parry_ends_at - action.target.stun_ends_at
                                        for i in self.trigger_list[action.target.must_parry_ends_at]:
                                            if i.name == "Must Parry" and i.target == action.target:
                                                self.trigger_list[action.target.must_parry_ends_at].remove(i)
                                else:
                                    end_time = self.time + 10*num_of_rounds
                                    if action.target.must_parry_ends_at > self.time:
                                        must_parry_duration = action.target.must_parry_ends_at - self.time
                                action.target.stun_ends_at = end_time
                                action.target.must_parry_ends_at = end_time + must_parry_duration
                                trig = trigger.Trigger("Stun", action.target, end_time)
                                self.add_trigger(trig)
                                log_message = log_message + " Stunned: " + snp[0]
                            if crit[6] != "0~0":
                                snp = crit[6].split("~")
                                num_of_rounds = int(snp[0])
                                penalty = int(snp[1])
                                initiative_loss_duration = 0
                                if action.target.must_parry_ends_at > self.time:
                                    end_time = action.target.must_parry_ends_at + 10*num_of_rounds
                                    for i in self.trigger_list[action.target.must_parry_ends_at]:
                                        if i.name == "Must Parry" and i.target == action.target:
                                            self.trigger_list[action.target.must_parry_ends_at].remove(i)
                                    if action.target.initiative_loss_ends_at > action.target.must_parry_ends_at:
                                        initiative_loss_duration = action.target.initiative_loss_ends_at - action.target.must_parry_ends_at
                                        for i in self.trigger_list[action.target.initiative_loss_ends_at]:
                                            if i.name == "Initiative Loss" and i.target == action.target:
                                                self.trigger_list[action.target.initiative_loss_ends_at].remove(i)
                                else:
                                    end_time = self.time + 10*num_of_rounds
                                    if action.target.initiative_loss_ends_at > self.time:
                                        initiative_loss_duration = action.target.initiative_loss_ends_at - self.time
                                action.target.must_parry_ends_at = end_time
                                action.target.initiative_loss_ends_at = end_time + initiative_loss_duration
                                trig = trigger.Trigger("Must Parry", action.target, end_time)
                                self.add_trigger(trig)
                                log_message = log_message + " Must Parry: " + snp[0]

                            self.add_to_log(log_message)
                        action.target.hits += -damage
                        action.target.update_status()
                    break
