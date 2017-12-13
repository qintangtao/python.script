# python常用脚本集

## python_utils.py
### class switch
python模仿switch<br>

## python_ida.py
### def getFunAddrByName
通过函数名从某地址开始搜索函数地址<br>
```Bash
Get function addr by function name.

@param base: Search start address
@param size: Search address size
@param size: Search function name

@return: 0 is could not find
```

### def getOpStr
获取某地址处字符串汇编<br>
```Bash
Get operand of an instruction.
Get number used in the operand.

@param addr: address of instruction
@param idx: number of operand

@return: 0 is could not find
```

### def printAsm
从某地址开始打印汇编<br>
```Bash
print asm.

@param addr: start address
@param debug: print debug log

@return: 0 is could not find
```