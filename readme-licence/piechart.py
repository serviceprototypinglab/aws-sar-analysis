import pylab
import numpy as np
import collections

pcts = {
	"Academic": 4,
	"Amazon ASL": 2,
	"Apache*": 117,
	"BSD 2-Clause*": 8,
	"© Amazon": 26,
	"custom A": 2,
	"custom B": 2,
	"© Apple": 3,
	"GNU GPL*": 10,
	"ISC": 2,
	"MIT*": 214,
	"MIT NoPerm": 4,
	"MIT-variant": 9,
	"custom C": 2,
	"other (long)": 40,
	"other (short)": 81
}
pcts = collections.OrderedDict(sorted(pcts.items()))

from cycler import cycler
colors = pylab.cm.gray(np.linspace(0.2,0.8,5))
pylab.rcParams['axes.prop_cycle'] = cycler(color=colors)

fig, ax = pylab.subplots(figsize=(6, 4.5), subplot_kw=dict(aspect="equal"))

def labelling(val):
	a = int(val / 100 * sum(list(pcts.values())))
	if val > 4:
		lbl = "{:d}\n[{:.1f}%]".format(a, val)
	elif a >= 3:
		lbl = "{:d}".format(a)
	else:
		lbl = ""
	print(val, a, lbl)
	return lbl

wedges, texts, lbls = ax.pie(list(pcts.values()), wedgeprops=dict(width=0.5), startangle=30, autopct=labelling, pctdistance=0.75)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

# Reference: https://matplotlib.org/gallery/pie_and_polar_charts/pie_and_donut_labels.html
xf = 1.35 # 1.35
yf = 1.60 # 1.40
yforig = yf
prvang = None
for i, p in enumerate(wedges):
	text = list(pcts.keys())[i]
	ang = (p.theta2 - p.theta1)/2. + p.theta1
	oang = ang
	if prvang:
		if ang < prvang + 8:
			ang = prvang + 8
			x = np.cos(np.deg2rad(ang))
			yf += 0.17 * np.sign(x) * np.sign(y)
			if np.sign(x) * np.sign(y) > 0:
				direc = "up"
			else:
				direc = "down"
			print(direc, oang, prvang, ang, yf, np.sign(x), np.sign(y), text)
		else:
			yf = yforig
			print("reset", text)
			if i == len(pcts.keys()) - 1:
				yf -= 0.18
	else:
		print("skip", text)
	prvang = ang
	oy = np.sin(np.deg2rad(oang))
	ox = np.cos(np.deg2rad(oang))
	y = np.sin(np.deg2rad(ang))
	x = np.cos(np.deg2rad(ang))
	horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
	connectionstyle = "angle,angleA=0,angleB={}".format(oang)
	kw["arrowprops"].update({"connectionstyle": connectionstyle})
	ax.annotate(text, xy=(ox, oy), xytext=(xf*np.sign(ox), yf*oy), horizontalalignment=horizontalalignment, **kw)

ax.set_title("Function licences")

#pylab.show()
pylab.savefig("piechart.pdf", format="pdf")
