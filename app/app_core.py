#!/usr/bin/env python
#coding: utf-8

import re
import os
import sys
import cmd
import shlex
from app.app_func import g
from app.app_func import ps
from app.app_func import addlog
from app.app_func import unlog
from app.app_func import backup
from app.app_func import getshell
from app.app_func import ssh_inter

class CLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        # 设置命令提示符
        self.prompt = "\033[96m> \033[0m"
        self.intr = ""

    def do_help(self, args):
        if args == "":
            print ("帮助")
            print ("------------")
            print ("addlog/add [username]:[password]@[host]    添加流量日志/Add log")
            print ("unlog/un [username]:[password]@[host]      卸载流量日志/Remove log")
            print ("backup/bac [username]:[password]@[host]    备份WEB目录/Back up the WEB directory")
            print ("------------")
            print ("getshell/get [url] [method] [passworld]    管理webshell/use webshell")
            print ("ssh [host]/[num]                           自动查找已连接过的主机进行ssh")
            print ("g   [num]                                  自动连接已记录过的webshell")
            print ("------------")
            print ("shell/s [command]                          使用shell命令/Use shell commands")
            print ("quit/q                                     退出工具/Quit")
        elif args == "add":
            print ("example:>add user:pass@127.0.0.1")
        else:
            print ("unknown command")

    def do_addlog(self, args1):
        if re.match(r'.*?\:.*?\@.*?',args1):
            username = args1.split(':')[0]
            passwd = args1.split(':')[1].split('@')[0]
            host = args1.split(':')[1].split('@')[1]
            addlog(username,passwd,host)
        else:
            print ("Wrong!")

    def do_unlog(self, args1):
        if re.match(r'.*?\:.*?\@.*?',args1):
            username = args1.split(':')[0]
            passwd = args1.split(':')[1].split('@')[0]
            host = args1.split(':')[1].split('@')[1]
            unlog(username,passwd,host)
        else:
            print ("Wrong!")

    def do_backup(self, args1):
        if re.match(r'.*?\:.*?\@.*?',args1):
            username = args1.split(':')[0]
            passwd = args1.split(':')[1].split('@')[0]
            host = args1.split(':')[1].split('@')[1]
            backup(username,passwd,host)
        else:
            print ("Wrong!")

    def do_getshell(self, args1):
        comline = ' '.join(args1.split())
        url = comline.split(' ')[0]
        method = comline.split(' ')[1]
        passwd = comline.split(' ')[2]
        getshell(url,method,passwd)

    def do_ssh(self,args):
        ssh_inter(args)

    def do_g(self,args):
        g(args) 

    def do_ps(self,args):
        ps()

    def do_EOF(self, line):
        return True
    
    def emptyline(self):
        pass
 
    def do_quit(self, args):
        "quit this program"
        sys.exit()

    def do_shell(self, args):
        #run a shell commad
        os.system(args)
        
    do_q = do_quit
    do_add = do_addlog
    do_un = do_unlog
    do_bac = do_backup
    do_h = do_help
    do_s = do_shell
    do_get = do_getshell