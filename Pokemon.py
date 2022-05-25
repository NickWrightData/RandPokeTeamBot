#IDEAS FOR APRIL FOOL'S:
#COMPLETELY random:
#-levels
#-shininess
#-abilities
#-moves
#-image rotation (subtle = around 90 deg angles, non-subtle = anything within 360 degrees
#-typings

from postgres import postgres
import random			#for selecing random pokémon, forms (.................)
import os

class Pokemon:
	
	allPokemon = 890 + 1 #893 Pokémon, plus 1 so that the last one can be selected
	shinyOdds = 8192 + 1 #See above
	directory = r'C:\Users\PC\Desktop\twitterBots\pokemonTeams\\'
	subdirectory = '\HOME\\'
	
	dex_id = -1
	dex_id_string = "-1"
	name = "default"
	form_name = "nothing"
	twitter_name = "default"
	image = "nothing.png"
	type_a = "nothing"
	type_b = "nothing"
	forms = False
	gend_diff = False
	gend_ratio = -1
	gender = "None"
	cherish_only = False
	poke_only = False
	level = 1;
	min_lvl = 1;
	move_1 = "Nothing"
	move_2 = "Nothing"
	move_3 = "Nothing"
	move_4 = "Nothing"

	
	form_id = -10000
	weaknesses = {}
	resistances = {}
	immunities = {}
	ability = "nothing"
	
	shiny = False	
	
	#Not implemented yet
	
	teamWeaknesses = {}
	teamResistances = {}
	teamImmunities = {}
	
	weaknessesQuery = """SELECT type_id, weaknesses
						FROM ((
							SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as weaknesses
							FROM pkmn
							JOIN weaknesses ON pkmn.type_a = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 2 AND pkmn.id = %s
							EXCEPT (SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as weaknesses
								FROM pkmn JOIN weaknesses ON pkmn.type_b = weaknesses.defending_type
								JOIN types ON attacking_type = types.type_id
								WHERE weaknesses.multiplier = 0.5 OR weaknesses.multiplier = 0)
						) UNION ALL (
							SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as weaknesses
							FROM pkmn
							JOIN weaknesses ON pkmn.type_b = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 2 AND pkmn.id = %s
							EXCEPT (SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as weaknesses
								FROM pkmn JOIN weaknesses ON pkmn.type_a = weaknesses.defending_type
								JOIN types ON attacking_type = types.type_id
								WHERE weaknesses.multiplier = 0.5 OR weaknesses.multiplier = 0)
						)) foo"""
			
	resistancesQuery = """SELECT type_id, resistances
						FROM ((
							SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as resistances
							FROM pkmn
							JOIN weaknesses ON pkmn.type_a = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 0.5 AND pkmn.id = %s
							EXCEPT (SELECT pkmn.id, pkmn.name, types.type_id AS resistance_id, types.name as weaknesses
								FROM pkmn JOIN weaknesses ON pkmn.type_b = weaknesses.defending_type
								JOIN types ON attacking_type = types.type_id
								WHERE weaknesses.multiplier = 2 OR weaknesses.multiplier = 0)
						) UNION ALL (
							SELECT pkmn.id, pkmn.name, types.type_id AS type_id, types.name as resistances
							FROM pkmn
							JOIN weaknesses ON pkmn.type_b = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 0.5 AND pkmn.id = %s
							EXCEPT (SELECT pkmn.id, pkmn.name, types.type_id AS resistance_id, types.name as weaknesses
								FROM pkmn JOIN weaknesses ON pkmn.type_a = weaknesses.defending_type
								JOIN types ON attacking_type = types.type_id
								WHERE weaknesses.multiplier = 2 OR weaknesses.multiplier = 0)
						)) foo"""
						
	immunitiesQuery = """SELECT type_id, type_name
						FROM ((
							SELECT pkmn.id, pkmn.name, types.type_id as type_id, types.name as type_name
							FROM pkmn
							JOIN weaknesses ON pkmn.type_a = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 0 AND pkmn.id = %s
						) UNION ALL (
							SELECT pkmn.id, pkmn.name, types.type_id as type_id, types.name as type_name
							FROM pkmn
							JOIN weaknesses ON pkmn.type_b = weaknesses.defending_type
							JOIN types ON attacking_type = types.type_id
							WHERE weaknesses.multiplier = 0 AND pkmn.id = %s
						)) foo"""
						
	def resetAll():
		Pokemon.dex_id = -1
		Pokemon.dex_id_string = "-1"
		Pokemon.name = "default"
		Pokemon.form_name = "nothing"
		Pokemon.twitter_name = "default"
		Pokemon.image = "nothing.png"
		Pokemon.type_a = "nothing"
		Pokemon.type_b = "nothing"
		Pokemon.forms = False
		Pokemon.gend_diff = False
		Pokemon.gend_ratio = -1
		Pokemon.gender = "None"
		Pokemon.cherish_only = False
		Pokemon.poke_only = False
		Pokemon.level = 1;
		Pokemon.min_lvl = 1;
		Pokemon.move_1 = "Nothing"
		Pokemon.move_2 = "Nothing"
		Pokemon.move_3 = "Nothing"
		Pokemon.move_4 = "Nothing"
		Pokemon.form_id = -10000
		Pokemon.weaknesses = {}
		Pokemon.resistances = {}
		Pokemon.immunities = {}
		Pokemon.ability = "nothing"
		Pokemon.shiny = False
		Pokemon.teamWeaknesses = {}
		Pokemon.teamResistances = {}
		Pokemon.teamImmunities = {}
						
	def getRandomMoveset(self):
		return postgres.runQuery("""SELECT name
									FROM moves
									ORDER BY RANDOM() LIMIT 4""")
	
	def getAllAbilityResWeak(self, ability):
		return postgres.runQuery("""SELECT tp1.name, tp2.name, tp3.name
							FROM abilities ab
							LEFT JOIN types tp1 ON ab.resist = tp1.type_id
							LEFT JOIN types tp2 ON ab.weakness = tp2.type_id
							LEFT JOIN types tp3 ON ab.immunity = tp3.type_id
							WHERE ab.name = %s""", [ability]);
	
	def getRandomAbility(self, pkmn):
		result = postgres.runQuery("""SELECT ab1.name, ab2.name, ab3.name
					FROM pkmn
					LEFT JOIN abilities ab1 ON ability_1 = ab1.id
					LEFT JOIN abilities ab2 ON ability_2 = ab2.id
					LEFT JOIN abilities ab3 ON hidden_ability = ab3.id
					WHERE pkmn.id = %s""", [pkmn])[0]
					
		result = [x for x in result if x != None]
		return random.choice(result)
	
	def addWeakness(self, name):
		if name not in self.immunities:
			if name in self.weaknesses:
				self.weaknesses[name]+=1
			else:
				self.weaknesses[name]=1
			
			#add team weakness
			if name in self.teamResistances:
				self.teamResistances[name] -= 1;
				if self.teamResistances[name] == 0:
					self.teamResistances.pop(name)
			elif name in self.teamWeaknesses:
				self.teamWeaknesses[name] += 1;
			else:
				self.teamWeaknesses[name] = 1;
	
	def addResistance(self, name):
		if name not in self.immunities:
			if name in self.resistances:
				self.resistances[name]+=1
			else:
				self.resistances[name]=1
			
			#add team resistance	
			if name in self.teamWeaknesses and self.teamWeaknesses[name] > 0:
				self.teamWeaknesses[name] -= 1
				if self.teamWeaknesses[name] == 0:
					self.teamWeaknesses.pop(name)
			elif name in self.teamResistances:
				self.teamResistances[name] += 1
			else:
				self.teamResistances[name] = 1
			
	def addImmunity(self, name):
		if name in self.immunities:
			self.immunities[name]+=1
		else:
			self.immunities[name]=1
		if name in self.resistances:
			self.resistances.pop(name)
			self.teamResistances.pop(name)
		if name in self.weaknesses:
			self.weaknesses.pop(name)
			self.teamWeaknesses.pop(name)
			
		#add team immunity
		if name in self.teamImmunities:
			self.teamImmunities[name] += 1
		else:
			self.teamImmunities[name] = 1
	
	def monNumZeroes(self, monnum):
		if monnum < 10:
			return "00"+str(monnum)
		elif monnum < 100:
			return "0"+str(monnum)
		else:
			return str(monnum)
			
	def calcGendDiffs(self):
		imageCheck = self.image[:-4]
		
		femcheck = imageCheck + "f.png" in os.listdir(self.directory+self.subdirectory)
		malecheck = imageCheck + "m.png" in os.listdir(self.directory+self.subdirectory)
		
		flip = random.choice(range(1,9))
		
		if self.gend_ratio == -1:
			gen = "Genderless"
		elif flip <= self.gend_ratio:
			gen = "Male"
			if malecheck:
				self.image = imageCheck + "m.png"
		else:
			gen = "Female"
			if femcheck:
				self.image = imageCheck + "f.png"
			
		self.gender = gen
			
	#def printAll(self):
	#	print(self.dex_id)
	#	print(self.name)
	#	print(self.twitter_name)
	#	print(self.image)
	#	print(self.type_a)
	#	print(self.type_b)
	#	print(self.form_id)
	#	print(self.weaknesses)
	#	print(self.defenses)
	#	print(self.ability)
	#	print(self.shiny)
	
	def __init__(self, id = -1, regionText = "", typeText = "", FEtext = ""):
	
		self.weaknesses = {}
		self.resistances = {}
		self.immunities = {}
		
		#Choose the id!
		#print("Selecting Pokémon Dex ID...")
		if id != -1:
		#	print(id)
			self.dex_id = id
		else:
			self.dex_id = random.choice(range(1,self.allPokemon))
		
		#Get the general data (name, typings...etc)
		#print("Selecting Data...")
		[self.name, self.form_name, self.twitter_name, self.image, self.type_a, self.type_b, self.forms, self.gend_diff, self.gend_ratio, self.cherish_only, self.poke_only, self.min_lvl] = postgres.runQuery("""
								SELECT name, form_name_addition, twitter_name, image, type_a, type_b, forms, gender_diffs, gender_ratio, cherish_only, poke_only, min_lvl
								FROM pkmn
								WHERE id = %s"""+regionText+typeText+FEtext, [self.dex_id])[0];
		
		#We'll need to pick a random form if this id has them, and re-pull that form's data
		if self.forms:
			#print("Selecting Forms...")
			formList = [random.choice(postgres.runQuery("""
							SELECT id, name, form_name_addition, twitter_name, image, type_a, type_b, gender_diffs, gender_ratio, cherish_only, poke_only, min_lvl
							FROM pkmn
							WHERE (form_of = %s
							OR id = %s)"""+regionText+typeText+FEtext, [self.dex_id, self.dex_id]))]
			[self.form_id, self.name, self.form_name, self.twitter_name, self.image, self.type_a, self.type_b, self.gend_diff, self.gend_ratio, self.cherish_only, self.poke_only, self.min_lvl] = random.choice(formList)
		else:
			self.form_id = self.dex_id
		
		self.dex_id_string = self.monNumZeroes(self.dex_id)
		
		#print("Selecting Gender...")
		self.calcGendDiffs()
		
		#Get Level!
		#print("Selecting Level...")
		self.level = random.choice(range(self.min_lvl,101))		
		
		#Check Shiny
		#print("Shiny Check!")
		shinyCheck = random.choice(range(1,self.shinyOdds))
		if shinyCheck == 1 and self.dex_id <= 890:
			#print("SHINYYYYYYYYYYYYYYYYYYY")
			self.shiny = True;
			if self.image[-4:] == ".png":
				self.image = self.image[:-4] + "s" + ".png"
		
		#Get Ability
		#print("Selecting Ability...")
		self.ability = self.getRandomAbility(self.form_id)
		resweakimm = self.getAllAbilityResWeak(self.ability)[0]
		if resweakimm[0]:
			#print("WEAKNESS!")
			self.addResistance(resweakimm[0]);
		if resweakimm[1]:
			#print("RESISTANCE!")
			self.addWeakness(resweakimm[1]);
		if resweakimm[2]:
			#print("IMMUNITY!")
			self.addImmunity(resweakimm[2]);
		
		if resweakimm[0] is None and resweakimm[1] is None and resweakimm[2] is None:
			if self.ability == "Thick Fat":
				#print("thick fat!")
				self.addResistance("Fire")
				self.addResistance("Ice")
			if self.ability == "Wonder Guard":
				#print("WONDER GUARD!")
				self.addImmunity("Water")
				self.addImmunity("Electric")
				self.addImmunity("Grass")
				self.addImmunity("Ice")
				self.addImmunity("Poison")
				self.addImmunity("Ground")
				self.addImmunity("Psychic")
				self.addImmunity("Bug")
				self.addImmunity("Dragon")
				self.addImmunity("Steel")
				self.addImmunity("Fairy")
		
		#print("Getting weaknesses/resistances/immunities...")
		#Get the weaknesses based on type(s) (Using name, not id at the present time)
		result = postgres.runQuery(self.weaknessesQuery, [self.form_id, self.form_id])
		
		for weakness in result:
			self.addWeakness(weakness[1])
		
		#Get the resistances based on type(s)
		result = postgres.runQuery(self.resistancesQuery, [self.form_id, self.form_id])
		
		for resistance in result:
			self.addResistance(resistance[1])
		
		#Get the immunities based on type(s)
		result = postgres.runQuery(self.immunitiesQuery, [self.form_id, self.form_id])
		
		for immunity in result:
			#This is just a formality; no two defending types have the same immunities;
			#or put it another way, no attacking type is ineffective to two types.
			self.addImmunity(immunity[1])
		#self.printAll()
		
		[self.move_1, self.move_2, self.move_3, self.move_4] = self.getRandomMoveset()
		self.move_1 = self.move_1[0]
		self.move_2 = self.move_2[0]
		self.move_3 = self.move_3[0]
		self.move_4 = self.move_4[0]
		
		#postgres.runQuery("""SELECT name, type_a, type_b, image, 
		#							FROM pkmn
		#							WHERE id = %s 
		#								OR form_of = %s""", [self.dex_id, self.dex_id]);
		
		
		#if result[0][5]:
		#	formNames.append(result[0][12])
		#else:
		#	formNames.append(" ")
		