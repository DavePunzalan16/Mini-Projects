#group members
#{fronda, grafil, lopez, pael, punzalan, salvador}
import sys
import pygame
import random
from pygame import mixer


mixer.init()
mixer.music.load('DMPassets/SHEESH.mp3')
mixer.music.play(1000)
SC_Z = 640, 480                     # screen size
# IMAGES
BGM = pygame.image.load('DMPassets/BGM1.jpeg')
BGM1 = pygame.image.load('DMPassets/NIGHTMODE.JPG')
BGM2 = pygame.image.load('DMPassets/NIGHTANGLE.png')
BGM3 = pygame.image.load('DMPassets/NIGHTNIGHT.png')
BGMS = pygame.image.load('DMPassets/space.jpg')
icon_app = pygame.image.load('DMPassets/Title.png')

pygame.display.set_icon(icon_app)
BALL_ICON = pygame.image.load('BALL.png')
#PADDLE_IMAGE = pygame.image.load('PADDLE.png')
# Object of dimensions
BK_W = 60                           # brick width
BK_H = 15                           # brick height
P_W = 100                            # paddle width
P_H = 12                            # paddle height
BL_D = 16                           # ball diameter
BL_R = BL_D / 2                     # ball radius
MX_P_X = SC_Z[0] - P_W              # MAX PADDLE X
MX_BL_X = SC_Z[0] - BL_D            # MAX BALL X
MX_BL_Y = SC_Z[1] - BL_D            # MAX BALL Y
# Paddle Y coordinate
P_Y = SC_Z[1] - P_H - 25           # PADDLE Y
# Color of a constants
BLK = (0, 0, 0)                     # BLACK
W = (255, 255, 255)                 # WHITE
GD = (255, 215, 0)                  # GOLD
SKB = (0, 239, 255)                 # SKY BLUE
ORNG = (255, 154, 0)                # ORANGE
RD = (255, 99, 71)                  # RED
D_D = (184, 134, 11)                # DARK GOLDENROD
M_N = (128, 0, 0)                   # MAROON
L_E = (0,0,205)                     # DARK BLUE
# State of the constants
S_BIP = 0                           # BALL IN PADLE
S_P = 1                             # PLAYING
S_W = 2                             # WON
S_G_O= 3                            # GAME OVER
S_N_L = 4                           # NEXT LEVEL
S_PS = 5                             # PAUSE
#class of power ups

#class of the game
class Shatterdart:
  def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode(SC_Z)
      pygame.display.set_caption("SHATTERDART 1.02")
      self.clock = pygame.time.Clock()
      self.powerup_respawn_timer = 0  # Initialize the power-up respawn timer
      if pygame.font:
          self.font = pygame.font.Font(None, 30)
      else:
          self.font = None
      # These define the initial constants at the very beginning and they are never resetted.
      self.lives = 3
      self.level = 1
      self.score = 0
      self.Paddle_Speed = 18
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
          pygame.draw.rect(self.screen, self.BRICK_COLOUR, brick)
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
          self.ball_vel = [5, -5]
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
              if self.BRICK_COLOUR == GD:
                  self.score += 3
              elif self.BRICK_COLOUR == RD:
                  self.score += 5
              elif self.BRICK_COLOUR == SKB:
                  self.score += 8
              elif self.BRICK_COLOUR == ORNG:
                  self.score += 10
              else:
                  self.score += (self.level * 5)
              self.ball_vel[1] = -self.ball_vel[1]
              self.bricks.remove(brick)
              break
      if self.ball.colliderect(self.paddle):
          self.ball.top = P_Y - BL_D
          self.ball_vel[1] = -self.ball_vel[1]
      elif self.ball.top > self.paddle.top:
          self.lives -= 1
          if self.lives > 0:
              self.state = S_BIP
          # The Code below shows when the user could win the game.
          elif self.lives == 0 and self.score >= 1500:
              self.state = S_W
          elif self.lives == 0 and self.score < 1500:
              self.state = S_G_O

# power ups

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
      selected_item = 0
      menu_background = pygame.image.load('DMPassets/NIGHTNIGHT.png')  # Load your menu background image

      while True:
          self.screen.blit(menu_background, (0, 0))  # Display the menu background

          # Title text
          title_text = menu_font.render("SHATTERDART", True, W)
          title_rect = title_text.get_rect(center=(SC_Z[0] / 2, 100))
          self.screen.blit(title_text, title_rect)

          # Credits text
          credit_text = menu_font.render("Made by PYGROUP2 CS2C", True, W)
          credit_rect = credit_text.get_rect(center=(SC_Z[0] / 2, 160))
          self.screen.blit(credit_text, credit_rect)

          for i, item in enumerate(['Start Game', 'Exit']):
              if i == selected_item:
                  text = menu_font.render('-> ' + item, True, W)
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
                      selected_item = (selected_item - 1) % 2
                  if event.key == pygame.K_DOWN:
                      selected_item = (selected_item + 1) % 2
                  if event.key == pygame.K_RETURN:
                      if selected_item == 0:  # Start Game selected
                          self.run_game()
                      elif selected_item == 1:  # Exit selected
                          pygame.quit()
                          sys.exit()

          pygame.display.update()
  def run_game(self):

      while 1:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()

          self.clock.tick(50)
          #RGB
          self.screen.fill(BLK)
          #BACKGROUND
          self.check_input()

          if self.level == 1:
              self.BRICK_COLOUR = W
              self.screen.blit(BGM, (0, 0))
          elif self.level == 2:
              self.BRICK_COLOUR = GD
              self.screen.blit(BGMS, (0, 0))
          elif self.level == 3:
              self.BRICK_COLOUR = RD
              self.screen.blit(BGM1, (0, 0))
          elif self.level == 4:
              self.BRICK_COLOUR = D_D
              self.screen.blit(BGM2, (0, 0))
          else:
              self.BRICK_COLOUR = M_N
              self.screen.blit(BGM3, (0, 0))

          if self.state == S_P:
              self.move_ball()
              self.handle_collisions()
          elif self.state == S_BIP:
              self.ball.left = self.paddle.left + self.paddle.width / 2
              self.ball.top = self.paddle.top - self.ball.height
              #show message
              self.show_message("PRESS SPACE TO LAUNCH THE BALL")
          elif self.state == S_G_O:
              self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
          elif self.state == S_W:
              self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
          elif self.state == S_N_L:
              self.show_message("YOU WON THIS LEVEL! PRESS TO CONTINUE")
          self.draw_bricks()
          # Draw paddle
          pygame.draw.rect(self.screen, L_E, self.paddle)
          # Draw paddle using the paddle image
          #self.screen.blit(PADDLE_IMAGE, (self.paddle.left, self.paddle.top))
          # Draw ball
          self.screen.blit(BALL_ICON, (int(self.ball.left), int(self.ball.top)))  # Blit the ball icon image
          self.show_stats()
          pygame.display.flip()

try:
   if __name__ == "__main__":
       game = Shatterdart()
       game.show_menu()  # Show the menu initially
except:
   print("Your brick-busting session ended like a ninja sneak-out. Thanks for your epic hits!")