"""
Author: Darrien Guan and Agilan Hariharan
Last Modified: December 14, 2023
Creation date: December 11, 2023
Description: Sprites for Break-Out game.
"""

# I - Import and Initialize - Start IDEA
import pygame
import breakoutSprites
pygame.init()
pygame.mixer.init()

# D - Display configuration
screen = pygame.display.set_mode((900, 480))
pygame.display.set_caption("Super Breakout")

def create_bricks():
    """Function creates bricks for game"""
    bricks = pygame.sprite.Group()

    for i in range(18):
        bricks.add(breakoutSprites.Brick("PURPLE",5,i))
        bricks.add(breakoutSprites.Brick("RED",6,i))
        bricks.add(breakoutSprites.Brick("YELLOW",7,i))
        bricks.add(breakoutSprites.Brick("ORANGE",8,i))
        bricks.add(breakoutSprites.Brick("GREEN",9,i))
        bricks.add(breakoutSprites.Brick("BLUE",10,i))

    return bricks

def create_hearts():
    """Function creates hearts for game."""
    hearts_sprites = pygame.sprite.Group()
    
    for heart_pos in range(3):
        hearts_sprites.add(breakoutSprites.Hearts(screen, heart_pos))

    return hearts_sprites

def main():
    
    # E - Entities
    background = pygame.image.load("game_assets/background.jpeg")
    background = pygame.transform.scale(background, screen.get_size())
    background = background.convert()

    # Load Sounds/music
    damage_sfx = pygame.mixer.Sound("audio/damage.ogg")
    pygame.mixer.music.load("audio/background_music.ogg")
    
    all_sprites = pygame.sprite.Group()

    ball = breakoutSprites.Ball(screen)
    paddle = breakoutSprites.Paddle(screen)
    lava = breakoutSprites.Lava(screen)
    
    # Create bricks and hearts for game
    bricks = create_bricks()
    hearts_sprites = create_hearts()

    # Background music
    pygame.mixer.music.play(-1, 0.0)
    
    # Add all sprites to all_sprites list
    all_sprites.add(ball, lava, paddle)
    
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    score = 0
    hearts_remaining = 3
    win_status = None
    start_stat = False # Users have to press

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate (Darrien has a 240 fps monitor so its 240 fps)
        clock.tick(240)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    start_stat = True

            if event.type == pygame.KEYDOWN and win_status == False:
                if event.key == pygame.K_q:
                    hearts_remaining = 3
                    win_status = None
                    score = 0

                    # Reset game stats and sprites
                    bricks = create_bricks()
                    paddle.reset(screen)
                    hearts_sprites = create_hearts()
                    ball.reset()
        
        # Win_status setter
        if hearts_remaining == 0:
            win_status = False
            
        if score >= 378:
            win_status = True
        
        # Only continue game if damged is false
        if start_stat == True:
            # Update your sprites
            all_sprites.update(screen)
            
            if score >= 378:
                win_status = True

            if win_status == None:
                
                # Reset ball if it goes below the lava
                if ball.rect.top > 440:
                    damage_sfx.play()
                    heart_sprite = hearts_sprites.sprites()[hearts_remaining-1]
                    heart_sprite.empty_heart(screen)
                    hearts_remaining -= 1
                    start_stat = False
                    
                    # reset ball and paddle position
                    paddle.reset(screen)
                    ball.reset()
                
                # Check for collisions
                bounces = pygame.sprite.spritecollide(ball, bricks, True)
                for bounce in bounces:
                    score += bounce.points()
                    ball.collision()
                    bounce.play_sound()

                # Bounce ball off paddle
                if pygame.sprite.collide_rect(ball, paddle):
                    paddle.play_sound()
                    ball.speed[1] = -ball.speed[1]

        # R - Refresh display
        screen.blit(background, (0,0))
        
        if win_status == None:
            all_sprites.draw(screen)
            bricks.draw(screen)

        # Display score
        font = pygame.font.Font("game_assets/minecraft_font.otf", 40)
        white = (255, 255, 255)
        score_text = font.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))
        hearts_sprites.draw(screen)
        
        # Check if all bricks are destroyed
        if win_status == True:
            font = pygame.font.Font("game_assets/minecraft_font.otf", 69)
            white = (255, 255, 255)
            score_text = font.render("YOU WIN!", True, white)
            screen.blit(score_text, (screen.get_width()/2 - (score_text.get_width()/2), screen.get_height()/2 - (score_text.get_height()/2)))
        
        elif win_status == False:
            font = pygame.font.Font("game_assets/minecraft_font.otf", 69)
            white = (255, 255, 255)
            score_text = font.render("YOU LOST!", True, white)
            screen.blit(score_text, (screen.get_width()/2 - (score_text.get_width()/2), screen.get_height()/2 - (score_text.get_height()/2)))

        pygame.display.flip()

    # Close the game window, set the X
    pygame.quit()
    
main()