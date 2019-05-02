# Generate plots based on automatically generated statistics file.

import pandas as pd
import pylab
import seaborn
import sys
import os

FONT = 16

def plot_autostats(cmap):
	df = pd.read_csv("autostats/autostats.csv")
	df = df.set_index(["#stamp"])

	#df["counter"] *= 10

	#figsize=(8.0, 5.5+1)

	ax = df.plot(cmap=cmap, ylim=[0, max(df["total"]) + 50], fontsize=FONT)
	ax.set_xlabel("date", fontsize=FONT)
	ax.set_ylabel("# of registered cloud functions", fontsize=FONT)
	ax.set_title("Evolution of AWS Serverless Application Repository", fontsize=FONT)
	ax.legend(fontsize=FONT)

	#ax.set_ylim(top=df["counter"].max() + 100)

	pylab.setp(ax.xaxis.get_majorticklabels(), rotation=70)
	#ax.set_xticks(range(0, len(df["counter"]), 2))
	pylab.tight_layout()

	#pylab.show()
	os.makedirs("plots", exist_ok=True)
	pylab.savefig("plots/autostats-plot.{}.png".format(cmap))

if __name__ == "__main__":
	if len(sys.argv) not in (1, 2):
		print("Syntax: {} [<colourmap>]".format(sys.argv[0]), file=sys.stderr)
		print("Colourmaps: e.g. gray, seismic", file=sys.stderr)
		sys.exit(1)

	cmap = "gray"
	if len(sys.argv) == 2:
		cmap = sys.argv[1]

	plot_autostats(cmap)
