import pygame
import os, inspect
import random

# Locate the working directory
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))  # compatible with interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup screen
screenWidth = 400
screenHeight = 300
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Empire City")

# Clock to manage screen updates
clock = pygame.time.Clock()

# Load images
background = pygame.image.load(os.path.join(assets, "map.png"))
crosshair = pygame.image.load(os.path.join(assets, "viseur.png"))
arrowLeft = pygame.image.load(os.path.join(assets, "fleche_gauche.png"))
arrowRight = pygame.image.load(os.path.join(assets, "fleche_droite.png"))
banditStreetSprite = pygame.image.load(os.path.join(assets, "bandit_rue.png"))
banditWindowSprite = pygame.image.load(os.path.join(assets, "bandit_window4.png"))

# Game dimensions and decorations
decorWidth = background.get_width()
decorHeight = background.get_height()

# Central reference point (e.g., church bell)
referencePointX = 350
referencePointY = 525

# Adjusted reference point to center the map view
referenceX = referencePointX - screenWidth // 2
referenceY = referencePointY - screenHeight // 2

# Crosshair speed and initial position
crosshairSpeed = 5
crosshairOffsetX = screenWidth // 2
crosshairOffsetY = screenHeight // 2

# Orange zone dimensions to limit map view movement
orangeZoneWidth = screenWidth * 2 // 3
orangeZoneHeight = screenHeight * 2 // 3
orangeZoneX = (screenWidth - orangeZoneWidth) // 2
orangeZoneY = (screenHeight - orangeZoneHeight) // 2

# Window positions for bandit appearances
windowPositions = [
    (814, 332),
    (987, 340),
    (1225, 504),
    (1226, 122),
    (1928, 338)
]

