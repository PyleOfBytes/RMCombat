__author__ = 'Yaacov'

import csv
import verbose as v

verbose_msg=True


class AttackTable:
    def __init__(self, filename):
        with open(filename) as attack_table_file:
            v.p(verbose_msg,"Reading attack table: " + filename)
            readCSV = csv.reader(attack_table_file, delimiter=',')
            self.name = next(readCSV)[1]
            self.critical_type = next(readCSV)[1]
            line = next(readCSV)
            self.hands = line[1]
            line = next(readCSV)
            self.min_length = float(line[1])
            self.max_length = float(line[2])
            line = next(readCSV)
            self.min_weight = float(line[1])
            self.max_weight = float(line[2])
            line = next(readCSV)
            self.fumble = int(line[2])
            line = next(readCSV)
            self.breakage_num = int(line[2])
            line = next(readCSV)
            self.min_strength = int(line[1])
            self.max_strength = int(line[2])
            if len(line)==4:
                self.strength_type = line[3]
            else:
                self.strength_type = None
            line = next(readCSV)
            self.ranges = []
            ranges = int(line[1])
            if ranges > 0:
                for i in range(0, ranges):
                    line = next(readCSV)
                    self.ranges.append([int(line[1]), int(line[2]), int(line[3])])
            line = next(readCSV)
            self.results = []
            for i in readCSV: #readCSV.line_num - 9 - ranges):
                self.results.append(i)
