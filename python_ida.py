#!/usr/bin/python
# -*- coding: UTF-8 -*-
import python_utils

"""
    Get function addr by function name.

    @param base: Search start address
    @param size: Search address size
    @param size: Search function name

    @return: 0 is could not find
"""
def getFunAddrByName(base,size,fname):
    addr=base
    endaddr=base+size
    while addr <= endaddr:
        addr=NextHead(addr)
        sname=Name(addr)
        #print "%s %s" % (hex(addr),sname)
        if fname == sname:
            return addr
    return 0

def test_getFunAddrByName():
	addr=0x401000
	end=0x490E7C
	print "name_addr=0x%x" % getFunAddrByName(addr, end, "start")

"""
    Get operand of an instruction.
    Get number used in the operand.

    @param addr: address of instruction
    @param idx: number of operand

    @return: 0 is could not find
"""
'''
GetOpType
// returns:
//      -1      bad operand number passed
//      0       None
//      1       General Register (al,ax,es,ds...)
//      2       Memory Reference
//      3       Base + Index
//      4       Base + Index + Displacement
//      5       Immediate
//      6       Immediate Far Address
//      7       Immediate Near Address
//      8       FPP register
//      9       386 control register
//      10      386 debug register
//      11      386 trace register
//      12      Condition (for Z80)
//      13      bit (8051)
//      14      bitnot (8051)
'''
def getOpStr(addr, idx):
    asm=""
    type=GetOpType(addr,idx)
    for case in switch(type):
        if case(0):       
            break
        if case(1):
            asm+=GetOpnd(addr, idx)
            break
        if case(2):
            asm+=GetOpnd(addr, idx)
            break
        if case(3):
            asm+=GetOpnd(addr, idx)
            break
        if case(4):
            asm+=GetOpnd(addr, idx)
            break
        if case(5):
            asm+=hex(GetOperandValue(addr,idx))
            break
        if case(6):
            #asm+="short "
            asm+=hex(GetOperandValue(addr,idx))
        if case(7):
            asm+="short "
            asm+=hex(GetOperandValue(addr,idx))
            break
        if case():
            break
    return asm

"""
    print asm.

    @param addr: start address
    @param debug: print debug log

    @return: 0 is could not find
"""
def printAsm(addr,debug):
    addr = PrevHead(addr)
    while True:
        addr = NextHead(addr)
        op=GetMnem(addr)
        if debug == 1:
            opTyoe0=GetOpType(addr,0)
            opTyoe1=GetOpType(addr,1)
            print "%s %d %d" % (op, opTyoe0, opTyoe1)
        asm=hex(addr)
        asm+=" "
        asm+=op
        tmp=getOpStr(addr, 0)
        if tmp != "":
            asm+=" "
            asm+=tmp
        tmp=getOpStr(addr, 1)
        if tmp != "":
            asm+=" "
            asm+=tmp
        print asm
        if op=="retn":
            break

def test_printAsm():
    addr = 0x452590
    dumpAsm(addr, 0)


if __name__ == "__main__":
    test_getFunAddrByName()
    test_printAsm()