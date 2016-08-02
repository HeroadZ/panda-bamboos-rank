
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import re
import time
import pickle
import os.path

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
		anchorUrl = "http://www.panda.tv/" + roomNumber
		driver.get(anchorUrl)
		time.sleep(0.5)
		try:
			anchorId = driver.find_element_by_css_selector("body .room-head-info-hostname").get_attribute("innerHTML")
			bamboos = driver.find_element_by_css_selector("body .room-bamboo-num").get_attribute("innerHTML")
		except NoSuchElementException:
			anchorId = "none"
			bamboos = "none"
			print("not found in " + roomNumber)
		idList.append(anchorId)
		bambooList.append(bamboos)
	return idList, bambooList

#将得到的竹子进行单位统一
def bambooRank(bambooList):
	bambooRankList = []
	for item in bambooList:
		multiFactor = 1000
		if('mm' in item):
			multiFactor = 1
		if(item == "none"):
			item = "0"
		tmp = re.findall('\d+[\.]?\d*', item)[0]
		bambooRankList.append(float(tmp) * multiFactor)
	return bambooRankList

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

def saveResult(result):
	with open('panda_bamboos_rank.csv', 'w+', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["竹子数量单位(mm)", "主播id", "主播房间号"])
		writer.writerows(result)
	f.closed

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
	driver.implicitly_wait(1)

	# maxPages = getMaxPages(driver)
	maxPages = 2
	roomNumberList = getAllRoom(maxPages, driver)
	roomNumberList = incrementRoom(roomNumberList)
	idList, bambooList = getBambooAndId(roomNumberList, driver)
	driver.close()

	bambooRankList = bambooRank(bambooList)
	mixed = sorted(zip(bambooRankList, idList, roomNumberList), reverse = True)
	saveResult(mixed)

if __name__ == '__main__':
	main()