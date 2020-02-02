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

    def draw(self, windows):
        pygame.draw.circle(windows, (255, 0, 0), self.position, 8)
        text = font.render(self.blePoint, True, (255, 255, 255))
        windows.blit(text, (50, 40))

blePoints = []
i = 0
for addr, name in nearby_devices:
    ble = BlePoint(addr, name, position[i])
    blePoints.append(ble)
    i += 1

def drawWindows():
    pygame.draw.rect(windows, (0, 255, 0), (0, 0, 900, 600), 3)
    for ble in blePoints:
        ble.draw(windows)
    pygame.display.update()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    drawWindows()
pygame.quit()
        