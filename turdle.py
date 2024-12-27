import pygame
import random
import time

pygame.init()

win = pygame.display.set_mode((500, 600))
pygame.display.set_caption("TURDLE")

a = pygame.image.load('shit.png')
pygame.display.set_icon(a)

cog = pygame.transform.scale(pygame.image.load('cog.png').convert_alpha(), (30, 30))

font = pygame.font.SysFont('Calibri', 50, bold=True)
letterFont = pygame.font.SysFont('Calibri', 40, bold=True)
endFont = pygame.font.SysFont('Calibri', 30, bold=True)
settingFont = pygame.font.SysFont('Calibri', 20, bold=True)

word = ""
selectedBox = 0
selectedRow = 0

incorrectTimer = 0
finished = False

customWords = False

mouseDown = False

settingsMenu = False

letters = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
]   

validWords = []

with open("words.txt") as w:
    validWords = w.readlines()

for i in range(len(validWords)):
    validWords[i] = validWords[i].rstrip('\n')

possibleWords = []

with open("wordsToGuess.txt") as w:
    possibleWords = w.readlines()

for i in range(len(possibleWords)):
    possibleWords[i] = possibleWords[i].rstrip('\n')

if customWords:
    word = possibleWords[random.randint(0, len(possibleWords)-1)]
else: 
    word = validWords[random.randint(0, 1000)]

addedButton = False
addedCustomButton = False

def ConvertToWord(row):
    w = ""

    for l in letters[row]:
        w += l

    return w

def Reset():
    global letters, word, selectedBox, selectedRow, incorrectTimer, finished, startTime, endTime, buttons, addedButton, settingsMenu, addedCustomButton, customWords

    letters = [
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]
    ]   

    if customWords:
        word = possibleWords[random.randint(0, len(possibleWords)-1)]
    else: 
        word = validWords[random.randint(0, 1000)]
    selectedBox = 0
    selectedRow = 0

    incorrectTimer = 0
    finished = False

    startTime = time.time()
    endTime = 0

    addedButton = False

startTime = time.time()
endTime = 0

