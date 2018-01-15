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


def get_funcaddr_by_funcname(base, size, fname):
    addr = base
    endaddr = base + size
    while addr <= endaddr:
        addr = NextHead(addr)
        sname = Name(addr)
        # print "%s %s" % (hex(addr),sname)
        if fname == sname:
            return addr
    return 0


def test_get_funcaddr_by_funcname():
    addr = 0x401000
    end = 0x490E7C
    print "name_addr=0x%x" % get_funcaddr_by_funcname(addr, end, "start")

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
#
# op_t.type
#                 Description                          Data field
o_void     =  0 # No Operand                           ----------
o_reg      =  1 # General Register (al,ax,es,ds...)    reg
o_mem      =  2 # Direct Memory Reference  (DATA)      addr
o_phrase   =  3 # Memory Ref [Base Reg + Index Reg]    phrase
o_displ    =  4 # Memory Reg [Base Reg + Index Reg + Displacement] phrase+addr
o_imm      =  5 # Immediate Value                      value
o_far      =  6 # Immediate Far Address  (CODE)        addr
o_near     =  7 # Immediate Near Address (CODE)        addr
o_idpspec0 =  8 # Processor specific type
o_idpspec1 =  9 # Processor specific type
o_idpspec2 = 10 # Processor specific type
o_idpspec3 = 11 # Processor specific type
o_idpspec4 = 12 # Processor specific type
o_idpspec5 = 13 # Processor specific type
                # There can be more processor specific types
