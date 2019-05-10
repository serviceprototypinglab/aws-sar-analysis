# Generate plots based on automatically generated statistics file.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_autostats(cmap, filename, fileformat):
	df = pd.read_csv(filename)
	df = df.set_index(["#stamp"])

	#df["counter"] *= 10

	#figsize=(8.0, 5.5+1)

	cmapuse = cmap
	colorlist = None
	style = None
	if cmap == "gray":
		cmapuse = None
		colorlist = ["#929292", "#c7c7c7", "#5d5d5d"]
		stlye = ["-", "--", ".-"]
		#pylab.style.use("grayscale")
		#pylab.rcParams["axes.prop_cycle"] = pylab.rcParams["axes.prop_cycle"][20:]

	ax = df.plot(cmap=cmapuse, ylim=[0, max(df["total"]) + 50], fontsize=FONT, color=colorlist, style=style)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("# of registered cloud functions", fontsize=FONT)
	ax.set_title("Evolution of AWS Serverless Application Repository", fontsize=FONT)
	ax.legend(fontsize=FONT)

	ax.plot((344, 344), (0, 580), dashes=[2, 2, 10, 2], c="gray")
	ax.text(330, 280, "inclusion of caps", rotation="vertical", fontsize=FONT)

	#ax.set_ylim(top=df["counter"].max() + 100)

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	#ax.set_xticks(range(0, len(df["counter"]), 2))
	pylab.tight_layout()

	#pylab.show()
	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/autostats-plot.{}.{}".format(cmap, fileformat))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_autostats(cmap, "autostats/autostats.csv", "png")
