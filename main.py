from random import randint
import math
import cv2

def read():
	f = open("coords.dat", "r")
	ret = f.readlines()
	f.close()
	ter = []
	for i in range(len(ret)):
		ret[i] = ret[i][0:-1]
		ret[i] = ret[i].split(", ")
		ret[i] = ret[i][0:-1]
		for j in range(len(ret[i])):
			ter.append(int(ret[i][j]))

	return ter

def recognizeHand():
	global sortCoords, razmersImage, pixelRazmers
	hand = read()
	razmersHand = [9, 15]
	razmersImage = [31, 23]
	minRaz = 0
	result = []
	for k in range(1000): # качество распознования
		sortPhoto = []

		xPoint = randint(0, razmersImage[0]-razmersHand[0]-1)
		yPoint = randint(0, razmersImage[1]-razmersHand[1]-1)

		points = [[xPoint, xPoint+razmersHand[0]], [yPoint, yPoint+razmersHand[1]]]

		# кусок изображения
		for i in range(points[1][0], points[1][1]):
			for j in range(points[0][0], points[0][1]):
				sortPhoto.append(sortCoords[i][j])

		# вычисление разницы
		mainRaz = 0

		for i in range(0, len(sortPhoto)):
			if sortPhoto[i]!=hand[i]:
				mainRaz += 1

		if minRaz==0 or mainRaz<minRaz:
			minRaz = mainRaz
			result = [xPoint*20, yPoint*20]

	if minRaz>45:
		result = [0, 0]

	return result

def getSortCoords(coords):
	sort = []
	for i in range(20, len(coords), 20):
		sort.append([])
		for j in range(20, len(coords[i]), 20):
			actives = 0

			for k in range(i-20, i):
				actives += sum(coords[k][j-20:j])//255

			if actives>17:
				sort[-1].append(1)
			else:
				sort[-1].append(0)

	return sort

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while 1:
	succes, cr = cap.read()
	coords = cv2.Canny(cr, 100, 100)

	sortCoords = getSortCoords(coords)

	x, y = recognizeHand()

	if x!=0:
		cv2.rectangle(cr, (x, y), (x+20*9, y+20*15), (0, 255, 0), 2)

	cv2.imshow("image",cr)

	if cv2.waitKey(1) & 0xFF==ord('q'):
		break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()