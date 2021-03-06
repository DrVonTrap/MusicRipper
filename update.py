#! /usr/bin/python3

import database
import reddit
import youtube_dl
import postProcess
import os
import youtubeURLGrabber
import time
import sys
from subprocess import call

subReddits = []
subReddits.append( ("FutureBass", "Genre") )
subReddits.append( ("Glitch", "Genre") )
subReddits.append( ("Vaporwave", "Genre") )
subReddits.append( ("House", "Genre") )
subReddits.append( ("TropicalHouse", "Genre") )

def gatherNewRedditURLs():
	global subReddits
	database.initDB()

	# download reddit urls
	for subReddit_ in subReddits:
		subReddit = subReddit_[0]
		print("getting urls for", subReddit)
		urlList = reddit.getHot(subReddit, 100) + reddit.getTopMonth(subReddit, 100)
		for url in urlList:
			database.addURL(url, subReddit_)

		database.saveDB()

def downloadURLs():
	database.initDB()

	for thing in database.nextURLToDownload():
		(group, url) = thing
		print('\t' + "trying to download", url, "to", group)

		try:
			argsList = ["youtube-dl"]
			argsList.extend([url])
			# argsList.extend(["--restrict-filenames"])
			argsList.extend(["--output", "Downloads/" + str(group[1]) + "/" + str(group[0]) + "/%(id)s - %(title)s.%(ext)s"])
			argsList.extend(["--extract-audio"])
			argsList.extend(["--audio-format", "mp3"])
			argsList.extend(["--youtube-skip-dash-manifest"])

			call(argsList)

			database.markURLAsClosed(url, group)
			database.saveDB()
		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
		# os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
	if "-r" in sys.argv:
		gatherNewRedditURLs()

	if "-y" in sys.argv:
		youtubeURLGrabber.addYouTubeCuratorURLs()

	if "-u" in sys.argv:
		downloadURLs()

# downloadURLs()
