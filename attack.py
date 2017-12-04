__author__ = 'Yaacov'

import verbose as v

verbose_msg = True


class Attack:
    def __init__(self, name="Dagger", table="Dagger", OB=15, ranged=False, ranges=[]):
        self.name = name
        self.table = table
        self.OB = OB
        self.ranged = ranged
        self.ranges = ranges

    def __str__(self):
        if self.ranged:
            ranged_text = " (R)"
        else:
            ranged_text = ""

        text=self.name + ranged_text + " - " + str(self.OB)

        return text

    def update_attack(self, name, table, OB, ranged, ranges):
        self.name = name
        self.table = table
        self.OB = OB
        self.ranged = ranged
        self.ranges = ranges