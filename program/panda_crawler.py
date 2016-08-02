
import csv
import pickle
import os.path
import requests
import grequests
from operator import itemgetter

#最大线程数为10
MaxWorkers = 5

def exception_handler(request, exception):
	print("Request failed")

#得到推荐前100的房间号
def getTop100List():
	top100List = []
	prefix = "http://static.api.m.panda.tv/android_hd/alllist_.json?pageno="
	rs = (grequests.get(prefix + str(u)) for u in range(1,11))
	output = grequests.map(rs, exception_handler=exception_handler)
	for item in output:
		info = (item.json())["data"]["items"]
		[top100List.append(data_id["id"]) for data_id in info]
	return top100List

#控制最大线程数
def controlMaxWorkers(prefix, List):
	rs = (grequests.get(prefix + u) for u in List)
	output = grequests.map(rs, exception_handler=exception_handler) 
	return output

#得到该房间的主播id和竹子
def getBambooAndId(roomNumberList):
	idList = []
	bambooList = []
	prefix = "http://www.panda.tv/api_room?roomid="
	for u in ([roomNumberList[i:i+MaxWorkers] for i in range(0, len(roomNumberList), MaxWorkers)]):
		output = controlMaxWorkers(prefix, u)
		for item in output:
			if(item):
				info = item.json()
				print(info['data']['hostinfo']['name'])
				idList.append(info['data']['hostinfo']['name'])
				bambooList.append(round(int(info['data']['hostinfo']['bamboos'])/1e6, 2))
			else:
				idList.append("none")
				bambooList.append("none")
				print("not get ")				
	return idList, bambooList


#记录爬取的房间号
def recordRoomList(roomNumberList):
	with open('roomList.pickle', 'wb') as f:
		pickle.dump(roomNumberList, f)

#读取文件中的房间号
def readRoomList():
	with open('roomList.pickle', 'rb') as f:
  		roomNumberList = pickle.load(f)
	return roomNumberList

#保存为csv文件
def saveResult(result):
	with open('panda_bamboos_rank.csv', 'w+', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["主播id", "竹子数量单位(m)", "主播房间号"])
		writer.writerows(result)

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


def main():
	top100List = getTop100List()
	HotList = incrementRoom(top100List)
	idList, bambooList = getBambooAndId(HotList)
	mixed = sorted(zip(idList, bambooList, HotList), reverse = True, key = itemgetter(1))
	saveResult(mixed)

if __name__ == '__main__':
	main()