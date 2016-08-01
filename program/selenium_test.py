
from selenium import webdriver
import csv
import time
import pickle
import os.path
import math
import requests

#得到正在直播的最大页数
def getMaxPages(driver):
	maxPages = driver.find_element_by_xpath('//*[@id="pages-container"]/div/div/a[7]').get_attribute("innerHTML")
	return int(maxPages)

#得到正在直播的所有房间号
def getAllRoom(maxPages, driver):
	roomNumberList = []
	for x in range(1, maxPages + 1):
		print("这是第" + str(x) + "页")
		singleList = driver.find_elements_by_xpath('//*[@id="later-play-list"]/li')
		for item in singleList:
			roomNumberList.append(item.get_attribute("data-id"))


		nextPage = driver.find_element_by_class_name("j-page-next")
		nextPage.click()
		time.sleep(1)
	return roomNumberList

#得到该房间的主播id和竹子
def getBambooAndId(roomNumberList, driver):
	idList = []
	bambooList = []
	for roomNumber in roomNumberList:
		url = "http://www.panda.tv/api_room?roomid=" + roomNumber
		print(roomNumber)
		info = (requests.get(url)).json()
		anchorId = info['data']['hostinfo']['name']
		bamboos = info['data']['hostinfo']['bamboos']
		idList.append(anchorId)
		bambooList.append(math.ceil(int(bamboos)/1000))
	return idList, bambooList


#记录爬取的房间号
def recordRoomList(roomNumberList):
	with open('roomList.pickle', 'wb') as f:
		pickle.dump(roomNumberList, f)
	f.close()

#读取文件中的房间号
def readRoomList():
	with open('roomList.pickle', 'rb') as f:
  		roomNumberList = pickle.load(f)
	f.close()
	return roomNumberList

#保存为csv文件
def saveResult(result):
	with open('panda_bamboos_rank.csv', 'w+', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["竹子数量单位(mm)", "主播id", "主播房间号"])
		writer.writerows(result)
	f.closed

#增量判断
def incrementRoom(roomNumberList):
	if(not os.path.isfile("roomList.pickle")):
		recordRoomList(roomNumberList)
		return
	existRoomList = readRoomList()
	for item in roomNumberList:
		if(item in existRoomList):
			continue
		else:
			existRoomList.append(item)
	recordRoomList(existRoomList)
	return existRoomList


def main():
	listUrl = "http://www.panda.tv/all"

	driver = webdriver.Chrome('chromedriver.exe')
	driver.get(listUrl)
	# maxPages = getMaxPages(driver)
	maxPages = 2
	roomNumberList = getAllRoom(maxPages, driver)
	driver.close()

	roomNumberList = incrementRoom(roomNumberList)
	idList, bambooList = getBambooAndId(roomNumberList, driver)

	mixed = sorted(zip(bambooList, idList, roomNumberList), reverse = True)
	saveResult(mixed)
	print("done")

if __name__ == '__main__':
	main()