def moveCrosshair(keys, offsetX, offsetY):
    """Move the crosshair within screen boundaries."""
    if keys[pygame.K_UP]: offsetY -= crosshairSpeed
    if keys[pygame.K_DOWN]: offsetY += crosshairSpeed
    if keys[pygame.K_LEFT]: offsetX -= crosshairSpeed
    if keys[pygame.K_RIGHT]: offsetX += crosshairSpeed

    offsetX = max(crosshair.get_width() // 2, min(offsetX, screenWidth - crosshair.get_width() // 2))
    offsetY = max(crosshair.get_height() // 2, min(offsetY, screenHeight - crosshair.get_height() // 2))

    return offsetX, offsetY

def adjustReference(offsetX, offsetY, referenceX, referenceY):
    """Adjust map reference point based on crosshair position."""
    if offsetX < orangeZoneX: referenceX -= orangeZoneX - offsetX
    elif offsetX > orangeZoneX + orangeZoneWidth: referenceX += offsetX - (orangeZoneX + orangeZoneWidth)
    if offsetY < orangeZoneY: referenceY -= orangeZoneY - offsetY
    elif offsetY > orangeZoneY + orangeZoneHeight: referenceY += offsetY - (orangeZoneY + orangeZoneHeight)

    referenceX = max(0, min(referenceX, decorWidth - screenWidth))
    referenceY = max(0, min(referenceY, decorHeight - screenHeight))

    return referenceX, referenceY

def manageBanditAppearance(currentTime, startTime, banditAppeared):
    """Manage the appearance of a bandit either on the street or in a window."""
    banditX, banditY = None, None
    appearanceType = random.choice(["street", "window"])
    currentSprite = banditStreetSprite if appearanceType == "street" else banditWindowSprite
    
    if currentTime - startTime >= 3 and not banditAppeared:
        if appearanceType == "street":
            banditX = random.randint(0, decorWidth - currentSprite.get_width())
            banditY = decorHeight - currentSprite.get_height()
        else:
            banditX, banditY = random.choice(windowPositions)
            banditX -= currentSprite.get_width() // 2
            banditY -= currentSprite.get_height() // 2
        
        banditAppeared = True
        print("Bandit appeared at coordinates", banditX, banditY, "(" + appearanceType + ")")

    return banditX, banditY, banditAppeared, currentSprite

def drawBandit(screen, banditAppeared, banditX, banditY, referenceX, referenceY, sprite, banditScreenX=None, banditScreenY=None):
    """Draw the bandit on the screen."""
    if banditAppeared and banditX is not None and banditY is not None:
        banditScreenX = banditX - referenceX
        banditScreenY = banditY - referenceY
        screen.blit(sprite, (banditScreenX, banditScreenY))
    return banditScreenX, banditScreenY

def handleShooting(keys, banditVisible, banditAppeared, offsetX, offsetY, banditScreenX, banditScreenY, sprite, lastShootTime):
    """Handle shooting logic."""
    shootPerformed = False
    if keys[pygame.K_SPACE]:
        shootPerformed = True
        offsetY -= 10  # Simulate recoil
        if banditVisible:
            # Check if the shot hit the bandit
            if offsetX >= banditScreenX and offsetX <= banditScreenX + sprite.get_width() and offsetY >= banditScreenY and offsetY <= banditScreenY + sprite.get_height():
                print("Bandit hit at coordinates", banditScreenX, banditScreenY)
                banditVisible = False
                banditAppeared = False
                lastShootTime = pygame.time.get_ticks() / 1000
            else:
                print("Missed shot.")
    return shootPerformed, lastShootTime, banditVisible, banditAppeared, offsetY

def checkBanditReappearance(banditVisible, currentTime, lastShootTime):
    """Check if the bandit should reappear."""
    return not banditVisible and (currentTime - lastShootTime >= 3)

def showAimingHelp(screen, offsetX, banditScreenX, arrowLeft, arrowRight):
    """Show aiming help arrows."""
    gap = banditScreenX - offsetX
    if abs(gap) > 200:  # Adjust sensitivity as needed
        if gap > 0:
            screen.blit(arrowRight, (offsetX + 50, offsetY - 20))
        else:
            screen.blit(arrowLeft, (offsetX - 50, offsetY - 20))

# Main game loop
done = False
startTime = int(pygame.time.get_ticks() / 1000)
banditAppeared = False
shootPerformed = False
banditVisible = False
lastShootTime = 0
currentSprite = banditStreetSprite
banditScreenX, banditScreenY = -1, -1
banditX, banditY = -1, -1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    currentTime = int(pygame.time.get_ticks() / 1000)

    # Handle shooting
    shootPerformed, lastShootTime, banditVisible, banditAppeared, offsetY = handleShooting(keys, banditVisible, banditAppeared, crosshairOffsetX, crosshairOffsetY, banditScreenX, banditScreenY, currentSprite, lastShootTime)

    # Check bandit reappearance
    if checkBanditReappearance(banditVisible, currentTime, lastShootTime):
        banditX, banditY, banditAppeared, currentSprite = manageBanditAppearance(currentTime, startTime, banditAppeared)
        banditVisible = banditAppeared

    crosshairOffsetX, crosshairOffsetY = moveCrosshair(keys, crosshairOffsetX, crosshairOffsetY)
    referenceX, referenceY = adjustReference(crosshairOffsetX, crosshairOffsetY, referenceX, referenceY)

    # Draw game elements
    viewArea = pygame.Rect(referenceX, referenceY, screenWidth, screenHeight)
    screen.blit(background, (0, 0), area=viewArea)
    if banditVisible:
        banditScreenX, banditScreenY = drawBandit(screen, banditVisible, banditX, banditY, referenceX, referenceY, currentSprite, banditScreenX, banditScreenY)
        showAimingHelp(screen, crosshairOffsetX, banditScreenX, arrowLeft, arrowRight)
    screen.blit(crosshair, (crosshairOffsetX - crosshair.get_width() // 2, crosshairOffsetY - crosshair.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
