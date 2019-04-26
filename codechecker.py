import pandas as pd
import glob
import sys
import os

def codechecker(filename, tmpdir, pullcode=True, verbose=True):
	df = pd.read_csv(filename, names=["id", "fqid", "vendor", "deployments", "tags", "description", "url"])

	urllist = list(df["url"])
	hascloned = {}
	success = 0
	failure = 0
	unpulled = 0
	dupe = 0
	otherurls = {}
	nourls = 0
	for i, url in enumerate(urllist):
		if "github.com" in str(url):
			urlstem = "/".join(url.split("/")[:5])
			urlpath = "/".join(url.split("/")[5:])
			if urlstem in hascloned:
				print("reuse {} ({})".format(urlstem, hascloned[urlstem]))
				dupe += 1
			elif pullcode:
				if os.path.isdir("{}/_codechecker/{}".format(tmpdir, i)):
					print("clone-update {}...".format(urlstem))
					origdir = os.getcwd()
					os.chdir("{}/_codechecker/{}".format(tmpdir, i))
					os.system("git pull")
					os.chdir(origdir)
					hascloned[urlstem] = i
					success += 1
				else:
					print("clone {}...".format(urlstem))
					os.makedirs("{}/_codechecker".format(tmpdir), exist_ok=True)
					ret = os.system("git clone {} {}/_codechecker/{}".format(urlstem, tmpdir, i))
					if ret:
						print("!!! ERROR")
						failure += 1
						continue
					else:
						success += 1
						hascloned[urlstem] = i
			else:
				unpulled += 1
				hascloned[urlstem] = i

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
				os.system("rm -rf {}/_codefolders/{}".format(tmpdir, i))
				os.system("cp -r {}/_codechecker/{}/{} {}/_codefolders/{}".format(tmpdir, hascloned[urlstem], urlpath, tmpdir, i))
			#if origdir:
			#	os.chdir("_codechecker/{}".format(hascloned[urlstem]))
			#	os.system("git checkout master")
			#	os.chdir(origdir)
		else:
			if pd.isnull(url):
				nourls += 1
			else:
				urlstem = url
				if "/" in url:
					urlstem = url.split("/")[2]
				otherurls[urlstem] = otherurls.get(urlstem, 0) + 1

	print("failures {} + success {} = unique github repos {} + dupes {} = github {} + other {} + none {} = total {}".format(failure, success, failure + success + unpulled, dupe, failure + success + unpulled + dupe, len(urllist) - failure - success - unpulled - dupe - nourls, nourls, len(urllist)))
	print("others", otherurls)

	return len(urllist), failure, success, unpulled, dupe, nourls

tmpdir = "."
stats = False
if len(sys.argv) == 2:
	tmpdir = sys.argv[1]
	if sys.argv[1] == "--stats":
		stats = True

#filenames = glob.glob("autostats/autocontents-*.csv")
filenames = glob.glob("autocontents-*.csv")
filenames.sort()

if not stats:
	codechecker(filenames[-1], tmpdir)
else:
	f = open("codechecker.csv", "w")
	print("#date,total,github-unique,github-dupe,other,none", file=f)
	for filename in filenames:
		date = filename.replace("autocontents-", "").replace(".csv", "")
		total, fign, sign, unpulled, dupe, nourls = codechecker(filename, None, False)
		other = total - unpulled - dupe - nourls
		print("{},{},{},{},{},{}".format(date, total, unpulled, dupe, other, nourls), file=f)
	f.close()
