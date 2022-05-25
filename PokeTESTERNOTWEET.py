import random			
from datetime import datetime

from Pokemon import Pokemon
from postgres import postgres
from pokeTeams3 import Team
import PokeRequestResponder


type_names = {2:"Bug",
	15:"Dark",
	14:"Dragon",
	11:"Electric",
	17:"Fairy",
	6:"Fighting",
	10:"Fire",
	7:"Flying",
	13:"Ghost",
	1:"Grass",
	4:"Ground",
	9:"Ice",
	0:"Normal",
	3:"Poison",
	12:"Psychic",
	5:"Rock",
	16:"Steel",
	8:"Water"}
			
while (1):
	#to_test = to_test.reverse()
	input_tweet = input("TWEET! ")
	
	startTime=datetime.now()
	print(startTime)
	
	if input_tweet == "random":
		allMons = postgres.runQuery("SELECT name FROM pkmn")
	
		input_tweet = random.choice(["swsh ",""])
		input_tweet += " ".join(random.sample(["kanto", "johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar"],k=1))
		input_tweet += " "
		
		input_tweet += " ".join(random.sample([i[0] for i in allMons],k=1))
		input_tweet += " "
		#input_tweet += " ".join(random.sample(["normal", "bug","dark","dragon","electric","fairy","fighting",
		#			"fire","flying","ghost","grass","ground","ice","poison","psychic","rock","steel","water"],k=1))
		input_tweet += " " + random.choice([" duplicates",""])
	
	print(input_tweet)
		

	try: 
		
		result = PokeRequestResponder.respondToTweet(input_tweet, False, isATest=True)
		
		if result == 0:
			print("Well this is awkward...it looks like no Pokémon fit that description! 🤷\n\n(If this is wrong, please let me know!)")
		elif result == -1:
			print("Whoops! Got an error! Try again! :)")

	except BaseException as error:
		print('An exception occurred (NO TWEET): '+str(error))
		try:
			errorTweetText = ""
			print(error)
			#errorTweetText = "Whoops! Got an error! Try again! :)"
			#Team.tweetOut(userTweet=tweet.id_str, testing=False, tweetText=errorTweetText, imagePathFront="error", imagePathBack="error")
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
		
		
print("Searching for Tweets...")