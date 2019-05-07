# Generate plots based on CSV file produced by dupedetector.py.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_dupes(cmap):
	df = pd.read_csv("dupedetector.csv")
	df = df.set_index(["#date"])

	ax = df["dupespct"].plot(cmap=cmap, fontsize=FONT)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("duplicate functions in %", fontsize=FONT)
	ax.set_title("Evolution of AWS SAR Duplicate Functions", fontsize=FONT)
	ax.legend(fontsize=FONT)

	if cmap != "gray":
		pylab.rcParams["axes.prop_cycle"] = pylab.rcParams["axes.prop_cycle"][2:]

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	pylab.savefig("dupedetector.{}.png".format(cmap))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_dupes(cmap)
