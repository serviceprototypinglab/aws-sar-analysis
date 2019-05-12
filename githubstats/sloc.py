import glob
import subprocess
import json
import os

folders = glob.glob("_codefolders/*")

langs = {}

for folder in folders:
	print(folder)
	foldername = folder.split("/")[-1]
	datadir = os.path.expanduser("~/.slocdata/{}".format(foldername))
	#os.makedirs(datadir, exist_ok=True)
	#cmd = "sloccount --cached --datadir {} {}".format(datadir, folder)
	cmd = "sloccount {}".format(folder)
	p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
	s = p.stdout.decode()
	instats = False
	for line in s.split("\n"):
		line = line.strip()
		if line.startswith("Totals grouped by"):
			instats = True
		elif instats:
			if not line:
				instats = False
			else:
				lang, num, pct = line.split()
				lang = lang[:-1]
				num = int(num)
				pct = float(pct[1:-2])
				print("#", lang, num, pct)
				if not foldername in langs:
					langs[foldername] = []
				langs[foldername].append((lang, num, pct))

f = open("sloc.json", "w")
json.dump(langs, f)
f.close()
