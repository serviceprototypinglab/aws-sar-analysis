import pandas as pd
import glob
import sys

def plusminus(filenames):
	nameslist = ["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"]

	oldnames = None
	addsum = 0
	removesum = 0

	f = open("plusminus.csv", "w")
	print("#date,plus,minus", file=f)

	for filename in filenames:
		df = pd.read_csv(filename, names=nameslist)

		names = {}
		add = 0
		remove = 0

		for idx, row in df.iterrows():
			if oldnames and not row["id"] in oldnames:
				add += 1
			names[row["id"]] = True

		if oldnames:
			for name in oldnames:
				if not name in names:
					remove -= 1

		# suppress "caps" addition on 26.04.2019
		if add == 89:
			add = 0

		date = filename.split("/")[-1].replace("autocontents-", "").replace(".csv", "")

		print(date, add, remove)
		print("{},{},{}".format(date, add, remove), file=f)

		oldnames = names.copy()
		addsum += add
		removesum += remove

	f.close()

	addavg = round(addsum / len(filenames), 1)
	removeavg = round(removesum / len(filenames), 1)

	print("Total adds/removes: {}/{}".format(addsum, removesum))
	print("Daily average: {}/{} over {} days".format(addavg, removeavg, len(filenames)))

if len(sys.argv) != 2:
	print("Syntax: {} <filepattern.csv> # e.g. autocontents-yyyy-mm-dd.csv or 'autocontents-*.csv'".format(sys.argv[0]), file=sys.stderr)
	sys.exit(1)

filepattern = sys.argv[1]

filenames = glob.glob(filepattern)
filenames.sort()
plusminus(filenames)
