# group members
# {fronda, grafil, lopez, pael, punzalan, salvador}
import sys
import pygame
import random
from pygame import mixer

mixer.init()
mixer.music.load('BienAssets/song5.mp3')
mixer.music.play(-1)
SC_Z = 640, 480  # screen size
# IMAGES
BGM = pygame.image.load('DMPassets/BGM1.jpeg')
BGM1 = pygame.image.load('DMPassets/NIGHTMODE.JPG')
BGM2 = pygame.image.load('DMPassets/NIGHTANGLE.png')
BGM3 = pygame.image.load('DMPassets/NIGHTNIGHT.png')
BGMS = pygame.image.load('DMPassets/space.jpg')
icon_app = pygame.image.load('DMPassets/Title.png')

pygame.display.set_icon(icon_app)
BALL_ICON = pygame.image.load('BALL.png')
PADDLE_IMAGE = pygame.image.load('DMPassets/100X15PADDLE.png')
# Object of dimensions
BK_W = 60  # brick width
BK_H = 15  # brick height
P_W = 100  # paddle width
P_H = 15  # paddle height
BL_D = 20  # ball diameter
BL_R = BL_D / 2  # ball radius
MX_P_X = SC_Z[0] - P_W  # MAX PADDLE X
MX_BL_X = SC_Z[0] - BL_D  # MAX BALL X
MX_BL_Y = SC_Z[1] - BL_D  # MAX BALL Y
# Paddle Y coordinate
P_Y = SC_Z[1] - P_H - 25  # PADDLE Y
# Color of a constants
BLK = (0, 0, 0)  # BLACK
W = (255, 255, 255)  # WHITE
L_E = (0, 0, 205)  # DARK BLUE
# State of the constants
S_BIP = 0  # BALL IN PADLE
S_P = 1  # PLAYING
S_W = 2  # WON
S_G_O = 3  # GAME OVER
S_N_L = 4  # NEXT LEVEL
S_PS = 5  # PAUSE

# class of power ups
# Constants for power-up dimensions
POWER_WIDTH = 20
POWER_HEIGHT = 20


# PowerUp Class Definition
class PowerUp(pygame.Rect):
    def __init__(self, x, y, color):
        super().__init__(x, y, POWER_WIDTH, POWER_HEIGHT)
        self.color = color
        self.falling_speed = 2  # The speed at which the power-up falls

    # Define a new move method specifically for PowerUp
    def move_powerup(self):
        self.y += self.falling_speed


