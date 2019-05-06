import pandas as pd
import glob
import sys
import os
import json
import subprocess
import time

def codechecker(filename, tmpdir, pullcode=True, verbose=True):
	df = pd.read_csv(filename, names=["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"])

	urllist = list(df["url"])
	namelist = list(df["id"])
	hascloned = {}
	hasclonednow = {}
	folders = {}
	namedfolders = {}
	needscopy = {}
	needscopyurl = {}
	success = 0
	failure = 0
	unpulled = 0
	dupe = 0
	otherurls = {}
	nourls = 0
	statsnew = 0
	statsupdated = 0
	prevtime = 0

	if pullcode:
		if os.path.isfile("codecheckerrepos.json"):
			f = open("codecheckerrepos.json")
			hascloned = json.load(f)
		if os.path.isfile("codecheckerfolders.json"):
			f = open("codecheckerfolders.json")
			folders = json.load(f)
		if os.path.isfile("codecheckernamedfolders.json"):
			f = open("codecheckernamedfolders.json")
			namedfolders = json.load(f)
		if os.path.isfile("_codestamp"):
			f = open("_codestamp")
			prevtime = int(f.read().strip())
			print("last run {}s ago".format(int(time.time()) - prevtime))
		f = open("_codestamp", "w")
		print(str(int(time.time())), file=f)
		f.close()

	for i, urlname in enumerate(zip(urllist, namelist)):
		url, name = urlname
		ipos = len(hascloned) + 1
		if "github.com" in str(url):
			urlstem = "/".join(url.split("/")[:5])
			urlpath = "/".join(url.split("/")[5:])
			if urlstem in hasclonednow:
				ipos = hasclonednow[urlstem]
				print("REPO reuse {} ({})".format(urlstem, ipos))
				dupe += 1
			elif pullcode:
				if urlstem in hascloned:
					ipos = hascloned[urlstem]
				if os.path.isdir("{}/_codechecker/{}".format(tmpdir, ipos)):
					print("REPO clone-update {}... ({})".format(urlstem, ipos))
					if time.time() - prevtime > 3600:
						origdir = os.getcwd()
						os.chdir("{}/_codechecker/{}".format(tmpdir, ipos))
						os.system("git -c core.askpass=true fetch -q")
						p = subprocess.run("git diff origin/HEAD", shell=True, stdout=subprocess.PIPE)
						if p.stdout:
							statsupdated += 1
							os.system("git merge origin/HEAD")
							needscopy[urlstem] = True
						os.chdir(origdir)
					else:
						print("     (skip actual update check due to short succession)")
					hascloned[urlstem] = ipos
					hasclonednow[urlstem] = ipos
					success += 1
				else:
					print("REPO clone {}... ({})".format(urlstem, ipos))
					os.makedirs("{}/_codechecker".format(tmpdir), exist_ok=True)
					ret = os.system("git -c core.askpass=true clone -q {} {}/_codechecker/{}".format(urlstem, tmpdir, ipos))
					if ret:
						print("!!!! ERROR cloning")
						failure += 1
						continue
					else:
						success += 1
						hascloned[urlstem] = ipos
						hasclonednow[urlstem] = ipos
						needscopy[urlstem] = True
						statsnew += 1
			else:
				unpulled += 1
				hascloned[urlstem] = ipos

			if not url in folders:
				folders[url] = str(ipos) + "-" + str(len(folders) + 1)
			if not name in namedfolders:
				namedfolders[name] = folders[url]
			if pullcode:
				fpos = folders[url]
				if urlstem in needscopy and needscopy[urlstem] and not url in needscopyurl:
					needscopyurl[url] = False
					print(" DIR produce folder {}".format(fpos))
					os.makedirs("{}/_codefolders".format(tmpdir), exist_ok=True)
					origdir = None
					if urlpath.startswith("tree"):
						tree, treename, *rest = urlpath.split("/")
						urlpath = "/".join(rest)
						origdir = os.getcwd()
						os.chdir("{}/_codechecker/{}".format(tmpdir, hascloned[urlstem]))
						os.system("git checkout -q {}".format(treename))
						os.chdir(origdir)
					os.system("rm -rf {}/_codefolders/{}".format(tmpdir, fpos))
					os.system("cp -r {}/_codechecker/{}/{} {}/_codefolders/{}".format(tmpdir, hascloned[urlstem], urlpath, tmpdir, fpos))
				else:
					print(" DIR reuse existing folder {}".format(fpos))
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
		f = open("codecheckerfolders.json", "w")
		json.dump(folders, f, sort_keys=True)
		f.close()
		f = open("codecheckernamedfolders.json", "w")
		json.dump(namedfolders, f, sort_keys=True)
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
