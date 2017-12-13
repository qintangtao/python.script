class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

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

def dumpAsm(addr,debug):
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
    
if __name__ == "__main__":
    addr = 0x452590
    dumpAsm(addr, 0)