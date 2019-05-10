import os
import yaml
import sys
import shutil
import datetime

foldersdir = "_codefolders"
samsdir = "_sams"

copysams = False
copysamscode = False
if len(sys.argv) == 2 and sys.argv[1] == "--copy":
	copysams = True
if len(sys.argv) == 2 and sys.argv[1] == "--copycode":
	copysams = True
	copysamscode = True
if copysams:
	os.makedirs(samsdir, exist_ok=True)

folders = os.listdir(foldersdir)

yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

gsamok = 0
gother = 0
gbroken = 0
ghassam = 0

code_none = 0
code_local = 0
code_remote = 0
code_zip = 0

gcode_none = 0
gcode_remote = 0
gcode_zip = 0
gcode_local_mixed = 0

for folder in folders:
	print("------", folder)
	folderpath = os.path.join(foldersdir, folder)
	targetfolder = os.path.join(samsdir, folder)
	samok = 0
	other = 0
	broken = 0
	rcode_none = 0
	rcode_local = 0
	rcode_remote = 0
	rcode_zip = 0
	needscopycode = False
	zips = []
	sams = []
	for root, dirs, files in os.walk(folderpath):
		#print(root, dirs, files)
		for yamlfile in [f for f in files if f.endswith(".yml") or f.endswith(".yaml")]:
			yamlfile = os.path.join(root, yamlfile)
			#print("YAML", yamlfile)
			try:
				y = yaml.load(open(yamlfile))
			except:
				#print("ERROR", yamlfile)
				broken += 1
			else:
				if y and "Transform" in y and y["Transform"] == "AWS::Serverless-2016-10-31":
					#print("SAM found")
					samok += 1
					targetyamlfile = os.path.join(targetfolder, str(samok) + ".yaml")
					sams.append(os.path.join("code", "/".join(yamlfile.split("/")[1:])))
					if copysams:
						os.makedirs(targetfolder, exist_ok=True)
						shutil.copy(yamlfile, targetyamlfile)
					hascode = False
					haslocalcode = False
					localzips = []
					if "Resources" in y:
						for r in y["Resources"]:
							if "Type" in y["Resources"][r] and y["Resources"][r]["Type"] == "AWS::Serverless::Function":
								if "Properties" in y["Resources"][r] and "CodeUri" in y["Resources"][r]["Properties"]:
									uri = y["Resources"][r]["Properties"]["CodeUri"]
									hascode = True
									if type(uri) == str and not uri.startswith("s3://"):
										if uri.endswith(".zip"):
											zippath = os.path.join(folderpath, uri)
											#print("ZIP", zippath)
											localzips.append(zippath)
										else:
											haslocalcode = True

					if haslocalcode:
						needscopycode = True

					zips += localzips

					if not hascode:
						rcode_none += 1
					elif haslocalcode:
						rcode_local += 1
					elif localzips:
						rcode_zip += 1
					else:
						rcode_remote += 1
				else:
					#print("SAM not found")
					other += 1

	if rcode_zip and not rcode_local and copysamscode:
		valid = True
		for zip in zips:
			if not os.path.isfile(zip):
				valid = False
		if valid:
			#print("ALL VALID ZIPs!")
			targetfolderzips = os.path.join(targetfolder, "zipcode")
			os.makedirs(targetfolderzips, exist_ok=True)
			for zipfile in zips:
				shutil.copy(zipfile, targetfolderzips)
		else:
			rcode_local += rcode_zip
			rcode_zip = 0
			needscopycode = True

	if needscopycode and copysamscode:
		targetcodefolder = os.path.join(targetfolder, "code")
		shutil.rmtree(os.path.join(targetcodefolder), ignore_errors=True)
		shutil.copytree(folderpath, targetcodefolder)
		shutil.rmtree(os.path.join(targetcodefolder, ".git"), ignore_errors=True)

		f = open(os.path.join(targetfolder, "code-sams.yaml"), "w")
		yaml.dump(sams, f)
		f.close()

	code_none += rcode_none
	code_local += rcode_local
	code_remote += rcode_remote
	code_zip += rcode_zip
	if rcode_local:
		gcode_local_mixed += 1
	elif rcode_zip:
		gcode_zip += 1
	elif rcode_remote:
		gcode_remote += 1
	elif rcode_none:
		gcode_none += 1

	if samok:
		ghassam += 1
	gsamok += samok
	gother += other
	gbroken += broken
	print("=> {} ok SAMs, {} other, {} unclear/broken".format(samok, other, broken))

gsamokavg = round(gsamok / len(folders), 2)
gotheravg = round(gother / len(folders), 2)
gbrokenavg = round(gbroken / len(folders), 2)

createcsv = False
if not os.path.isfile("samfinder.csv"):
	createcsv = True

date = datetime.date.today()
f = open("samfinder.csv", "a")
if createcsv:
	print("#date,repos,reposwithsams,sams,samsperrepo,yamlperrepo,brokenperrepo,samnocode,samremotecode,samzipcode,samfoldercode,reponocode,reporemotecode,repozipcode,repofoldercode", file=f)
print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(date, len(folders), ghassam,gsamok, gsamokavg, gotheravg, gbrokenavg, code_none, code_remote, code_zip, code_local, gcode_none, gcode_remote, gcode_zip, gcode_local_mixed), file=f)
f.close()

print("AVG: {} ok SAMs, {} other, {} unclear/broken".format(gsamokavg, gotheravg, gbrokenavg))
print("{} out of {} function repositories contain a SAM file ({}%).".format(ghassam, len(folders), round(100 * ghassam / len(folders), 2)))
print("Out of {} SAMs, {} reference no code, {} reference only remote (S3) code resources, {} reference local zipped code, and {} reference only local code in folders.".format(gsamok, code_none, code_remote, code_zip, code_local))
print("Out of {} SAM-containing function repositories, {} reference no code, {} reference only remote (S3) code resources, {} reference only local zipped code, and {} reference local in folders or mixed local/zipped/remote code.".format(ghassam, gcode_none, gcode_remote, gcode_zip, gcode_local_mixed))
if copysams:
	print("Copied SAMs into {}".format(samsdir))
if copysamscode:
	print("Copied local code into {}".format(samsdir))
