import argparse
import re
import requests
import shutil
import string

from ConfigParser import ConfigParser
from lxml import html

# Read from the arguments
parser = argparse.ArgumentParser(description='A script to download all of the videos associated with a Mindbites course')
parser.add_argument("-f", "--finish", help="The number of the video in the list at which to finish downloading", default=9999, required=False)
parser.add_argument("-o", "--out", help="The folder in which all of the videos will be downloaded", default="./", required=False)
parser.add_argument("-r", "--replace", help="A path to an INI file which contains a listing of corrections to apply when naming the video files", default="./replace.ini", required=False)
parser.add_argument("-s", "--start", help="The number of the video in the list at which to start downloading", default=1, required=False)
parser.add_argument("-v", "--view", help="Preview a listing of video files names as they will be downloaded", default=False, required=False)

required = parser.add_argument_group('required arguments')
required.add_argument("-c", "--course", help="The name of the course", required=True)
required.add_argument("-e", "--email", help="User's email address used for logging in", required=True)
required.add_argument("-p", "--password", help="User's password used for logging in", required=True)
required.add_argument("-u", "--url", help="The URL of the Mindbites page containing the listing of videos", required=True)

args = vars(parser.parse_args())

# Read from the configuration file
config = ConfigParser()
config.optionxform = str
config.read(args["replace"])

# Pages
pageWithDownloads = args["url"]
loginPage = "http://www.mindbites.com/login"
rootDomain = "http://mindbites.com"

# Login credentials
email = args["email"]
password = args["password"]

# Where to start and finish
finish = int(args["finish"])
start = int(args["start"])

# Name changing
courseUrlName = args["course"].lower()
courseUrlName = re.sub(" ", "\\\-", courseUrlName)
courseUrlName = re.sub("[^a-z0-9\\\-]", "", courseUrlName)

beginRemove = "http:\/\/mindbites\.com\/protected\/lesson\/[0-9]+\-(" + courseUrlName + "\-)?"
endRemove = "\/video_files\/download"

section = "mindbites"
options = config.options(section)
replace = {}

key = ""
value = ""

for option in options:
	key = re.sub("^[\"\']", "", option)
	key = re.sub("[\"|\']$", "", key)
	
	value = config.get(section, option)
	value = re.sub("^[\"\']", "", value)
	value = re.sub("[\"|\']$", "", value)
	
	replace[key] = value

# Previewing and output
outFolder = args["out"]
preview = bool(args["view"])

def main():
	# Perform the login
	payload = {
		"email": email,
		"password": password,
		"commit": ""
	}

	print "[Logging in]"
	session = requests.session()
	result = session.post(loginPage, data = payload, headers = dict(referer = loginPage))

	# Obtain the list of videos to download
	print "[Examining course page]"
	result = session.get(pageWithDownloads, headers = dict(referer = pageWithDownloads))
	tree = html.fromstring(result.content)
	downloadLinks = tree.xpath("//*[@id='overview']/div[5]/ul/li/a[2]/@href")
	iterations = 1
	
	print "[Ready]"
	print ""

	for link in downloadLinks:
		link = rootDomain + link

		# Name each of the files
		name = re.sub(beginRemove, "", link)
		name = re.sub(endRemove, "", name)
		name = re.sub("\-", " ", name)
		name = string.capwords(name)

		for key in replace:
			name = re.sub(key, replace[key], name)

		name = format(iterations, "03") + " - " + name + ".mp4"

		# Are we allowed to download this?
		if iterations < start:
			iterations += 1
			continue
			
		if iterations > finish:
			break
			
		# Show what is being downloaded
		print "[" + str(iterations) + "]"
		print "Link: " + link
		print "Name: " + name

		iterations += 1

		# Download and save the video
		if preview:
			print " "
			continue
		
		print "[Downloading]"

		path = outFolder + name
		video = session.get(link, stream = True)

		with open(path, 'wb') as handle:
			for block in video.iter_content(1024):
				handle.write(block)

		print "[Done]"
		print " "
		
	print "[All done]"

if __name__ == "__main__":
	main()