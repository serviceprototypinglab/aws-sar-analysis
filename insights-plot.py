# Generate plots based on automatically generated statistics file.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_insights_totals(cmap, filename, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["#stamp"])

	ax = df[["functions", "vendors"]].plot(cmap=cmap, ylim=[0, max(df["functions"]) * 1.1], fontsize=FONT)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("# of cloud functions, vendors", fontsize=FONT)
	ax.set_title("Evolution of AWS Serverless Application Repository", fontsize=FONT)
	ax.legend(fontsize=FONT)

	if cmap != "gray":
		pylab.rcParams["axes.prop_cycle"] = pylab.rcParams["axes.prop_cycle"][2:]

	ax2 = ax.twinx()
	df["deployments"].plot(ax=ax2, ylim=[0, max(df["deployments"]) * 1.2], fontsize=FONT, linestyle=":")
	ax2.set_ylabel("# of cloud function deployments", fontsize=FONT)
	ax2.legend(fontsize=FONT)

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/insights-totals-plot.{}.{}".format(cmap, fileformat))

def plot_insights_percent(cmap, filename, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["#stamp"])

	cmapuse = cmap
	colorlist = None
	style = None
	if cmap == "gray":
		cmapuse = None
		colorlist = ["#929292", "#c7c7c7"]
		style = ["-", "--"]

	ax = df.plot(cmap=cmapuse, ylim=[0, 1], fontsize=FONT, color=colorlist, style=style)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("% of cloud functions, deployments by AWS", fontsize=FONT)
	ax.set_title("Evolution of AWS Serverless Application Repository", fontsize=FONT)
	ax.legend(fontsize=FONT)

	ax.plot((288, 288), (0, 1), dashes=[2, 2, 10, 2], c="gray")
	ax.text(274, 0.78, "inclusion of caps", rotation="vertical", fontsize=FONT)

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/insights-percent-plot.{}.{}".format(cmap, fileformat))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_insights_totals(cmap, "insights-totals.csv", "png")
	plot_insights_percent(cmap, "insights-percent.csv", "png")
