from cmu_graphics import *
import random
import copy
import shortestPath
import math
from physics import Gravity 
import time
from PIL import Image 
import os

class Player:
    def __init__(self, cx, cy, r, xv, yv):
        self.cx = cx
        self.cy = cy
        self.xv = xv
        self.yv = yv
        self.r = r
        self.playerHealth = 50 
        self.playerWeakAttack = 5 
        self.playerStrongAttack = 10
        self.playerDig = 20

class Enemy:
    def __init__(self, cx, cy, r, xv, yv, isFollowing=False):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.xv = xv
        self.yv = yv
        self.facing = random.choice(['left', 'right']) #https://www.youtube.com/watch?v=whDf00oel-E&t=11s 
        self.isFollowing = isFollowing
        self.health = 50
        self.theta = 45
        self.pathRadius = 50
        self.moveClockwise = False

    def __repr__(self):
        return f"Enemy(cx={self.cx}, cy={self.cy}, r={self.r}, xv={self.xv}, yv={self.yv})"
    
    def getRadiusEndpoint(self, x, y, r, theta): #from csacademy notes 
        return (x + r*math.cos(math.radians(theta)),
                y - r*math.sin(math.radians(theta)))

    def update(self, app): 
        row, col = getRowCol(app, self.cx, self.cy, app.cellWidth, app.cellHeight)
        if not self.isFollowing:
            if self.facing == 'left': #https://www.youtube.com/watch?v=whDf00oel-E&t=11s 
                if col >= 0 and not app.tiles[row][col]:
                    self.cx -= 5
                else:
                    self.facing = 'right'
            elif self.facing == 'right': #https://www.youtube.com/watch?v=whDf00oel-E&t=11s 
                nextCol = col+1
                if nextCol < app.cols and not app.tiles[row][nextCol]:
                    self.cx += 5
                else:
                    self.facing = 'left'
        else:
            self.followPlayer(app)
        
    def followPlayer(self, app):
        self.cx, self.cy = self.getRadiusEndpoint(app.player.cx, app.player.cy, self.pathRadius, self.theta) #from csacademy notes
        eRow, eCol = getRowCol(app, self.cx, self.cy, app.cellWidth, app.cellHeight)

        if (eRow == app.rows-1 or eRow == 0 or
            eCol == app.cols-1 or eCol == 0):
            self.moveClockwise = not self.moveClockwise

        if (eRow+1 < app.rows and app.tiles[eRow+1][eCol] or
            eRow-1 >= 0 and app.tiles[eRow-1][eCol] or
            eCol+1 < app.cols and app.tiles[eRow][eCol+1] or
            eCol-1 >= 0 and app.tiles[eRow][eCol-1]):
            self.moveClockwise = not self.moveClockwise

        if 0 <= eRow < app.rows and 0 <= eCol < app.cols:
            if app.tiles[eRow][eCol]:
                newRow, newCol = self.findClosestCave(app, eRow, eCol)
                self.cx, self.cy = getPos(app, newRow, newCol, app.cellWidth, app.cellHeight)
    
    def findClosestCave(self, app, startRow, startCol):
        closestDist = float('inf') #chatgpt
        closestCave = None

        for row in range(app.rows):
            for col in range(app.cols):
                if not app.tiles[row][col]:
                    distance = math.sqrt((startRow-row)**2 + (startCol-col)**2)
                    if distance < closestDist:
                        closestDist = distance
                        closestCave = (row, col)
        return closestCave
    
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
    def move(self, playerX, playerY):
        dx = playerX - self.x
        dy = playerY - self.y
        dist = (dx**2+dy**2)**0.5
        directionX = dx/dist #chatgpt
        directionY = dy/dist #chatgpt
        self.x += self.speed*directionX
        self.y += self.speed*directionY

def loadPilImage(fileName):
    return Image.open(os.path.join('images', fileName)) #from demo-pil-scaling.py

def onAppStart(app):
    app.width = 1000
    app.height = 600
    app.rows = 40
    app.cols = 40
    app.rowsOnScreen = 10
    app.colsOnScreen = 10
    app.stepsPerSecond = 10

    loadImages(app)
    mainMenu(app)
    designGame(app)
    startGame(app)
    animation(app)

def animation(app):
    pWalk ='walk.png'
    pWalkSprite = loadSpritePilImages(pWalk, 6)
    pWalkScreenSprite = loadSpritePilImages(pWalk, 2)
    app.pWalkSprite = [CMUImage(pilImage) for pilImage in pWalkSprite]
    app.pWalkScreenSprite = [CMUImage(pilImage) for pilImage in pWalkScreenSprite]
    app.pSpriteInd = 0

def loadPilImage(fileName):
    return Image.open(os.path.join('images', fileName))

