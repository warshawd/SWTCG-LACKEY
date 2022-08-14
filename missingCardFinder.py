import os
import io

sets = {"AOTC": 180, "SR": 90, "ANH": "A New Hope", "BOY": "Battle of Yavin", "JG": "Jedi Guardians", "ESB": "The Empire Strikes Back",
"RAS": "Rogues and Scoundrels", "PM": "The Phantom Menace", "ROTJ": "Return of the Jedi", "ROTS": "Revenge of the Sith", "FOTR": 120,
"SAV": 90, "BOE": 180, "RAW": 120, "ION": 180, "BOH": 60, "BH": 75, "MAND": 75, "SITH": "Legacy of the Force: Sith",
"SMUG": "Legacy of the Force: Smugglers", "JEDI": "Legacy of the Force: Jedi", "RO2": "Rule of Two",
"TOR": "The Old Republic", "CWSO": "The Clone Wars: Separatist Offensive", "RS": "Rogue Squadron", "ER": "Empire Rising", "EE": "Empire Eternal", "AGD": "The Clone Wars: A Galaxy Divided",
"TDT": "The Dark Times", "CAD": "Clones and Droids", "TFA": "The Force Awakens", "VP": "The New Jedi Order: Vector Prime", "TAL": "The Old Republic: Tales and Legends",
"SBS": "The New Jedi Order: Star by Star", "DAN": "The Old Republic: Days and Nights", "BL": "The Clone Wars: Battle Lines", "RO": "Rogue One",
"TEN": "Tenth Anniversary", "BOSB": "Battle of Starkiller Base", "TLJ": "The Last Jedi", "SOR": "Spark of Rebellion", "BF": "Battlefront", "JK": "Jedi Knight",
"TUF": "The New Jedi Order: The Unifying Force", "BOC": "Battle of Crait", "SOLO": "Solo: A Star Wars Story", "KAE": "The Old Republic: Knights and Exiles",
"TM": "The Mandalorian", "15TH": "15th Anniversary", "TROS": "The Rise of Skywalker", "AAA": "Apprentices and Assassins", "FOR": "Fires of Rebellion", 
"BOTS": "Battle of the Sarlacc", "TMW": "The Mandalorian Way"}

baseSetPath = "SWTCG-LACKEY/starwars/sets/"
# baseSetPath = "LackeyCCG/plugins/starwars/sets/"

missingCards = {}
allCards = {}

def constructSetFilePath(setCode):
  basePath = baseSetPath
  return basePath + setCode + ".txt"


def processULCard(imageFrag, currentSet, cards):
	# print(imageFrag)
	imagePath = baseSetPath + "setimages/" + currentSet + "/" + imageFrag
	if not os.path.exists(imagePath):
		missingCards[imageFrag] = "Image file doesn't exist in folder " + currentSet + ": " + imageFrag
		# print("imagePath is " + imagePath)

	slicedFrag = imageFrag[:-4]
	if slicedFrag not in cards.keys():
		missingCards[slicedFrag] = slicedFrag + " not found in " + currentSet + ".txt"
		# if currentSet == "TMW":
		# 	print("slicedFrag is " + slicedFrag)
	else:
		cards[slicedFrag] = False
	# print(cards)
	


def processSetFile(setCode):
	cards = {}
	with io.open(baseSetPath + setCode + ".txt", "r", encoding='cp1252') as setFile:
		firstLine = True
		for line in setFile:
			if firstLine:
				firstLine = False
				continue
			card = line.split('\t')
			name = card[0]
			imageFrag = card[2]
			# if imageFrag.startswith("TMW02"):
			# 	print(imageFrag)
			cards[imageFrag] = True
			if name in allCards.keys():
				print("Duplicate entry found for card: " + name)
			else:
				allCards[name] = True
	# if setCode == "ROTS":
	# 	print(cards)
	return cards


def processUpdateList():
	with io.open("SWTCG-LACKEY/starwars/updatelist.txt", "r", encoding='cp1252') as updateList:
	# with io.open("LackeyCCG/plugins/starwars/updatelist.txt", "r", encoding='cp1252') as updateList:
		counter = 0

		# Skip down to the actual cards
		for line in updateList:
			if not line.startswith("CardImageURLs:"):
				continue
			break


		currentSet = ""
		cards = {}
		for line in updateList:
			nextSet = line.partition('/')[0]
			imageLink = line.split('\t')[0].split('/')[1]
			if nextSet != currentSet:
				for key in cards.keys():
					if cards[key] == True:
						# print("key was true for " + key)
						missingCards[key] = key + " from set file " + currentSet + " had no corresponding updateList entry"
				currentSet = nextSet
				cards = processSetFile(currentSet)
			processULCard(imageLink, currentSet, cards)
		# for card in cards.keys():
		# 	if cards[card] == False:
		# 		print("Duplicate entry found for card: " + card)

def main():

  processUpdateList()
  for key in missingCards:
  	print(missingCards[key])

main()