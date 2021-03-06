import glob
import os
import operator
import yaml
import collections
import sys

yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

types = {}
runtimes = {}
foldertypes = {}
allsams = 0

samrootfolder = "extracted-sams"
if len(sys.argv) == 2:
	samrootfolder = sys.argv[1]

print("Scanning SAMs...")
samfolders = glob.glob(os.path.join(samrootfolder, "*"))
for samfolder in samfolders:
	localtypes = {}
	sams = os.listdir(samfolder)
	for sam in sams:
		if not os.path.isfile(os.path.join(samfolder, sam)):
			continue
		y = yaml.load(open(os.path.join(samfolder, sam)))
		if "Resources" in y:
			allsams += 1
			for r in y["Resources"]:
				if "Type" in y["Resources"][r]:
					t = y["Resources"][r]["Type"]
					if t.startswith("AWS::Serverless::"):
						print("S {} {}".format(r, t))
					else:
						print("R {} {}".format(r, t))
					types[t] = types.get(t, 0) + 1
					localtypes[t] = 1

					if t == "AWS::Serverless::Function":
						if "Properties" in y["Resources"][r]:
							if "Runtime" in y["Resources"][r]["Properties"]:
								rt = y["Resources"][r]["Properties"]["Runtime"]
								runtimes[rt] = runtimes.get(rt, 0) + 1
				else:
					print("R {} <untyped>?".format(r))

	for t in localtypes:
		foldertypes[t] = foldertypes.get(t, 0) + 1

print("Evaluating {} SAMs...".format(allsams))
#types = collections.OrderedDict(sorted(types.items(), key=lambda x: x[1], reverse=True))
#print(types)
for rtype in sorted(types):
	pct = round(100 * types[rtype] / allsams, 1)
	fpct = round(100 * foldertypes.get(rtype, 0) / len(samfolders), 1)
	print("{:50s} {:3d} ({:4.1f}%) [folder: {:3d} ({:4.1f}%)]".format(rtype, types[rtype], pct, foldertypes.get(rtype, 0), fpct))

print("Evaluating runtimes...")
numfunctions = types["AWS::Serverless::Function"]
for runtime in sorted(runtimes):
	pct = round(100 * runtimes[runtime] / numfunctions, 1)
	print("{:20s} {:3d} ({:4.1f}%)".format(runtime, runtimes[runtime], pct))
