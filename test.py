import bluetooth
import pygame
pygame.init()
windows = pygame.display.set_mode((900, 600))
font = pygame.font.Font('freesansbold.ttf', 12)
nearby_devices = bluetooth.discover_devices(lookup_names=True)
position = [(40, 40), (-1, -1), (-1, -1)]

class BlePoint(object):
    def __init__(self, addr, name, position):
        self.blePoint = addr + name
        self.position = position
        self.radius = 10
        # self.txPower = 
        # self.rssi = 

    # def distanceCalculation(self):

    # def convert(self, distance):
    #     return round(distance * 37.7952755906)
    # # real pixel distance = the return number / 0.01, fixed for fit the win screen

    def draw(self, windows):
        # distance = self.distanceCalculation()
        # pixelDistance = self.convert(distance)
        pygame.draw.circle(windows, (255, 0, 0), self.position, 6)
        text = font.render(self.blePoint, True, (255, 255, 255))
        windows.blit(text, (self.position[0], self.position[1] + 15))
        # pygame.draw.circle(windows, (255, 255, 255), self.position, pixelDistance, 1)


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
        
