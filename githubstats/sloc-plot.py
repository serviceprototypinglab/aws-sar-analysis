import json
import pandas as pd
import pylab
import collections

limit = 3000

pd.set_option('display.width', 130)
pd.set_option('display.max_rows', 999)

f = open("sloc.json")
sloc = json.load(f)
langs = [lang[0] for codefolder in list(sloc.values()) for lang in codefolder]
langsfiltered = [lang[0] for codefolder in list(sloc.values()) for lang in codefolder if lang[1] > 20]
langs = sorted(list(set(langs)))
langsfiltered = sorted(list(set(langsfiltered)))
print("Total:")
print(langs)
print("Filtered (>20 lines)(minus: {}):".format(set(langs).difference(set(langsfiltered))))
print(langsfiltered)

maxlines = 0

#sloc_sorted = sorted(sloc.items(), key=lambda kv: sum(x[1] for x in kv[1]))
#sloc = collections.OrderedDict(sloc_sorted)

d = {}
for codefolder in sloc:
	lines = 0
	for langstat in sloc[codefolder]:
		lines += langstat[1]
	if lines > maxlines:
		maxlines = lines
		print("record", codefolder, maxlines, sloc[codefolder])

	if lines > limit:
		print("skip", codefolder, maxlines, sloc[codefolder])
		continue

	d[codefolder] = {}
	for lang in langs:
		d[codefolder][lang] = 0
		for langstat in sloc[codefolder]:
			if lang == langstat[0]:
				d[codefolder][lang] = langstat[1]

d_sorted = sorted(d.items(), key=lambda kv: sum(kv[1][x] for x in kv[1]))
d = collections.OrderedDict(d_sorted)

df = pd.DataFrame(d).transpose()
print(df)
print("Considered: {} out of {} ({}%) with limit {}".format(len(df), len(sloc), round(100 * len(df) / len(sloc), 2), limit))

ax = df.plot(kind="bar", stacked=True, width=1.0, cmap="gray")
ax.get_xaxis().set_ticks([])
ax.set_title("Function implementations")
#pylab.show()
pylab.savefig("sloc.pdf", format="pdf")
