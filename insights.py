#autocontents-2018-09-15.csv
#alexa-skills-kit-nodejs-factskill,arn:aws:serverlessrepo:us-east-1:173334852312:applications/alexa-skills-kit-nodejs-factskill,Alexa Skills Kit,11102,"skills,fact,alexa","This Alexa sample skill is a template for a basic fact skill. Provided a list of interesting facts about a topic, Alexa will select a fact at random and tell it to the user when the skill is invoked."

import pandas as pd
import glob
import sys

def insights_content(filename, verbose=True):
	nameslist = ["id", "fqid", "vendor", "deployments", "tags", "description", "url", "caps"]
	df = pd.read_csv(filename, names=nameslist)
	num_total = len(df)

	dfv = df.groupby(["vendor"])["vendor"].agg(["count"])
	num_vendors = len(dfv)

	num_downloads = df["deployments"].sum()

	dft = dfv.sort_values("count", ascending=False)
	dfd = df.sort_values("deployments", ascending=False)
	dfd = dfd[["id", "deployments"]].set_index(["id"])

	num_aws = 0
	dl_aws = 0
	for awsvendor in ("AWS", "AWS Secrets Manager", "AWS Greengrass", "AWS Elastic Load Balancing", "AWS SageMaker Ground Truth", "AWS Sample", "AWS Serverless Application Repository", "AWS WorkMail", "Alexa Skills Kit", "Alexa for Business"):
		countvar = dfv[(dfv.index == awsvendor)]["count"]
		if len(countvar) > 0:
			num_aws += countvar[0]
			dl_aws += df[(df["vendor"] == awsvendor)]["deployments"].sum()
	pct_aws = round(num_aws / num_total, 2)
	pct_awsdl = round(dl_aws / num_downloads, 2)

	if verbose:
		print("total vendors: {}".format(num_vendors))
		print("total functions: {}".format(num_total))
		print(" - avg per vendor : {}".format(num_total / num_vendors))
		print(" - without capabilities: {}".format(len(df[pd.isnull(df["caps"])])))
		print("total deployments: {}".format(num_downloads))
		print(" - avg per function: {}".format(num_downloads / num_total))
		print(" - avg per vendor : {}".format(num_downloads / num_vendors))
		print()
		print("top vendors:")
		#dft = dfv[(dfv["count"] > 2)]
		print(dft.head(10))
		print()
		print("top deployments:")
		print(dfd.head(10))
		print()
		print("percentage of AWS-provided functions:")
		print(pct_aws)
		print()
		print("percentage of AWS-provided function deployments:")
		print(pct_awsdl)

		print()
		print("percentage of function deployments over all vendors:")
		for idxvendor, vendor in dfv.iterrows():
			countsum = 0
			for idxfunc, func in df[df["vendor"] == vendor.name].iterrows():
				count = df[df["id"] == func["id"]]["deployments"].iloc[0]
				countsum += count
			countsum /= vendor["count"]
			print("* {:30s} {:6.1f}".format(vendor.name, countsum))

		null = df[["tags"]][pd.isnull(df["tags"])]
		notnull = df[["tags"]][pd.notnull(df["tags"])]
		print()
		print("tags:")
		print("- set {}, not set {}, percent set {}".format(len(notnull), len(null), 100 * len(notnull) / (len(null) + len(notnull))))

		alltags = []
		for idxtag, tag in notnull.iterrows():
			tags = tag["tags"].split(",")
			alltags += tags
		alltags.sort()

		dftags = pd.DataFrame(alltags, columns=["tags"])
		dftc = dftags.groupby(["tags"])["tags"].agg(["count"])
		print("- total {}".format(len(dftags)))
		print("  - avg per function: {}".format(len(dftags) / num_total))
		dftc = dftc.sort_values("count", ascending=False)
		print("- unique {}".format(len(dftc)))

		taglen = 0
		tagmax = 0
		tagmaxtag = None
		for idxtag, tag in dftc.iterrows():
			taglen += len(idxtag)
			if len(idxtag) > tagmax:
				tagmax = len(idxtag)
				tagmaxtag = idxtag
		taglen /= len(dftc)
		print("  - avg length: {}".format(taglen))
		print("  - max length: {} ({})".format(tagmax, tagmaxtag))

		print("- top:")
		print(dftc.head(10))

		dftc.to_csv("insights_tags_longtail.csv")

		null = df[["url"]][pd.isnull(df["url"])]
		notnull = df[["url"]][pd.notnull(df["url"])]
		urllist = list(df["url"])
		gh = len([url for url in urllist if "github.com" in str(url)])
		print()
		print("urls:")
		print("- set {}, not set {}, percent set {}".format(len(notnull), len(null), 100 * len(notnull) / (len(null) + len(notnull))))
		print("- github {}, percent github {}".format(gh, 100 * gh / len(df)))

	return num_total, num_vendors, num_downloads, pct_aws, pct_awsdl

if len(sys.argv) == 1:
	ft = open("insights-totals.csv", "w")
	fp = open("insights-percent.csv", "w")
	print("#stamp,functions,vendors,deployments", file=ft)
	print("#stamp,awsfunctions,awsdeployments", file=fp)
	filenames = glob.glob("autostats/autocontents-*.csv")
	filenames.sort()
	for filename in filenames:
		datestr = filename[23:33]
		num_total, num_vendors, num_downloads, pct_aws, pct_awsdl = insights_content(filename, False)
		print("{},{},{},{}".format(datestr, num_total, num_vendors, num_downloads), file=ft)
		print("{},{},{}".format(datestr, pct_aws, pct_awsdl), file=fp)
	ft.close()
	fp.close()
else:
	filenames = glob.glob("autostats/autocontents-*.csv")
	filenames.sort()
	insights_content(filenames[-1])
