#!/Users/roy/anaconda3/bin/python

import sys


def dataIN(filename):
	with open(filename, 'r') as fh:
		data = fh.readlines()
	return data


def set_pdbFields():

	global chPos
	global xCoor_start
	global xCoor_end
	global yCoor_start
	global yCoor_end	
	global zCoor_start
	global zCoor_end
	global atom_start
	global atom_end

	chPos = 21
	xCoor_start = 30
	xCoor_end = 38
	yCoor_start = 38
	yCoor_end = 46
	zCoor_start = 46
	zCoor_end = 54
	atom_start = 12
	atom_end = 16


def get_atomLines(data):
	
	atomLines = [line for line in data if line.startswith("ATOM") and line[atom_start:atom_end].startswith(" CA")]
	return atomLines


def get_Coordinates(atomLines):

	chains = set([line[chPos] for line in atomLines])

	atomCoor = {ch: {'x':[], 'y':[], 'z':[]} for ch in chains}

	var_null = [(atomCoor[line[chPos]]['x'].append(float(line[xCoor_start:xCoor_end])),
					atomCoor[line[chPos]]['y'].append(float(line[yCoor_start:yCoor_end])),
					atomCoor[line[chPos]]['z'].append(float(line[zCoor_start:zCoor_end])))
					for line in atomLines]

	return atomCoor


def get_avgCoordinates(atomCoor):

	avgCoor = {ch: {'x':sum(atomCoor[ch]['x'])/len(atomCoor[ch]['x']),
					'y':sum(atomCoor[ch]['y'])/len(atomCoor[ch]['y']),
					'z':sum(atomCoor[ch]['z'])/len(atomCoor[ch]['z'])}
					for ch in atomCoor.keys()}

	return avgCoor


def create_atomLines(avgCoor):

	record = 'ATOM'
	serialNum = 1
	atomName = ' CA'
	altLoc = ''
	resName = 'GLY'
	resSeq = 1
	iCode = ''

	avg_atomLines = [f"{record:<6}{serialNum:>5} {atomName:<4}{altLoc:1}{resName:>3} {ch:1}{resSeq:>4}{iCode:1}   {avgCoor[ch]['x']:>8.3f}{avgCoor[ch]['y']:>8.3f}{avgCoor[ch]['z']:8.3f}\n" for ch in sorted(avgCoor.keys())]

	print(''.join(avg_atomLines))


def main():

	filename = sys.argv[1]

	set_pdbFields()

	pdb_data = dataIN(filename)
	atomLines = get_atomLines(pdb_data)
	atomCoor = get_Coordinates(atomLines)
	avgCoor = get_avgCoordinates(atomCoor)
	create_atomLines(avgCoor)

main()
