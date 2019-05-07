import pandas as pd
import sys
import glob
import os

statsfile = "githubstats.csv"

if len(sys.argv) != 2:
	print("Syntax: {} <filepattern.csv> # e.g. 'github-contents-*.csv'", file=sys.stderr)
	sys.exit(1)

filepattern = sys.argv[1]

datafiles = glob.glob(filepattern)
datafiles.sort()

def stats(column):
	mm = int(df[column].mean() / df[column].median())
	print("{:10s} min: {:4d} / max: {:4d} / mean: {:4d} / median: {:4d} / std: {:4d} / MM: {:4d}".format(column, int(df[column].min()), int(df[column].max()), int(df[column].mean()), int(df[column].median()), int(df[column].std()), mm))
	return mm

if not "autocontents" in datafiles[0]:
	statsfile = "githubstats.custom.csv"
if not os.path.isfile(statsfile):
	f = open(statsfile, "w")
	print("#date,stars-mm,watchers-mm,forks-mm", file=f)
else:
	f = open(statsfile, "a")

for datafile in datafiles:
	if "autocontents" in datafile:
		# old format without 'caps'
		df = pd.read_csv(datafile, names="name,id,publisherAlias,deploymentCount,homePageUrl,stars,watchers,forks,language,labels,description".split(","))
	else:
		df = pd.read_csv(datafile)
	dfgh = df[["stars", "watchers", "forks", "language"]][pd.notnull(df["stars"])]
	#print(dfgh)

	smm = stats("stars")
	wmm = stats("watchers")
	fmm = stats("forks")

	date = datafile.split("/")[-1].replace(".csv", "")
	date = date.replace("autocontents-", "")
	date = date.replace("github-contents-", "")
	print("{},{},{},{}".format(date, smm, wmm, fmm), file=f)

	dfl = pd.DataFrame()
	dfl["langpop"] = dfgh.groupby("language").size()
	dfl["pct"] = 100 * round(dfl["langpop"] / len(dfgh), 3)
	print(dfl)

f.close()
