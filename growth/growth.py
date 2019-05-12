import pandas as pd
import glob
import pylab
import sys

def growth(filename1, filename2, cmap, fileformat):
	nameslist = ["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"]
	df1 = pd.read_csv(filename1, names=nameslist)
	df2 = pd.read_csv(filename2, names=nameslist)

	df1 = df1[["id", "deployments"]]
	df2 = df2[["id", "deployments"]]
	df1["deployments2"] = pd.Series([0] * len(df1))

	for idx, row in df1.iterrows():
		try:
			val = df2[df2["id"] == row["id"]]["deployments"].values[0]
		except:
			pass
		else:
			df1.at[idx, "deployments2"] = val

	df1["growth"] = df1["deployments2"] - df1["deployments"]
	df1["growthrate"] = (100 * df1["growth"] / df1["deployments"])

	df = df1[["id", "deployments", "growthrate"]]
	df = df[(df["deployments"] > 100) & (df["deployments"] < 1000)]

	print(df.sort_values("growthrate"))

	ax = df.plot.scatter("deployments", "growthrate", c=cmap)
	for idx, row in df[df["growthrate"] > 10].iterrows():
		ax.text(row["deployments"] + 10, row["growthrate"], row["id"], va="center")
	pylab.savefig("growth.{}.{}".format(cmap, fileformat))

	avg = round(100 * df1["growth"].sum() / df1["deployments"].sum(), 2)

	print("Selected: {} out of {}.".format(len(df), len(df1)))
	print("Average 30-day growth: {}%.".format(avg))

	print("Top deployments comparison:")
	print(df1.head())

def growthvendors(filename1, filename2, cmap, fileformat):
	nameslist = ["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"]
	df1 = pd.read_csv(filename1, names=nameslist)
	df2 = pd.read_csv(filename2, names=nameslist)

	dfv1 = df1.groupby(["vendor"])["vendor"].agg(["count"])
	dfv2 = df2.groupby(["vendor"])["vendor"].agg(["count"])
	dfv1["count2"] = pd.Series([0] * len(dfv1))

	for idx, row in dfv1.iterrows():
		try:
			val = dfv2.loc[idx]["count"]
		except:
			dfv1.at[idx, "count2"] = 0
		else:
			dfv1.at[idx, "count2"] = val
	dfv1["count2"] = dfv1["count2"].astype(int)
	dfv1 = dfv1.sort_values("count", ascending=False)

	dfv1["growth"] = dfv1["count2"] - dfv1["count"]
	dfv1["growthrate"] = (100 * dfv1["growth"] / dfv1["count"])

	df = dfv1
	#df = df[(df["count"] > 4) & (df["count"] < 40)]
	df = df[df["count"] > 4]

	print(df.sort_values("growthrate"))

	ax = df.plot.scatter("count", "growthrate", c=cmap)
	for idx, row in df[df["growthrate"] > 5].iterrows():
		offset = 2
		if row["count"] > 50:
			offset = -9
		print(idx, offset)
		ax.text(row["count"] + offset, row["growthrate"], idx, va="center")
	pylab.savefig("growthvendors.{}.{}".format(cmap, fileformat))

	avg = round(100 * dfv1["growth"].sum() / dfv1["count"].sum(), 2)

	print("Selected: {} out of {}.".format(len(df), len(dfv1)))
	print("Average 30-day growth <same as overall function growth>: {}%.".format(avg))

	print("Top vendors comparison:")
	print(dfv1.head())

if len(sys.argv) != 2:
	print("Syntax: {} <filepattern.csv> # e.g. autocontents-yyyy-mm-dd.csv or 'autocontents-*.csv'".format(sys.argv[0]), file=sys.stderr)
	sys.exit(1)

filepattern = sys.argv[1]

filenames = glob.glob(filepattern)
filenames.sort()
growth(filenames[-31], filenames[-1], "gray", "png")
growthvendors(filenames[-31], filenames[-1], "gray", "png")
