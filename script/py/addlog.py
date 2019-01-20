#!/usr/bin/env python
#coding=utf-8

import os
import sys

def scan_files(directory, prefix=None, postfix=None):
	file_list = []
	directory = os.path.normpath(directory)
	for parent, dirnames, filenames in os.walk(directory):
		for filename in filenames:
			if postfix:
				if filename.endswith(postfix):
					file_list.append(os.path.join(parent, filename))
			elif prefix:
				if filename.startswith(prefix):
					file_list.append(os.path.join(parent, filename))
			else:
				file_list.append(os.path.join(parent, filename))
				
	return file_list
	
def set_waf(filename, waf_file):
	if filename == waf_file:
		return
	try:
		stat = os.stat(os.path.dirname(filename))
		os.system('chmod 666 ' + filename)
		if os.access(filename, os.F_OK) and os.access(filename, os.R_OK) and os.access(filename, os.W_OK):
			fp = open(filename, 'r')
			src_fcont = fp.read()
			fp.close()
			if not src_fcont.startswith('<?php require_once("' + waf_file +'");?>\n'):
				fp = open(filename, 'w')
				dst_fcont = '<?php require_once("' + waf_file +'");?>\n' + src_fcont
				fp.write(dst_fcont)
				fp.close()
		os.chmod(filename, stat.st_mode)
	except:
		pass
		
def unset_waf(filename, waf_file):
	if filename == waf_file:
		return
	try:
		stat = os.stat(os.path.dirname(filename))
		os.system('chmod 666 ' + filename)
		if os.access(filename, os.F_OK) and os.access(filename, os.R_OK) and os.access(filename, os.W_OK):
			fp = open(filename, 'r')
			src_fcont = fp.read()
			fp.close()
			if src_fcont.startswith('<?php require_once("' + waf_file +'");?>\n'):
				fp = open(filename, 'w')
				dst_fcont = src_fcont[len('<?php require_once("' + waf_file +'");?>\n'):] 
				fp.write(dst_fcont)
				fp.close()
		os.chmod(filename, stat.st_mode)
	except:
		pass
		
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'Usage: ' + sys.argv[0] + ' [set|unset] /var/www/html /var/tmp/waf.php'
		exit()
	
	directory = os.path.normpath(sys.argv[2])
	waf_file = os.path.normpath(sys.argv[3])
	file_list = scan_files(directory, postfix='.php')
	
	for phpfile in file_list:
		if sys.argv[1] == 'set':
			set_waf(phpfile, waf_file)
		else:
			unset_waf(phpfile, waf_file)