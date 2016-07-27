import pickle

def readRoomList():
	with open('roomList.pickle', 'rb') as f:
  		roomNumberList = pickle.load(f)
	f.close()
	return roomNumberList

a = readRoomList()
print(a)

