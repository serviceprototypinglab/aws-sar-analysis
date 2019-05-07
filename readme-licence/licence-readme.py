import pandas as pd
import os
import urllib.request
import time
import sys

if len(sys.argv) != 3:
	print("Syntax: {} <autocontents.csv> licence|readme".format(sys.argv[0]), file=sys.stderr)
	sys.exit(-1)
datafile = sys.argv[1]
mode = sys.argv[2]

do_readme = False
do_licence = False
if mode == "readme":
	do_readme = True
elif mode == "licence":
	do_licence = True
else:
	print("Invalid mode.", file=sys.stderr)
	sys.exit(-1)

if do_licence:
	os.makedirs("licences", exist_ok=True)
if do_readme:
	os.makedirs("readmes", exist_ok=True)

df = pd.read_csv(datafile, names="name,id,publisherAlias,deploymentCount,labels,description,url,caps".split(","))
# Old "students" format
#df = pd.read_csv(datafile, names="name,id,publisherAlias,deploymentCount,homePageUrl,stars,watchers,forks,language,labels,description".split(","))
for fid in df["id"]:
	arn, name = fid.split("/")
	licencefile = "licences/{}.licence".format(name)
	readmefile = "readmes/{}.readme".format(name)

	urlbase = "https://serverlessrepo.aws.amazon.com/applications"

	if do_licence:
		if os.path.isfile(licencefile):
			print("L +", fid)
		else:
			print("L -", fid)

			url = "{}/{}~{}/license.txt".format(urlbase, arn, name)

			f = urllib.request.urlopen(url)
			s = f.read().decode()
			f.close()

			f = open(licencefile, "w")
			f.write(s)
			f.close()

			time.sleep(5)

	if do_readme:
		if os.path.isfile(readmefile):
			print("R +", fid)
		else:
			print("R -", fid)

			url = "{}/{}~{}/readme.md.txt".format(urlbase, arn, name)

			f = urllib.request.urlopen(url)
			s = f.read().decode()
			f.close()

			f = open(readmefile, "w")
			f.write(s)
			f.close()

			time.sleep(5)
