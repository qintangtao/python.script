#!/usr/bin/python
# -*- coding: UTF-8 -*-


class BaseReg:

    def __init__(self, names):
        self._names = names
        for name in self._names:
            setattr(self, name, GetRegValue(name))

    def __str__(self):
        fmt = '{'
        append = False
        for name in self._names:
            if append:
                fmt += ', '
            else:
                append = True
            fmt += "'%s':0x%08x" % (name, getattr(self, name))
        fmt += '}'
        return fmt

    def __eq__(self, value):
        for name in self._names:
            if value == getattr(self, name):
                return True
        return False


class ArmReg(BaseReg):

    def __init__(self):
        regnames = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7',
                    'R8', 'R9', 'R10', 'R11', 'R12', 'SP', 'LR', 'PC']
        BaseReg.__init__(self, regnames)

    def __eq__(self, value):
        for i in xrange(0, 13):
            if value == getattr(self, self._names[i]):
                return True
        return False

if __name__ == "__main__":
    r = ArmReg()
    print r
    print (r == 0xbeb506f8)
