#!/usr/bin/env python
# -------------------imports------------------------#
import pygame
import random
from pygame.locals import *
from sys import exit
# -------------------------classes---------------------------#
class Game:
    def __init__(self):
        self.name = "Emily"
        self.rungame = False
        self.highscore = 0
        self.swordlvl = 1
        self.swordcost = 20
        self.coins = 0
        self.guild = False
        self.lives = 3
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.gamefill = pygame.image.load("imgs/game_fill.png")
        self.menufill = pygame.image.load("imgs/menufill.png")
        self.clock = pygame.time.Clock()
        self.enemytimer = 3000
        self.cointimer = 3000
        self.fps = 60
        self.smallfont = pygame.font.Font(None, 24)
        self.bigfont = pygame.font.Font(None, 48)
        self.acc = [0, 0]

    def button(self, msg, x, y, w, h, ic, ac, size=1, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()

        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        if size == 1:
            text = self.smallfont.render(msg, True, (255, 255, 255))
        else:
            text = self.bigfont.render(msg, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text, textRect)

    def swrdlvlup(self):
        if self.coins >= self.swordcost:
            self.coins -= self.swordcost
            self.swordlvl += 1
            self.swordcost = 20 + 5 * self.swordlvl

    def joinguild(self):
        self.guild = True

    def startgame(self):
        self.rungame = True

    def showtext(self, msg, x, y, variable=None):
        if variable != None:
            text = self.smallfont.render(msg + str(variable), True, (255, 255, 255))
        else:
            text = self.smallfont.render(msg, True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.topright = [x, y]
        self.screen.blit(text, textrect)


class Hearts:
    def __init__(self):
        self.img = pygame.image.load("imgs/heart.png")
        self.number = 3

    def show_health(self):
        if self.number >= 1:
            game.screen.blit(self.img, (575, 15))
            if self.number >= 2:
                game.screen.blit(self.img, (595, 15))
                if self.number == 3:
                    game.screen.blit(self.img, (615, 15))


class Player:
    def __init__(self):
        self.img = pygame.image.load("imgs/player_ng.png")
        self.x = 25
        self.y = 100
        self.vel = 7

    def draw(self):
        game.screen.blit(self.img, (self.x, self.y))
        sword.move()

    def move(self):
        if key_state[0]:
            if self.y - self.vel >= 0:
                self.y -= self.vel
            else:
                self.y = 0

        elif key_state[1]:
            if self.y + self.vel <= 430:
                self.y += self.vel
            else:
                player.y = 430

    def playerrect(self):
        playrect = pygame.Rect(player.img.get_rect())
        playrect.left = player.x
        playrect.top = player.y
        return playrect


class Sword:
    def __init__(self):
        self.img = pygame.image.load("imgs/sword1.png")
        self.x = player.x
        self.y = player.y
        self.vel = 7
        self.throws = []

    def draw(self):
        for i in self.throws:
            game.screen.blit(self.img, (i[0], i[1]))

    def throw(self):
        for projectile in self.throws:
            if projectile[0] < 640:
                projectile[0] += self.vel
            else:
                self.throws.pop(self.throws.index(projectile))

            self.draw()

    def move(self):
        game.screen.blit(self.img, (player.x + 45, player.y + 25))


class Enemy:
    def __init__(self):
        self.img = pygame.image.load("imgs/zom1-1.png")
        self.x = 640
        self.y = 100
        self.vel = 1
        self.level = 1
        self.enemies = [[self.x, self.y, self.level]]

    def new(self):
        self.y = random.randint(50, 430)
        self.enemies.append([self.x, self.y, self.level])

    def levelup(self):
        self.level += 1
        self.vel += 0.5
        player.vel += 0.5
        if self.level == 2:
            enemy.img = pygame.image.load("imgs/zom2-1.png")
        elif self.level >= 2:
            enemy.img = pygame.image.load("imgs/zom3-1.png")


class Coin:
    def __init__(self):
        self.img = pygame.image.load("imgs/coin.png")
        self.x = 640
        self.y = 100
        self.vel = 2
        self.coins = [[640, 300]]

    def new(self):
        self.y = random.randint(50, 430)
        self.coins.append([self.x, self.y])


# -------------------------main code----------------------------#
pygame.init()
game = Game()  # initialize game/user
initialized = True

while initialized:

    while not game.rungame:

        game.screen.fill(0)
        game.screen.blit(game.menufill, (0, 0))

        # colors
        darkgrey = (169, 169, 169)
        grey = (192, 192, 192)

        # join guild box
        game.button("Join Guild", 75, 175, 150, 50, darkgrey, grey, action=game.joinguild)
        if not game.guild:
            game.showtext("No Guild.", 185, 230)
        else:
            game.showtext("Guild Joined!", 205, 230)

        # upgrade sword box
        game.button("Upgrade Sword", 410, 175, 150, 50, darkgrey, grey, action=game.swrdlvlup)
        game.showtext("Sword Level: ", 540, 230, game.swordlvl)
        game.showtext("Cost: ", 530, 150, game.swordcost)

        # play game box
        game.button("Play Game!", 205, 300, 225, 100, darkgrey, grey, size=2, action=game.startgame)

        game.showtext("Coins: ", 590, 15, game.coins)  # coin count

        game.showtext("High Score: ", 125, 15, game.highscore)  # high score

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # screen refresh
        pygame.display.flip()
        game.clock.tick(game.fps)

    # run game
    if game.rungame:

        # reset game
        game.acc = [0, 0]

        # Initialize classes:
        health = Hearts()
        player = Player()
        sword = Sword()
        enemy = Enemy()
        coin = Coin()

        # game states
        key_state = [False, False]  # w, s keys (up, down)

        if game.guild:
            player.img = pygame.image.load('imgs/player_g.png')

        if game.swordlvl == 2:
            sword.img = pygame.image.load('imgs/sword2.png')
        elif game.swordlvl >= 3:
            sword.img = pygame.image.load('imgs/sword3.png')

        while game.rungame:
            # set timers
            game.enemytimer -= random.randint(0, 100)
            game.cointimer -= random.randint(0, 100)

            # clear the screen before drawing it again
            game.screen.fill(0)
            game.screen.blit(game.gamefill, (0, 0))

            # draw the screen elements
            player.draw()

            # throwing swords
            sword.throw()

            # --------enemies---------#
            if game.enemytimer <= 0:
                enemy.new()
                game.enemytimer = 4000

            # handle collisions
            for e in enemy.enemies:
                enemyrect = pygame.Rect(enemy.img.get_rect())
                enemyrect.left = e[0]
                enemyrect.top = e[1]

                if enemyrect.left <= 0:
                    health.number -= 1
                    enemy.enemies.pop(enemy.enemies.index(e))

                if enemyrect.colliderect(player.playerrect()):
                    enemy.enemies.pop(enemy.enemies.index(e))
                    health.number -= 1

                for throw in sword.throws:
                    swordrect = pygame.Rect(sword.img.get_rect())
                    swordrect.left = throw[0]
                    swordrect.top = throw[1]
                    if enemyrect.colliderect(swordrect):
                        sword.throws.pop(sword.throws.index(throw))
                        e[2] -= game.swordlvl
                        if e[2] <= 0:
                            game.acc[0] += 1
                            enemy.enemies.pop(enemy.enemies.index(e))
                            if game.acc[0] % 15 == 0:
                                enemy.levelup()

                e[0] -= enemy.vel

            for e in enemy.enemies:
                game.screen.blit(enemy.img, (e[0], e[1]))

            # --------coins----------#
            if game.cointimer <= 0:
                coin.new()
                game.cointimer = 5000

            # handle collisions
            for c in coin.coins:

                coinrect = pygame.Rect(coin.img.get_rect())
                coinrect.left = c[0]
                coinrect.top = c[1]

                if coinrect.left <= 0:
                    coin.coins.pop(coin.coins.index(c))

                if coinrect.colliderect(player.playerrect()):
                    coin.coins.pop(coin.coins.index(c))
                    game.coins += 1

                c[0] -= coin.vel

            for c in coin.coins:
                game.screen.blit(coin.img, c)

            # ---------screen-------#
            # Show text
            game.showtext("Enemies Eliminated: ", 175, 15, game.acc[0])
            game.showtext("Coins: ", 350, 15, game.coins)
            game.showtext("Health:", 550, 15)
            health.show_health()
            if health.number <= 0:
                if game.acc[0] > game.highscore:
                    game.highscore = game.acc[0]
                game.rungame = False

            # update the screen
            pygame.display.flip()
            # loop through the events
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # event handler
                if event.type == pygame.KEYDOWN:

                    if event.key == K_w:
                        key_state[0] = True
                    elif event.key == K_s:
                        key_state[1] = True

                    # throwing the sword
                    if event.key == K_SPACE:
                        game.acc[1] += 1
                        if len(sword.throws) < 5:
                            sword.throws.append([player.x + 35, player.y + 25])

                elif event.type == pygame.KEYUP:

                    if event.key == K_w:
                        key_state[0] = False
                    elif event.key == K_s:
                        key_state[1] = False

            # Move player based on list of key_states
            player.move()

            game.clock.tick(game.fps)
