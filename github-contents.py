# Code partially based on:
# https://github.com/alfunx/UZH-BMINF005/blob/master/autocontents.py
# (aweSoME student group at UZH)

import pandas as pd
import sys
import glob
import urllib.request
import time
import json
import os

def githubstats(url):
	link = url.replace("github.com", "api.github.com/repos")
	if "/tree" in link:
		link = link[:link.index("/tree")]

	try:
		print("-> fetch: {} (for {})".format(link, url))
		f = urllib.request.urlopen(link)
		gh_content = f.read().decode()
		s = json.loads(gh_content)
	except Exception as e:
		print("ERROR", e)
		time.sleep(65)
		return None, None, None, None
	else:
		time.sleep(65)
		return s["stargazers_count"], s["subscribers_count"], s["forks_count"], s["language"]

if len(sys.argv) != 2:
	print("Syntax: {} <filepattern.csv> # e.g. autocontents-yyyy-mm-dd.csv or autocontents-*.csv", file=sys.stderr)
	sys.exit(1)

filepattern = sys.argv[1]

datafiles = glob.glob(filepattern)
datafiles.sort()
datafile = datafiles[-1]

date = datafile.split("/")[-1].replace("autocontents-", "").replace(".csv", "")

print("Retrieving GitHub metadata for {} ({})".format(date, datafile))

outfile = "github-contents-{}.csv".format(date)
autoskip = []
if os.path.isfile(outfile):
	df = pd.read_csv(outfile)
	autoskip = list(df["#function"])
	f = open(outfile, "a")
else:
	f = open(outfile, "w")
	print("#function,stars,watchers,forks,language", file=f)

df = pd.read_csv(datafile, names="name,id,publisherAlias,deploymentCount,labels,description,homePageUrl,caps".split(","))
dfurl = df[["name", "homePageUrl"]]
for idx, name, url in dfurl.itertuples():
	if name in autoskip:
		print("** autoskip already present: {}".format(name))
		continue
	if type(url) == str and "github.com" in url:
		stars, watchers, forks, language = githubstats(url)
		if stars is not None:
			print("{},{},{},{},{}".format(name, stars, watchers, forks, language), file=f)
			f.flush()
	else:
		print("## skip:  {}".format(url))

f.close()
