import pandas as pd
import pylab
import seaborn
from matplotlib.ticker import MaxNLocator
import sys
import os

FONT = 16
#FONT = None

def plot(filename, cmap, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["#date"])

	cmapuse = cmap
	colorlist = None
	style = None
	if cmap == "gray":
		cmapuse = None
		colorlist = ["#929292", "#c7c7c7", "#5d5d5d"]
		stlye = ["-", "--", ".-"]

	ax = df.plot(cmap=cmapuse, fontsize=FONT, color=colorlist, style=style)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("# of added/removed cloud functions", fontsize=FONT)
	ax.set_title("Evolution of AWS Serverless Application Repository", fontsize=FONT)
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	pylab.tight_layout()

	#pylab.show()
	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/plusminus.{}.{}".format(cmap, fileformat))

if len(sys.argv) not in (1, 2):
	print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
	print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
	sys.exit(1)

cmap = "gray"
if len(sys.argv) == 2:
	cmap = sys.argv[1]

plot("plusminus.csv", cmap, "png")
