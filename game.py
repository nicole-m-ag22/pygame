import sys
import pygame
from pygame.locals import *

print (sys.argv)

class MainGame:
    def __init__(self):
        pygame.init()
        width = int(sys.argv[1]) if len(sys.argv) > 1 else 640
        height = int(sys.argv[2]) if len(sys.argv) > 2 else 480
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('niki brick breaker')
        self.font = pygame.font.Font(None, int(height / 15))
        self.player_rect = pygame.Rect(int(width / 2 - width / 10), int(height - height / 12), int(width / 5), int(height / 30))  # Create a rectangle for the player
        self.ball_rect = pygame.Rect(int(width / 2 - width / 100), int(height / 2 - height / 50), int(width / 50), int(height / 50))  # Create a rectangle for the ball
        self.ball_speed = pygame.Vector2(int(width / 10), int(height / 10))  # Set the initial speed of the ball
        self.clock = pygame.time.Clock()  # Create a clock object to track time
        self.blocks = self.create_blocks()  # Create the blocks
        self.main()

    def create_blocks(self):
        blocks = []
        block_width = int(self.screen.get_width() / 10)  
        block_height = int(self.screen.get_height() / 30) 
        num_blocks_x = int(sys.argv[3]) if len(sys.argv) > 3 else 10 
        num_blocks_y = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        gap = int(self.screen.get_width() / 100)
        start_x = (self.screen.get_width() - (num_blocks_x * (block_width + gap))) // 2
        start_y = int(self.screen.get_height() / 10)
        for i in range(num_blocks_y):
            for j in range(num_blocks_x):
                x = start_x + j * (block_width + gap) + (block_width + gap) / 2 * (i % 2)
                y = start_y + i * (block_height + gap)
                block_rect = pygame.Rect(x, y, block_width, block_height)
                blocks.append(block_rect)
        
        # Ensure the ball is below the lowest row of blocks
        ball_bottom = max([block.bottom for block in blocks])
        self.ball_rect.y = ball_bottom + int(self.screen.get_height() / 100)
        
        return blocks

    def main(self):
        while True:
            dt = self.clock.tick(60) / 1000.0  # Calculate the time since the last frame in seconds

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
            if keys[K_LEFT]:  
                self.player_rect.x -= int(self.screen.get_width() / 5) * dt
                if self.player_rect.left < 0:  
                    self.player_rect.left = 0  
            if keys[K_RIGHT]:  
                self.player_rect.x += int(self.screen.get_width() / 5) * dt
                if self.player_rect.right > self.screen.get_width():  
                    self.player_rect.right = self.screen.get_width() 

            self.ball_rect.x += self.ball_speed.x * dt  
            self.ball_rect.y += self.ball_speed.y * dt  

            if self.ball_rect.left < 0 or self.ball_rect.right > self.screen.get_width():
                self.ball_speed.x *= -1  
                self.ball_speed.y *= 1  

            if self.ball_rect.top < 0:
                self.ball_speed.y *= -1  
            elif self.ball_rect.bottom > self.screen.get_height():
                # Ball hits the bottom boundary
                pygame.display.set_caption('You lost')  
                pygame.time.delay(2000)  
                sys.exit()

            if self.ball_rect.colliderect(self.player_rect):  # Check if the ball collides with the player rectangle
                if self.ball_rect.centerx < self.player_rect.left: 
                    self.ball_speed.x = -abs(self.ball_speed.x)  
                elif self.ball_rect.centerx > self.player_rect.right:  
                    self.ball_speed.x = abs(self.ball_speed.x)  
                else:  
                    self.ball_speed.y *= -1

            for block in self.blocks:
                if self.ball_rect.colliderect(block):  # Check if the ball collides with a block
                    if self.ball_rect.top <= block.bottom and self.ball_rect.bottom >= block.top:  
                        self.ball_speed.y *= -1  
                    self.blocks.remove(block)

            if len(self.blocks) == 0:  # Check if all blocks are broken
                pygame.display.set_caption('You won')  #
                pygame.time.delay(2000)  
                sys.exit()  

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), self.player_rect)  
            pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball_rect) 
            for block in self.blocks:
                pygame.draw.rect(self.screen, (255, 0, 0), block)  
            pygame.display.flip()

MainGame()