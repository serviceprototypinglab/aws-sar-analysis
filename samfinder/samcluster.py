import glob
import os
import operator
import yaml
import collections
import sys

yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

clusters = {}
folders = {}
samcount = 0

samrootfolder = "extracted-sams"
if len(sys.argv) == 2:
	samrootfolder = sys.argv[1]

print("Scanning SAMs...")
samfolders = glob.glob(os.path.join(samrootfolder, "*"))
for samfolder in samfolders:
	sams = os.listdir(samfolder)
	for sam in sams:
		samcount += 1
		rc = []
		y = yaml.load(open(os.path.join(samfolder, sam)))
		if "Resources" in y:
			for r in y["Resources"]:
				if "Type" in y["Resources"][r]:
					t = y["Resources"][r]["Type"]
					rc.append(t)
		rc = sorted(list(set(rc)))
		#print(rc)

		rcs = ",".join(rc)
		clusters[rcs] = clusters.get(rcs, 0) + 1
		if not rcs in folders:
			folders[rcs] = []
		folders[rcs].append(os.path.basename(samfolder))

print("Cluster analysis...")
print("{} clusters over {} SAM files".format(len(clusters), samcount))
print("significant > 5 occurrences")
for rcs in clusters:
	if clusters[rcs] > 5:
		pct = round(100 * clusters[rcs] / samcount, 1)
		print("[{:3d}] [{:4.1f}%] {}".format(clusters[rcs], pct, rcs))
print("complex > 5 resources")
for rcs in clusters:
	if rcs.count(",") > 5:
		print("[{:3d}] ({:2d}x) {}".format(clusters[rcs], rcs.count(","), rcs))
print("significant folders")
for rcs in folders:
	if len(folders[rcs]) > 5:
		print(rcs, folders[rcs])
