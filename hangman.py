import pygame
import random

pygame.init()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
YELLOW = (255, 255, 0)

# Load the background image
background = pygame.image.load('background.jpg')  # Replace 'background_image.jpg' with the filename of your background image

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
hint_font = pygame.font.SysFont('arial', 30)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'),
               pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'),
               pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'),
               pygame.image.load('hangman6.png')]

limbs = 0
hint = ''
tries_left = 7


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    global hint
    global tries_left

    # Draw the background image
    win.blit(background, (0, 0))
    

    # Draw buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, WHITE, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, WHITE)
    rect = label1.get_rect()
    length = rect[2]

    win.blit(label1, (winWidth / 2 - length / 2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))

    # Display the hint
    hint_label = hint_font.render("Hint: " + hint, 1, WHITE)
    win.blit(hint_label, (20, 150))

    # Display tries left
    tries_label = hint_font.render("Tries left: " + str(tries_left), 1, WHITE)
    win.blit(tries_label, (550, 125))

    pygame.display.update()


def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    word_hint = f[i][:-1].split(',')
    return word_hint[0], word_hint[1]


def hang(guess):
    global word
    global tries_left
    if guess.lower() not in word.lower():
        tries_left -= 1
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return i
    return None


def end(winner=False):
    global limbs
    global guessed
    global tries_left

    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'

    redraw_game_window()
    pygame.time.delay(500)

    if winner:
        label = lost_font.render(winTxt, 1, BLACK)
        win.fill(GREEN)
        wordTxt = lost_font.render(word.upper(), 1, BLACK)
        wordWas = lost_font.render('The word was: ', 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, WHITE)
        win.fill(RED)
        wordTxt = lost_font.render(word.upper(), 1, WHITE)
        wordWas = lost_font.render('The word was: ', 1, WHITE)

    win.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    global hint
    global tries_left

    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word, hint = randomWord()
    tries_left = 7


increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([YELLOW, x, y, 20, True, 65 + i])

word, hint = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
            elif pygame.K_a <= event.key <= pygame.K_z:
                letter = chr(event.key).upper()
                if letter not in guessed:
                    guessed.append(letter)
                    button_index = ord(letter) - 65
                    buttons[button_index][4] = False
                    if hang(letter):
                        if limbs != 6:
                            limbs += 1
                        else:
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            button_index = buttonHit(clickPos[0], clickPos[1])
            if button_index is not None:
                letter = chr(buttons[button_index][5])
                if letter not in guessed:
                    guessed.append(letter)
                    buttons[button_index][4] = False
                    if hang(letter):
                        if limbs != 6:
                            limbs += 1
                        else:
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)

pygame.quit()

