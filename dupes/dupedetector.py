import pandas as pd
import glob
import sys

if len(sys.argv) != 2:
	print("Syntax: {} <filepattern.csv> # e.g. autocontents-yyyy-mm-dd.csv or 'autocontents-*.csv'", file=sys.stderr)
	sys.exit(1)

filepattern = sys.argv[1]

datafiles = glob.glob(filepattern)
datafiles.sort()

csvmode = False
if len(datafiles) > 1:
	csvmode = True

if csvmode:
	f = open("dupedetector.csv", "w")
	print("#date,dupes,dupespct", file=f)

for datafile in datafiles:
	present = {}
	dupes = {}

	df = pd.read_csv(datafile, names="name,id,publisherAlias,deploymentCount,labels,description,homePageUrl,caps".split(","))
	for idx, fid, vendor in df[["id", "publisherAlias"]].itertuples():
		arn, name = fid.split("/")
		if not name in present:
			present[name] = vendor
		else:
			d = dupes.get(name, [])
			if not present[name] in d:
				d.append(present[name])
			d.append(vendor)
			dupes[name] = d

	ndupes = sum(len(dupes[x]) for x in dupes)
	dupepct = round(100 * ndupes / len(df), 2)
	if csvmode:
		date = datafile.replace(".csv", "")[-10:]
		print("{},{},{}".format(date, ndupes, dupepct), file=f)
	else:
		print(dupes)
		print("{} → {} out of {} = {}%".format(len(dupes), ndupes, len(df), dupepct))

if csvmode:
	f.close()
