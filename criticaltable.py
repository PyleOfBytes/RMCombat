__author__ = 'Yaacov'

import csv
import verbose as v

verbose_msg=True


class CriticalTable:
    def __init__(self, filename):
        with open(filename) as critical_table_file:
            v.p(verbose_msg,"Reading critical table: " + filename)
            readCSV = csv.reader(critical_table_file, delimiter=',')
            line = next(readCSV)
            self.name = line[1]
            severity_levels = line[3]
            self.columns = {}
            for i in range(0, int(severity_levels)):
                line = next(readCSV)
                column = []
                self.columns[line[0]] = column
                for j in range(0, int(line[1])):
                    line = next(readCSV)
                    if line[13] != "":
                        cond_result = [int(line[14]), int(line[15]), int(line[16]), line[17], line[18], line[19],
                                                     line[20], line[21], line[22], line[23]]
                        result = ["condition", int(line[0]), int(line[1]), line[2], int(line[3]), int(line[4]), int(line[5]), line[6], line[7],
                                                line[8], line[9], line[10], line[11], line[12], line[13], cond_result]
                    else:
                        result = ["nocondition", int(line[0]), int(line[1]), line[2], int(line[3]), int(line[4]), int(line[5]), line[6], line[7],
                                  line[8], line[9], line[10], line[11], line[12]]
                    column.append(result)

