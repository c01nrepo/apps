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
from datetime import datetime

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
			make_tgzfile(root, './pkg/%s%s.tgz'%(manifest['pkg'],manifest['version']))
			manifest['url'] = 'pkg/%s%s.tgz'%(manifest['pkg'],manifest['version'])
			listing['apps'].append(manifest)

	# Write Listings
	json.dump(listing, open('./listing.json','w'))
	print('\nlisting.json', listing)

	# TODO Categories


app_start()