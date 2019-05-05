import pandas as pd
import glob
import sys
import os
import json
import subprocess

def codechecker(filename, tmpdir, pullcode=True, verbose=True):
	df = pd.read_csv(filename, names=["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"])

	urllist = list(df["url"])
	hascloned = {}
	hasclonednow = {}
	success = 0
	failure = 0
	unpulled = 0
	dupe = 0
	otherurls = {}
	nourls = 0
	statsnew = 0
	statsupdated = 0

	if pullcode:
		if os.path.isfile("codecheckerrepos.json"):
			f = open("codecheckerrepos.json")
			hascloned = json.load(f)

	for i, url in enumerate(urllist):
		ipos = len(hascloned) + 1
		if "github.com" in str(url):
			urlstem = "/".join(url.split("/")[:5])
			urlpath = "/".join(url.split("/")[5:])
			if urlstem in hasclonednow:
				print("reuse {} ({})".format(urlstem, hasclonednow[urlstem]))
				dupe += 1
			elif pullcode:
				if urlstem in hascloned:
					ipos = hascloned[urlstem]
				if os.path.isdir("{}/_codechecker/{}".format(tmpdir, ipos)):
					print("clone-update {}...".format(urlstem))
					origdir = os.getcwd()
					os.chdir("{}/_codechecker/{}".format(tmpdir, ipos))
					os.system("git fetch")
					p = subprocess.run("git diff origin/HEAD", shell=True, stdout=subprocess.PIPE)
					if p.stdout:
						statsupdated += 1
						os.system("git merge origin/HEAD")
					os.chdir(origdir)
					hascloned[urlstem] = ipos
					hasclonednow[urlstem] = ipos
					success += 1
				else:
					print("clone {}...".format(urlstem))
					os.makedirs("{}/_codechecker".format(tmpdir), exist_ok=True)
					ret = os.system("git clone {} {}/_codechecker/{}".format(urlstem, tmpdir, ipos))
					if ret:
						print("!!! ERROR")
						failure += 1
						continue
					else:
						success += 1
						hascloned[urlstem] = ipos
						hasclonednow[urlstem] = ipos
						statsnew += 1
			else:
				unpulled += 1
				hascloned[urlstem] = ipos

			if pullcode:
				os.makedirs("{}/_codefolders".format(tmpdir), exist_ok=True)
				origdir = None
				if urlpath.startswith("tree"):
					tree, treename, *rest = urlpath.split("/")
					urlpath = "/".join(rest)
					origdir = os.getcwd()
					os.chdir("{}/_codechecker/{}".format(tmpdir, hascloned[urlstem]))
					os.system("git checkout {}".format(treename))
					os.chdir(origdir)
				os.system("rm -rf {}/_codefolders/{}".format(tmpdir, ipos))
				os.system("cp -r {}/_codechecker/{}/{} {}/_codefolders/{}".format(tmpdir, hascloned[urlstem], urlpath, tmpdir, ipos))
			#if origdir:
			#	os.chdir("_codechecker/{}".format(hascloned[urlstem]))
			#	os.system("git checkout master") # origin/HEAD?
			#	os.chdir(origdir)
		else:
			if pd.isnull(url):
				nourls += 1
			else:
				urlstem = url
				if "/" in url:
					urlstem = url.split("/")[2]
				otherurls[urlstem] = otherurls.get(urlstem, 0) + 1

	if pullcode:
		f = open("codecheckerrepos.json", "w")
		json.dump(hascloned, f, sort_keys=True)
		f.close()

	print("failures {} + success {} = unique github repos {} + dupes {} = github {} + other {} + none {} = total {}".format(failure, success, failure + success + unpulled, dupe, failure + success + unpulled + dupe, len(urllist) - failure - success - unpulled - dupe - nourls, nourls, len(urllist)))
	print("others", otherurls)
	print("stats: new {}, updated {}".format(statsnew, statsupdated))

	if os.path.isfile("codecheckerstats.csv"):
		f = open("codecheckerstats.csv", "a")
	else:
		f = open("codecheckerstats.csv", "w")
		print("#date,new,updated", file=f)
	date = filename.replace("autostats/", "").replace("autocontents-", "").replace(".csv", "")
	print("{},{},{}".format(date, statsnew, statsupdated), file=f)
	f.close()

	return len(urllist), failure, success, unpulled, dupe, nourls

tmpdir = "."
stats = False
if len(sys.argv) == 2:
	tmpdir = sys.argv[1]
	if sys.argv[1] == "--stats":
		stats = True

if not os.path.isdir("autostats"):
	print("Error: must be run in the parent directory of 'autostats'.", file=sys.stderr)
	sys.exit(-1)

filenames = glob.glob("autostats/autocontents-*.csv")
filenames.sort()

if not stats:
	codechecker(filenames[-1], tmpdir)
else:
	f = open("codechecker.csv", "w")
	print("#date,total,github-unique,github-dupe,other,none", file=f)
	for filename in filenames:
		date = filename.replace("autostats/", "").replace("autocontents-", "").replace(".csv", "")
		total, fign, sign, unpulled, dupe, nourls = codechecker(filename, None, False)
		other = total - unpulled - dupe - nourls
		print("{},{},{},{},{},{}".format(date, total, unpulled, dupe, other, nourls), file=f)
	f.close()
