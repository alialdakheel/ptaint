"""
Test ptaint.py
"""
import sys
import random
from math import isclose
import ptaint

def test_ptaint_FBD():
    from programs import FBD
    program = FBD()
    refs = program.gen_ref()
    inps = [random.random() for _ in range(2)]

    inf = ptaint.ptaint_numeric(inps, program, refs)

    print(f"Inputs:{inps}, refs:{refs}, inf:{inf}")
    print("isclose", [isclose(i, 0.0, abs_tol=1e-15) for i in inf])

def test_ptaint_TBPD():
    from programs import TBPD
    program = TBPD()
    refs = [[0.6], [0.0]]
    inps = [random.random() for _ in range(2)]
    # inps = [0.6, 0.5]

    inf = ptaint.ptaint_numeric(inps, program, refs)

    print(f"Inputs:{inps}, refs:{refs}, inf:{inf}")
    print("isclose", [isclose(i, 0.0, abs_tol=1e-15) for i in inf])


if __name__=="__main__":
    test_ptaint_FBD()
    test_ptaint_TBPD()
