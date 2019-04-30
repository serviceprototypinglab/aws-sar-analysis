# Load all essential statistics from AWS SAR including exact number of Lambdas as well as metadata.

import urllib.request
import json
import itertools
import math
import csv
import datetime
import sys

caps = ["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM", "CAPABILITY_RESOURCE_POLICY", "CAPABILITY_AUTO_EXPAND"]

def pullstatistics(stamp, custom):
	neededpages = None

	f = open("autocontents-{}.csv".format(stamp), "w")
	w = csv.writer(f)

	approx = 0
	totalnocaps = 0
	if custom:
		totalwithcaps = 0
	else:
		totalwithcaps = -1

	for page in itertools.count(start=1):
		link = "https://shr32taah3.execute-api.us-east-1.amazonaws.com/Prod/applications/browse?pageSize=100"
		if page > 1:
			link += "&pageNumber=" + str(page)
		if custom:
			link += "&includeAppsWithCapabilities=" + ",".join(caps)

		resource = urllib.request.urlopen(link)
		content = resource.read().decode("utf-8")
		struct = json.loads(content)

		if page == 1:
			approx = struct["approximateResultCount"]
			neededpages = math.ceil(approx / 100)
			print("Approximately {} results.".format(approx))
			print("Applications:")

		for app in struct["applications"]:
			print("- {} / {}".format(app["name"], app["id"]))
			print("  by: {}".format(app["publisherAlias"]))
			print("  deployments: {}".format(app["deploymentCount"]))
			print("  labels: {}".format(",".join(app["labels"])))

			fields = []
			fields.append(app["name"])
			fields.append(app["id"])
			fields.append(app["publisherAlias"])
			fields.append(app["deploymentCount"])
			fields.append(",".join(app["labels"]))
			fields.append(app["description"])
			if "homePageUrl" in app:
				fields.append(app["homePageUrl"])
			else:
				fields.append("")
			fields.append(",".join(app["requiredCapabilitiesForLatestVersion"]))

			if app["requiredCapabilitiesForLatestVersion"]:
				totalwithcaps += 1
			else:
				totalnocaps += 1

			w.writerow(fields)

		if page == neededpages:
			break

	f.close()

	stf = open("autostats.csv", "a")
	stw = csv.writer(stf)
	stw.writerow([stamp, approx, totalnocaps, totalwithcaps])
	stf.close()

custom = False
if len(sys.argv) == 2:
	if sys.argv[1] == "--custom":
		custom = True

pullstatistics(datetime.date.isoformat(datetime.date.today()), custom)
