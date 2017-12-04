import verbose as v

__author__ = 'Yaacov'

verbose_msg = True


class Combatant:
    """Common base class for all combatants"""
    def __init__(self, combat, attacks_list={}, name="", max_hits=30, hits=30, status="Normal", max_PP=0, PP=0, AT=1,
                 DB_melee=0, DB_ranged=0, max_exhpts=40, exhpts=40, init_bonus=0, constitution=50):
        self.combat = combat
        if name:
            self.name = name
        else:
            self.name = "Orc " + str(combat.num_of_combatants)
        self.max_hits = max_hits
        self.hits = hits
        self.status = status
        self.max_PP = max_PP
        self.PP = PP
        self.attacks_list = attacks_list
        self.AT = AT
        self.DB_melee = DB_melee
        self.DB_ranged = DB_ranged
        self.max_exhpts = max_exhpts
        self.exhpts = exhpts
        self.initiative_bonus = init_bonus
        self.current_action = None
        self.stun_no_parry_ends_at = 0
        self.stun_ends_at = 0
        self.must_parry_ends_at = 0
        self.initiative_loss_ends_at = 0
        self.constitution = constitution
        self.time_of_death = None

    def __str__(self):
        return self.name

    def update_info(self, name, max_hits, hits, status, max_PP, PP, AT, DB_melee, DB_ranged, max_exhpts, exhpts, init_bonus):
        self.name = name
        self.max_hits = max_hits
        self.hits = hits
        self.status = status
        self.max_PP = max_PP
        self.PP = PP
        self.AT = AT
        self.DB_melee = DB_melee
        self.DB_ranged = DB_ranged
        self.max_exhpts = max_exhpts
        self.exhpts = exhpts
        self.initiative_bonus = init_bonus

    def add_attack(self, attack):
        self.attacks_list[attack.name]= attack

    def get_attack(self, name):
        return self.attacks_list[name]

    def get_attack_names(self):
        return list(self.attacks_list.keys())

    def update_status(self):
        if self.hits > 0:
            if self.stun_no_parry_ends_at > self.combat.time:
                self.status = "Stunned, No Parry"
            elif self.stun_ends_at > self.combat.time:
                self.status = "Stunned"
            elif self.must_parry_ends_at > self.combat.time:
                self.status = "Must Parry"
            else:
                self.status = ""
            hit_percentage = float(self.hits) / float(self.max_hits)
            i = 0
            while hit_percentage > self.combat.hits_statuses[i][0]:
                i += 1
            self.status = self.status + "/" + self.combat.hits_statuses[i][1]
        elif self.hits > -self.constitution:
            self.status = "Unconscious"
        elif self.hits <= -self.constitution:
            self.status = "Dead"
