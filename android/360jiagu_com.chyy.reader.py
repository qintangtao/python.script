#!/usr/bin/python
# -*- coding: UTF-8 -*-
import python_ida
import logging
import time
import shutil
import os
import sys
import reg


class QihooJiagu:

    def __init__(self):
        self.py_file = sys.argv[0]
        self.py_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.opcode_decode_path = self.py_path + "\\opcode_decode"
        self.fix_time = int(time.time())
        self.open_func_addr = BADADDR
        self.strtol_func_done_addr = BADADDR
        self.mmap_func_addr = BADADDR
        self.mmap_func_done_addr = BADADDR
        self.munmap_func_addr = BADADDR
        self.strstr_func_addr = BADADDR
        self.time_func_done_addr = BADADDR
        self.jni_onload_addr = BADADDR
        self.JNIEnv_FindClass = BADADDR
        self.JNIEnv_FindClass_done_addr = BADADDR
        self.JNIEnv_RegisterNatives = BADADDR
        self.rtld_db_dlactivity_addr = BADADDR
        self.strtol_func_done_addr_bp = 0
        self.strstr_func_addr_bp = 0
        self.JNIEnv_bp = 0
        self.fix_rtld_db_dlactivity_finish = 0
        self.fix_tracerpid_finish = 0
        self.fix_android_server_port_finish = 0
        self.fix_time_finish = 0
        self.exit = False
        # com.chyy.reader com.chyy.reader.ui.activity.SplashActivity
        self.activity_handle = None
        self.activity_name = "com/chyy/reader/ui/activity/SplashActivity"
        self.activity_onCreate_addr = BADADDR
        self.jiagu_second_seg_base = BADADDR
        self.jiagu_opcode_table_addr = BADADDR
        self.jiagu_opcode_entry_addr = BADADDR
        self.jiagu_opcode_code_addr = BADADDR

    def __logging_config(self):
        filename = self.py_file + '.log'
        '''
        logging.basicConfig(level=logging.INFO,
                            format='{%(funcName)s:%(lineno)d} <%(levelname)s> %(message)s',
                            filename=filename,
                            filemode='w')
        '''
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s] <%(levelname)s> {%(filename)s:%(lineno)d--%(funcName)s} %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=filename,
                            filemode='w')

    def __init_addr(self, initjnienv=True, analyze=True):
        if analyze:
            analyze_area_module("libc.so")

        self.open_func_addr = get_func_addr("open")
        if BADADDR == self.open_func_addr:
            logging.error("get open function address faild.")
            return False
        logging.info("open_func_addr=0x%x", self.open_func_addr)

        self.strtol_func_done_addr = get_func_end_addr_by_name("strtol")
        if BADADDR == self.strtol_func_done_addr:
            logging.error("get strtol function done address faild.")
            return False
        logging.info("strtol_func_done_addr=0x%x", self.strtol_func_done_addr)

        self.mmap_func_addr = get_func_addr("mmap")
        if BADADDR == self.mmap_func_addr:
            logging.error("get mmap function address faild.")
            return False
        logging.info("mmap_func_addr=0x%x", self.mmap_func_addr)

        self.mmap_func_done_addr = get_func_end_addr_by_name("mmap")
        if BADADDR == self.mmap_func_done_addr:
            logging.error("get mmap function done address faild.")
            return False
        logging.info("mmap_func_done_addr=0x%x", self.mmap_func_done_addr)

        self.munmap_func_addr = get_func_addr("munmap")
        if BADADDR == self.munmap_func_addr:
            logging.error("get munmap function address faild.")
            return False
        logging.info("munmap_func_addr=0x%x", self.munmap_func_addr)

        self.strstr_func_addr = get_func_addr("strstr")
        if BADADDR == self.strstr_func_addr:
            logging.error("get strstr function address faild.")
            return False
        logging.info("strstr_func_addr=0x%x", self.strstr_func_addr)

        self.time_func_done_addr = get_func_end_addr_by_name("time")
        if BADADDR == self.time_func_done_addr:
            logging.error("get time function done address faild.")
            return False
        logging.info("time_func_done_addr=0x%x", self.time_func_done_addr)

        self.jni_onload_addr = get_func_addr_module(
            "libjiagu-411485247.so", "JNI_OnLoad")
        if BADADDR == self.jni_onload_addr:
            logging.error("get jni_onload function address faild.")
            return False
        logging.info("jni_onload_addr=0x%x", self.jni_onload_addr)

        self.rtld_db_dlactivity_addr = get_func_addr_module(
            "linker", "rtld_db_dlactivity")
        if BADADDR == self.rtld_db_dlactivity_addr:
            logging.error(
                "get rtld_db_dlactivity_addr function address faild.")
            return False
        logging.info("rtld_db_dlactivity_addr=0x%x",
                     self.rtld_db_dlactivity_addr)

        if initjnienv:
            return self.__init_jnienv_addr()
        return True

    def __init_jnienv_addr(self):
        soname = "libdvm.so"
        analyze_area_module(soname)

        base = get_module_base(soname)
        if base == None:
            logging.error("get_module_base(%s) faild.", soname)
            return False

        size = get_module_size(base)
        if size == -1:
            logging.error("get_module_size(%s) faild.", soname)
            return False

        self.JNIEnv_FindClass = self.__get_func_addr(
            base, size, "aCheck_findclas")
        if self.JNIEnv_FindClass == BADADDR:
            logging.error("find JNIEnv_FindClass addr faild.")
            return False
        logging.info("JNIEnv_FindClass=0x%x", self.JNIEnv_FindClass)

        self.JNIEnv_RegisterNatives = self.__get_func_addr(
            base, size, "aCheck_register")
        if self.JNIEnv_RegisterNatives == BADADDR:
            logging.error("find JNIEnv_RegisterNatives addr faild.")
            return False
        logging.info("JNIEnv_RegisterNatives=0x%x",
                     self.JNIEnv_RegisterNatives)

        self.JNIEnv_FindClass_done_addr = get_func_end_addr(
            self.JNIEnv_FindClass)
        if BADADDR == self.JNIEnv_FindClass_done_addr:
            logging.error(
                "get JNIEnv_FindClass_done_addr function address faild.")
            return False
        logging.info("JNIEnv_FindClass_done_addr=0x%x",
                     self.JNIEnv_FindClass_done_addr)

        return True

    def __get_func_addr(self, base, size, name):
        addr = get_addr_by_name(base, size, name)
        if addr == BADADDR:
            return BADADDR

        for x in XrefsTo(addr):
            asm = GetDisasm(x.frm)
            logging.debug("0x%x : %s", x.frm, asm)
            if asm.find("ADD") != -1 and asm.find("PC") != -1:
                return get_func_start_addr(x.frm)

        return BADADDR

    def __del_all_bpt(self):
        DelBpt(self.open_func_addr)
        DelBpt(self.strtol_func_done_addr)
        DelBpt(self.strstr_func_addr)
        DelBpt(self.time_func_done_addr)
        DelBpt(self.mmap_func_done_addr)
        DelBpt(self.mmap_func_addr)
        DelBpt(self.munmap_func_addr)

    def __bp_open(self):
        str = GetString(GetRegValue("r0"))
        logging.debug("open(%s)", str)
        if self.fix_rtld_db_dlactivity_finish == 0:
            if str == "/system/bin/linker":
                logging.debug("AddBpt strstr_func_addr %x",
                              self.strstr_func_addr)
                AddBpt(self.strstr_func_addr)
                self.__fix_rtld_db_dlactivity()
                self.fix_rtld_db_dlactivity_finish = 1
                DelBpt(self.open_func_addr)
                return

    def __bp_strstr(self):
        str0 = GetString(GetRegValue("r0"))
        str = GetString(GetRegValue("r1"))
        logging.debug("strstr(%s,%s)", str0, str)

        if self.fix_tracerpid_finish == 0 and self.strtol_func_done_addr_bp == 0:
            if str0.find("TracerPid") != -1:
                logging.debug("AddBpt strtol_func_done_addr")
                AddBpt(self.strtol_func_done_addr)
                self.strtol_func_done_addr_bp = 1
                return

        if self.fix_android_server_port_finish == 0:
            if str == "00000000:5D8A":
                self.__fix_android_server_port()
                self.fix_android_server_port_finish = 1
                return

    def __bp_mmap(self):
        r = ArmReg()
        logging.debug('mmap: ' + str(r))

    def __bp_mmap_done(self):
        r = ArmReg()
        logging.debug('mmap_done: ' + str(r))
        if r.R0 == 0x4a425000:
            self.exit = True

    def __bp_munmap(self):
        r = ArmReg()
        logging.debug('munmap: ' + str(r))

    def __bp_JNIEnv_FindClass(self):
        strClass = GetString(GetRegValue("r1"))
        logging.debug("JNIEnv_FindClass(%s)", strClass)
        if self.activity_onCreate_addr == BADADDR and strClass == self.activity_name:
            AddBpt(self.JNIEnv_FindClass_done_addr)
            # DelBpt(self.JNIEnv_FindClass)

    def __bp_JNIEnv_FindClass_done(self):
        self.activity_handle = GetRegValue("r0")
        logging.debug("activity_handle=0x%x",
                      self.activity_handle)
        DelBpt(self.JNIEnv_FindClass_done_addr)
        # logging.debug("AddBpt JNIEnv_RegisterNatives: 0x%x", self.JNIEnv_RegisterNatives)
        # AddBpt(self.JNIEnv_RegisterNatives)

    def __bp_JNIEnv_RegisterNatives(self):
        env = GetRegValue("r0")
        clazz = GetRegValue("r1")
        base = GetRegValue("r2")
        count = GetRegValue("r3")
        logging.debug(
            "__JNIEnv_RegisterNatives(0x%x, 0x%x, 0x%x, %d)", env, clazz, base, count)
        for i in xrange(0, count):
            addr = base + i * 3 * 4
            func_name = GetString(DbgDword(addr))
            func_type = GetString(DbgDword(addr + 4))
            func_addr = DbgDword(addr + 8)
            logging.debug(
                "%d: JNINativeMethod{%s, %s, 0x%x}", i, func_name, func_type, func_addr)
            if self.activity_onCreate_addr == BADADDR and self.activity_handle is not None and self.activity_handle == clazz:
                if func_name == "onCreate":
                    self.activity_onCreate_addr = func_addr - 1
                    logging.debug("fidn onCreate.addr: 0x%x",
                                  self.activity_onCreate_addr)
                    self.jiagu_second_seg_base = self.__get_second_seg_base(
                        self.activity_onCreate_addr)
                    if self.jiagu_second_seg_base != BADADDR:
                        logging.debug("jiagu_second_seg_base: 0x%x",
                                      self.jiagu_second_seg_base)
                        AnalyzeArea(self.activity_onCreate_addr,
                                    self.activity_onCreate_addr + 0x20)
                        self.__analyze_area_seg(self.jiagu_second_seg_base)
                        AddBpt(
                            self.activity_onCreate_addr)
                        #self.exit = True
                    else:
                        logging.error("__get_second_seg_base failed.")
                        self.exit = True

    def __fix_rtld_db_dlactivity(self):
        logging.info("fix rtld_db_dlactivity")
        PatchWord(self.rtld_db_dlactivity_addr, 0xBF00)

    def __fix_tracerpid(self):
        logging.info("fix /proc/self/status")
        logging.info("fix before: %s", hex(GetRegValue("r0")))
        SetRegValue(0, "r0")
        logging.info("fix after: %s", hex(GetRegValue("r0")))

    def __fix_android_server_port(self):
        logging.info("fix /proc/net/tcp")
        r1 = GetRegValue("r1")
        PatchByte(r1 + 0xc, 0x42)

    def __fix_time(self):
        logging.info("fix time 0x%x", self.fix_time)
        SetRegValue(self.fix_time, "r0")
        self.fix_time = self.fix_time + 1

    def __get_second_seg_base(self, addr):
        base = FirstSeg()
        while base != BADADDR:
            # name=SegName(base)
            start = SegStart(base)
            end = SegEnd(base)
            if addr >= start and addr <= end:
                break
            base = NextSeg(base)
        return base

    def __analyze_area_seg(self, base):
        start = SegStart(base)
        end = SegEnd(base)
        logging.debug('AnalyzeArea(0x%x, 0x%x)', start, end)
        AnalyzeArea(start, end)

    def __dump_dex(self):
        base = FirstSeg()
        while base != BADADDR:
            name = SegName(base)
            if name.startswith("debug"):
                start = SegStart(base)
                ver = DbgRead(start, 7)
                if ver == "dex\n035":
                    # end=SegEnd(base)
                    size = DbgDword(start + 0x20)
                    logging.info("dump dex(%s, 0x%x:0x%x) called",
                                 name, start, size)
                    path = self.py_path + "\\" + name + ".dex"
                    dump_mem(path, start, size)
                    logging.info("dump dex(%s, 0x%x:0x%x) done",
                                 name, start, size)
            base = NextSeg(base)

    def __find_jumptable(self, base, size):
        end = base + size
        addr = base
        while addr != BADADDR:
            if addr >= end:
                break
            asm = GetDisasm(addr)
            logging.debug("0x%x, %s", addr, asm)
            # if asm.find("jumptable") != -1 or asm.find('switch') != -1 or asm.find('case') != -1 or asm.find('default') != -1:
            #    logging.debug("0x%x, %s", addr, asm)
            addr = NextHead(addr)
        return BADADDR

    def __find_opcode_insns(self, base, size, value):
        end = base + size
        addr = base
        while addr + 4 < end:
            if value == DbgDword(addr):
                return addr
            addr += 1
        return BADADDR

    def __hit_opcode_table(self, base):
        hit = 0
        addr = PrevHead(base)
        while True:
            addr = NextHead(addr)
            asm = GetDisasm(addr)
            # logging.debug(asm)
            # print asm
            if asm.startswith("DCW"):
                hit = hit + 1
            else:
                break
        return hit

    def __find_opcode_table(self, base, size):
        end = base + size
        addr = base
        while addr != BADADDR:
            if addr >= end:
                break

            list_xref = []
            for xref in XrefsTo(addr):
                list_xref.append(xref)

            count = len(list_xref)
            if count > 30:
                logging.debug(
                    "------------------------------------0x%x:%d", addr, count)
                if qj.__hit_opcode_table(addr) > 10:
                    logging.info(
                        '==============================================0x%x:%d', addr, count)
                    # for xref in list_xref:
                    # logging.debug('%d %s from 0x%x to 0x%x', xref.type,
                    # XrefTypeName(xref.type), xref.frm, xref.to)
                    return addr

            addr = NextHead(addr)
        return BADADDR

    def __find_opcode_entry(self, base):
        addr = PrevHead(base)
        while addr != BADADDR:
            asm = GetDisasm(addr)
            logging.debug(asm)

            if asm.find("PUSH") != -1 and asm.find("LR") != -1:
                break

            list_xref = []
            for xref in XrefsTo(addr):
                list_xref.append(xref)

            count = len(list_xref)
            if count > 1:
                logging.info(
                    '==============================================0x%x:%d', addr, count)
                # for xref in list_xref:
                # logging.debug('%d %s from 0x%x to 0x%x', xref.type,
                # XrefTypeName(xref.type), xref.frm, xref.to)
                return addr

            addr = PrevHead(addr)

        return BADADDR

    def __decode_dalvik_opcode(self):
        vm_ctx_addr = GetRegValue("R4")
        opcode_addr = DbgDword(vm_ctx_addr)
        decode_key = DbgByte(vm_ctx_addr + 4)
        # logging.debug("vm_ctx_addr:0x%x, opcode_addr:0x%x,
        # decode_key:0x%x",vm_ctx_addr,opcode_addr,decode_key)
        opcode_end = opcode_addr + 0x3f8
        while True:
            opcode_encode = DbgByte(opcode_addr)
            opcode_decode = opcode_encode ^ decode_key
            logging.debug("opcode_encode:0x%x, opcode_decode:0x%x",
                          opcode_encode, opcode_decode)
            opcode_addr = opcode_addr + 1
            if opcode_addr >= opcode_end:
                return

    def get_dalvik_opcode_code_table(self):
        path = self.py_path + "\\dalvik_opcode_code.table"
        fp = open(path, "r")
        if not fp:
            logging.error("open %s failed.", path)
            return None
        dalvik_opcode_code_table = fp.readlines()
        fp.close()
        return dalvik_opcode_code_table

    def get_dalvik_opcode_code(self, dalvik_opcode_code_table, index):
        dalvik_opcode_code_table_line = dalvik_opcode_code_table[index]
        dalvik_opcode_code_table_line_list = dalvik_opcode_code_table_line.split(
            ",")
        return dalvik_opcode_code_table_line_list[0]

    def write_dalvik_opcode_asm(self, dalvik_opcode_code_table, index, dalvik_opcode_asm_lines):
        filename = self.get_dalvik_opcode_code(dalvik_opcode_code_table, index)
        path = self.py_path + "\\opcode\\" + filename
        if os.path.exists(path):
            return
        fp = open(path, "w")
        if not fp:
            logging.error("open %s failed.", path)
            return
        fp.writelines(dalvik_opcode_asm_lines)
        fp.close()

    def __goto_next(self, addr):
        logging.debug("__goto_next(0x%x)", addr)
        AddBpt(addr)
        while True:
            ResumeProcess()
            event = GetDebuggerEvent(WFNE_SUSP, -1)
            if event < 0:
                logging.error("event:0x%x", event)
                DelBpt(addr)
                return False
            logging.debug("event:0x%x", event)
            if event != 0x10:
                continue
            ea = GetEventEa()
            if ea == addr:
                DelBpt(addr)
                return True

    def __is_while(self, base, end):
        addr = base
        while addr != BADADDR and addr <= end:
            type = GetOpType(addr, 0)
            if type == 5 or type == 6 or type == 7:
                return True
            addr = NextHead(addr)
        return False

    def __tracing_opcode(self, entry_addr):
        logging.info("=======================================================")
        opcode_path = self.py_path + "\\opcode"
        if os.path.isdir(opcode_path):
            shutil.rmtree(opcode_path)
        os.makedirs(opcode_path)
        DelBpt(entry_addr)
        EnableTracing(TRACE_STEP, 1)
        ResumeProcess()
        dump_asm = False
        tracing_opcode_index = -1
        dalvik_opcode_code_table = self.get_dalvik_opcode_code_table()
        dalvik_opcode_asm_lines = []
        goaddr_start = BADADDR
        while True:
            event = GetDebuggerEvent(WFNE_ANY, -1)
            if event <= 1:
                break

            addr = GetEventEa()
            if addr == entry_addr:
                dump_asm = False

            asm = GetDisasm(addr)
            logging.debug("0x%x %s", addr, asm)

            if dump_asm == False:
                if addr == 0x4A512CC4 or addr == 0x4A53CBA0:
                    logging.info(
                        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++, %d", tracing_opcode_index)
                    if len(dalvik_opcode_asm_lines) > 0:
                        self.write_dalvik_opcode_asm(
                            dalvik_opcode_code_table, tracing_opcode_index, dalvik_opcode_asm_lines)
                        dalvik_opcode_asm_lines = []
                    tracing_opcode_index = tracing_opcode_index + 1
                    dump_asm = True

            if dump_asm == True:
                # asm=GetDisasm(addr)
                dalvik_opcode_asm_lines.append(strf("%s\n", asm))
                # logging.info("0x%0x %s", addr, asm)

            list_xref = []
            for xref in XrefsTo(addr):
                list_xref.append(xref)

            if len(list_xref) > 1:
                goaddr_start = addr

            if dump_asm == True and asm.startswith("BNE"):
                type = GetOpType(addr, 0)
                if type in [o_mem, o_far, o_near, o_displ]:
                    goaddr = GetOperandValue(addr, 0)
                    if goaddr_start != BADADDR and goaddr >= goaddr_start and goaddr < addr:
                        logging.debug(
                            "addr:0x%x, goaddr_start:0x%x, goaddr:0x%x", addr, goaddr_start, goaddr)
                        EnableTracing(TRACE_STEP, 0)
                        nextaddr = NextHead(addr)
                        self.__goto_next(nextaddr)
                        EnableTracing(TRACE_STEP, 1)
                        ResumeProcess()
                        goaddr_start = BADADDR
                        asm = GetDisasm(nextaddr)
                        logging.debug("0x%x %s", nextaddr, asm)
                        dalvik_opcode_asm_lines.append(strf("%s\n", asm))

        EnableTracing(TRACE_STEP, 0)

    def __tracing_opcode_oncreate2(self, start, end, value):
        logging.debug(
            "=======================================================")
        EnableTracing(TRACE_INSN, 1)
        ResumeProcess()
        while True:
            event = GetDebuggerEvent(WFNE_ANY, -1)
            logging.debug('event: 0x%x', event)
            if event <= 0:
                break

            addr = GetEventEa()
            logging.debug('addr: 0x%x', addr)
            if addr >= start and addr <= end:
                asm = GetDisasm(addr)
                logging.debug(asm)
                if self.__has_reg_value(value):
                    logging.debug('__has_reg_value')
                    break

        EnableTracing(TRACE_INSN, 0)
        PauseProcess()

    def __tracing_opcode_oncreate(self, start, end, value, count=-1):
        logging.debug(
            "=======================================================")
        bp_addr = BADADDR
        StepInto()
        i = 0
        while True:
            event = GetDebuggerEvent(WFNE_SUSP, 30)
            if event <= 0:
                logging.debug("event: 0x%x", event)
                break

            if event != BREAKPOINT:
                logging.debug("event: 0x%x", event)
                StepOver()
                continue

            if bp_addr != BADADDR:
                #logging.debug('DelBpt %x', bp_addr)
                DelBpt(bp_addr)
                bp_addr = BADADDR

            i += 1
            if count > 0 and i > count:
                break

            #addr = GetEventEa()
            r = ArmReg()
            addr = r.PC

            if addr >= start and addr <= end:
                if r == value:
                    break
                logging.debug(str(r))
                '''
                if asm.startswith("BL") or asm.startswith("BLX"):
                    bl_addr = GetOperandValue(addr, 0)
                    if bl_addr >= start and bl_addr <= end:
                        #logging.debug('0x%x jmp 0x%x StepInto', addr, bl_addr)
                        StepInto()
                    else:
                        #logging.debug('0x%x jmp 0x%x StepOver', addr, bl_addr)
                        StepOver()
                else:
                    StepInto()
                '''
                StepInto()
            else:
                # StepUntilRet()
                bp_addr = r.LR - 1
                #logging.debug('AddBpt %x', bp_addr)
                AddBpt(bp_addr)
                ResumeProcess()

    def __tracing_code(self, start, end, value, count=-1):
        find = False
        bp_addr = BADADDR
        StepInto()
        i = 0
        while True:
            event = GetDebuggerEvent(WFNE_SUSP, 30)
            if event <= 0 or event != BREAKPOINT:
                logging.debug("event: 0x%x", event)
                break

            if bp_addr != BADADDR:
                DelBpt(bp_addr)
                bp_addr = BADADDR

            r = ArmReg()
            addr = r.PC

            logging.debug(str(r))

            if r == value:
                find = True
                break

            i += 1
            if count > 0 and i > count:
                break

            if addr >= start and addr <= end:
                StepInto()
            else:
                bp_addr = r.LR
                if AddBpt(bp_addr) is False:
                    bp_addr -= 1
                    AddBpt(bp_addr)
                ResumeProcess()
        return find

    def __is_while(self, addr):
        opcode = get_arm_opcode(addr)
        if opcode != 0x1A:
            return False
        if 7 != GetOpType(addr, 0):
            return False
        jmp_addr = GetOperandValue(addr, 0)
        if jmp_addr >= addr:
            return False
        offset = jmp_addr
        while offset < addr:
            opcode = get_arm_opcode(offset)
            # BEQ=0x0A B=0xEA BNE=0x1A BX=0xE1
            if (opcode == 0x0A or opcode == 0xEA or opcode == 0xE1 or opcode == 0x1A) and 7 == GetOpType(offset, 0):
                jmp_addr_tmp = GetOperandValue(offset, 0)
                if jmp_addr_tmp < jmp_addr or jmp_addr_tmp > addr:
                    return False
            offset = NextHead(offset)
        return True

    def __tracing_code_value(self, start, end, value, count=-1):
        find = False

        '''
        stack_base = get_seg_base('[stack]')
        if stack_base != BADADDR:
            stack_end = SegEnd(stack_base)
        else:
            return find
        '''

        bp_addr = BADADDR
        StepInto()
        i = 0
        while True:
            event = GetDebuggerEvent(WFNE_SUSP, 30)
            if event <= 0:
                logging.debug("event: 0x%x", event)
                break

            if event != BREAKPOINT:
                logging.debug("event: 0x%x", event)
                break

            if bp_addr != BADADDR:
                DelBpt(bp_addr)
                bp_addr = BADADDR

            r = ArmReg()
            addr = r.PC
            asm = GetDisasm(addr)
            logging.debug('0x%08x %s', addr, asm)
            logging.debug(str(r))

            i += 1
            if count > 0 and i > count:
                logging.debug("count")
                break

            if addr >= start and addr <= end:
                if self.__eq_addr_value(r, value):
                    find = True
                    break
                '''
                if self.__is_while(addr):
                    bp_addr = NextHead(addr)
                    AddBpt(bp_addr)
                    ResumeProcess()
                else:
                    StepInto()
                '''
                StepInto()
            else:
                bp_addr = r.LR
                if AddBpt(bp_addr) is False:
                    bp_addr -= 1
                    AddBpt(bp_addr)
                ResumeProcess()
        return find

    def __eq_addr_value(self, reg, value):
        for i in xrange(0, 13):
            val = getattr(reg, 'R%d' % i)
            if val != 0:
                elf = DbgDword(val)
                if elf is not None and elf == value:
                    return True
        return False

    def __has_reg_value(self, value):
        find = False
        strlog = '\n'
        for i in xrange(0, 13):
            rn = "r%d" % i
            rv = GetRegValue(rn)
            strlog += '%s:0x%x\n' % (rn, rv)
            if rv == value:
                find = True
                break

        rn = "sp"
        rv = GetRegValue(rn)
        strlog += '%s:0x%x\n' % (rn, rv)

        rn = "lr"
        rv = GetRegValue(rn)
        strlog += '%s:0x%x\n' % (rn, rv)

        rn = "pc"
        rv = GetRegValue(rn)
        strlog += '%s:0x%x\n' % (rn, rv)

        logging.debug(strlog)
        return find

    def __make_comm(self, addr, desc):
        MakeComm(addr, desc)
        for xref in XrefsTo(addr):
            logging.debug('%d %s from 0x%x to 0x%x', xref.type,
                          XrefTypeName(xref.type), xref.frm, xref.to)
            MakeComm(xref.frm, desc)

    def __save_switch_offset_table(self, switch_table_path, switch_table_addr):
        switch_table = []
        offset = switch_table_addr
        for x in xrange(255):
            logging.debug('%d 0x%x 0x%08x', x, offset, DbgDword(offset))
            switch_table_line = '0x%08x\n' % DbgDword(offset)
            switch_table.append(switch_table_line)
            offset += 4

        offset = switch_table_addr
        while offset != BADADDR:
            asm = GetDisasm(offset)
            logging.debug('find default case: ' + asm)
            if asm.find('default case') != -1:
                break
            offset = PrevHead(offset)
        def_addr = GetOperandValue(offset, 0)
        logging.debug('find default case addr: ' + hex(def_addr))
        def_addr_off = def_addr - switch_table_addr
        logging.debug('0x%08x', def_addr_off)
        switch_table_line = '0x%08x' % def_addr_off
        switch_table.append(switch_table_line)
        fp2 = open(switch_table_path, "w")
        if not fp2:
            return
        fp2.writelines(switch_table)
        fp2.close()

    def __dump_decode_insns(self):
        vm_ctx_addr = GetRegValue("r4")
        opcode_addr = DbgDword(vm_ctx_addr)
        decode_key = DbgByte(vm_ctx_addr + 4)
        logging.debug(
            '__dump_insns: opcode_addr:0x%x decode_key:0x%x', opcode_addr, decode_key)
        size = 0x3f8

        dump_mem(self.py_path + '\\360_encode.insns', opcode_addr, size)

        data = bytearray([0] * size)
        for i in xrange(size):
            data[i] = DbgByte(opcode_addr + i) ^ decode_key
        decode_insns_path = self.py_path + '\\360_decode.insns'
        fpw = open(decode_insns_path, "wb")
        if not fpw:
            logging.error('cannot open the %s for writing', decode_insns_path)
        fpw.write(data)
        fpw.close()

    def __loop(self):
        self.__del_all_bpt()
        AddBpt(self.jni_onload_addr)
        while True:
            ResumeProcess()
            code = GetDebuggerEvent(WFNE_SUSP, -1)
            if code <= 0:
                return Failed(code)
            # logging.debug("GetDebuggerEvent(): %x", code)

            if code != 0x10:
                continue

            eventEa = GetEventEa()
            # logging.debug("GetEventEa(): %x", eventEa)

            if eventEa == self.jni_onload_addr:
                DelBpt(self.jni_onload_addr)
                AddBpt(self.open_func_addr)
                AddBpt(self.time_func_done_addr)
            elif eventEa == self.open_func_addr:
                self.__bp_open()
            elif eventEa == self.strstr_func_addr:
                self.__bp_strstr()
            elif eventEa == self.strtol_func_done_addr:
                if self.fix_tracerpid_finish == 0:
                    self.__fix_tracerpid()
                    self.fix_tracerpid_finish = 1
                    DelBpt(self.strtol_func_done_addr)
            elif eventEa == self.time_func_done_addr:
                self.__fix_time()
                if self.JNIEnv_bp == 1:
                    self.fix_time_finish += 1
                    if self.fix_time_finish == 2:
                        AddBpt(self.mmap_func_addr)
                        AddBpt(self.mmap_func_done_addr)
                        AddBpt(self.munmap_func_addr)
                        #self.exit = True
            elif eventEa == self.mmap_func_addr:
                self.__bp_mmap()
            elif eventEa == self.mmap_func_done_addr:
                self.__bp_mmap_done()
            elif eventEa == self.munmap_func_addr:
                self.__bp_munmap()
            elif eventEa == self.JNIEnv_FindClass:
                self.__bp_JNIEnv_FindClass()
            elif eventEa == self.JNIEnv_FindClass_done_addr:
                self.__bp_JNIEnv_FindClass_done()
            elif eventEa == self.JNIEnv_RegisterNatives:
                self.__bp_JNIEnv_RegisterNatives()
            elif eventEa == self.activity_onCreate_addr:
                self.exit = True
                self.__dump_dex()
                '''
                start = SegStart(self.jiagu_second_seg_base)
                end = SegEnd(self.jiagu_second_seg_base)
                self.jiagu_opcode_table_addr = self.__find_opcode_table(
                    start, end - start)
                if self.jiagu_opcode_table_addr != BADADDR:
                    self.jiagu_opcode_entry_addr = self.__find_opcode_entry(
                        self.jiagu_opcode_table_addr)
                    if self.jiagu_opcode_entry_addr != BADADDR:
                        AddBpt(self.jiagu_opcode_entry_addr)
                        # self.exit = True
                    else:
                        logging.error("__find_opcode_entry failed.")
                        self.exit = True
                else:
                    logging.error("__find_opcode_table failed.")
                    self.exit = True
                '''

            elif eventEa == self.jiagu_opcode_entry_addr:
                self.__save_switch_offset_table(
                    self.py_path + '\\360_switch_offset.table', self.jiagu_opcode_table_addr)
                self.__dump_decode_insns()
                self.exit = True
                """
                if self.jiagu_opcode_code_addr == BADADDR:
                self.jiagu_opcode_code_addr = opcode_offset
                # self.__tracing_opcode(self.jiagu_opcode_entry_addr)
                self.exit = True
                else:
                if opcode_offset > self.jiagu_opcode_code_addr + 0x3f0:
                self.exit = True
                """
            if self.fix_tracerpid_finish == 1 and self.fix_android_server_port_finish == 1:
                DelBpt(self.strstr_func_addr)

            if self.fix_tracerpid_finish == 1 and self.fix_android_server_port_finish == 1 and self.fix_rtld_db_dlactivity_finish == 1 and self.JNIEnv_bp == 0:
                logging.debug("AddBpt JNIEnv_FindClass: 0x%x",
                              self.JNIEnv_FindClass)
                AddBpt(self.JNIEnv_FindClass)
                logging.debug("AddBpt JNIEnv_RegisterNatives: 0x%x",
                              self.JNIEnv_RegisterNatives)
                AddBpt(self.JNIEnv_RegisterNatives)
                self.JNIEnv_bp = 1

            if self.exit:
                break

    def run(self):
        self.__logging_config()
        ret = self.__init_addr()
        if ret == True:
            self.__loop()

    def test(self):
        # soname="libdvm.so"
        # analyze_area_module(soname)
        logging.debug("0x%x", self.JNIEnv_FindClass)
        self.JNIEnv_FindClass_done_addr = get_func_end_addr(
            self.JNIEnv_FindClass)
        if BADADDR == self.JNIEnv_FindClass_done_addr:
            logging.error(
                "get JNIEnv_FindClass_done_addr function address faild.")
        logging.info("JNIEnv_FindClass_done_addr=0x%x",
                     self.JNIEnv_FindClass_done_addr)

    def test_find_opcode_execute_entry(self):
        base = self.__find_opcode_table(0x4A512000, 0x4A5AB000 - 0x4A512000)
        logging.debug('__find_opcode_table: 0x%x', base)
        #logging.info("0x%x", self.__find_opcode_entry(base))

    def test_find_jumptable(self):
        #self.__find_jumptable(0x4A512000, 0x4A5AB000 - 0x4A512000)
        dump_mem(self.py_path + '\\second.so',
                 0x4A512000, 0x4A5AB000 - 0x4A512000)

    def test_find_opcode_insns(self):
        start = 0x4A443000
        end = 0x4A4A7000
        addr = self.__find_opcode_insns(start, end - start, 0xc035b0c5)
        logging.debug('__find_opcode_insns: 0x%x', addr)

    def test_decode_dalvik_opcode(self):
        self.__decode_dalvik_opcode()

    def test_tracing_opcode(self):
        self.__tracing_opcode(0x4A512CA6)

    def test_save_switch_offset_table(self):
        self.__save_switch_offset_table(
            self.py_path + '\\360_switch_offset.table', 0x4a512ccc)

    def test_dump_decode_insns(self):
        self.__dump_decode_insns()

    def test_analyze_area_seg(self):
        seg_base = self.__get_second_seg_base(0x4a51f10b)
        if seg_base != BADADDR:
            logging.debug('__get_second_seg_base 0x%x.', seg_base)
            self.__analyze_area_seg(seg_base)
        else:
            logging.error('__get_second_seg_base failed.')

    def test_dump_dex(self):
        self.__dump_dex()

    def test_tracing_code(self):
        find = self.__tracing_code(
            0x4A512000, 0x4A5AB000, 0x4A443000 + 0x54370)
        if find:
            self.__tracing_code(0x4A512000, 0x4A5AB000, 0xb0c5, 200)

    def test_tracing_code_value(self):
        (base, end) = get_seg('libjiagu.so')
        logging.debug('libjiagu.so 0x%x:0x%x', base, end)
        logging.debug(self.__tracing_code(base, end, 0x4A477008, 1000))
        # debug083 4A425000 4A477000 R W . D . byte 00 public DATA 32 00 00

    def test_has_reg_value(self):
        self.__has_reg_value(0x4A497370)

    def test_make_comm(self):
        self.__make_comm(0x40731EBC, 'GetMethodID')

    def test_is_while(self):
        logging.debug(self.__is_while(0x4A3C94A8))

    def test_dump_seg(self):
        path = self.py_path + '\\stack'

    def test_find_dword_seg(self):
        logging.debug(find_dword_seg('[stack]', 0x464C457F))


def main():
    qj = QihooJiagu()
    qj.run()
    '''
    addr = GetRegValue('PC')
    if addr == 0x40003DDA:
        qj.run()
    else:
        qj.test_tracing_code_value()
    '''

if __name__ == "__main__":
    main()
