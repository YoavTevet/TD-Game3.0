import pygame
import os
from projectiles import Bullet
import math

current_path = os.path.dirname(__file__)


class TackShooter:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pic = pygame.image.load(os.path.join(current_path, "tack_shooter.png"))
        self.bullets = []
        self.lvl = 3
        self.shoot_count = 20
        self.shoot_num = 40
        self.rect = pygame.Rect(self.x + 1, self.y + 1, self.pic.get_width() - 3, self.pic.get_height() - 3)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.xvel
            bullet.y += bullet.yvel
            bullet.distance += math.sqrt(bullet.xvel ** 2 + bullet.yvel ** 2)  # pythagoras theorem
            if abs(bullet.distance) > bullet.max_distance:
                self.bullets.remove(bullet)

            bullet.rect.x, bullet.rect.y = bullet.x, bullet.y

    def shoot(self):
        # those are the bullets firing sideways. will be added at any level
        self.bullets.append(Bullet(self.x, self.y + self.pic.get_height() / 2))
        self.bullets.append(Bullet(self.x + self.pic.get_width(), self.y + self.pic.get_height() / 2, xvel=5))
        if self.lvl >= 2:  # those are the bullets moving up and down
            self.bullets.append(Bullet(self.x + self.pic.get_width() / 2, self.y, xvel=0, yvel=-5))
            self.bullets.append(Bullet(self.x + self.pic.get_width() / 2, self.y + self.pic.get_height(), xvel=0, yvel=5))
        if self.lvl >= 3:  # bullets going 'slant ways'
            self.bullets.append(Bullet(self.x, self.y, xvel=-5, yvel=-5))
            self.bullets.append(Bullet(self.x + self.pic.get_width(), self.y + self.pic.get_height(), xvel=5, yvel=5))
            self.bullets.append(Bullet(self.x, self.y + self.pic.get_height(), xvel=-5, yvel=5))
            self.bullets.append(Bullet(self.x + self.pic.get_width(), self.y, xvel=5, yvel=-5))


class Tank:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pic = pygame.image.load(os.path.join(current_path, 'tank.png'))
        self.bullets = []
        self.lvl = 1
        self.rect = pygame.Rect(self.x, self.y, self.pic.get_width(), self.pic.get_height())
        self.shoot_count = 20
        self.shoot_num = 20

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x += bullet.xvel
            bullet.y += bullet.yvel
            bullet.distance += bullet.xvel
            if abs(bullet.distance) > bullet.max_distance:
                self.bullets.remove(bullet)
            elif bullet.power < 1:
                self.bullets.remove(bullet)
            # keeping the bullet rect updated
            bullet.rect.x, bullet.rect.y = bullet.x, bullet.y

    def shoot(self):
        self.bullets.append(Bullet(self.x, self.y + self.pic.get_height() / 2 - 3))


class Sniper:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pic = pygame.image.load(os.path.join(current_path, 'tank_pic.png'))
        self.bullets = []
        self.rect = pygame.Rect(self.x, self.y, self.pic.get_width(), self.pic.get_height())
        self.shoot_count = 20
        self.shoot_num = 20

    def shoot(self, char):
        x_gap = self.rect.centerx - char.rect.centerx
        y_gap = self.rect.centery - char.rect.centery
        distance = math.sqrt((self.rect.centerx - char.rect.centerx) ** 2 + (self.rect.centery - char.rect.centery) ** 2)
        stops = (distance / 16)

        self.bullets.append(Bullet(self.x, self.rect.centery, max_distance=distance, xvel=x_gap / stops, yvel=y_gap / stops))

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.x -= bullet.xvel
            bullet.y -= bullet.yvel
            bullet.distance += abs(math.sqrt(bullet.xvel ** 2 + bullet.yvel ** 2))
            bullet.rect.x, bullet.rect.y = bullet.x, bullet.y

            if bullet.max_distance < bullet.distance:
                self.bullets.remove(bullet)
