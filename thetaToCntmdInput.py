"""
	Take a theta2 output file as input and convert it to the right format for CNT-MD.

"""

import sys
from glob import glob


inFileDir = sys.argv[1]
outFile = sys.argv[2]
# 
# #PARAMS
# 2 #number of chromosomes
# 4 #number of samples
# 6 6 #number of segments for each chromosome
# #SAMPLES
# 1 : 2.14 1.43 1.43 3.71 2.0 2.0 | 3.29 3.29 4.0 2.0 2.0 1.29
# 2 : 1.0 2.0 2.0 1.0 2.0 2.0 | 1.0 0.0 0.0 1.0 2.0 2.0
# 3 : 2.9 2.0 2.0 3.85 2.0 2.0 | 2.9 2.85 3.8 1.95 2.0 1.05
# 4 : 1.55 1.99 1.99 1.83 2.0 2.0 | 1.56 0.84 1.11 1.28 2.0 1.72

#1. Read all copy numbers for all samples, we need to run CNT-MD for all samples at once
sampleCopyNumbers = dict()

#1.1 Get all files with the right name in the directory
subdirs = glob(inFileDir + "/*/")

for subdir in subdirs:
	thetaOutFiles = glob(subdir + "/output/*.n2.results")
	if len(thetaOutFiles) < 1:
		continue
	
	thetaOutFile = thetaOutFiles[0]
		
	with open(thetaOutFile, 'r') as f:
		
		lineCount = 0
		for line in f:
			if lineCount < 1: #skip header
				lineCount += 1
				continue
			
			splitLine = line.split("\t")
			
			#C is in the 3rd column
			c = splitLine[2]
			
			copyNumbers = c.split(":")
			splitSubDir = subdir.split("/")
			sampleName = splitSubDir[-2]
			
			sampleCopyNumbers[sampleName] = copyNumbers
	
print sampleCopyNumbers	

#Write the copy numbers to a CNT-MD infile

with open(outFile, 'w') as out:
	
	out.write("#PARAMS\n")
	out.write(str(len(sampleCopyNumbers[sampleCopyNumbers.keys()[0]])) + "\n") #number of chromosomes
	out.write(str(len(sampleCopyNumbers)) + "\n")
	
	for chromosome in sampleCopyNumbers[sampleCopyNumbers.keys()[0]]:
		
		out.write("1 ") #number of segments, 1 in our case
	out.write("\n")	
	out.write("#SAMPLES\n")	
	
	for sample in sampleCopyNumbers:
		copyNumbers = " | ".join(sampleCopyNumbers[sample])
		print copyNumbers
		out.write(sample + " : " + copyNumbers + "\n")




