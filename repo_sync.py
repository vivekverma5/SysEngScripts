#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

'''
Repo Sync script to read from repo_sync.cfg file 
Create repo if does not exist using mirror
Run repo sync on mirror
run repo sync on repository 

'''

def repo_init(parameters_array,repo_path,src_branch):
	##Parshing parameters array to find parameters from repo_sync.conf file
	gerrit_server = parameters_array[0]
	gerrit_user	= parameters_array[1]
	project_manifest = parameters_array[2]
	branch_name = parameters_array[3]
	mirror = parameters_array[4]

	##path of Grok SRC foler
	grok_path = repo_path
	##name of folder related to branch
	src_folder = src_branch

	## doing cd for Grok source path then making branch folder inside it
	os.chdir(grok_path)
	os.mkdir(src_branch)
	os.chdir(src_branch)

	print ("Running Repo init for %s" % (branch_name))
	print ("Repo init command")
	print("repo init -u ssh://%s@%s:9418%s --repo-url=ssh://%s@%s:9418%s --repo-branch=stable -b %s  --no-repo-verify --reference %s "% (gerrit_user, gerrit_server, project_manifest, gerrit_user, gerrit_server, project_manifest, branch_name, mirror ) )
	
	##Command for repo init.
	repo_init_cmd = """repo init -u ssh://%s@%s:9418%s --repo-url=ssh://%s@%s:9418%s --repo-branch=stable -b %s  --no-repo-verify --reference %s """% (gerrit_user, gerrit_server, project_manifest, gerrit_user, gerrit_server, project_manifest, branch_name, mirror )
	
	#print repo_init_cmd

	## Running repo init command
	os.system(repo_init_cmd)

def mirror_sync(parameters_array):
	##Function to repo sync on mirror
	mirror = parameters_array[4].rstrip(os.linesep)
	
	##Repo Sync Command 
	repo_sync_cmd = "repo sync -j10 -c"

	##Running repo sync on mirror first
	##cd to mirror
	os.chdir(mirror)

	print ("Running Repo sync for Mirror %s" % (mirror))
	print ("Repo Sync command")
	print (repo_sync_cmd )

	## Running Repo Sync
	os.system(repo_sync_cmd)


def repo_sync(parameters_array,branch_check):
	branch_name = parameters_array[3]
	src_path = branch_check
	
	##Repo Sync Command 
	repo_sync_cmd = "repo sync -j10 -c"

	##cd to Grok SRC branch folder
	os.chdir(src_path)
	
	print ("Running Repo sync for %s" % (branch_name))
	print ("Repo Sync command")
	print (repo_sync_cmd )

	## Running Repo Sync
	os.system(repo_sync_cmd)


def main():

	##Path where OpenGrok SRC folder is located
	repo_path = "/var/opengrok/src/"
	
	##reading repo_sync.conf file
	with open('repo_sync.conf') as f:
		for line in f:
			##Only read lines which are not commented out in repo_sync.conf
			if '##' in line:
				pass
			else:
				##creating parameters array consisting each attributes. 
		   		parameters = line.split(' ')
		   		#print parameters
		   		## Calling function for mirror sync
		   		mirror_sync(parameters)
		   		##getting branch name and finding folder associated with branch name in Grok SRC path
				branch_name = parameters[3].replace("/", "_")
				src_branch = branch_name[1:]
				#print ("branch name %s" % (src_branch))
				branch_check = repo_path + src_branch
				#print ("branch check %s" % (branch_check))
				## script will call repo_sync function if folder such as fireos_main_dev exist in Grok SRC path otherwise will call repo_init() function.
				if os.path.exists(branch_check):
					repo_sync(parameters,branch_check)
				else:
					repo_init(parameters,repo_path, src_branch)
		
main()





  
