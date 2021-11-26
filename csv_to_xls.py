#!/usr/bin/env python3
from openpyxl import Workbook
import csv
import sys
wb = Workbook()
ws = wb.active
with open(sys.argv[1], 'r') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save(sys.argv[2])
