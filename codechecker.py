import pandas as pd
import glob
import sys
import os

def codechecker(filename, tmpdir, verbose=True):
	df = pd.read_csv(filename, names=["id", "fqid", "vendor", "deployments", "tags", "description", "url"])

	urllist = list(df["url"])
	hascloned = {}
	success = 0
	failure = 0
	dupe = 0
	for i, url in enumerate(urllist):
		if "github.com" in str(url):
			urlstem = "/".join(url.split("/")[:5])
			urlpath = "/".join(url.split("/")[5:])
			if urlstem in hascloned:
				print("reuse {} ({})".format(urlstem, hascloned[urlstem]))
				dupe += 1
			else:
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

	print("failures {} + success {} = unique repos {} + dupes {} = github {} + other {}".format(failure, success, failure + success, dupe, failure + success + dupe, len(urllist) - failure - success - dupe))

tmpdir = "."
if len(sys.argv) == 2:
	tmpdir = sys.argv[1]

#filenames = glob.glob("autostats/autocontents-*.csv")
filenames = glob.glob("autocontents-*.csv")
filenames.sort()
codechecker(filenames[-1], tmpdir)
