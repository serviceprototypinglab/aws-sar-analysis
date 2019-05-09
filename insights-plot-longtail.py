# Generate plots based on automatically generated statistics file.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_insights_longtails(cmap, filename, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["tags"])

	if cmap != "gray":
		pylab.rcParams["axes.prop_cycle"] = pylab.rcParams["axes.prop_cycle"][2:]

	ax = df["count"].plot(cmap=cmap, fontsize=FONT)
	ax.set_xlabel("tag", fontsize=FONT)
	ax.set_ylabel("# of tag instances", fontsize=FONT)
	ax.set_title("Long-tail distribution of unique tags", fontsize=FONT)
	ax.legend(fontsize=FONT)

	sampling = 25
	ax.set_xticks([i * sampling for i in range(len(df) // sampling)])
	ax.set_xticklabels([list(df.index)[i] for i in range(len(df) // sampling)])

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/insights-longtail-tags.{}.{}".format(cmap, fileformat))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_insights_longtails(cmap, "insights_tags_longtail.csv", "png")