class Button():
    def __init__(self, x, y, w, h, col, t, text=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.text = text
        self.col = col

        self.type = t

    def Draw(self):
        global settingsMenu, buttons

        if self.type == "Play Again" and settingsMenu == True:
            return

        if not finished and self.type == "Play Again":
            buttons.remove(self)

        pygame.draw.rect(win, self.col, (self.x, self.y, self.w, self.h))

        if self.text != None:
            t = letterFont.render(self.text, True, (255, 255, 255))
            win.blit(t, (self.x + self.w/2 - letterFont.size(self.text)[0]/2, self.y + self.h/2 - letterFont.size(self.text)[1]/2))

    def Update(self):
        global mouseDown, settingsMenu

        if mouseDown:
            p = pygame.mouse.get_pos()

            if p[0] in range(self.x, self.x + self.w) and p[1] in range(self.y, self.y+self.h):
                self.Clicked()

        if self.type == "Custom Words":
            if settingsMenu == False:
                buttons.remove(self)

    def Clicked(self):
        global letters, word, selectedBox, selectedRow, incorrectTimer, finished, startTime, endTime, buttons, addedButton, settingsMenu, addedCustomButton, customWords

        if self.type == "Play Again":
            Reset()

            buttons.remove(self)

        if self.type == "Settings":
            if settingsMenu == False: 
                settingsMenu = True
                addedCustomButton = False

            else: 
                settingsMenu = False
                addedCustomButton = True

        if self.type == "Custom Words":
            if self.text == "Disabled":
                self.text = "Enabled"
                self.col = (100, 200, 100)

                customWords = True

            else:
                self.text = "Disabled"
                self.col = (200, 100, 100)

                customWords = False

            Reset()

buttons = []

finishedButton = Button(100, 475, 300, 75, (100, 200, 100), 'Play Again', text='Play Again!')
settingsButton = Button(150, 250, 200, 100, (200, 100, 100), 'Custom Words', text='Disabled')

buttons.append(Button(456, 17, 30, 30, (200, 200, 200), 'Settings'))

running = True
while running:
    win.fill((200,200,200))
    
    title = font.render('TURDLE', True, (0, 0, 0))
    win.blit(title,(250 - font.size('TURDLE')[0]/2,10))

    pygame.draw.line(win, (150, 169, 169), (0, 60), (500, 60))

    for i in range(6):
        correctCount = 0
        correctLetters = []
        wrongSpotLetters = []
        for j in range(5):
            col = (150, 150, 150)
            letterCol = (255, 255, 255)
            letterBoxCol = (75, 75, 75)
            width = 2

            if (selectedBox == j and selectedRow == i):
                col = (50, 10, 50)
                
                width = 3

            if i < selectedRow:
                if letters[i][j] == word[j]:
                    letterBoxCol = (100, 200, 100)

                    correctCount += 1
                    correctLetters.append(letters[i][j])

                elif letters[i][j] in word and word.count(letters[i][j]) > correctLetters.count(letters[i][j]) and word.count(letters[i][j]) > wrongSpotLetters.count(letters[i][j]):
                    letterBoxCol = (200, 200, 100)
                    wrongSpotLetters.append(letters[i][j])

                pygame.draw.rect(win, letterBoxCol, (100 + j*60, 195 + i*60, 50, 50))

            if letters[i][j] != 0:
                if i == selectedRow:
                    letterCol = (150, 150, 150)

                l = letterFont.render(letters[i][j].upper(), True, letterCol)
                win.blit(l, (125 + j*60 - letterFont.size(letters[i][j].upper())[0]/2, 220 + i*60 - letterFont.size(letters[i][j].upper())[1]/2))

            pygame.draw.rect(win, col, (100 + j*60, 195 + i*60, 50, 50), width)

        if selectedRow == 6 or correctCount == 5:
            finished = True
            pygame.draw.rect(win, (200, 200, 200), (50, 150, 400, 380))
            pygame.draw.rect(win, (200, 200, 200), (50, 150, 400, 300))

            if correctCount == 5:
                winFont = endFont.render(f"Congratulations!", True, (100, 100, 100))
                win.blit(winFont, (250 - endFont.size('Congratulations!')[0]/2, 100))

            else:
                winFont = endFont.render(f"Try again", True, (100, 100, 100))
                win.blit(winFont, (250 - endFont.size('Try again')[0]/2, 100))

            winFont = endFont.render(f"The word was:", True, (100, 100, 100))
            win.blit(winFont, (250 - endFont.size('The word was:')[0]/2, 175))
            winFont = endFont.render(word, True, (100, 100, 100))
            win.blit(winFont, (250 - endFont.size(word)[0]/2, 225))

            if endTime == 0:
                endTime = time.time()

            winFont = endFont.render(f"You finished in {int(endTime-startTime)} seconds!", True, (100, 100, 100))
            win.blit(winFont, (250 - endFont.size(f"You finished in {int(endTime-startTime)} seconds!")[0]/2, 300))

            winFont = endFont.render(f"It took you {selectedRow} tries!", True, (100, 100, 100))
            win.blit(winFont, (250 - endFont.size(f"It took you {selectedRow} tries!")[0]/2, 350))

            break

    if incorrectTimer > 0:
        incorrectTimer -= 1

        winFont = endFont.render(f"Not a real word!", True, (100, 100, 100))
        win.blit(winFont, (250 - endFont.size('Not a real word!')[0]/2, 100))

    if finished:
        if not addedButton:
            buttons.append(finishedButton)
            addedButton = True   

    if settingsMenu:
        pygame.draw.rect(win, (100, 100, 100), (50, 100, 400, 450))

        s = letterFont.render(f"Settings", True, (250, 250, 250))
        win.blit(s, (250 - letterFont.size('Settings')[0]/2, 130))

        s = settingFont.render(f"CUSTOM WORDS", True, (250, 250, 250))
        win.blit(s, (250 - settingFont.size('CUTSOM WORDS')[0]/2, 200))

        if not addedCustomButton:
            buttons.append(settingsButton)
            addedCustomButton = True

    for b in buttons:
        b.Draw()

    win.blit(cog, (456, 15, 30, 30), special_flags=pygame.BLEND_PREMULTIPLIED)

    pygame.display.update()

    mouseDown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if 97 <= event.key <= 122:
                if selectedBox < 5:
                    letters[selectedRow][selectedBox] = event.unicode
                    selectedBox += 1

                    if selectedBox == 5: selectedBox = 4
            else:
                if event.key == 8:
                    if letters[selectedRow][4] == 0: 
                        selectedBox -= 1
                    
                    letters[selectedRow][selectedBox] = 0
                    
                    if selectedBox == -1: selectedBox = 0

                if event.key == 13 and letters[selectedRow][4] != 0:
                    guess = ConvertToWord(selectedRow)

                    if guess in validWords:
                        selectedRow += 1
                        selectedBox = 0
                    else: incorrectTimer = 2000

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True

            if finished:
                if event.pos[0] in range(100, 400) and event.pos[1] in range(475, 550):
                    letters = [
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]
                    ]   

                    word = "penis"
                    selectedBox = 0
                    selectedRow = 0

                    incorrectTimer = 0
                    finished = False

    for b in buttons:
        b.Update()