# class of the game
class Shatterdart:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SC_Z)
        pygame.display.set_caption("SHATTERDART 2.1")
        self.clock = pygame.time.Clock()
        self.powerup_respawn_timer = 0  # Initialize the power-up respawn timer

        self.power_ups = []  # Initialize the power-up list

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None
        # These define the initial constants at the very beginning and they are never resetted.
        self.lives = 3
        self.level = 1
        self.score = 0
        self.Paddle_Speed = 18
        # Load brick images
        self.brick_images = {
            1: pygame.image.load('bricks_icon/YELLOW.png'),
            2: pygame.image.load('bricks_icon/RED.png'),
            3: pygame.image.load('bricks_icon/BLUE.png'),
            4: pygame.image.load('bricks_icon/ORANGE.png'),
            5: pygame.image.load('bricks_icon/GREEN.png'),
            6: pygame.image.load('bricks_icon/PINK.png'),
            7: pygame.image.load('bricks_icon/PURPLE.png'),
        }
        # Define scores for each level
        self.brick_scores = {
            1: 3,  # Example score for level 1
            2: 5,  # Example score for level 2
            3: 8,  # Example score for level 3
            4: 10,  # Example score for level 4
            5: 15,  # Example score for level 5
        }

        self.init_game()

    def init_game(self):
        self.state = S_BIP
        self.paddle = pygame.Rect(300, P_Y, P_W, P_H)
        self.ball = pygame.Rect(300, P_Y - BL_D, BL_D, BL_D)
        if self.level == 1:
            self.ball_vel = [8, -8]
        elif self.level == 2:
            self.ball_vel = [8.5, -8.5]
        elif self.level == 3:
            self.ball_vel = [9, -9]
        elif self.level == 4:
            self.ball_vel = [11, -11]
        elif self.level == 5:
            self.ball_vel = [13, -13]
        else:
            self.ball_vel = [15, -15]
        self.create_bricks()

    def create_bricks(self):
        y_ofs = 60
        self.bricks = []
        for i in range(7):
            x_ofs = 30
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs, y_ofs, BK_W, BK_H))
                x_ofs += BK_W + 14
            y_ofs += BK_H + 10

    def draw_bricks(self):
        for brick in self.bricks:
            # Get the brick image for the current level
            brick_image = self.brick_images[self.level]
            self.screen.blit(brick_image, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.left -= self.Paddle_Speed
            if self.paddle.left < 0:
                self.paddle.left = 0
        if keys[pygame.K_RIGHT]:
            self.paddle.left += self.Paddle_Speed
            if self.paddle.left > MX_P_X:
                self.paddle.left = MX_P_X
        if keys[pygame.K_SPACE] and self.state == S_BIP:
            self.ball_vel = self.ball_vel
            self.state = S_P
        elif keys[pygame.K_RETURN] and self.state == S_N_L:
            self.level += 1
            self.init_game()
            self.level_difficulty()
        elif keys[pygame.K_RETURN] and (self.state == S_G_O or self.state == S_W):
            self.init_game()
            self.lives = 3
            self.score = 0
            self.level = 1
            self.Paddle_Speed = 20
            self.ball_vel = [7, -7]
        if len(self.bricks) == 0:
            self.state = S_N_L
        if keys[pygame.K_SPACE] and self.ball.top > self.paddle.top:
            if self.state == S_G_O and self.lives > 0:
                self.state = S_BIP
            else:
                self.state = S_G_O

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]
        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MX_BL_X:
            self.ball.left = MX_BL_X
            self.ball_vel[0] = -self.ball_vel[0]
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MX_BL_Y:
            self.ball.top = MX_BL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                # Get the score for the current level, defaulting to 16 if the level is beyond the defined scores
                score_for_brick = self.brick_scores.get(self.level, 16)
                self.score += score_for_brick
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break  # Only remove one brick per collision

                # Spawn a power-up at the brick's position

        # Paddle collision
        if self.ball.colliderect(self.paddle):
            self.ball.top = P_Y - BL_D
            self.ball_vel[1] = -self.ball_vel[1]


        # Ball falls below paddle
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = S_BIP
            elif self.lives == 0 and self.score >= 1500:
                self.state = S_W
            elif self.lives == 0 and self.score < 1500:
                self.state = S_G_O

    # power ups

    # Call this method in your game loop to handle power-up movement and activation
    def handle_powerups(self):
        for power_up in self.power_ups[:]:  # Iterate over a copy of the list
            power_up.move_powerup()
            # Draw the power-up
            pygame.draw.rect(self.screen, power_up.color, power_up)
            # Remove power-up if it falls off the screen
            if power_up.y > SC_Z[1]:
                self.power_ups.remove(power_up)
            # Check for collision with paddle
            elif power_up.colliderect(self.paddle):
                self.activate_powerup(power_up)

    # Define the method to activate a power-up
    def activate_powerup(self, power_up):
        # Example activation: extend the paddle
        self.extend_paddle()

    # Method to extend the paddle
    def extend_paddle(self):
        self.paddle.inflate_ip(20, 0)  # Increase paddle width by 20
        # Set a timer to deactivate the power-up effect after a certain duration
        self.paddle_extend_active = True
        self.paddle_extend_timer = pygame.time.get_ticks()

    def power_up(self):
        self.powerup_width = 20
        self.powerup_height = 20
        self.powerup_x = random.randint(0, 640 - self.powerup_width)
        self.powerup_y = 50
        self.paddleExtend_Active = False
        self.paddleExtend_timer = 0
        self.shield_timer = 0

        self.collision_powerup = (
                self.paddle.left < self.powerup_x + self.powerup_width and
                self.paddle.right > self.powerup_x and
                self.paddle.top < self.powerup_y + self.powerup_height and
                self.paddle.bottom > self.powerup_y
        )

        if self.collision_powerup:
            self.powerup_x = random.randint(0, 640 - self.powerup_width)
            self.powerup_y = 50
            self.paddleExtend_Active = True
            self.paddleExtend_timer = pygame.time.get_ticks()

        if self.paddleExtend_Active:
            current_time = pygame.time.get_ticks()
            if current_time - self.paddleExtend_timer > 5000:
                self.paddleExtend_Active = False

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.powerup_x, self.powerup_y, self.powerup_width, self.powerup_height))

        if not self.paddleExtend_Active:
            current_time = pygame.time.get_ticks()
            if current_time - self.powerup_respawn_timer > 3000:
                self.powerup_x = random.randint(0, 640 - self.powerup_width)
                self.powerup_y = 50
                self.powerup_respawn_timer = pygame.time.get_ticks()  # Update the timer

    def level_difficulty(self):
        if self.level == 2:
            self.Paddle_Speed = 16
            self.ball_vel = [8, -8]
            self.lives += 3
        elif self.level == 3:
            self.Paddle_Speed = 14
            self.ball_vel = [8.5, -8.5]
            self.lives += 2
        elif self.level == 4:
            self.Paddle_Speed = 12
            self.ball_vel = [9, -9]
            self.lives += 2
        elif self.level == 5:
            self.paddle_speed = 10
            self.ball_vel = [11, -11]
            self.lives += 1
        elif self.level == 6:
            self.paddle_speed = 10
            self.ball_vel = [13, -13]
            self.lives += 1
        else:
            self.Paddle_Speed = 8
            self.ball_vel = [15, -15]
            self.lives += 1

    def show_stats(self):
        frame_image = pygame.image.load('DMPassets/frame_image.PNG')
        if self.font:
            score_text = " SCORE: " + str(self.score)
            lives_text = " LIVES: " + str(self.lives)
            level_text = " LEVEL: " + str(self.level)
            stats_text = score_text.ljust(15) + lives_text.ljust(15) + level_text
            font_surface = self.font.render(stats_text, True, W)
            text_rect = font_surface.get_rect(center=(SC_Z[0] // 2, 25))
            self.screen.blit(frame_image, (0, 0))
            self.screen.blit(font_surface, text_rect)

    def show_message(self, message):
        if self.font:
            font_surface = self.font.render(message, True, W)
            text_rect = font_surface.get_rect(
                center=(SC_Z[0] // 2, SC_Z[1] // 1.6))  # Adjust the divisor here to move the text lower
            self.screen.blit(font_surface, text_rect)

    def show_menu(self):
        menu_font = pygame.font.Font(None, 36)
        credits_font = pygame.font.Font(None, 16)
        title_font = pygame.font.Font(None, 72)
        selected_item = 0
        menu_background = pygame.image.load('JioAssets/neoncitybg.png')  # Load your menu background image

        while True:
            self.screen.blit(menu_background, (0, -50))  # Display the menu background

            # Title text
            title_text = title_font.render("SHATTERDART", True, W)
            title_rect = title_text.get_rect(center=(SC_Z[0] / 2, 100))
            self.screen.blit(title_text, title_rect)

            # Credits text
            credit_text = credits_font.render("Brought to you by PyGroup 2 - CS2C", True, W)
            credit_rect = credit_text.get_rect(center=(SC_Z[0] - 540, 8))
            self.screen.blit(credit_text, credit_rect)

            for i, item in enumerate(['Start', 'Songs', 'Exit']):
                if i == selected_item:
                    text = menu_font.render('> ' + item, True, W)
                else:
                    text = menu_font.render(item, True, W)
                text_rect = text.get_rect(center=(SC_Z[0] / 2, SC_Z[1] / 2 + i * 50))
                self.screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % 3
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % 3
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:  # Start Game selected
                            self.run_game()
                        elif selected_item == 1:  # Open settings
                            Shatterdart.settings_menu(self)


                        elif selected_item == 2:  # Exit selected
                            pygame.quit()
                            sys.exit()

            pygame.display.update()

    def settings_menu(self):
        menu_font = pygame.font.Font(None, 36)
        selected_item = 0
        settings = True
        screen = pygame.display.set_mode(SC_Z)
        settings_bg = pygame.image.load('JioAssets/neoncitybg.png')  # Load your settings background image

        while settings:
            screen.blit(settings_bg, (0, -50))  # Display the settings background

            for i, item in enumerate(
                    ['Back', 'Extraterrestrial', 'Star Wars theme', 'Stay at your house', 'Powerwalkin', 'On The Knife',
                     'Teenage Color', 'Howling', 'Disable music']):
                if i == selected_item:
                    text = menu_font.render('> ' + item, True, W)
                else:
                    text = menu_font.render(item, True, W)
                text_rect = text.get_rect(center=(SC_Z[0] / 2, (SC_Z[1] / 2 - 100) + i * 30))
                screen.blit(text, text_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % 9
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % 9
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:  # Start Game selected
                            settings = False


                        elif selected_item == 1:  # Song 1
                            mixer.music.load('DMPassets/SHEESH.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 2:  # Song 2
                            mixer.music.load('JioAssets/bgmusic.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 3:  # Song 3
                            mixer.music.load('JioAssets/song2.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 4:  # Song 4
                            mixer.music.load('BienAssets/song4.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 5:  # Song 5
                            mixer.music.load('BienAssets/song5.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 6:  # Song 6
                            mixer.music.load('BienAssets/song6.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 7:  # Song 7
                            mixer.music.load('BienAssets/song7.mp3')
                            mixer.music.play(-1)


                        elif selected_item == 8:  # Exit selected
                            mixer.music.pause()

    def pause(self):
        paused = True
        screen = pygame.display.set_mode(SC_Z)
        pause_bg = pygame.image.load('JioAssets/space.png')
        menu_font = pygame.font.Font(None, 36)
        selected_item = 0

        while paused:
            screen.blit(pause_bg, (0, 0))

            for i, item in enumerate(['Resume', 'Songs', 'Main menu']):
                if i == selected_item:
                    text = menu_font.render('> ' + item, True, W)
                else:
                    text = menu_font.render(item, True, W)
                text_rect = text.get_rect(center=(SC_Z[0] / 2, SC_Z[1] / 2 + i * 50))
                screen.blit(text, text_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % 3
                    if event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % 3
                    if event.key == pygame.K_RETURN:
                        if selected_item == 0:  # Back to main pause
                            paused = False
                        elif selected_item == 1:  # Settings selected
                            Shatterdart.settings_menu(self)


                        elif selected_item == 2:  # menu selected
                            game.show_menu()

    def run_game(self):

        bgm_files = {
            1: 'JioAssets/SHEESH.mp3',
            2: 'JioAssets/bgmusic.mp3',
            3: 'JioAssets/song2.mp3',
            4: 'BienAssets/song4.mp3',
            5: 'BienAssets/song5.mp3',
            6: 'BienAssets/song6.mp3',
            7: 'BienAssets/song7.mp3'
        }

        current_level = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

            self.clock.tick(50)
            self.screen.fill(BLK)  # Filling the screen with black to clear it

            self.check_input()

            # Blit the background for the current level
            if self.level == 1:
                self.screen.blit(BGM, (0, 0))
            elif self.level == 2:
                self.screen.blit(BGMS, (0, 0))
            elif self.level == 3:
                self.screen.blit(BGM1, (0, 0))
            elif self.level == 4:
                self.screen.blit(BGM2, (0, 0))
            elif self.level == 5:
                self.screen.blit(BGM, (0, 0))
            elif self.level == 6:
                self.screen.blit(BGMS, (0, 0))
            elif self.level == 7:
                self.screen.blit(BGM1, (0, 0))
            elif self.level == 8:
                self.screen.blit(BGM2, (0, 0))
            else:
                self.screen.blit(BGM3, (0, 0))

            if self.level != current_level:
                current_level = self.level
                if self.level == 1:
                    mixer.music.load(bgm_files[4])
                elif self.level == 2:
                    mixer.music.load(bgm_files[2])
                elif self.level == 3:
                    mixer.music.load(bgm_files[3])
                elif self.level == 4:
                    mixer.music.load(bgm_files[6])
                else:
                    mixer.music.load(bgm_files[7])

                mixer.music.play(-1)
            if self.state == S_P:
                self.move_ball()
                self.handle_collisions()
            elif self.state == S_BIP:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == S_G_O:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == S_W:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
            elif self.state == S_N_L:
                self.show_message("YOU WON THIS LEVEL! PRESS ENTER TO CONTINUE")

            # Draw bricks with images
            self.draw_bricks()

            # Draw paddle and ball
            pygame.draw.rect(self.screen, L_E, self.paddle)
            self.screen.blit(PADDLE_IMAGE, (self.paddle.left, self.paddle.top))
            self.screen.blit(BALL_ICON, (int(self.ball.left), int(self.ball.top)))

            # Display the score, lives, and level
            self.show_stats()

            pygame.display.flip()

try:
    if __name__ == "__main__":
        game = Shatterdart()
        game.show_menu()  # Show the menu initially
except:
    print("Your brick-busting session ended like a ninja sneak-out. Thanks for your epic hits!")

