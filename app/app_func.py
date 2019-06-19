#!/usr/bin/env python
#coding: utf-8

import os
import re
import cmd
import json
import paramiko
import requests
from app.app_common_class import SSHClient
from app.app_common_class import Output
from app.app_common_class import ShellCLI

def sftp_upload_file(host,user,passwd,local_file,server_file):
    output=Output()
    try:
        remote = paramiko.Transport((host, 22))
        remote.connect(username=user, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(remote)
        sftp.put(local_file, server_file)
        output.print_info("upload "+local_file+" success")
        remote.close()
    except Exception as error:
        output.print_result(error)


def addlog(username,passwd,host):
    port = 22
    web_path = '/var/www/html'
    auth = (True,passwd)
    output = Output()
    try:
        output.print_info('upload log and script ...')
        sftp_upload_file(host,username,passwd,'./script/py/addlog.py','/home/addlog.py')
        sftp_upload_file(host,username,passwd,'./script/php/log-record.php','/home/log-record.php')
        output.print_info("Execute script")
        addlog_user = SSHClient(host, port, username, auth, timeout=5)
        addlog_user.save_log() #write log
        output.print_info('write log success')
        addlog_user.exec_command('python /home/addlog.py set '+web_path+' /home/log-record.php')
        output.print_result("add log success to "+web_path)
    except Exception as error:
        print ("[\033[1;31merror\033[0m] %s" % (error))


def unlog(username,passwd,host):
    port = 22
    web_path = '/var/www/html'
    auth = (True,passwd)
    output = Output()
    try:
        output.print_info('Execute script')
        unlog_user = SSHClient(host, port, username, auth, timeout=5)
        unlog_user.save_log() #write log
        output.print_info('write log success')
        unlog_user.exec_command('python /home/addlog.py unset '+web_path+' /home/log-record.php')
        output.print_result("you have unlog to "+web_path)
    except Exception as error:
        print ("[\033[1;31merror\033[0m] %s" % (error))


def backup(username,passwd,host):
    port = 22
    web_path = '/var/www/html'
    backup_path = '/tmp/backup_'+host+'_.tar.gz'
    auth = (True,passwd)
    output = Output()
    try:
        output.print_info('Execute Command')
        bac_user = SSHClient(host, port, username, auth, timeout=5)
        bac_user.save_log() #write log
        output.print_info('write log success')
        bac_user.exec_command('tar -czvf '+backup_path+' '+web_path)
        output.print_result("you have backed up "+web_path+" in "+backup_path)
    except Exception as error:
        print ("[\033[1;31merror\033[0m] %s" % (error))


def getshell(host,method,passwd):
    #port = 80
    output = Output()
    try:
        output.print_info('Start Connecting')
        shell = ShellCLI(host,method,passwd)
        shell.shell_cmd_loop()
        #shell.save_info('./runtime/shell.log') #可能会记录无用shell
    except Exception as error:
        print ("[\033[1;31merror\033[0m] %s" % (error))


def ps():
    filepath = './runtime/log.json'
    if os.path.isfile(filepath):
        with open(filepath) as json_file:
            log = json.load(json_file)
            ssh_id = 0
            shell_id = 0
            print ('-------------------SSH-------------------\n')
            for ssh in log['ssh']:
                print ('['+str(ssh_id)+']. '+ssh['username']+':'+ssh['passwd']+'@'+ssh['host'])
                ssh_id = ssh_id + 1
            print ('-------------------SHELL-----------------\n')
            for shell in log['shell']:
                print ('['+str(shell_id)+']. '+shell['url']+' '+shell['method']+' '+shell['passwd'])
                shell_id = shell_id + 1
    else:
        print ('File not exist!')


def ssh_interbak(host):
    file_path = './runime/run.log'
    if os.path.isfile(file_path):
        hosts = open(file_path)
        for line in hosts.readlines():
            if host in line:
                args1 = line.strip() 
                if re.match(r'.*?\:.*?\@.*?',args1):
                    username = args1.split(':')[0]
                    passwd = args1.split(':')[1].split('@')[0]
                    host = args1.split(':')[1].split('@')[1]
                    auth = (True,passwd)
                    port = 22
                    ssh_client = SSHClient(host, port, username, auth, timeout=5)
                    ssh_client.interaction()
                else:
                    print ("Format Wrong!")
    else:
        print ('no '+file_path)


def ssh_inter(num):
    file_path = './runtime/log.json'
    ssh_id = 0
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            log = json.load(json_file)
            for ssh in log['ssh']:
                if str(ssh_id) == num:
                    username = ssh['username']
                    passwd = ssh['passwd']
                    host = ssh['host']
                    auth = (True,passwd)
                    port = ssh['port']
                    ssh_client = SSHClient(host, port, username, auth, timeout=5)
                    ssh_client.interaction()
                    break
                ssh_id = ssh_id + 1
    else:
        print ('no '+file_path)


def g(num):
    file_path = './runtime/log.json'
    shell_id = 0
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            log = json.load(json_file)
            for shell in log['shell']:
                if str(shell_id) == num:
                    url = shell['url']
                    method = shell['method']
                    passwd = shell['passwd']
                    getshell(url,method,passwd)
                    break
                shell_id = shell_id + 1
    else:
        print ('no '+file_path)
