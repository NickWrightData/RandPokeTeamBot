import tweepy			#for tweeting out result
from PIL import Image, ImageDraw, ImageFont	#for joining images together, etc
import random			
import os				#for grabbing/manipulating files
import re
from datetime import datetime

from Pokemon import Pokemon
from postgres import postgres
from pokeTeams3 import Team
import PokeRequestResponder

CONSUMER_KEY = Team.CONSUMER_KEY
CONSUMER_SECRET = Team.CONSUMER_SECRET
ACCESS_KEY = Team.ACCESS_KEY
ACCESS_SECRET = Team.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
me = api.me()

class MyStreamListener(tweepy.StreamListener):

	def on_status(self, tweet):
		startTime=datetime.now()
		print(startTime)
		print('@'+tweet.user.screen_name+": \""+tweet.text+"\"")
		try:
			
			if tweet.user.id == me.id:
				#I'm this tweet's author, so ignore it
				print("i'm the author!")
			else:
				result = PokeRequestResponder.respondToTweet(tweet.text, tweet.id_str, isATest=False)
				if result == 0:
					errorTweetText = "Well this is awkward...it looks like no Pokémon fit that description! 🤷\n\n(If this is wrong, please let me know!)"
					Team.tweetOut(userTweet=tweet.id_str, testing=False, tweetText=errorTweetText, imagePathFront="error", imagePathBack="error")
				elif result == -1:
					errorTweetText = "Whoops! Got an error! Try again! :)"
					Team.tweetOut(userTweet=tweet.id_str, testing=False, tweetText=errorTweetText, imagePathFront="error", imagePathBack="error")
				else:
					pass
					#This is handled in the RequestResponder now
					#Team.tweetATeam(result["test"], result["userTweet"], result["team"], result["regionText"], result["typeText"])

		except BaseException as error:
			print('An exception occurred (scan): '+str(error))
			try:
				errorTweetText = ""
				print(error)
				errorTweetText = "Whoops! Got an error! Try again! :)"
				Team.tweetOut(userTweet=tweet.id_str, testing=False, tweetText=errorTweetText, imagePathFront="error", imagePathBack="error")
			except BaseException as error2:
				print("UGH!" +str(error2))
			print('continuing...')
		
		Pokemon.resetAll()
		
		endTime=datetime.now()
		print(endTime-startTime)
		print("==============================================================================")	
	
	def on_error(self, status):
		#logger.error(status)
		print(status)
		
try:		
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=['@RandPokeTeamBot team me'], is_async=True)
	print("Searching for Tweets...")
except:
	print("WHOOPSIE")