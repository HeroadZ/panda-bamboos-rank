
import pickle
import os.path
import requests
from datetime import datetime
from pymongo import MongoClient

#得到推荐前20的房间号
def getTop20List():
	top20List = []
	prefix = "http://static.api.m.panda.tv/android_hd/alllist_.json?pageno="
	for i in range(1,3):
		info  = ((requests.get(prefix + str(i))).json())["data"]["items"]
		[top20List.append(data_id["id"]) for data_id in info]
	return top20List

#得到该房间的主播id和竹子
def getBambooAndName(roomNumberList):
	roomInfoList = []
	prefix = "http://www.panda.tv/api_room_v2?roomid="
	for u in roomNumberList:
		singleRoom = []
		singleRoom.append(u)
		info = (requests.get(prefix + str(u))).json()
		if(info):
			print(info['data']['hostinfo']['name'])
			singleRoom.append(info['data']['hostinfo']['name'])
			singleRoom.append(round(int(info['data']['hostinfo']['bamboos'])/1e6, 2))
		else:
			singleRoom.append(["none", "none"])
			print("not get")
		roomInfoList.append(singleRoom)				
	return roomInfoList


#记录爬取的房间号
def recordRoomList(roomNumberList):
	with open('roomList.pickle', 'wb') as f:
		pickle.dump(roomNumberList, f)

#读取文件中的房间号
def readRoomList():
	with open('roomList.pickle', 'rb') as f:
  		roomNumberList = pickle.load(f)
	return roomNumberList


#增量判断
def incrementRoom(roomNumberList):
	if(not os.path.isfile("roomList.pickle")):
		recordRoomList(roomNumberList)
		return roomNumberList
	existRoomList = readRoomList()
	for item in roomNumberList:
		if(item in existRoomList):
			continue
		else:
			existRoomList.append(item)
	recordRoomList(existRoomList)
	return existRoomList

#获取字典形式
def getDict(roomInfoList):
	roomInfoDict = {}
	for item in roomInfoList:
		singleRoom = {"name": item[1], "bamboos": item[2], "date": datetime.utcnow()}
		roomInfoDict["room" + str(item[0])] = singleRoom
	return roomInfoDict

#存储到mongodb
def saveToMongo(roomInfoDict):
	client = MongoClient()
	db = client.pandaTV
	for k,v in roomInfoDict.items():
		collection = db[k]
		collection.insert(v)
	client.close()

def main():
	top20List = getTop20List()
	HotList = incrementRoom(top20List)
	roomInfoList = getBambooAndName(HotList)
	roomInfoDict = getDict(roomInfoList)
	saveToMongo(roomInfoDict)
	print(str(datetime.now()) + " done!")


if __name__ == '__main__':
	main()