# Generate plots based on CSV file produced by codechecker.py.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_codechecker(cmap, filename, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["#date"])

	cmapuse = cmap
	colorlist = None
	style = None
	if cmap == "gray":
		cmapuse = None
		colorlist = ["#000000", "#929292", "#929292", "#c7c7c7", "#c7c7c7"]
		style = ["-", "--", "-", "--", "-"]

	ax = df.plot(cmap=cmapuse, fontsize=FONT, color=colorlist, style=style)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("# of cloud functions + code repositories", fontsize=FONT)
	ax.set_title("Evolution of AWS SAR Code Repositories", fontsize=FONT)
	leg = ax.legend(fontsize=FONT, loc="upper left")

	ax.plot((288, 288), (0, 550), dashes=[2, 2, 10, 2], c="gray")
	ax.text(274, 340, "inclusion of caps", rotation="vertical", fontsize=FONT)

	if cmap != "gray":
		pylab.rcParams["axes.prop_cycle"] = pylab.rcParams["axes.prop_cycle"][2:]

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/codechecker.{}.{}".format(cmap, fileformat))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_codechecker(cmap, "codechecker.csv", "png")
