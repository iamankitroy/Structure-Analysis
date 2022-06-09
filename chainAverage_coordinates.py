#!/Users/roy/anaconda3/bin/python
# This script is used to calculate the geometric centroids of every chain in a PDB file.
# Geometric centroids are calcilated from CA atom coordinates.
# Input: <PDB-file>

import sys


#--- Get data
def dataIN(filename):
	with open(filename, 'r') as fh:
		data = fh.readlines()
	return data


#--- Set PDB fields
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

	chPos = 21			# chain ID position
	xCoor_start = 30	# x-coordinate start position
	xCoor_end = 38		# x-coordinate end position
	yCoor_start = 38	# y-coordinate start position
	yCoor_end = 46		# y-coordinate end position
	zCoor_start = 46	# z-coordinate start position
	zCoor_end = 54		# z-coordinate end position
	atom_start = 12		# atom name start position
	atom_end = 16		# atom name end position


#--- Get ATOM lines
def get_atomLines(data):
	
	# ATOM lines of CA atoms
	atomLines = [line for line in data if line.startswith("ATOM") and line[atom_start:atom_end].startswith(" CA")]
	return atomLines


#--- Get coordinates
def get_Coordinates(atomLines):

	# all chain IDs
	chains = set([line[chPos] for line in atomLines])

	# initialize atom coordinates
	atomCoor = {ch: {'x':[], 'y':[], 'z':[]} for ch in chains}

	# store x, y and z coordinates for all CA atoms of every chain
	var_null = [(atomCoor[line[chPos]]['x'].append(float(line[xCoor_start:xCoor_end])),
					atomCoor[line[chPos]]['y'].append(float(line[yCoor_start:yCoor_end])),
					atomCoor[line[chPos]]['z'].append(float(line[zCoor_start:zCoor_end])))
					for line in atomLines]

	return atomCoor


#--- Calulate average coordinate
def get_avgCoordinates(atomCoor):

	# average coordinates of every chain
	avgCoor = {ch: {'x':sum(atomCoor[ch]['x'])/len(atomCoor[ch]['x']),
					'y':sum(atomCoor[ch]['y'])/len(atomCoor[ch]['y']),
					'z':sum(atomCoor[ch]['z'])/len(atomCoor[ch]['z'])}
					for ch in atomCoor.keys()}

	return avgCoor


#--- Create dummy ATOM lines
def create_atomLines(avgCoor):

	record = 'ATOM'
	serialNum = 1
	atomName = ' CA'
	altLoc = ''
	resName = 'GLY'
	resSeq = 1
	iCode = ''

	# dummy ATOM lines for every chain centroid
	avg_atomLines = [f"{record:<6}{serialNum:>5} {atomName:<4}{altLoc:1}{resName:>3} {ch:1}{resSeq:>4}{iCode:1}   {avgCoor[ch]['x']:>8.3f}{avgCoor[ch]['y']:>8.3f}{avgCoor[ch]['z']:8.3f}\n" for ch in sorted(avgCoor.keys())]

	print(''.join(avg_atomLines))


# Main function
def main():

	filename = sys.argv[1]					# PDB file name

	set_pdbFields()							# set PDB fields

	pdb_data = dataIN(filename)				# get PDB data
	atomLines = get_atomLines(pdb_data)		# get ATOM lines
	atomCoor = get_Coordinates(atomLines)	# get CA atom coordinates
	avgCoor = get_avgCoordinates(atomCoor)	# calculate average coordinate for every chain
	create_atomLines(avgCoor)				# create ATOM lines for chain centroids

main()

# Ankit Roy
# 9th June, 2022
