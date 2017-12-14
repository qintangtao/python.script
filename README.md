# python常用脚本集

## python_utils.py
### class switch
python模仿switch<br>
```Bash
v = 'ten'
for case in switch(v):
    if case('one'):
        print 1
        break
    if case('two'):
        print 2
        break
    if case('ten'):
        print 10
        break
    if case('eleven'):
        print 11
        break
    if case():
        print "something else!"
```

## python_ida.py
### def get_funcaddr_by_funcname(base,size,fname)
通过函数名从某地址开始搜索函数地址<br>
```Bash
Get function addr by function name.

@param base: Search start address
@param size: Search address size
@param size: Search function name

@return: 0 is could not find
```

### def get_op_instruction(addr, idx)
获取某地址处指令<br>
```Bash
Get operand of an instruction.
Get number used in the operand.

@param addr: address of instruction
@param idx: number of operand

@return: 0 is could not find
```

### def print_instruction(addr,debug)
从某地址开始打印指令<br>
```Bash
print instruction.

@param addr: start address
@param debug: print debug log

@return: 0 is could not find
```

### def dump_mem(filepath, ea, size)
dump内存到文件<br>
```Bash
Dump memory to file

@param filepath: path to output file
@param ea: linear address to save from
@param size: number of bytes to save

@return: 0 - error, 1 - ok
```