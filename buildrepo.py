# Run with python3!

thistool = '''
    ____          _  __     __
   / __ ) __  __ (_)/ /____/ /
  / __  |/ / / // // // __  /
 / /_/ // /_/ // // // /_/ /
/_____/ \__,_//_//_/ \__,_/

   ______ ____  ___ _   __
  / ____// __ \<  // | / /
 / /    / / / // //  |/ /
/ /___ / /_/ // // /|  /
\____/ \____//_//_/ |_/

    ____
   / __ \ ___   ____   ____
  / /_/ // _ \ / __ \ / __ \
 / _, _//  __// /_/ // /_/ /
/_/ |_| \___// .___/ \____/
            /_/
'''

import tarfile
import os
import json
import hashlib
import sys
import time
from datetime import datetime

def sha256(filename):
	BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
	sha256 = hashlib.sha256()
	with open(filename, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
	return sha256.hexdigest()

def make_tgzfile(source_dir,output_filename):
	with tarfile.open(output_filename, 'w:gz') as tar:
		tar.add(source_dir, arcname=os.path.basename(source_dir))
	print('Made %s Tarfile'%output_filename)

def app_start():
	print(thistool)

	listing = {
		'version':datetime.now().strftime('%y%m%d%H%M'),
		'apps':[]
	}

	MANIFEST_REQUIREMENTS = ['name', 'desc', 'tags', 'author', 'version', 'pkg', 'start', 'pubEpoch', 'url', 'sha256']

	if os.path.exists('./pkg'): # Clear old pkgs
		import shutil
		shutil.rmtree('./pkg')
		print('Clearing out ./pkg folder')
	os.mkdir('./pkg')

	for root, dirs, files in os.walk('./src'): # Index and compress modules
		print('Walking', root, dirs, files)
		if 'manifest.json' in files:
			manifest = json.load(open('./%s/manifest.json'%root))
			print('Packing 📦 %s %s'%(manifest['name'], manifest['version']))
			output_filename = 'pkg/%s-%s.tgz'%(manifest['pkg'],manifest['version'])
			make_tgzfile(root, './'+output_filename)
			manifest['url'] = output_filename
			manifest['sha256'] = sha256(output_filename)
			listing['apps'].append(manifest)
			for r in MANIFEST_REQUIREMENTS:
				if r not in manifest:
					print('⚠️  Requirement "%s" not satisfied in pkg "%s"'%(r, manifest['pkg']))
					time.sleep(5) # Delay to show error

	UNQIUE_REQUIREMENTS = ['name', 'pkg', 'url', 'sha256']
	for r in UNQIUE_REQUIREMENTS:
		checkUnique = {}
		for manifest in listing['apps']:
			if manifest[r] in checkUnique.keys():
				print('☢️  Check of unique requirement "%s" failed!\n😡  Conflict between packages "%s" and "%s"'%(r,manifest['pkg'],checkUnique[manifest[r]]))
				time.sleep(5) # Delay to show error
			else:
				checkUnique[manifest[r]] = manifest['pkg']

	# Write Listings
	json.dump(listing, open('./listing.json','w'))
	print('\n✏️  listing.json written.')

	# TODO Categories


app_start()
