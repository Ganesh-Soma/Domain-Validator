import subprocess
import sys
import re
import signal
import socket
from bs4 import BeautifulSoup
import requests
import argparse
import threading

parser = argparse.ArgumentParser() 
parser.add_argument("-s",dest="single_input",help="E.g : www.amrita.edu",metavar="Single Input")
parser.add_argument("-f",dest="file_input",help="E.g : domains.txt",metavar="File Input")
parser.add_argument("-o",dest="file_output",help="E.g : output.txt",metavar="File Output")

if len(sys.argv)==1:
	parser.print_help()
	sys.exit(1)
args=parser.parse_args()

global flag_write
global ofile
flag_write = False


def sig_handler(signum,frm):
	print("\n [+] Keyboard Intrrupt, Exiting ...")
	if flag_write:
		ofile.close()
	sys.exit()

signal.signal(signal.SIGINT,sig_handler)


def check_val(domain_name):

	cmd = "host %s"%domain_name
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True).communicate()[0]

	valid = re.search('has address'.encode(),p)
	timed_out = re.search('timed out'.encode(),p)
	not_valid = re.search('not found'.encode(),p)

	if valid:
		output = "%s : Valid website "%domain_name

		flag=0
		https_domain_name = "http://"+domain_name
		#http_domain_name = "http://"+domain_name
		try:
			r = requests.get(https_domain_name)
			soup = BeautifulSoup(r.content, 'html5lib')
			for f in soup.body.find_all('form'):
				flag=1
				break
		except:
			flag = 2
			print("%s : Unable to connect with server"%domain_name)

		if(flag==1):
			print(output+"- Testable")
			if flag_write:
				writer = "%s \n"%domain_name
				ofile.write(writer)
				

		elif(flag==0):
			print(output+"- Not Testable")

	elif not_valid:
		output = "%s : Not a Valid website"%domain_name
		print(output)

	else:
		output = "%s : Connection Timed Out"%domain_name
		print(output)

	

if args.file_output:
	output_file = args.file_output
	ofile = open(output_file,'w')
	flag_write = True

if args.single_input:
	check_val(args.single_input)
	if flag_write:
		print("[+] Testable Websites saved in %",output_file)

if args.file_input:
	ifile = open(args.file_input,'r').readlines()
	for domain in ifile:
		domain = domain.strip('\n')
		check_val(domain)

	if flag_write:
		print("\n [+] Testable Websites saved in ",args.file_output)
		ofile.close()
		

