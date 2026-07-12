import pygame as pg
import random
import sys
import os

# Initialize Pygame
pg.init()
pg.mixer.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.45          
BIRD_FLAP_SPEED = -7     
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 160     
PIPE_SPEED = 3.5
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)

# Screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Pro Flappy Bird")
clock = pg.time.Clock()

# Load images
background_img = pg.image.load("assets/bg.png").convert()
ground_img = pg.image.load("assets/ground.png").convert()
pipe_img = pg.image.load("assets/pipedown.png").convert_alpha()

# Sounds
flap_sound = pg.mixer.Sound("assets/swoosh.wav")
point_sound = pg.mixer.Sound("assets/point.wav")
hit_sound = pg.mixer.Sound("assets/hit.wav")

# Scale images
background_img = pg.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_img = pg.transform.scale(ground_img, (SCREEN_WIDTH, GROUND_HEIGHT))
pipe_img = pg.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

# --- High Score Logic ---
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f: f.write("0")

def get_high_score():
    with open("highscore.txt", "r") as f: return int(f.read())

def save_high_score(new_score):
    high_score = get_high_score()
    if new_score > high_score:
        with open("highscore.txt", "w") as f: f.write(str(new_score))

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super(Bird, self).__init__()
        self.img_list = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_factor),
                         pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(), scale_factor)]
        self.image_index = 0
        self.base_image = self.img_list[self.image_index]
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.y_velocity = 0
        self.anim_counter = 0

    def rotate_bird(self):
        # Rotation Logic: Velocity ke mutabiq bird ko rotate karna
        new_bird = pg.transform.rotozoom(self.base_image, -self.y_velocity * 3, 1)
        return new_bird

    def update(self):
        self.playAnimation()
        # Gravity apply ho rahi hai
        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity
        self.image = self.rotate_bird()

    def flap(self):
        self.y_velocity = BIRD_FLAP_SPEED
        flap_sound.play()

    def playAnimation(self):
        if self.anim_counter == 5:
            self.base_image = self.img_list[self.image_index]
            self.image_index = 1 if self.image_index == 0 else 0
            self.anim_counter = 0
        self.anim_counter += 1

class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super(Pipe, self).__init__()
        self.image = pg.transform.flip(pipe_img, False, inverted)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y if not inverted else y - self.rect.height

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

def create_pipe_pair():
    gap_y = random.randint(150, 400)
    top_pipe = Pipe(SCREEN_WIDTH + 50, gap_y - (PIPE_GAP // 2), inverted=True)
    bottom_pipe = Pipe(SCREEN_WIDTH + 50, gap_y + (PIPE_GAP // 2))
    return top_pipe, bottom_pipe

def main():
    bird = Bird(1.0)
    pipes = pg.sprite.Group()
    all_sprites = pg.sprite.Group(bird)
    
    high_score = get_high_score()
    score = 0
    font = pg.font.SysFont("Arial", 30, bold=True)
    ground_scroll = 0

    # Start Screen
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit(); sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: waiting = False
        
        screen.blit(background_img, (0,0))
        text = font.render("Press SPACE to Flap", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        pg.display.flip()

    # Game Loop
    running = True
    spawn_pipe = pg.USEREVENT
    pg.time.set_timer(spawn_pipe, 1500) # Har 1.5 second baad pipe

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit(); sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                bird.flap()
            if event.type == spawn_pipe:
                t, b = create_pipe_pair()
                pipes.add(t, b); all_sprites.add(t, b)

        # Update
        all_sprites.update()

        # Collision
        if pg.sprite.spritecollide(bird, pipes, False) or bird.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT or bird.rect.top <= 0:
            hit_sound.play()
            save_high_score(int(score))
            running = False

        # Score
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not hasattr(pipe, 'scored'):
                pipe.scored = True
                score += 0.5
                if score % 1 == 0: point_sound.play()

        # Draw
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        
        # Infinite Ground
        ground_scroll -= PIPE_SPEED
        if abs(ground_scroll) > 35: ground_scroll = 0
        screen.blit(ground_img, (ground_scroll, SCREEN_HEIGHT - GROUND_HEIGHT))
        screen.blit(ground_img, (ground_scroll + SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        # Score Display
        sc_text = font.render(f"Score: {int(score)}  High: {high_score}", True, WHITE)
        screen.blit(sc_text, (10, 10))

        pg.display.flip()
        clock.tick(FPS)

    # Game Over State
    pg.time.delay(500)
    main() 

if __name__ == "__main__":
    main()