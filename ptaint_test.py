"""
Test ptaint.py
"""
import sys
sys.path.append('../neural-taint-analysis')
import random
import ptaint

def test_ptaint_FBD():
    from programs import first_byte_dependent
    program = first_byte_dependent
    refs = [[0.0], [0.0]]
    inps = [random.random() for _ in range(2)]

    inf = ptaint.ptaint_numeric(inps, program, refs)
    
    print(f"Inputs:{inps}, refs:{refs}, inf:{inf}")

def test_ptaint_TBPD():
    from programs import two_byte_partial_dependance as program
    refs = [[0.6], [0.0]]
    #inps = [random.random() for _ in range(2)]
    inps = [0.6, 0.5]

    inf = ptaint.ptaint_numeric(inps, program, refs)
    
    print(f"Inputs:{inps}, refs:{refs}, inf:{inf}")


if __name__=="__main__":
    test_ptaint_FBD()
    test_ptaint_TBPD()