'''


def get_op_instruction(addr, idx):
    asm = ""
    type = GetOpType(addr, idx)
    for case in switch(type):
        if case(o_void):
            break
        if case(o_reg):
            asm += GetOpnd(addr, idx)
            break
        if case(o_mem):
            asm += GetOpnd(addr, idx)
            break
        if case(o_phrase):
            asm += GetOpnd(addr, idx)
            break
        if case(o_displ):
            asm += GetOpnd(addr, idx)
            break
        if case(o_imm):
            asm += hex(GetOperandValue(addr, idx))
            break
        if case(o_far):  # Immediate Far Address
            #asm+="short "
            asm += hex(GetOperandValue(addr, idx))
        if case(o_near):  # Immediate Near Address
            asm += "short "
            asm += hex(GetOperandValue(addr, idx))
            break
        if case():
            break
    return asm

"""
print instruction.

@param addr: start address
@param equals: if op = equals return
@param insaddr: if insaddr=1 print ins addr
@param save: if save!=null save ins to file
@param debug: print debug log

@return: 0 is could not find
"""


def print_instruction(addr, equals, insaddr, save, debug):
    addr = PrevHead(addr)
    while True:
        addr = NextHead(addr)
        op = GetMnem(addr)
        if debug == 1:
            opTyoe0 = GetOpType(addr, 0)
            opTyoe1 = GetOpType(addr, 1)
            print "%s %d %d" % (op, opTyoe0, opTyoe1)
        instruction = ""
        if insaddr == 1:
            instruction += hex(addr)
            instruction += " "
        instruction += op
        tmp = get_op_instruction(addr, 0)
        if tmp != "":
            instruction += " "
            instruction += tmp
        tmp = get_op_instruction(addr, 1)
        if tmp != "":
            instruction += " "
            instruction += tmp
        if save != "":
            save_file_a(save, instruction + "\n")
        print instruction
        if op == equals:
            break
        """
            POP.W           {R4-R8,PC}
            BX              LR
            POP.W           {R1-R11,PC}
        """


def print_instruction_arm(addr, insaddr, save, debug):
    print_instruction(addr, "B", insaddr, save, debug)


def print_instruction_x86(addr, insaddr, save, debug):
    print_instruction(addr, "retn", insaddr, save, debug)


def test_print_instruction():
    addr = 0x36146
    # filepath="e://aa.arm"
    filepath = ""
    if (filepath != "" and os.path.isfile(filepath)):
        os.remove(filepath)
    print_instruction_arm(addr, 1, filepath, 0)


def disasm(addr):
    addr = PrevHead(addr)
    while True:
        addr = NextHead(addr)
        asm = GetDisasm(addr)
        print asm
        if asm.find("BX") != -1 and asm.find("LR") != -1:
            break
        if asm.find("POP") != -1 and asm.find("PC") != -1:
            break
        if asm.startswith("DCD"):
            break


def get_disasm(addr):
    return GetDisasm(addr)

"""
Dump memory to file

@param filepath: path to output file
@param ea: linear address to save from
@param size: number of bytes to save

@return: 0 - error, 1 - ok
"""


def dump_mem(filepath, ea, size):
    of = idaapi.fopenWB(filepath)
    if of:
        retval = idaapi.base2file(of, 0, ea, ea + size)
        idaapi.eclose(of)
        return retval
    else:
        return 0


def test_dump_mem():
    start = get_func_addr("open")
    end = get_func_end_addr(start)
    dump_mem("e://aa.a", start, end - start)


def get_func_addr(name):
    return LocByName(name)


def get_func_addr_ex(base, name):
    return LocByNameEx(base, name)


def get_func_start_addr(addr):
    addr = NextHead(addr)
    while True:
        addr = PrevHead(addr)
        asm = GetDisasm(addr)
        if asm.find("PUSH") != -1 and asm.find("LR") != -1:
            return addr
    return BADADDR


def get_func_end_addr(addr):
    addr = PrevHead(addr)
    while True:
        addr = NextHead(addr)
        asm = GetDisasm(addr)
        # print asm
        if asm.find("BX") != -1 and asm.find("LR") != -1:
            return addr
        if asm.find("POP") != -1 and asm.find("PC") != -1:
            return addr
    return BADADDR


def get_func_end_addr_by_name(name):
    return get_func_end_addr(get_func_addr(name))


def get_func_addr_module(module, name):
    base = get_module_base(module)
    if base == None:
        return BADADDR
    func_addr = get_func_addr_ex(base, name)
    if func_addr == BADADDR:
        return BADADDR
    size = GetModuleSize(base)
    if func_addr > base + size:
        return BADADDR
    return func_addr


def get_addr_by_name(base, size, desired_name):
    current_address = base
    end_address = base + size
    while current_address <= end_address:
        current_address = NextHead(current_address)
        name = Name(current_address)
        # print "%s: %s" %(hex(current_address), name)
        if desired_name in name:
            return current_address
    return BADADDR


def get_module_base(module):
    base = GetFirstModule()
    while base != None:
        name = GetModuleName(base)
        if name.find(module) != -1:
            break
        base = GetNextModule(base)
    return base


def get_module_size(base):
    return GetModuleSize(base)


def analyze_area_module(name):
    base = get_module_base(name)
    if base == None:
        return
    size = get_module_size(base)
    AnalyzeArea(base, base + size)


def get_seg_base(segname):
    base = FirstSeg()
    while base != BADADDR:
        name = SegName(base)
        if name == segname:
            return base
        base = NextSeg(base)
    return base


def get_seg(name):
    base = get_seg_base(name)
    if base == BADADDR:
        return None
    end = SegEnd(base)
    return (base, end)


def dump_seg(path, name):
    base = get_seg_base(name)
    if base != BADADDR:
        end = SegEnd(base)
    else:
        return False
    dump_mem(path, base, end - base)
    return True


def find_dword(start, end, value):
    end -= 3
    while start < end:
        if value == DbgDword(start):
            return start
        start += 1
    return -1


def find_dword_seg(name, value):
    base = get_seg_base(name)
    if base == BADADDR:
        return -1
    end = SegEnd(base)
    return find_dword(base, end, value)


def get_arm_opcode(addr):
    return ((DbgDword(addr) & 0xFF000000) >> 24)


def get_string():
    return GetString(GetRegValue("r0"))

if __name__ == "__main__":
    print hex(get_arm_opcode(GetRegValue("PC")))
