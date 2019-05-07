import glob

texts = {}

licencefiles = glob.glob("licences/*.licence")
for licencefile in licencefiles:
	firstlines = "/".join(open(licencefile).readlines()).replace("\n", "")
	if firstlines.startswith("/"):
		firstlines = firstlines[1:]
	firstlines = firstlines.strip()

	if firstlines.startswith("MIT License"):
		firstlines = "MIT License/+VARIANTS"
	elif firstlines.startswith("Apache License"):
		firstlines = "Apache License/+VARIANTS"
	elif firstlines.startswith("GNU GENERAL PUBLIC LICENSE"):
		firstlines = "GNU GENERAL PUBLIC LICENSE/+VARIANTS"
	elif firstlines.startswith("BSD 2-Clause License"):
		firstlines = "BSD 2-Clause License/+VARIANTS"

	texts[firstlines] = texts.get(firstlines, 0) + 1

print("Licence texts:", len(licencefiles))
other = 0
othershort = 0
for text in sorted(texts):
	if texts[text] > 1:
		print("{:3d} [{:4.1f}%] {:60s}".format(texts[text], round(100 * texts[text] / len(licencefiles), 1), text[:60]))
	else:
		if len(text) < 100:
			othershort += 1
		else:
			other += 1
			#print("O", text[:60])

print("=> More than 1 occurrence including variants:", len(texts) - other - othershort)
print("Other long:  {:3d} [{:4.1f}%]".format(other, round(100 * other / len(licencefiles), 1)))
print("Other short: {:3d} [{:4.1f}%]".format(othershort, round(100 * othershort / len(licencefiles), 1)))
