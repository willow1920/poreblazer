#!/usr/bin/python
"""
poreblazer.py - a utility to assist running poreblazer analysis on lammps output
By Sibo Lin, August 20, 2020
input: a lammps output file (.lmps)
output: poreblazer output (density, ffv, accessible surface area, etc.)
setup: edit the variables to reflect your system's setup: poreblazerEXE, UFFfile, and defaultsFile; make this file executable (chmod)
execution: poreblazer.py file.lmps
"""
import sys, os
from shutil import copyfile
poreblazerEXE = "/home/SXL374/poreblazer/poreblazer.exe"
UFFfile = "/home/SXL374/poreblazer/HKUST1/UFF.atoms"
defaultsFile = "/home/SXL374/poreblazer/HKUST1/defaults.dat"

def main():
	for word in sys.argv:
		print word
	if os.path.isfile(sys.argv[1]):
		print('reading lmps file: ' + sys.argv[1])
		f = file(sys.argv[1])
		filename = sys.argv[1].split('.')[0]
	else:
		print(sys.argv[1] + ' is not a file')
	x = 0
	y = 0
	z = 0
	for line in f:
		if 'xlo xhi' in line:
			x = 2*float(line.split()[1])
			print('x dim = ' + str(x))
		elif 'ylo yhi' in line:
			y = 2*float(line.split()[1])
			print('y dim = ' + str(y))
		elif 'zlo zhi' in line:
			z = 2*float(line.split()[1])
			print('z dim = ' + str(z))
		elif x*y*z != 0:
			break
	f.close()
	f = open('input.dat','w')
	f.write(filename + '_poreblazer.xyz\n')
	f.write(str(x) + '\t' + str(y) + '\t' + str(z) + '\n')
	f.write('90 \t 90 \t 90 \n')
	f.close()
	
	#for poreblazer code related to surface area, need to transpose .xyz file so all atoms are in the positive octant
	f = open(filename + '_poreblazer.xyz',"w+")
	g = open(filename + '.xyz')
	for line in g:
		newLine = line
		if len(line.split()) == 4:
			if is_number(line.split()[1]) and is_number(line.split()[2]) and is_number(line.split()[3]):
				newLine = line.split()[0] + transpose(line.split()[1],x) + transpose(line.split()[2],y) + transpose(line.split()[3],y) + "\n"
		f.write(newLine)	
	f.close()
	g.close()

	copyfile(UFFfile,"UFF.atoms")
	copyfile(defaultsFile,"defaults.dat")
	os.system(poreblazerEXE + " < input.dat | tee poreblazerOutput.txt")

def transpose(n,dim):
	return "\t" + str(float(n)+dim/2)

def is_number(n):
	try:
		float(n)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	main()