def loadSpritePilImages(file, size):
    spritestrip = loadPilImage(file)
    spritePilImages = []
    
    for i in range(10):
        spriteImage = spritestrip.crop((100*i, 0, 100+100*i, 100))
        imgW, imgH = spriteImage.size
        resizedImg = spriteImage.resize((imgW//size, imgH//size))
        spritePilImages.append(resizedImg)
    return spritePilImages

def loadImages(app):
    #this function references demo-pil-scaling.py
    playerS = loadPilImage('mushroom.png')
    enemyS = loadPilImage('enemy.png')
    healthS = loadPilImage('heart.png')
    strengthS = loadPilImage('strength.png')
    buttonBg = loadPilImage('button.png')
    mapS = loadPilImage('map.png')
    homeS = loadPilImage('home.png')
    caveS = loadPilImage( 'cave.png')
    wallS = loadPilImage('wall.png')
    entranceS = loadPilImage('entrance.png')
    exitS = loadPilImage('exit.png')
    eBallS = loadPilImage('enemyBall.png')
    pBallS = loadPilImage('playerBall.png')
    helpS = loadPilImage('help.png')
    checkS = loadPilImage('check.png')
    backS = loadPilImage('back.png')
    mainBg = loadPilImage('mainBg.png')
    
    elements = [('playerS',playerS), 
                ('enemyS', enemyS),
                ('healthS', healthS),
                ('strengthS', strengthS),
                ('eBallS', eBallS),
                ('pBallS', pBallS)]
    tiles = [('caveS', caveS),
             ('wallS', wallS),
             ('entranceS', entranceS),
             ('exitS', exitS)]
    resized = {}
    for name, elem in elements:
        elemWidth, elemHeight = elem.size
        worldSize = elem.resize((elemWidth//6, elemHeight//6))
        screenSize = elem.resize((elemWidth//2, elemHeight//2))
        resized[name] = worldSize
        resized[f'{name}Screen'] = screenSize
    for name, tile in tiles:
        tileWidth, tileHeight = tile.size
        screenSize = tile.resize((tileWidth*4, tileHeight*4))
        resized[name] = tile
        resized[f'{name}Screen'] = screenSize

    bWidth, bHeight = buttonBg.size
    buttonBg = buttonBg.resize((bWidth*2, bHeight*2))
    mapS = mapS.resize((bWidth//2, bHeight//2))
    homeS = homeS.resize((bWidth//2, bHeight//2))
    helpS = helpS.resize((bWidth//2, bHeight//2))
    checkS = checkS.resize((bWidth//2, bHeight//2))
    backS = backS.resize((bWidth//2, bHeight//2))
    # cWidth, cHeight = mainBg.size
    # mainBg = mainBg.resize((cWidth*2, cHeight*2))
    resized['buttonBg'] = buttonBg
    resized['mapS'] = mapS
    resized['homeS'] = homeS
    resized['helpS'] = helpS
    resized['checkS'] = checkS
    resized['backS'] = backS
    resized['mainBg'] = mainBg

    #the following loop is written by chatgpt 
    for name, resizedImg in resized.items():
        setattr(app, name, CMUImage(resizedImg)) 

def mainMenu(app):
    app.startMenu = True
    app.instructions = False
    app.gameView = False
    app.makeGame = False
    app.backButton = 'https://static.thenounproject.com/png/2961062-200.png'

def startGame(app):
    app.cave = []
    app.tiles = [[random.random() < 0.50 for col in range(app.cols)] for row in range(app.rows)] #chat
    app.streTreasures = [[random.random() < 0.025 for col in range(app.cols)] for row in range(app.rows)]
    app.healthTreasures = [[random.random() < 0.025 for col in range(app.cols)] for row in range(app.rows)]
    app.path = None
    app.isJumping = False
    app.isFlying = False
    app.enemyIsFollowing = False
    app.enemies = []
    app.enemiesScreen = []
    app.balls = []
    app.ballsScreen = []
    app.enemyHealth = 50
    app.mapOn = False
    app.paused = False
    app.playerWon = False
    app.playerLost = False
    app.playerWalking = False
    app.lastTime = time.time()

    generateCave(app)
    connect(app, app.entrance, app.exit)
    #after connceting the caves, check valid pos of entrance again
    if not app.tiles[app.playerCRow+1][app.playerCCol]:
        app.entrance = startingPos(app)
        app.playerCRow, app.playerCCol = app.entrance[0], app.entrance[1]
    playerCx, playerCy = getPos(app, app.playerCRow, app.playerCCol, app.cellWidth, app.cellHeight)
    app.player = Player(playerCx, playerCy, 7, 0, 0)

    setCameraBounds(app)
    initializePlayer(app)
    spawnEnemy(app)
    
def designGame(app):
    app.buttonBorder = ['SlateGray']*7
    app.buttons = ['cave', 'wall', 'player', 'enemy', 'health', 'strength', 'exit']
    app.isSelected = [False]*7
    app.boardLeft, app.boardTop = 100, 110
    app.boardW, app.boardH = 800, 480
    app.tilesDesign = [[True for col in range(app.cols)] for row in range(app.rows)]
    app.caveDesign = []
    app.enemyRowCol = []
    app.enemiesDesign = []
    app.healthTList = [[None for col in range(app.cols)] for row in range(app.rows)]
    app.streTList = [[None for col in range(app.cols)] for row in range(app.rows)]
    app.lastRow, app.lastCol = None, None
    app.playerRowCol = None
    app.exitRowCol = None
    app.intro = False
    app.designMode = True
    app.enemyCount = app.healthCount = app.strengthCount = 0
    app.hasPlayer = False
    app.hasCave = False
    app.hasExit = False
    app.hasEnemy = False
    getCellSize(app)

def resetGame(app):
    app.cave = []
    app.tiles = [[random.random() < 0.50 for col in range(app.cols)] for row in range(app.rows)] #chat
    app.streTreasures = [[random.random() < 0.025 for col in range(app.cols)] for row in range(app.rows)]
    app.healthTreasures = [[random.random() < 0.025 for col in range(app.cols)] for row in range(app.rows)]
    app.path = None
    app.isJumping = False
    app.isFlying = False
    app.enemyIsFollowing = False
    app.enemies = []
    app.enemiesScreen = []
    app.balls = []
    app.ballsScreen = []
    app.enemyHealth = 50
    app.mapOn = False
    app.paused = False
    app.playerWon = False
    app.playerLost = False
    app.playerWalking = False
    app.lastTime = time.time()

    generateCave(app)
    connect(app, app.entrance, app.exit)
    #after connceting the caves, check valid pos of entrance again
    if not app.tiles[app.playerCRow+1][app.playerCCol]:
        app.entrance = startingPos(app)
        app.playerCRow, app.playerCCol = app.entrance[0], app.entrance[1]
    playerCx, playerCy = getPos(app, app.playerCRow, app.playerCCol, app.cellWidth, app.cellHeight)
    app.player = Player(playerCx, playerCy, 7, 0, 0)

    setCameraBounds(app)
    initializePlayer(app)
    spawnEnemy(app)

def initializePlayer(app):
    app.playerScreenCRow = app.playerCRow - app.topRow
    app.playerScreenCCol = app.playerCCol - app.leftCol
    playerCx, playerCy = getPos(app, app.playerScreenCRow, app.playerScreenCCol, app.cellWidthScreen, app.cellHeightScreen)
    app.playerScreen = Player(playerCx, playerCy, 20, 0, 0)

def setCameraBounds(app):
    app.player.cx, app.player.cy = getPos(app, app.playerCRow, app.playerCCol, app.cellWidth, app.cellHeight)
    app.cameraSize = 5 #row and col
    app.topRow = max(app.playerCRow - app.cameraSize, 0)
    app.bottomRow = min(app.playerCRow + app.cameraSize, app.rows-1)
    app.leftCol = max(app.playerCCol - app.cameraSize, 0)
    app.rightCol = min(app.playerCCol + app.cameraSize, app.cols-1)

    if app.topRow == 0:
        app.bottomRow += app.cameraSize-app.playerCRow
    elif app.bottomRow == app.rows-1:
        app.topRow -= app.playerCRow+app.cameraSize-(app.rows-1)
    if app.leftCol == 0:
        app.rightCol += app.cameraSize-app.playerCCol
    if app.rightCol == app.cols-1:
        app.leftCol -= app.playerCCol+app.cameraSize-(app.cols-1)

def generateCave(app):
    for _ in range(6):
        iterateTiles(app)
    for row in range(app.rows):
        for col in range(app.cols):
            if not app.tiles[row][col]:
                app.cave.append((row, col))
    getCellSize(app)
    #connect caves
    firstEmp = random.choice(app.cave)
    while True:
        secondEmp = random.choice(app.cave)
        if firstEmp != secondEmp:
            break
    connect(app, firstEmp, secondEmp)
    app.entrance = startingPos(app)
    app.exit = findValidExit(app)
    app.playerCRow, app.playerCCol = app.entrance

def findValidExit(app):
    while True:
        app.exit = startingPos(app)
        distance = math.sqrt((app.entrance[0]-app.exit[0])**2 + (app.entrance[1]-app.exit[1])**2)
        if distance > 25:
            break
    return app.exit

def getCellLeftTop(app, row, col, width, height):
    if app.gameView:
        cellLeft = col*width
        cellTop = row*height
    if app.makeGame:
        cellLeft = col*width + app.boardLeft
        cellTop = row*height + app.boardTop
    return cellLeft, cellTop

def getCellSize(app):
    app.cellWidth = app.width//app.rows
    app.cellHeight = app.height//app.cols

    app.cellWidthScreen = app.width//app.rowsOnScreen
    app.cellHeightScreen = app.height//app.colsOnScreen

    app.cellWidthDesign = app.boardW//app.rows #20
    app.cellHeightDesign = app.boardH//app.cols #12

def getPos(app, row, col, width, height):
    entityCx = col*width + (width/2)
    entityCy = row*height + (height/2)
    return entityCx, entityCy

def getRowCol(app, cx, cy, width, height):
    row = int((cy - (height//2)) // height)
    col = int((cx - (width//2)) // width)
    return row, col
    
def startingPos(app):
    isValidGround = False
    while not isValidGround:
        start = random.choice(app.cave)
        startRow = start[0]
        startCol = start[1]
        if startRow+1 < len(app.tiles[0]) and (startRow+1, startCol) not in app.cave:
            isValidGround = True 
    return (startRow, startCol)

def spawnEnemy(app):
    enemyCount = 0
    while enemyCount < 3:
        eRow, eCol = startingPos(app)
        eCx, eCy = getPos(app, eRow, eCol, app.cellWidth, app.cellHeight)
        enemy = Enemy(eCx, eCy, 7, 0, 0)
        app.enemies.append(enemy)

        eRowScreen = eRow - app.topRow
        eColScreen = eCol - app.leftCol
        eCxScreen, eCyScreen = getPos(app, eRowScreen, eColScreen, app.cellWidthScreen, app.cellHeightScreen)
        enemyScreen = Enemy(eCxScreen, eCyScreen, 20, 0, 0)
        app.enemiesScreen.append(enemyScreen)

        enemyCount += 1

def redrawAll(app):
    if app.startMenu:
        drawImage(app.mainBg, 0, 0)
        # drawRect(0, 0, app.width, app.height, fill='papayaWhip')
        drawLabel("agaric's curse", app.width//2, app.height//2, size=72, bold=True, fill='darkGoldenRod')
        drawImage(app.buttonBg, 250, 475, align='center')
        drawImage(app.buttonBg, 500, 475, align='center')
        drawImage(app.buttonBg, 750, 475, align='center')

        drawLabel('instructions', 250, 475, fill='white', size=24, bold=True)
        drawLabel('play', 500, 475, fill='white', size=24, bold=True)
        drawLabel('design', 750, 475, fill='white', size=24, bold=True)
    
    elif app.instructions: #the fonts dont work
        drawRect(0, 0, app.width, app.height, fill='papayaWhip')
        drawLabel("steps to survive the shroom monsters...", app.width//2, 50, font='Silkscreen', size=36)
        drawLabel('press left and right arrows to move around', 100, 150, size=18, align='left')
        drawLabel('press space bar to jump', 100, 250, size=18, align='left')
        drawLabel("press 'e' to attack an enemy!", 100, 350, size=18, align='left')
        drawLabel("press 'up' to fly and magically move through the walls!", 100, 450, size=18, align='left')
        drawLabel("press any arrow key and 'q' to dig into a wall", 100, 550, size=18, align='left')
        #draw back button
        drawImage(app.backS, 900, 500, align='center')

    elif app.gameView:
        if app.mapOn == True:
            for row in range(app.rows):
                for col in range(app.cols):
                    x = col*app.cellWidth + app.cellWidth//2
                    y = row*app.cellHeight + app.cellHeight//2
                    if app.tiles[row][col]:
                        drawImage(app.wallS, x, y, align='center')
                    else:
                        drawImage(app.caveS, x, y, align='center')
                        if app.streTreasures[row][col]:
                            drawImage(app.strengthS, x, y, align='center')
                        if app.healthTreasures[row][col]:
                            drawImage(app.healthS, x, y, align='center')
                        if (row, col) == app.entrance:
                            drawImage(app.entranceS, x, y, align='center')
                        if (row, col) == app.exit:
                            drawImage(app.exitS, x, y, align='center')
            #draw player 
            if not app.playerWalking:
                drawImage(app.playerS, app.player.cx, app.player.cy, align='center')
            else:
                drawImage(app.pWalkSprite[app.pSpriteInd], 
                          app.player.cx, app.player.cy, align='center')
            drawLabel(f'Health: {app.player.playerHealth}', app.player.cx, app.player.cy-20, size=12, fill='white')
            for enemy in app.enemies:
                drawImage(app.enemyS, enemy.cx, enemy.cy, align='center')
                drawLabel(f'Health: {enemy.health}', enemy.cx, enemy.cy-20, size=12, fill='white')
            for ball in app.balls:
                drawImage(app.eBallS, ball.x, ball.y, align='center')

        else:
        #draw screen
            for r in range(app.bottomRow+1-app.topRow):
                row = r + app.topRow
                for c in range(app.rightCol+1-app.leftCol):
                    col = c + app.leftCol
                    x = c*app.cellWidthScreen + app.cellWidthScreen//2
                    y = r*app.cellHeightScreen + app.cellHeightScreen//2
                    if app.tiles[row][col]:
                        drawImage(app.wallSScreen, x, y, align='center')
                    else:
                        drawImage(app.caveSScreen, x, y, align='center')
                        if app.streTreasures[row][col]:
                            drawImage(app.strengthSScreen, x, y, align='center')
                        if app.healthTreasures[row][col]:
                            drawImage(app.healthSScreen, x, y, align='center')
                        if (row, col) == app.entrance:
                            drawImage(app.entranceSScreen, x, y, align='center')
                        if (row, col) == app.exit:
                            drawImage(app.exitSScreen, x, y, align='center')
            #draw player 
            if not app.playerWalking:
                drawImage(app.playerSScreen, app.playerScreen.cx, app.playerScreen.cy, align='center')
            else:
                drawImage(app.pWalkScreenSprite[app.pSpriteInd], 
                          app.playerScreen.cx, app.playerScreen.cy, align='center')
            drawLabel(f'Health: {app.player.playerHealth}',app.playerScreen.cx, app.playerScreen.cy-30, size=18, fill='white')

            for i in range(len(app.enemiesScreen)):
                enemyScreen = app.enemiesScreen[i]
                enemy = app.enemies[i]
                drawImage(app.enemySScreen, enemyScreen.cx, enemyScreen.cy, align='center')
                drawLabel(f'Health: {enemy.health}', enemyScreen.cx, enemyScreen.cy-30, size=18, fill='white')
            for ball in app.ballsScreen:
                drawImage(app.eBallSScreen, ball.x, ball.y, align='center')
        #draw buttons
        drawImage(app.homeS, 925, 475, align='center')
        drawImage(app.mapS, 925, 550, align='center')

    if app.playerWon:
        drawRect(0, 0, app.width, app.height, fill='white', opacity=50)
        drawLabel('You Won!', app.width//2, 200, size=48, bold=True, fill='darkGoldenRod')
        drawImage(app.buttonBg, app.width//2, 300, align='center')
        drawLabel('Restart', app.width//2, 300, size=24, bold=True, fill='white')
        drawImage(app.buttonBg, app.width//2, 450, align='center')
        drawLabel('Home', app.width//2, 450, size=24, bold=True, fill='white')

    if app.playerLost:
        drawRect(0, 0, app.width, app.height, fill='white', opacity=50)
        drawLabel('You Lost...', app.width//2, 200, size=48, bold=True, fill='darkGoldenRod')
        drawImage(app.buttonBg, app.width//2, 300, align='center')
        drawLabel('Restart', app.width//2, 300, size=24, bold=True, fill='white')
        drawImage(app.buttonBg, app.width//2, 450, align='center')
        drawLabel('Home', app.width//2, 450, size=24, bold=True, fill='white')

    if app.makeGame:
        if app.intro:
            drawLabel('Time to make your own game!', app.width//2, 200, size=48)
            drawLabel('The design panel starts with all wall tiles, to draw caves', app.width//2, 250, size=16)
            drawLabel('click on the cave button in the menu on top and click and drag',app.width//2, 270, size=16)
            drawLabel('to fill the board. All other elements of the game has to be', app.width//2, 290, size=16)
            drawLabel('drawn in a cave tile, with the addition that the player has to', app.width//2, 310, size=16)
            drawLabel('be placed on the ground(in a cave tile, but on top of a wall tile)', app.width//2, 330, size=16)
            drawLabel('Each game is allowed to have up to three enemies and one player.', app.width//2, 350, size=16)
            drawLabel('Have fun!', app.width//2, 370, size=16)
            #next button
            drawImage(app.buttonBg, app.width//2, 450, align='center')
            drawLabel('Design!', app.width//2, 450, fill='white', size=24, bold=True)

        if app.designMode:
            #draw control panel
            drawRect(0, 0, app.width, 100, fill='tan', opacity=75)
            x = 130
            y = 50
            buttonX = 100
            buttonY = 60
            for i in range(7):
                drawRect(x, y, buttonX, buttonY, fill='floralWhite', align='center')
                x += 120
            #draw element
            drawImage(app.caveSScreen, 130, y, align='center')
            drawImage(app.wallSScreen, 250, y, align='center')
            drawImage(app.playerSScreen, 370, y, align='center')
            drawImage(app.enemySScreen, 490, y, align='center')
            drawImage(app.strengthSScreen, 610, y, align='center')
            drawImage(app.healthSScreen, 730, y, align='center')
            drawImage(app.exitSScreen, 850, y, align='center')

            drawRect(150, 60, 20, 12, fill='saddleBrown')
            drawRect(280, 60, 20, 12, fill='papayaWhip')
            drawCircle(405, 65, 5, fill='red')
            drawCircle(525, 65, 5, fill='gold')
            drawCircle(645, 65, 5, fill='olive')
            drawCircle(765, 65, 5, fill='orange')
            drawRect(865, 60, 20, 12, fill='green')
            #draw frame
            x = 130
            for i in range(7):
                drawRect(x, y, buttonX, buttonY, border=app.buttonBorder[i],
                        borderWidth=5, fill=None, align='center')
                x += 120
            #draw board
            for row in range(app.rows):
                for col in range(app.cols):
                    cellLeft, cellTop = getCellLeftTop(app, row, col, app.cellWidthDesign, app.cellHeightDesign)
                    x = cellLeft+app.cellWidthDesign//2
                    y = cellTop+app.cellHeightDesign//2
                    drawCell(app, row, col, None, app.cellWidthDesign, app.cellHeightDesign)                  
                    if (row, col) == app.playerRowCol:
                        drawCircle(x, y, 5, fill='red')
                    if (row, col) in app.enemyRowCol:
                        drawCircle(x, y, 5, fill='gold')
                    if (row, col) in app.healthTList:
                        drawCircle(x, y, 5, fill='olive')
                    if (row, col) in app.streTList:
                        drawCircle(x, y, 5, fill='orange')
                    if (row, col) == app.exitRowCol:
                        drawRect(col*app.cellWidthDesign + app.boardLeft, 
                                 row*app.cellHeightDesign + app.boardTop, 
                                 app.cellWidthDesign, app.cellHeightDesign, 
                                 fill='green')
            drawRect(app.boardLeft, app.boardTop, app.boardW, app.boardH, 
                    border='slateGray', borderWidth=1, fill=None)
            drawImage(app.helpS, 950, 500, align='center')
            drawImage(app.checkS, 950, 565, align='center')
            drawImage(app.homeS, 950, 435, align='center')

def drawCell(app, row, col, color, width, height):
    cellLeft, cellTop = getCellLeftTop(app, row, col, width, height)
    if app.gameView:
        drawRect(cellLeft, cellTop, width, height,
             fill=color)
    if app.makeGame:
        tile = app.tilesDesign[row][col]
        if tile == False:
            color = 'saddleBrown'
        elif tile == True:
            color = 'papayawhip'
        drawRect(cellLeft, cellTop, width, height, 
                 fill=color, border='gainsboro', borderWidth=0.5)

def iterateTiles(app):
    #followed https://www.youtube.com/watch?v=FSNUp_8Xvqo 
    #referenced https://code.tutsplus.com/generate-random-cave-levels-using-cellular-automata--gamedev-9664t 
    newTiles = copy.deepcopy(app.tiles)
    for row in range(app.rows):
        for col in range(app.cols):
            walls = wallsAround(app, row, col)
            if app.tiles[row][col]:
                if walls < 4:
                    newTiles[row][col] = False
                else:
                    newTiles[row][col] = True 
            else:
                if walls >= 5:
                    newTiles[row][col] = True
                else:
                    newTiles[row][col] = False
    app.tiles = newTiles

def wallsAround(app, row, col):
    count = 0
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if (i, j) != (row, col):
                if isSolid(app, i, j):
                    count += 1
    return count 

def isSolid(app, i, j):
    if ((i < 0 or i >= app.rows) or 
        (j < 0 or j >= app.cols)):
        return True 
    return app.tiles[i][j]

def collectTreasure(app):
    app.playerCRow, app.playerCCol = getRowCol(app, app.player.cx, app.player.cy, app.cellWidth, app.cellHeight)
    if (0 <= app.playerCRow < app.rows and 
        0 <= app.playerCCol < app.cols):
        if app.streTreasures[app.playerCRow][app.playerCCol]:
            removeTreasure(app, app.playerCRow, app.playerCCol, app.streTreasures)
            increaseAbility(app, app.streTreasures)
        elif app.healthTreasures[app.playerCRow][app.playerCCol]:
            removeTreasure(app, app.playerCRow, app.playerCCol, app.healthTreasures)
            increaseAbility(app, app.healthTreasures)

def removeTreasure(app, row, col, type):
    if 0 <= row < app.rows and 0 <= col < app.cols:
        type[row][col] = False
    
def increaseAbility(app, type):
    if type == app.streTreasures:
        if app.player.playerStrongAttack <= 14.5:
            app.player.playerStrongAttack += 0.5
    elif type == app.healthTreasures:
        if app.player.playerHealth <= 49:
            app.player.playerHealth += 1

#referenced https://www.redblobgames.com/pathfinding/a-star/introduction.html 
def connect(app, start, end):
    gStart = 0
    hStart = math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    startNode = shortestPath.Node(None, start[0], start[1], gStart, hStart)
    app.path = startNode.aStar(start, end, app.tiles)
    if app.path != None:
        for (row, col) in app.path:
            app.tiles[row][col] = False 
            app.cave.append((row, col))

def checkIfKeepMoving(app):
    app.playerCRow, app.playerCCol = getRowCol(app, app.player.cx, app.player.cy, app.cellWidth, app.cellHeight)

    if app.player.yv >= 0:
        if app.playerCRow >= app.rows-1 or app.tiles[app.playerCRow+1][app.playerCCol]:
            app.player.yv = 0
            app.player.cy = min((app.playerCRow*app.cellHeight + (app.cellHeight//2)), 
                                ((app.rows-1)*app.cellHeight + (app.cellHeight//2)))
            if app.tiles[app.playerCRow][app.playerCCol]:
                # print(app.playerCRow, app.playerCCol)
                app.player.cy = app.playerCRow * app.cellHeight - (app.cellHeight//2)

    elif app.player.yv < 0:
        if app.playerCRow - 1 < 0 or app.tiles[app.playerCRow-1][app.playerCCol]:
            app.player.yv = 0
            app.player.cy = max((app.playerCRow*app.cellHeight + (app.cellHeight//2)), 0)

    if app.player.xv < 0:
        if app.playerCCol - 1 < 0 or app.tiles[app.playerCRow][app.playerCCol-1]:
            app.player.xv = 0
            app.playerWalking = False
            app.player.cx = app.playerCCol*app.cellWidth + (app.cellWidth//2)
    
    elif app.player.xv > 0:
        if app.playerCCol >= app.cols-1 or app.tiles[app.playerCRow][app.playerCCol+1]:
            app.player.xv = 0
            app.playerWalking = False
            app.player.cx = app.playerCCol*app.cellWidth + (app.cellWidth//2)

def distance(app, pCx, pCy, eCx, eCy):
    return ((pCx - eCx)**2 + (pCy - eCy)**2)**0.5

def enemyAttack(app, enemy):
    currTime = time.time()
    if currTime - app.lastTime > random.randint(2, 5): #chatgpt
        if random.choice([True, False]):
            if app.player.playerHealth >= 0:
                app.lastTime = currTime
                ball = Ball(enemy.cx, enemy.cy) 
                app.balls.append(ball)
    if app.player.playerHealth == 0:
        app.playerLost = True
        app.paused = True

def mouseToCell(app, mouseX, mouseY):
    if app.makeGame:
        col = (mouseX - app.boardLeft) // app.cellWidthDesign
        row = (mouseY - app.boardTop) // app.cellHeightDesign
        return row, col

def onKeyHold(app, keys):
    if not app.mapOn:
        if 'right' in keys:
            app.player.xv = 40
            app.playerWalking = True
            checkIfKeepMoving(app)
            app.player.cx += app.player.xv * 0.15
            app.playerCCol = getRowCol(app, app.player.cx, app.player.cy, app.cellWidth, app.cellHeight)[1]
        
        elif 'left' in keys:
            app.player.xv = -40
            app.playerWalking = True
            checkIfKeepMoving(app)
            app.player.cx += app.player.xv * 0.15
            app.playerCCol = getRowCol(app, app.player.cx, app.player.cy, app.cellWidth, app.cellHeight)[1]

        if 'up' in keys:
            if app.isFlying == False:
                app.isFlying = True 

        if 'q' in keys and 'right' in keys:
            app.tiles[app.playerCRow][app.playerCCol+1] = False
            app.cave.append((app.playerCRow, app.playerCCol+1))
        if 'q' in keys and 'left' in keys:
            app.tiles[app.playerCRow][app.playerCCol-1] = False
            app.cave.append((app.playerCRow, app.playerCCol-1))
        if 'q' in keys and 'up' in keys:
            app.tiles[app.playerCRow-1][app.playerCCol] = False
            app.cave.append((app.playerCRow-1, app.playerCCol))
        if 'q' in keys and 'down' in keys:
            app.tiles[app.playerCRow+1][app.playerCCol] = False
            app.cave.append((app.playerCRow+1, app.playerCCol))

def onKeyPress(app, key):
    if not app.mapOn:
        if key == 'space':
            if app.isJumping == False:
                app.isJumping = True 
        #player attack and remove enemy if dead(revised by chatgpt)
        enemyRemoved = [] 
        enemyScreenRemoved = []
        if key == 'e':
            for i in range(len(app.enemies)):
                enemy = app.enemies[i]
                enemyScreen = app.enemiesScreen[i]
                worldDist = distance(app, app.player.cx, app.player.cy, enemy.cx, enemy.cy)
                if worldDist < 75: 
                    enemy.health -= app.player.playerWeakAttack
                if enemy.health <= 0:
                    enemyRemoved.append(enemy)
                    enemyScreenRemoved.append(enemyScreen)
            for enemy in enemyRemoved: 
                app.enemies.remove(enemy) 
                app.player.playerHealth = 50
            for enemy in enemyScreenRemoved:
                app.enemiesScreen.remove(enemy)

def onMousePress(app, mouseX, mouseY):
    if app.gameView:
        #switch between map view and screen view
        if 900 <= mouseX <= 950 and 525 <= mouseY <= 575:
            app.mapOn = not app.mapOn
            getCellSize(app)
        #end game button
        if 900 <= mouseX <= 950 and 450 <= mouseY <= 500:
            resetGame(app)
            app.gameView = False
            app.startMenu = True 

    if app.playerWon or app.playerLost:
        if 400 <= mouseX <= 600 and 250 <= mouseY <= 350: #restart
            resetGame(app)
        if 400 <= mouseX <= 600 and 400 <= mouseY <= 500: #home
            app.gameView = False
            app.startMenu = True
            resetGame(app)

    #switch scenes
    if app.startMenu == True:
        if 150 <= mouseX <= 350 and 425 <= mouseY <= 525:
            app.startMenu = False
            app.makeGame = False
            app.instructions = True     
        if 400 <= mouseX <= 600 and 425 <= mouseY <= 525:
            app.startMenu = False
            app.instructions = False
            app.gameView = True
        if 650 <= mouseX <= 850 and 425 <= mouseY <= 525:
            app.startMenu = False
            app.instructions = False
            app.makeGame = True

    if app.instructions == True:
        centerX, centerY = 900, 500
        radius = 25
        if (abs(mouseX-centerX) <= radius and abs(mouseY-centerY) <= radius):
            app.instrcutions = False
            app.startMenu = True 

    if app.makeGame:
        if app.intro:
                if 400 <= mouseX <= 600 and 400 <= mouseY <= 500:
                    app.intro = False
                    app.designMode = True
        if app.designMode:
            if 0 <= mouseX <= app.width and 0 <= mouseY <= 100:
                app.isSelected = [False]*7
                app.buttonBorder = ['SlateGray']*7
                if  80 <= mouseX <= 180 and 10 <= mouseY <= 90:
                    app.isSelected[0] = True
                    app.buttonBorder[0] = 'green'
                elif  200 <= mouseX <= 300 and 10 <= mouseY <= 90:
                    app.isSelected[1] = True
                    app.buttonBorder[1] = 'green'
                elif  320 <= mouseX <= 420 and 10 <= mouseY <= 90:
                    app.isSelected[2] = True
                    app.buttonBorder[2] = 'green'
                elif  440 <= mouseX <= 540 and 10 <= mouseY <= 90:
                    app.isSelected[3] = True
                    app.buttonBorder[3] = 'green'
                elif  560 <= mouseX <= 660 and 10 <= mouseY <= 90:
                    app.isSelected[4] = True
                    app.buttonBorder[4] = 'green'
                elif  680 <= mouseX <= 780 and 10 <= mouseY <= 90:
                    app.isSelected[5] = True
                    app.buttonBorder[5] = 'green'
                elif  800 <= mouseX <= 900 and 10 <= mouseY <= 90:
                    app.isSelected[6] = True
                    app.buttonBorder[6] = 'green'
            elif (app.boardLeft < mouseX < app.boardLeft+app.boardW and 
                app.boardTop < mouseY < app.boardTop+app.boardH):
                changeTile(app, mouseX, mouseY)
                changeCellElem(app, mouseX, mouseY)

        #hit confirm and help button
        if 920 <= mouseX <= 980 and 410 <= mouseY <= 460:
            app.makeGame = False
            app.startMenu = True

        if 920 <= mouseX <= 980 and 475 <= mouseY <= 525:
            app.intro = True
            app.designMode = False

        if 920 <= mouseX <= 980 and 540 <= mouseY <= 590:
            if app.hasPlayer and app.hasCave and app.hasExit and app.hasExit:
                resetGame(app)
                app.tiles = app.tilesDesign
                app.cave = app.caveDesign
                app.streTreasures = app.streTList
                app.healthTreasures = app.healthTList
                app.playerCRow, app.playerCCol = app.playerRowCol
                app.entrance = app.playerRowCol
                app.exit = app.exitRowCol
                app.enemiesScreen = []
                app.enemies = app.enemiesDesign
                setCameraBounds(app)
                app.makeGame = False 
                app.gameView = True 


def onMouseDrag(app, mouseX, mouseY):
    if app.makeGame:
        if (app.boardLeft < mouseX < app.boardLeft+app.boardW and 
            app.boardTop < mouseY < app.boardTop+app.boardH):
            changeTile(app, mouseX, mouseY)

def changeTile(app, mouseX, mouseY):
    row, col = mouseToCell(app, mouseX, mouseY)
    for i in range(2):
        if app.isSelected[i] == True:
            if app.buttons[i] == 'cave':
                app.tilesDesign[row][col] = False
                app.caveDesign.append((row, col))
                app.hasCave = True 
            elif app.buttons[i] == 'wall':
                app.tilesDesign[row][col] = True

def changeCellElem(app, mouseX, mouseY):
    row, col = mouseToCell(app, mouseX, mouseY)
    for i in range(2, len(app.isSelected)):
        if app.isSelected[i] == True:
            if not app.tilesDesign[row][col]:
                if app.buttons[i] == 'player':
                    if (not app.tilesDesign[row][col]) and (app.tilesDesign[row+1][col]):
                        if app.playerRowCol != None:
                            app.playerRowCol = None
                        app.playerRowCol = row, col
                        app.hasPlayer = True
                if app.buttons[i] == 'enemy':
                    if len(app.enemyRowCol) >= 3:
                        app.enemyRowCol.pop(0)
                        app.enemiesDesign.pop(0)
                    app.enemyRowCol.append((row, col))
                    app.hasEnemy = True
                    eCx, eCy = getPos(app, row, col, app.cellWidth, app.cellHeight)
                    enemy = Enemy(eCx, eCy, 15, 0, 0)
                    app.enemiesDesign.append(enemy)

                if app.buttons[i] == 'health':
                    app.healthTList[row][col] = True
                if app.buttons[i] == 'strength':
                    app.streTList[row][col] = True
                if app.buttons[i] == 'exit':
                    if app.exitRowCol != None:
                        app.exitRowCol = None
                    app.exitRowCol = row, col
                    app.hasExit = True 
                
def updateTilesInView(app):
    screenTiles = []
    for r in range(app.topRow, app.bottomRow + 1):
        rowTiles = []
        for c in range(app.leftCol, app.rightCol + 1):
            if 0 <= r < app.rows and 0 <= c < app.cols:
                rowTiles.append(app.tiles[r][c])
            else:
                rowTiles.append(False)
        screenTiles.append(rowTiles)
    return screenTiles

def onStep(app):
    if not app.paused:
        app.visibleTiles = updateTilesInView(app)
        if not app.isJumping and not app.isFlying:
            app.player.cy, app.player.yv = Gravity.falling(app.player.cy, app.player.yv, 120, 0.1)
        if app.isJumping:
            app.player.cy, app.player.yv = Gravity.jumping(app.player.cy, app.player.yv, -400, 100, 0.1)
            app.isJumping = False
        if app.isFlying:
            app.player.cy, app.player.yv = Gravity.flying(app.player.cy, app.player.yv, -400, 100, 0.05)
            app.isFlying = False
        app.player.cx = Gravity.moveXDir(app.player.cx, app.player.xv, 0.15)
        #convert world position to screen position
        app.playerScreen.cx = (app.player.cx - (app.leftCol * app.cellWidth))*4
        app.playerScreen.cy = (app.player.cy - (app.topRow * app.cellHeight))*4
        
        #friction
        app.playerCRow, app.playerCCol = getRowCol(app, app.player.cx, app.player.cy, app.cellWidth, app.cellHeight)
        if app.playerCRow < app.rows-1:
            if app.tiles[app.playerCRow+1][app.playerCCol]:
                app.player.xv *= (9/10)

        #check if game completed
        if len(app.enemies) == 0:
            if app.playerCRow == app.exit[0] and app.playerCCol == app.exit[1]:
                app.player.xv, app.player.yv = 0, 0
                app.player.cx, app.player.cy = getPos(app, app.exit[0], app.exit[1], app.cellWidth, app.cellHeight)
                app.playerWon = True
                app.paused = True

        #moving right
        if app.playerScreen.cx >= 800:
            app.leftCol = min(app.leftCol+1, app.cols-10)
            app.rightCol = min(app.rightCol+1, app.cols-1)
        #moving left 
        if app.playerScreen.cx <= 200:
            app.leftCol = max(app.leftCol-1, 0)
            app.rightCol = max(app.rightCol-1, 10)
        #moving down
        if app.playerScreen.cy >= 500:
            app.topRow = min(app.topRow+1, app.rows-10)
            app.bottomRow = min(app.bottomRow+1, app.rows-1)
        #moving up
        if app.playerScreen.cy <= 100:
            app.topRow = max(app.topRow-1, 0)
            app.bottomRow = max(app.bottomRow-1, 10)
        checkIfKeepMoving(app)
        collectTreasure(app) 

        app.enemiesScreen = []
        for enemy in app.enemies:
            screenCx = (enemy.cx - (app.leftCol * app.cellWidth))*4
            screenCy = (enemy.cy - (app.topRow * app.cellHeight))*4
            enemyScreen = Enemy(screenCx, screenCy, 20, 0, 0)
            app.enemiesScreen.append(enemyScreen)

            dist = distance(app, app.player.cx, app.player.cy, enemy.cx, enemy.cy)
            if dist <= 75:
                enemy.isFollowing = True
                enemy.update(app)
                enemyAttack(app, enemy)
                if enemy.moveClockwise:
                    enemy.theta -= 1
                else:
                    enemy.theta += 1
            else:
                enemy.isFollowing = False
                enemy.update(app)

        app.ballsScreen = []
        for ball in app.balls:
            screenCx = (ball.x - (app.leftCol * app.cellWidth))*4
            screenCy = (ball.y - (app.topRow * app.cellHeight))*4
            ballScreen = Ball(screenCx, screenCy)
            app.ballsScreen.append(ballScreen)

            ball.move(app.player.cx, app.player.cy)
            hitRange = 12
            if (app.player.cx-ball.x)**2 + (app.player.cy-ball.y)**2 < hitRange:
                app.player.playerHealth -= 5
                app.balls.remove(ball)

    if app.playerWalking == True:
        app.pSpriteInd = (app.pSpriteInd + 1) % len(app.pWalkSprite)
runApp()