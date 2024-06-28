"""
Author: Darrien Guan and Agilan Hariharan
Last Modified: December 14, 2023
Creation date: December 11, 2023
Description: Sprites for Break-Out game.
"""

import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("game_assets/diamond.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, screen.get_height()/2)
        self.speed = [1, 1]

    def update(self, screen):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.screen = screen

        # Bounces off of the Walls accounting for ball radius
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed[0] = -self.speed[0]  # Reverse only the x-component
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]  # Reverse only the y-component

    def collision(self):
    
        # Calculate the direction of the ball's movement
        if self.speed[0] > 0:
            x_direction = 1 
        else: 
            x_direction = -1

        if self.speed[1] > 0:
            y_direction = 1
        else:
            y_direction = -1

        # Bounce off other sprite, maintaining forward direction
        if abs(self.speed[0]) > abs(self.speed[1]):
            # If the ball is moving more horizontally, reverse the x-direction
            self.speed[0] = abs(self.speed[0]) * -x_direction
            self.speed[1] = abs(self.speed[1]) * y_direction
        else:
            # If the ball is moving more vertically, reverse the y-direction
            self.speed[0] = abs(self.speed[0]) * x_direction
            self.speed[1] = abs(self.speed[1]) * -y_direction

        # Move the ball away from the collided sprite
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def reset(self):
        self.rect.center = (self.screen.get_width()/2, self.screen.get_height()/2)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("game_assets/paddle.jpg")
        self.image = pygame.transform.scale(self.image, (100,20))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen.get_width()/2, screen.get_height()-20)

    def play_sound(self):
        """Plays random paddle bouncing sound whenever method is used."""
        bounce_sounds = random.choice(["Amethyst_Cluster_break1","Amethyst_Cluster_break2","Amethyst_Cluster_break3","Amethyst_Cluster_break4"])
        paddle_sfx = pygame.mixer.Sound("audio/paddle/"+bounce_sounds+".ogg")
        paddle_sfx.play()

    def update(self, screen):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= 2
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 900:
            self.rect.x += 2
            
    def reset(self, screen):
        """resets paddle to original position"""
        self.rect.midbottom = (screen.get_width()/2, screen.get_height()-20)

class Brick(pygame.sprite.Sprite):
    def __init__(self, colour, row, col):
        pygame.sprite.Sprite.__init__(self)

        self.colour_dict = {"PURPLE": (148,0,211), "RED": (255,0,0), "YELLOW": (255, 255, 0), 
                           "ORANGE":(255,69,0), "GREEN":(0,255,0), "BLUE":(0,0,255)}

        self.point_dict = {"PURPLE": 6, "RED": 5, "YELLOW": 4, 
                           "ORANGE": 3, "GREEN": 2, "BLUE": 1}
        
        self.brick_file_dict = {"PURPLE": "brick_img/violet_brick.jpeg", "RED": "brick_img/red_brick.jpeg", "YELLOW": "brick_img/yellow_brick.jpeg", 
                                "ORANGE": "brick_img/orange_brick.jpeg", "GREEN": "brick_img/green_brick.jpeg", "BLUE": "brick_img/blue_brick.jpeg"}

        if colour in self.colour_dict:
            self.rgb_colour = self.colour_dict[colour]

        if colour in self.point_dict:
            self.point_value = self.point_dict[colour]
        
        if colour in self.brick_file_dict:
            self.image_texture = self.brick_file_dict[colour]

        # Set image attributes
        self.image = pygame.image.load(self.image_texture)
        self.image = self.image.convert()

        # Get rect attributes
        self.rect = self.image.get_rect()

        self.rect.left = col * 50
        self.rect.top = row * 20

    def play_sound(self):
        self.sound_dict = {1:"audio/reg_note.mp3", 2:"audio/ice_note.mp3", 3:"audio/guitar_note.mp3", 4:"audio/flute_note.mp3", 5:"audio/bell_note.mp3", 6:"audio/bass_note.mp3"}

        if self.point_value in self.sound_dict:
            self.sound_sfx = pygame.mixer.Sound(self.sound_dict[self.point_value])
        
        self.sound_sfx.play()

    def points(self):
        return self.point_value

class Lava(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        '''Generates lava on the bottom of the window.'''
        pygame.sprite.Sprite.__init__(self)

        # Load lava image
        self.image = pygame.image.load("game_assets/lava.png")
        self.image = pygame.transform.scale(self.image, (screen.get_width(), 35))  # Adjust the size of the lava image

        # Set the initial position
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_height()  # Set the lava at the bottom of the screen

class Hearts(pygame.sprite.Sprite):
    
    def __init__(self, screen, heart_pos):
        """Generates hearts on top right"""
        pygame.sprite.Sprite.__init__(self)
        
        # Load heart image
        self.image = pygame.image.load("game_assets/heart.png")
        self.image = self.image.convert_alpha()
        
        # Set the intital positions
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen.get_width() - 50 - heart_pos*45, 5)
        
    def empty_heart(self, screen):
        """turns heart to empty heart"""
        
        # Load empty heart image
        self.image = pygame.image.load("game_assets/empty_heart.png")
        self.image = self.image.convert_alpha()