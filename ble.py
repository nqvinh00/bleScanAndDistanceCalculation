from bluepy.btle import Scanner, DefaultDelegate
import pygame
import numpy as np
from math import pow

pygame.init()
windows = pygame.display.set_mode((900, 600))
pygame.display.set_caption("BLE Scan")
font = pygame.font.Font('freesansbold.ttf', 12)
beaconPositions = {"42:41:41:41:41:41":(40, 40), "43:41:41:41:41:41":(800, 400), "44:41:41:41:41:41":(400, 0)}
beacons = []
run = True

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass

class Beacon(object):
    def __init__(self, addr, rssi, position):
        self.addr = addr
        self.rssi = rssi
        self.position = position
        self.txPower = 65

    def distanceCalculation(self):
        x = (self.rssi + self.txPower) / -40
        return pow(10, x)

    def convert(self, distance):
        return round(distance * 37.7952755906)

class Position(object):
    def __init__(self, beacons):
        self.xy = []
        self.distance = []

    def positionCalculation(self):
        d = []
        for i in beacons:
            dis = i.distanceCalculation()
            d.append(i.convert(dis))

        for i in range(len(beacons) - 1):
            self.xy.append([beacons[i + 1].position[0] - beacons[i].position[0], beacons[i + 1].position[1] - beacons[i].position[1]])
        for i in range(len(beacons) - 1):
            self.distance.append((d[i] * 2 - d[i + 1] * 2 - beacons[i].position[0] * 2 + beacons[i + 1].position[0] * 2 - beacons[i].position[1] * 2 + beacons[i + 1].position[1] * 2) / 2)   
        distance = np.asarray(self.distance)
        xy = np.asarray(self.xy)
        #print(distance)
        #print(xy)
        result = np.linalg.lstsq(xy, distance, rcond = None)[0].astype(int)
        return result

    def draw(self, windows):
        xy = self.positionCalculation()
        pygame.draw.circle(windows, (255, 0, 0), (xy[0], xy[1]), 6)
        text = font.render("Your position", True, (255, 255, 255))
        windows.blit(text, (xy[0], xy[1] + 15))

def rssiAverage(rssi, end):
    return sum(rssi[0:end]) / end

def smoothingRSSI(rssi, average):
    return rssi * 0.1 + average * 0.9

def drawWindow():
    pygame.draw.rect(windows, (0, 255, 0), (0, 0, 900, 600), 3)
    pygame.display.update()

rssi = {"42:41:41:41:41:41":[], "43:41:41:41:41:41":[], "44:41:41:41:41:41":[]}
macList = list(rssi.keys())
for i in range(5):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(3)
    for dev in devices:
        if dev.addr in beaconPositions:
            rssi[dev.addr].append(dev.rssi)

rssi_ = []
for i in rssi:
    if len(rssi[i]) != 0:
        rssi_.append(rssi[i])
rssi_smooth = [rssi_[i][0] for i in range(len(rssi_))]
for i in range(len(rssi_)):
    for end in range(2, len(rssi_[i]) + 1):
        rssi_smooth[i] = smoothingRSSI(rssi_smooth[i], rssiAverage(rssi_[i], end))
for i in range(len(rssi_)):
    beacon = Beacon(macList[i], rssi_smooth[i], beaconPositions[macList[i]])
    beacons.append(beacon)

pos = Position(beacons)
drawWindow()
pos.draw(windows)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()


from bluepy.blte import Scanner, DefaultDelegate
import pygame
import numpy as np
from math import pow

pygame.init()
windows = pygame.display.set_mode((900, 600))
pygame.display.set_caption("BLE Scan")
font = pygame.font.Font('freesansbold.ttf', 12)
beaconPositions = {"42:41:41:41:41:41":(40, 40, 50), "43:41:41:41:41:41":(800, 400, 50), "44:41:41:41:41:41":(400, 0, 50), "45:41:41:41:41:41":(400, 0, 164)}
beacons = []
floor_height_in_pixel = 114
run = True

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		pass

class Beacon(object):
	def __init__(self, addr, rssi, position):
		self.addr = addr
		self.rssi = rssi
		self.position = position
		self.txPower = 65

	def distanceCalculation(self):
		x = (self.rssi + self.txPower) / -40
		return pow(10, x)

	def convert(self, distance):
		return round(distance * 37.7952755906)

class Position(object):
	def __init__(self, beacons):
		self.xyz = []
		self.distance = []

	def positionCalculation(self):
		d = []
		for i in beacons:
			dis = i.distanceCalculation()
			d.append(i.convert(dis))

		for i in range(len(beacons) - 1):
			self.xyz.append([beacons[i + 1].position[0] - beacons[i].position[0], beacons[i + 1].position[1] - beacons[i].position[1], beacons[i + 1].position[2] - beacons[i].position[2]])
		for i in range(len(beacons) - 1):
			self.distance.append((d[i] * 2 - d[i + 1] * 2 - beacons[i].position[0] * 2 + beacons[i + 1].position[0] * 2 - beacons[i].position[1] * 2 + beacons[i + 1].position[1] * 2 - beacons[i].position[2] * 2 + beacons[i + 1].position[2] * 2) / 2)
		distance = np.asarray(self.distance)
		xyz = np.asarray(self.xyz)
		result = np.linalg.lstsq(xyz, d, rcond = None)[0].astype(int)
		return result

	def draw(self, windows):
		xyz = self.positionCalculation()
		floor = xyz[2] // floor_height_in_pixel + 1
		floor = "Floor" + str(floort)
		pygame.draw.circle(windows, (255, 0, 0), (xy[0], xy[1]), 6)
		text1 = font.render(floor, True, (255, 255, 255))
		text2 = font.render("Your position", True, (255, 255, 255))
		windows.blit(text1, (850, 10))
		windows.blit(text2, (xy[0], xy[1] + 15))

def rssiAverage(rssi, end):
	return sum(rssi[0:end]) / end

def smoothingRSSI(rssi, average):
	return rssi * 0.1 + average * 0.9

def drawWindow():
	pygame.draw.rect(windows, (0, 255, 0), (0, 0, 900, 600), 3)
	pygame.display.update()

rssi = {"42:41:41:41:41:41":[], "43:41:41:41:41:41":[], "44:41:41:41:41:41":[]}
macList = list(rssi.keys())
for i in range(5):
	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(3)
	for dev in devices:
		if dev.addr in beaconPositions:
			rssi[dev.addr].append(dev.rssi)

rssi_ = []
for i in rssi:
	if len(rssi[i]) != 0:
		rssi_.append(rssi[i])
rssi_smooth = [rssi_[i][0] for i in range(len(rssi_))]
for i in range(len(rssi_)):
	for end in range(2, len(rssi_[i]) + 1):
		rssi_smooth[i] = smoothingRSSI(rssi_smooth[i], rssiAverage(rssi_[i], end))
for i in range(len(rssi_)):
	beacon = Beacon(macList[i], rssi_smooth[i], beaconPositions[macList[i]])
	beacons.append(beacon)

pos = Position(beacons)
drawWindow()
pos.draw(windows)
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
pygame.quit()
