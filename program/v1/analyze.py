
from pymongo import MongoClient
import json
import time

def writeJsonFile(data,filename):
	with open(filename+".json", 'w') as f:
  		json.dump(data, f)

def get20Rank(db):
	bamboosList = []
	nameList = []
	rankDict = {}
	mycollections = db.collection_names()
	for item in mycollections:
		latest = db[item].find().sort('date',-1)[0]
		bamboosList.append(latest["bamboos"])
		nameList.append(latest["name"])
	bamboosList, nameList = zip(*sorted(zip(bamboosList, nameList), reverse=True))
	rankDict["name"] = nameList[0:19]
	rankDict["bamboos"] = bamboosList[0:19]
	writeJsonFile(rankDict, "bamboos_rank")

def main():
	client = MongoClient()
	db = client.pandaTV
	get20Rank(db)
	client.close()


if __name__ == '__main__':
	main()