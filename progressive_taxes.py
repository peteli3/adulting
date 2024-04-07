#!/usr/bin/env python3

import argparse
import json
import math

class Bracket:
    def __init__(self, start, end, rate):
        self.start = start
        self.end = end
        self.rate = rate
        self._owed = 0

    @classmethod
    def from_row(cls, row):
        start = row[0]
        end = math.inf if (row[1] == "inf") else row[1]
        rate = row[2]
        return cls(start=start, end=end, rate=rate)

    def record_owed(self, amount):
        self._owed = amount

    def owed(self):
        return round(self._owed, 2)

class TaxTable:
    def __init__(self, brackets):
        self.brackets = brackets

    def compute_taxes(self, taxable_income):
        taxes = 0
        for bracket in self.brackets:
            if taxable_income > bracket.end:
                layer = (bracket.end - bracket.start) * bracket.rate
                taxes += layer
                bracket.record_owed(layer)
            else:
                layer = (taxable_income - bracket.start) * bracket.rate
                taxes += layer
                bracket.record_owed(layer)
                break
        print(round(taxes, 2))

    def breakdown(self):
        print('-' * 80)
        for bracket in self.brackets:
            print(f'layer {bracket.start} ~ {bracket.end}: {bracket.owed()}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('overlord')
    parser.add_argument('year')
    parser.add_argument('filing_status')
    parser.add_argument('taxable_income', type=int, help='ex: form 1040 line 15 for irs')
    parser.add_argument('--breakdown', action='store_true')
    args = parser.parse_args()

    with open(f'{args.overlord}_rates.json', 'r') as f:
        config = json.load(f)
    rows = config[args.year][args.filing_status]
    table = TaxTable([ Bracket.from_row(r) for r in rows ])

    # this seems to always be slightly higher than what the IRS calculates
    # compare against form 1040 line 16
    table.compute_taxes(args.taxable_income)
    if args.breakdown:
        table.breakdown()

if __name__ == '__main__':
    main()

