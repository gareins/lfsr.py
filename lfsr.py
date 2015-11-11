#!/bin/python3

import argparse
import re
import sys
from functools import reduce
from operator import iadd

parser = argparse.ArgumentParser(description='Generate LFSR sequences for given polynomial.')

parser.add_argument('polynomial', metavar='P', type=str, 
                    help='Polynomial for LFSR. Example: x4+x2+1')

parser.add_argument('--start', dest='start', type=str, 
                    help='Print sequence generated from initial register value. Example: 1010')

parser.add_argument('--huge', dest='allow_huge', action='store_const', 
                    const=True, default=False,
                    help='By default, only first 100 lines are printed. This discards this limitation')

def generate_lfsr(poly, start, huge):
    max_poly = max(poly)
    top_bottom = "+" + "-" * ((max_poly + 1) * 2 - 1) + "+" + 3 * "-" + "+\n"
    str_print = top_bottom

    line = start[:]
    ctr = 0

    while True:
        # break when too big
        if not huge and ctr > 100:
            line = top_bottom.replace("-", " ")
            str_print += line + line + line
            break

        # Printing
        str_print += "|"
        for b in line:
            str_print += str(b) + " "

        str_print = str_print[:-1] + "| " + str(line[-1]) + " |"
        str_print += "\n"

        nxt = reduce(iadd, [line[i] for i in poly]) % 2
        line.pop()
        line.insert(0, nxt)

        # Check if already cycled
        if line == start:
            break
        ctr += 1

    str_print += top_bottom
    print(str_print[:-1])  # Do not print new line

if __name__ == "__main__":
    args = parser.parse_args()
    poly_str = str(args.polynomial)

    validator = re.compile("^(x\d*\+)*1$")
    valid = validator.match(poly_str)

    if not valid:
        print("Invalid polynomial. Exiting.")
        sys.exit(1)

    poly = set()
    for v in re.finditer("x(\d*)\+", poly_str):
        # Could include more syntactic checks, but I dont want to.
        num = int(v.group(1) if v.group(1) else "1") - 1
        poly.add(num)

    if args.start is not None:
        try:
            # Could include more syntactic checks, but I dont want to.
            start = [int(i) % 2 for i in args.start]
        except Exception as e:
            print("Cannot parse starting register value. Exiting")
            sys.exit(1)

        if len(start) != max(poly) + 1:
            print("Bad length for initial register value. %d!=%d. Exiting" % (len(start), max(poly) + 1))
            sys.exit(1)
    else:
        start = [0] * max(poly) + [1]

    generate_lfsr(poly, start, args.allow_huge)
