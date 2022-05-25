from PIL import Image, ImageDraw, ImageFont	#for joining images together, etc
import random			
import os				#for grabbing/manipulating files
import re
from datetime import datetime

from Pokemon import Pokemon
from postgres import postgres
from pokeTeams3 import Team

def respondToTweet(tweet_text, tweet_id_str, isATest):
	generationNums = {"kanto":1,
					"johto":2,
					"hoenn":3,
					"sinnoh":4,
					"unova":5,
					"kalos":6,
					"alola":7,
					"galar":8}
					
	typeNames = {"bug":2,
				"dark":15,
				"dragon":14,
				"electric":11,
				"fairy":17,
				"fighting":6,
				"fire":10,
				"flying":7,
				"ghost":13,
				"grass":1,
				"ground":4,
				"ice":9,
				"normal":0,
				"poison":3,
				"psychic":12,
				"rock":5,
				"steel":16,
				"water":8}

	try: 
		
		the_range = []
		swsh_only = False
		region_limit = False
		type_limit = False
		duplicates = False
		fully_evolved = False
		FEtext = ""
		#only_selected = False
		maxMon=890
		minMon=1
		
		monIDs = []
		
		rangeQuery = "SELECT id, name FROM pkmn WHERE id <= "+str(maxMon)+" AND id >= "+str(minMon)
		
		specificQuery = isAMonQuery = "SELECT id, name FROM pkmn WHERE LOWER(REGEXP_REPLACE(name, '[^a-zA-Z0-9]', '', 'g')) = %s"
		specificQueryEnd = " ORDER BY id ASC"
		
		print("Parsing Tweet...")
		#grab all words from tweet
		possibleMonWords = [re.sub(r'\W+', '', i).lower() for i in tweet_text.split()]
		
		#determine if tweet contains "swsh"
		if "swsh" in possibleMonWords:
			swsh_only = True
			rangeQuery += " AND in_galar IS TRUE"
			specificQuery += " AND in_galar IS TRUE "
		
		#...or "duplicates"
		if "duplicates" in possibleMonWords:
			duplicates = True
		
		#...or "fully" and "evolved"
		if "fully" in possibleMonWords and "evolved" in possibleMonWords:
			FEtext = " AND fully_evolved IS TRUE "
			rangeQuery += FEtext
			specificQuery += FEtext
			fully_evolved = True
			
		#determine which regions the tweet wants the team limited to
		regions = set(possibleMonWords).intersection(set(["kanto", "johto", "hoenn", "sinnoh", "unova", "kalos", "alola", "galar"]))
		types = set(possibleMonWords).intersection(set(["normal", "bug","dark","dragon","electric","fairy","fighting",
					"fire","flying","ghost","grass","ground","ice","poison","psychic","rock","steel","water"]))
		
		regText = ""
		typeTextA = ""
		typeTextB = ""
		typeTextAB = ""
		
		if len(regions) > 0:
			region_limit = True
			regText += " AND generation IN ("
			for region in regions:
				regText += str(generationNums[region.lower()])
				regText += ","
			regText = regText[:-1]
			regText += ")"
			rangeQuery += regText
			specificQuery += regText		
			
		if len(types) > 0:
			type_limit = True
			typeTextA += " AND (type_a IN ("
			typeTextB += " OR type_b IN ("
			for type in types:
				typeTextA += str(typeNames[type.lower()])
				typeTextA += ","
				typeTextB += str(typeNames[type.lower()])
				typeTextB += ","
			typeTextA = typeTextA[:-1]
			typeTextA += ")"
			typeTextB = typeTextB[:-1]
			typeTextB += ")"
			typeTextAB = typeTextA + typeTextB + ")"
			rangeQuery += typeTextAB
			specificQuery += typeTextAB
		
		print("Building team...")
        
		for monWord in possibleMonWords:
			if monWord.lower() in ("nidoranm", "nidoranmale", "nidoran_male", "nidoranmale"):
				monIDs.append(32)
			elif monWord.lower() in ("nidoranf", "nidoranfemale", "nidoran_female", "nidoranfemale"):
				monIDs.append(29)
			#elif monWord.lower() in ("mrmime", "mr_mime", "mr.mime", "mr._mime"):
				#monIDs.append(122)
			isAMon = postgres.runQuery(isAMonQuery, [monWord])
			result = postgres.runQuery(specificQuery+specificQueryEnd, [monWord])
			if len(result) >= 1:
				allSame = True
				name = result[0][1]
				for i in result:
					if i[1] != name:
						allSame = False
				if allSame:
					if name == "Nidoran":
						monIDs.append(random.choice([result[0][0],result[1][0]]))
					else:
						monIDs.append(result[0][0])
			elif isAMon:
				#It's a mon! BUT it wasn't selected...electric Blastoise, anyone?
				return 0
		
		the_range_result = postgres.runQuery(rangeQuery)
		
		if len(monIDs) >= 1:
			the_range = monIDs
			if not duplicates and (swsh_only or region_limit or type_limit or fully_evolved):
				#add the rest
				rest = 6-len(the_range)
				appending = [i[0] for i in random.sample(the_range_result, min(rest,len(the_range_result)))]
				for i in appending:
					if i not in the_range:
						the_range.append(i)
				random.shuffle(the_range)
		else:
			the_range = range(minMon,maxMon+1)
			if swsh_only or region_limit or type_limit or fully_evolved:
				the_range = [i[0] for i in the_range_result]
		
		if len(the_range) == 0:
			return 0
		elif len(the_range) == 6:
			pass
			#{"test":isATest, "userTweet":tweet_id_str, "team":the_range, "regionText":regText, "typeText":typeTextAB}
		elif duplicates:
			the_range = random.choices(the_range,k=6)
			#{"test":isATest, "userTweet":tweet_id_str, "team":random.choices(the_range,k=6), "regionText":regText, "typeText":typeTextAB}
		else:
			choices = 6
			if len(the_range) < 6:
				choices = len(the_range)
			the_range = random.sample(the_range,k=choices)
			#{"test":isATest, "userTweet":tweet_id_str, "team":random.sample(the_range,k=choices), "regionText":regText, "typeText":typeTextAB}
		Team.tweetATeam(isATest, tweet_id_str, the_range, regText, typeTextAB, FEtext)
		return 1

	except BaseException as error:
		print('An exception occurred (resp): '+str(error))
		errorTweetText = ""
		print(error)
		print('continuing...')
		return -1

def on_error(self, status):
	#logger.error(status)
	print(status)