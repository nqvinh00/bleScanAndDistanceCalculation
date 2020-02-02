import bluetooth
from bluetooth.ble import BeaconService
import pygame
pygame.init()
windows = pygame.display.set_mode((900, 600))
font = pygame.font.Font('freesansbold.ttf', 12)
service = BeaconService("hci0")
devices = service.scan(2)
nearby_devices = bluetooth.discover_devices(lookup_names=True)
position = [(40, 40), (-1, -1), (-1, -1)]

class BlePoint(object):
    def __init__(self, addr, name, position): #replace name with data with ble
        self.blePoint = addr + name
        self.position = position
        self.radius = 10
        # self.uuid = data[0]
        # self.major = data[1]
        # self.minor = data[2]
        # self.power = data[3]
        # self.rssi = data[4]
        # self.txPower = #need check with data[3] - power

    def distanceCalculation(self):
        pass

    def convert(self, distance):
        return round(int(distance) * 37.7952755906)
    # real pixel distance = the return number / 0.01, fixed for fit the win screen

    def draw(self, windows):
        # distance = self.distanceCalculation()
        # pixelDistance = self.convert(distance)
        pygame.draw.circle(windows, (255, 0, 0), self.position, 6)
        text = font.render(self.blePoint, True, (255, 255, 255))
        windows.blit(text, (self.position[0], self.position[1] + 15))
        pygame.draw.circle(windows, (255, 255, 255), self.position, 148, 1)


def drawWindows():
    pygame.draw.rect(windows, (0, 255, 0), (0, 0, 900, 600), 3)
    for ble in blePoints:
        ble.draw(windows)
    pygame.display.update()

blePoints = []
i = 0
for addr, name in nearby_devices:
    ble = BlePoint(addr, name, position[i])
    blePoints.append(ble)
    i += 1
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    drawWindows()
pygame.quit()
        
