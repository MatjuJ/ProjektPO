import pygame
import sys
import time

# Stałe
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 130, 15
BRICK_WIDTH, BRICK_HEIGHT = 80, 25
ROW_COUNT, COLUMN_COUNT = 3, 10

# Kolory - RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
BROWN = (100, 65, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 102, 0)
ORANGEYELLOW = (255, 144, 0)
PURPLE = (150, 0, 255)
PINK = (255, 0, 150)
blockColors = (PURPLE,RED,WHITE,GREEN,BLUE,PINK)




class Game:
    def __init__(self):
               
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.name=pygame.display.set_caption("Brick Breaker") 
       
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.running = False
       
        self.score = 0
        self.lives = 3
        self.level = 1
        
        self.ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, WHITE, self.screen)
        self.paddle = Paddle(WIDTH / 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, self.screen)
        self.bricks = []
        self.create_bricks()


    def create_bricks(self): # TWORZENIE "CEGIEŁEK"
        self.bricks.clear()
        for i in range(self.level + 2):  
            for j in range(COLUMN_COUNT ):  
                brick = Brick(j * (BRICK_WIDTH), i * (BRICK_HEIGHT), BRICK_WIDTH, BRICK_HEIGHT, BLUE, self.screen)
                brick.setColor(blockColors[i])
                self.bricks.append(brick)

    def show_message(self, text): #WYSWIETLANIE WIADOMOSCI ( GAME OVER LUB YOU'VE WON)
        large_font = pygame.font.Font(None, 35)  
        message_text = large_font.render(text, True, WHITE) 
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))    
        self.screen.blit(message_text, message_rect)
        pygame.display.update()
        self.clock.tick(False)
        


    def run(self):

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # NACISNIECIE SPACJI POWODUJE "UWOLNIENIE" PILECZKI
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ball.waiting_for_release = False

             # UDERZENIE CEGIELKI PRZEZ PILKE POWODUJE ZWIEKSZENIE WYNIKU O 1
            hit_brick = self.ball.move(self.paddle, self.bricks)
            if hit_brick:
                self.score += 1
            self.paddle.move()

            # STRATA ZYCIA JEZELI PILKA UDERZY O ZIEMIE, NASTEPUJE WTEDY RESET, ZMNIEJSZENE ZYCIA O 1 O
            if self.ball.y > HEIGHT:
                if self.lives>0:
                    self.lives-=1
                    self.ball.dy*=-1
                    self.ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, WHITE, self.screen)
                    self.paddle = Paddle(WIDTH / 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, self.screen)
                    time.sleep(1)
                else:
                    self.running=False


                    #JESLI OSIAGNIEMY 4 POZIOM LUB STRACIMY 3 ZYCIA TO NASTEPUJE POJAWIENIE SIE KOMINIKATU ORAZ ABY OPUSCIC PROGRAM NALEZY KLIKNAC ESC
            if self.lives == 0 or self.level == 4:
                self.ball.dx = 0
                self.ball.dy = 0

                while True: 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pygame.quit()
                            sys.exit()
                    self.screen.fill(BLACK)
                    self.show_message("GAME OVER. CLICK ESC TO QUIT THE GAME" if self.lives == 0 else "You've won. CLICK ESC TO QUIT")
                    pygame.display.flip()
                    self.clock.tick(60)

            #JESLI ROZBILISMY WSZYSTKIE CEGIELKI TO NASTEPUJE ZWIEKSZENIE LICZBY RZEDOW O 1, ZWIEKSZENIE POZIOMU O 1 ORAZ RESET
            if len(self.bricks) == 0:  
                self.level += 1
                self.create_bricks()
                self.ball.dy*=-1
                self.ball = Ball(WIDTH / 2, HEIGHT / 2, BALL_RADIUS, WHITE, self.screen)
                self.paddle = Paddle(WIDTH / 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, self.screen)
                time.sleep(1)

            self.screen.fill(GREY)
            self.ball.draw()
            self.paddle.draw()

            for brick in self.bricks:
                brick.draw()
            
            

            # PRZEDSTAWIENIE INFORMACJI O WYNIKU, LICZBIE ZYC ORAZ POZIOMIE W LEWYM DOLNYM ROGU
            score_text = self.font.render(f'Score: {self.score} ', 1, WHITE)
            self.screen.blit(score_text, (0, 525))
            level_text = self.font.render(f'Level: {self.level }' , 1, WHITE)
            self.screen.blit(level_text, (0, 575))
            lives_text = self.font.render(f'Lives: {self.lives } ' , 1, WHITE)
            self.screen.blit(lives_text, (0, 550))



            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()




class Ball:
    def __init__(self, x, y, radius, color, surface):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.surface = surface
        self.waiting_for_release = True
        self.dx=8
        self.dy=8


    def draw(self): # "rysunek pilki"
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def move(self, paddle, bricks):
        # KLIKNIECIE SPACJI = self.waiting_for_release = False
        if self.waiting_for_release:
            self.x = paddle.x + paddle.width / 2
            self.y = paddle.y - self.radius
      
        else:
              # MECHANIKA ODBIJANIA PILKI OD SCIANY LUB NASZEJ DESKROLKI
            self.x += self.dx
            self.y += self.dy

            if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
                self.dx *= -1

            if self.y - self.radius < 0: 
                self.dy *= -1

            if paddle.x < self.x < paddle.x + paddle.width and paddle.y < self.y < paddle.y + paddle.height:
                self.dy *= -1

            # TRAFIENIE W CEGIELKE SPOWODUJE JEJ USUNIECIE
            for brick in bricks:
                if brick.x < self.x < brick.x + brick.width and brick.y < self.y < brick.y + brick.height:
                    self.dy *= -1
                    if brick.hit() == 0:
                        bricks.remove(brick)
                    return True 
            return False  
    


class Paddle:
    def __init__(self, x, y, width, height, color, surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface

    def draw(self): 
        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self): #PORUSZANIE SIE NASZEJ "DESKROLKI"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x >0:
            self.x -= 10
        if keys[pygame.K_RIGHT] and self.x< WIDTH- self.width:
            self.x += 10
    




class Brick:
    def __init__(self, x, y, width, height, color, surface,hits=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.hits=hits
    
    def setColor(self, color = (0, 0, 0)):
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        self.color = (self.red, self.green, self.blue)
        return self.color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
    
    def hit(self):
        self.hits-=1
        return self.hits


if __name__ == '__main__':
    game = Game()
    game.run()
