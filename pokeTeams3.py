import tweepy			#for tweeting out result
#import sys
from PIL import Image, ImageDraw, ImageFont	#for joining images together, etc
import random			
import os				#for grabbing/manipulating files
from Pokemon import Pokemon
import re

class Team:
	#KEYS TO CONNECT TO TWITTER
	CONSUMER_KEY = #Consumer Key
	CONSUMER_SECRET = #Consumer Secret
	ACCESS_KEY = #Access Key
	ACCESS_SECRET = #Access Secret

	#Dev Account for Testing!
	TEST_CONSUMER_KEY = #Dev Account Consumer Key
	TEST_CONSUMER_SECRET = #Dev Account Consumer Secret
	TEST_ACCESS_KEY = #Dev Account Access Key
	TEST_ACCESS_SECRET = #Dev Account Acces Secret

	allPokemon = range(1,894) #1-893, inclusive
	gen1 = range(1,152)
	gen2 = range(152,252)
	gen3 = range(252,387)
	gen4 = range(387,494)
	gen5 = range(494,650)
	gen6 = range(650,722)
	gen7 = range(722,810)
	gen8 = range(810,894)
	test = range(101,102)
	#gen9 = range(894,)

	directory = r'C:\Users\PC\Desktop\twitterBots\pokemonTeams\\'
	subdirectory = '\HOME\\' #'\sugimori\\' #'\ThreeEvolved\\' #'\FEPs\\' #'\TE_NoBaby\\'
	textDirectory = '\\text\\'
	iconDirectory = '\\icons\\'
	restrictedDirectory = '\\restricted\\'	
	resultFront = 'RESULTteam.png'
	resultBack = 'RESULTback.png'
	
	iconSize = 512
	border = 15
	horiz = 2
	vert = 3

	typeNames = {2:"Bug",
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

	typeEmojis = {"Bug":"🐛",
	"Dark":"🕶",
	"Dragon":"🐉",
	"Electric":"⚡",
	"Fairy":"🌸",
	"Fighting":"✊",
	"Fire":"🔥",
	"Flying":"🕊",
	"Ghost":"👻",
	"Grass":"🍃",
	"Ground":"⛰",
	"Ice":"❄",
	"Normal":"⚪",
	"Poison":"☠",
	"Psychic":"🔮",
	"Rock":"🗿",
	"Steel":"⛓",
	"Water":"💧",
	2:"🐛",
	15:"🕶",
	14:"🐉",
	11:"⚡",
	17:"🌸",
	6:"✊",
	10:"🔥",
	7:"🕊",
	13:"👻",
	1:"🍃",
	4:"⛰",
	9:"❄",
	0:"⚪",
	3:"☠",
	12:"🔮",
	5:"🗿",
	16:"⛓",
	8:"💧"}
	
	resultTweet = ''
	userTweet = False 
	test = True
	
	images = []
	backImages = []
	imageNames = []
	names = []
	formNames = []
	types = []
	formids = []
	colors = []
	rotations = []
	xyoffsets = []

	def resetEachTime():
		Team.resultTweet = ''
		Team.userTweet = False 
		Team.test = True
		
		Team.images = []
		Team.backImages = []
		Team.imageNames = []
		Team.names = []
		Team.formNames = []
		Team.types = []
		Team.formids = []
		Team.colors = []
		Team.rotations = []
		Team.xyoffsets = []
	
	def borderText(x, y, draw, text, font, backgroundColor, thickBorder = False):

		if thickBorder:
			# thicker border
			draw.text((x-2, y-2), text, font=font, fill=backgroundColor)
			draw.text((x+2, y-2), text, font=font, fill=backgroundColor)
			draw.text((x-2, y+2), text, font=font, fill=backgroundColor)
			draw.text((x+2, y+2), text, font=font, fill=backgroundColor)
		else:
			# thin border
			draw.text((x-2, y), text, font=font, fill=backgroundColor)
			draw.text((x+2, y), text, font=font, fill=backgroundColor)
			draw.text((x, y-2), text, font=font, fill=backgroundColor)
			draw.text((x, y+2), text, font=font, fill=backgroundColor)

	def tweetOut(userTweet=False, testing=True, tweetText="", imagePathFront="", imagePathBack=""):
		Team.test = testing
		
		if tweetText == "":
			tweetText = Team.resultTweet
		
		if imagePathFront == "":
			imagePathFront = Team.directory+Team.resultFront
			
		if imagePathBack == "":
			imagePathBack = Team.directory+Team.resultBack
		#Connect to Twitter
		if not Team.test:
			auth = tweepy.OAuthHandler(Team.CONSUMER_KEY, Team.CONSUMER_SECRET)
			auth.set_access_token(Team.ACCESS_KEY, Team.ACCESS_SECRET)
		else:
			auth = tweepy.OAuthHandler(Team.TEST_CONSUMER_KEY, Team.TEST_CONSUMER_SECRET)
			auth.set_access_token(Team.TEST_ACCESS_KEY, Team.TEST_ACCESS_SECRET)
		api = tweepy.API(auth)
		
		#Actually tweet out tweet
		#print(imagePathFront)
		print(tweetText);
		
		print("Tweeting...")
		if (not Team.test):
			if imagePathFront != "error" and imagePathBack != "error":
				filenames = [imagePathFront, imagePathBack]
				media_ids = []
				for filename in filenames:
					 res = api.media_upload(filename)
					 media_ids.append(res.media_id)

				if userTweet:
					api.update_status(
						status=tweetText,
						media_ids=media_ids,
						in_reply_to_status_id=userTweet,
						auto_populate_reply_metadata=True
					)
				else:
					# Tweet out a REGULAR tweet with multiple images
					api.update_status(status=tweetText, media_ids=media_ids)		
			elif userTweet:
				api.update_status(
					status=tweetText,
					in_reply_to_status_id=userTweet,
					auto_populate_reply_metadata=True
				)
			
			print("TWEETED!!!")
		else:
			os.system(Team.directory+Team.resultBack)
			os.system(Team.directory+Team.resultFront)

	def isInt(s):
		try: 
			int(s)
			return True
		except ValueError:
			return False

	def fixPNG(im, bg_color=(255, 255, 255)):
		if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
			alpha = im.convert('RGBA').split()[-1]
			bg = Image.new("RGBA", im.size, bg_color)
			bg.paste(im, mask=alpha)
			return bg
			
	def numdash(char):
		return char is '-' or char.isdigit()

	def addFrontText(mon, image, imgcolor):	
		#Add text to the image!
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=45)
		(x, y) = (10, 10)
		
		#Shiny Deets
		shinyBuffer = 0;
		shinyFont = ImageFont.truetype(Team.directory+Team.textDirectory+'Symbola_hint.ttf', size=45)
		shinyMessage = ("*✨" if mon.shiny else "")
		shinyColor = (255,0,0)
		if mon.shiny:
			shinyBuffer = 70;
			Team.borderText(x, y, draw, shinyMessage, shinyFont, (255,255,255), True)
			draw.text((x, y), shinyMessage, fill=shinyColor, font=shinyFont)
		
		#back to the everyday
		message = mon.name
		color = tuple([int(i-150) for i in imgcolor])
		Team.borderText(x+shinyBuffer, y, draw, message, font, (255,255,255), True)
		draw.text((x+shinyBuffer, y), message, fill=color, font=font)
		
		if mon.cherish_only:
			ball = Team.directory+Team.iconDirectory+Team.restrictedDirectory+"ball_cherish.png"
		elif mon.poke_only:
			ball = Team.directory+Team.iconDirectory+"ball_poke.png"
		else:
			ball = Team.directory+Team.iconDirectory+random.choice([x for x in os.listdir(Team.directory+Team.iconDirectory) if "ball" in x])
		
		the_ball = Image.open(ball).resize((64,64))
		image.paste(the_ball, (Team.iconSize-74,Team.iconSize-74), mask=the_ball)
		
		if mon.gender != "None":
			male = Image.open(Team.directory+Team.iconDirectory+"male.png")
			female = Image.open(Team.directory+Team.iconDirectory+"female.png")
			genderless = Image.open(Team.directory+Team.iconDirectory+"genderless.png")
			if mon.gender == "Male":
				genderIcon = male
			elif mon.gender == "Female":
				genderIcon = female
			elif mon.gender == "Genderless":
				genderIcon = genderless
			image.paste(genderIcon, (Team.iconSize-74,10), mask=genderIcon)
		
		if mon.forms:
			font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
			(x, y) = (10, 60)
			message = " (" + (mon.form_name if mon.forms else "") +")"
			color = tuple([int(i-150) for i in imgcolor])
			Team.borderText(x, y, draw, message, font, (255,255,255))
			draw.text((x, y), message, fill=color, font=font)
				
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (10, Team.iconSize - 40)
		message = "Lv. " + str(mon.level)
		color = tuple([int(i-150) for i in imgcolor])
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
		
	def addBackText(mon, image, imgcolor):
		formHeight = 0
		
		if mon.forms:
			formHeight = 40
			
		color = tuple([int(i-150) for i in imgcolor])
		
		#Add text to the image!
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=45)
		(x, y) = (10, 10)
		
		#Shiny Deets
		shinyBuffer = 0;
		shinyFont = ImageFont.truetype(Team.directory+Team.textDirectory+'Symbola_hint.ttf', size=45)
		shinyMessage = ("*✨" if mon.shiny else "")
		shinyColor = (255,0,0)
		if mon.shiny:
			shinyBuffer = 70;
			Team.borderText(x, y, draw, shinyMessage, shinyFont, (255,255,255), True)
			draw.text((x, y), shinyMessage, fill=shinyColor, font=shinyFont)
		
		#back to the everyday
		message = "#"+mon.dex_id_string + " " + mon.name
		
		Team.borderText(x+shinyBuffer, y, draw, message, font, (255,255,255), True)
		draw.text((x+shinyBuffer, y), message, fill=color, font=font)
		
		#Add Form Text
		if mon.forms:
			font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
			(x, y) = (20, 60)
			message = " (" + (mon.form_name if mon.forms else "") +")"
			Team.borderText(x, y, draw, message, font, (255,255,255))
			draw.text((x, y), message, fill=color, font=font)
			
		#Add Ability Text
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (20, 60 + formHeight)
		message = "Ability: " + mon.ability
		color = tuple([int(i-150) for i in imgcolor])
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
			
		#Add "Moves:"
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (10, 110 + formHeight)
		message = "Moves:"
		#print(message)
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
		
		#Add Move 1 Text
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (20, 150 + formHeight)
		message = mon.move_1
		#print(message)
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
			
		#Add Move 2 Text
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (20, 190 + formHeight)
		message = mon.move_2
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
			
		#Add Move 3 Text
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (20, 230 + formHeight)
		message = mon.move_3
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)
			
		#Add Move 4 Text
		font = ImageFont.truetype(Team.directory+Team.textDirectory+'Roboto-Bold.ttf', size=30)
		(x, y) = (20, 270 + formHeight)
		message = mon.move_4
		Team.borderText(x, y, draw, message, font, (255,255,255))
		draw.text((x, y), message, fill=color, font=font)

	def tweetATeam(test=True, userTweet=False, team = random.choices(range(1,891),k=6), regionText="", typeText = "", FEtext = ""):
		Team.resetEachTime()
		#Grab all 6 Dex Pokémon we want to represent
		#[39,6,282,429,62,763]]#[Pokemon(i) for i in range(1,152)]#[9, 18, 34, 59, 71, 101]] #range(6)] #[658,448,778,6,197,700,445,384,282,94,887,248,1,849,249,722,681,609,25,133,405,724,571,745,823,330,635,254,257,872]]

		Team.userTweet = userTweet
		Team.test = test
		
		MasterMons = [Pokemon(i,regionText,typeText,FEtext) for i in team]
		
		teamWeak = Pokemon.teamWeaknesses
		teamResist = Pokemon.teamResistances
		teamImmunity = Pokemon.teamImmunities

		#Start setting up the image
		for mon in MasterMons:
			rg = range(200,256)
			r = random.choice(rg)
			g = random.choice(rg)
			b = random.choice(rg)
			while abs(r - g) < 50 and abs(g - b) < 10:
				r = random.choice(rg)
				g = random.choice(rg)
				b = random.choice(rg)
			currColor = (r, g, b)
			Team.colors.append(currColor)
			curr_rotation = random.choice(range(-3,4))
			Team.rotations.append(curr_rotation)
			thisImage = Team.fixPNG(Image.open(Team.directory+Team.subdirectory+mon.image), currColor).resize((Team.iconSize,Team.iconSize))
			Team.xyoffsets.append(int((thisImage.width - Team.iconSize)/2))
			backImage = Team.fixPNG(Image.open(Team.directory+Team.iconDirectory+"blank.png"), currColor).resize((Team.iconSize,Team.iconSize))
			Team.addFrontText(mon, thisImage, currColor)
			Team.addBackText(mon, backImage, currColor)
			thisImage = thisImage.rotate(curr_rotation, expand=1)
			backImage = backImage.rotate(curr_rotation*-1, expand=1)
			Team.images.append(thisImage)
			Team.backImages.append(backImage)
				
		heights, widths = zip(*(i.size for i in Team.images))

		height_diff = int(max(heights))-Team.iconSize
		width_diff = int(max(widths))-Team.iconSize
		width_diff = int(max(widths))-Team.iconSize

		new_im_front = Image.new('RGB', (Team.iconSize*Team.horiz+width_diff+Team.border*(Team.horiz+1), Team.iconSize*Team.vert+height_diff+Team.border*(Team.vert+1)),color=(255,255,255,0)) #+200
		new_im_back = Image.new('RGB', (Team.iconSize*Team.horiz+width_diff+Team.border*(Team.horiz+1), Team.iconSize*Team.vert+height_diff+Team.border*(Team.vert+1)),color=(255,255,255,0)) #+200

		x_offset = 0
		y_offset = 0
		for im in enumerate(Team.images):
			if im[0] > 0 and im[0]%Team.horiz == 0:
				y_offset += Team.iconSize
				x_offset = 0
			#x_offset = offset for each 512px image
			#xyoffsets = additional offset for increased size of each ROTATED image
			#height_diff = additional offset for increased size of entire image
			new_im_front.paste(im[1], (x_offset+(int(im[0]%Team.horiz*Team.border))-Team.xyoffsets[im[0]]+int(height_diff/2),y_offset+(int(im[0]/2)*Team.border)-Team.xyoffsets[im[0]]+int(width_diff/2)), mask=im[1])
			new_im_back.paste(Team.backImages[im[0]], (x_offset+(int(im[0]%Team.horiz*Team.border))-Team.xyoffsets[im[0]]+int(height_diff/2),y_offset+(int(im[0]/2)*Team.border)-Team.xyoffsets[im[0]]+int(width_diff/2)), mask=Team.backImages[im[0]])
			x_offset += Team.iconSize

		x_offset = 0
		#for im in images:
		#	new_im_front.paste(im, (x_offset,0))	
		#	x_offset += im.size[0]
			
		Team.resultTweet = ""

		#set up tweet and also image	
		count = 0;	
		for mon in MasterMons:
			firstTypeEmoji = Team.typeEmojis[mon.type_a]
			secondTypeEmoji = ""
			if mon.type_b != None:
				secondTypeEmoji = Team.typeEmojis[mon.type_b]
			Team.resultTweet+=("✨" if mon.shiny else "") + "#"+re.sub(r'\W+', '', mon.name) +" "+firstTypeEmoji+secondTypeEmoji+"\n"
			
			#if mon.forms or mon.shiny:
			#	formHeight = 30
			#else:
			#	formHeight = 0;
			
			#Add text to the image!
			#draw = ImageDraw.Draw(new_im_front)
			#font = ImageFont.truetype(directory+'Roboto-Bold.ttf', size=40)
			#(x, y) = (0 + (400 * count) - (1200 if count > 2 else 0), 100-formHeight + (900+formHeight if count > 2 else 1))
			#message = mon.name
			#color = 'rgb(0, 0, 0)' # black color
			#draw.text((x, y), message, fill=color, font=font)
			
			#if mon.forms or mon.shiny:
			#	both = (" " if mon.forms and mon.shiny else "")
			#	font = ImageFont.truetype(directory+'Roboto-Light.ttf', size=20)
			#	(x, y) = (0 + (400 * count) - (1200 if count > 2 else 0), 150-formHeight + (900+formHeight if count > 2 else 1))
			#	message = " (" + ("Shiny" if mon.shiny else "") + both + (mon.form_name if mon.forms else "") +")"
			#	color = 'rgb(0, 0, 0)' # black color
			#	draw.text((x, y), message, fill=color, font=font)
			
			#font = ImageFont.truetype(directory+'Roboto-Medium.ttf', size=30)
			#(x, y) = (0 + (400 * count) - (1200 if count > 2 else 0), 150 + (900 + formHeight if count > 2 else 1))
			#message = "Ability: " + mon.ability
			#color = 'rgb(0, 0, 0)' # black color
			#draw.text((x, y), message, fill=color, font=font)
			#count+=1
		new_im_front.save(Team.directory+Team.resultFront)
		new_im_back.save(Team.directory+Team.resultBack)
				
		teamWeak = {k: v for k, v in sorted(teamWeak.items(), key=lambda item: item[1], reverse=True)}
		teamResist = {k: v for k, v in sorted(teamResist.items(), key=lambda item: item[1], reverse=True)}
		teamImmunity = {k: v for k, v in sorted(teamImmunity.items(), key=lambda item: item[1], reverse=True)}
		Team.resultTweet += "😎: "
		for resistKey, resistVal in teamResist.items():
			Team.resultTweet += Team.typeEmojis[resistKey]
			if resistVal > 1:
				Team.resultTweet += "x " + str(resistVal)
			#if resistVal > 1:
			#	under = 2**resistVal
			#	if under == 2:
			#		Team.resultTweet += "x½"
			#	elif under == 4:
			#		Team.resultTweet += "x¼"
			#	elif under == 8:
			#		Team.resultTweet += "x⅛ "
			#	else:
			#		Team.resultTweet += ("x 1/" + str(under))
			Team.resultTweet += ", "
		Team.resultTweet = Team.resultTweet[:-2]
		Team.resultTweet += "\n😱: "
		for weakKey, weakVal in teamWeak.items():
			Team.resultTweet += Team.typeEmojis[weakKey]
			if weakVal > 1:
				Team.resultTweet += "x" + str(weakVal)#str(2**weakVal)
			Team.resultTweet += ", "
		Team.resultTweet = Team.resultTweet[:-2]
		if len(teamImmunity) > 0:
			Team.resultTweet += "\n🚫: "
			for immuneKey, immuneVal in teamImmunity.items():
				Team.resultTweet += Team.typeEmojis[immuneKey]
				if immuneVal > 1:
					Team.resultTweet += "x" + str(immuneVal)
				Team.resultTweet += ", "
			Team.resultTweet = Team.resultTweet[:-2]

		Team.resultTweet += "\n\n#Pokémon #RandomTeamGenerator"

		if not userTweet:
			Team.resultTweet = 'Tweet "@RandPokeTeamBot team me" to get a team!\n\n'+Team.resultTweet

		if Team.userTweet:
			Team.tweetOut(userTweet=Team.userTweet, testing=test)
		else:
			Team.tweetOut(testing=test)
			
		print("Success")
	
