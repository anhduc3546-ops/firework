import pygame
import random
import math
from PIL import Image
pygame.init()
screen = pygame.display.set_mode((1000, 800))
time= pygame.time.Clock()
g= 0.035
gra=0.02

pygame.mixer.init()
pygame.mixer.music.load("kiki.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

gif = Image.open("abe.gif")
gif_frames = []

try:
    while True:
        frame = gif.copy().convert("RGBA")
        frame = frame.resize((300, 200))
        gif_frames.append(
            pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        )
        gif.seek(len(gif_frames))
except EOFError:
    pass

gif_index = 0
gif_timer = 0
gif_delay = 5

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(70, 100)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        self.vy += gra
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

class Firework:

    def __init__(self):
        self.x = random.randint(100,800)
        self.y = 600
        self.speed = random.uniform(2, 6)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.exploded = False
        self.target_height = random.randint(150, 300)
    def update(self):
        self.y -= self.speed
        if self.y <= self.target_height:
            self.exploded = True
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
class Particles:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 4)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(40, 60)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        self.vy += gra
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
firework = []
particles = []
pa=[]
fi=[]
spawn_timer = 0
SPAWN_DELAY = 25
running = True
font = pygame.font.SysFont("comicsansms", 40,bold=True)
blink_timer = 0
blink_interval = 10
show_text = True
while running:
    time.tick(60)
    screen.fill((0, 0, 0))
    blink_timer += 1
    if blink_timer >= blink_interval:
        show_text = not show_text
        blink_timer = 0
    if show_text:
        text = font.render("Happy New Year", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        text_rect = text.get_rect(center=(500, 100))
        screen.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    spawn_timer += 1
    if spawn_timer >= SPAWN_DELAY:
        firework.append(Firework())
        fi.append(Firework())
        print(firework)
        print(fi)
        spawn_timer = 0
        spawn_timer = 0

    for fw in firework[:]:
        fw.update()
        fw.draw()
        if fw.exploded:
            for _ in range(60):
                particles.append(Particle(fw.x, fw.y))
            firework.remove(fw)
        for p in particles[:]:
            p.update()
            p.draw()
            if p.life <= 0:
                particles.remove(p)
        for a in fi[:]:
            a.update()
            a.draw()
            if a.exploded:
                for _ in range(100):
                    particles.append(Particles(a.x, a.y))
                fi.remove(a)
            for f in pa[:]:
                f.update()
                f.draw()
                if f.life <= 0:
                    pa.remove(f)
        gif_timer += 1
        if gif_timer >= gif_delay:
            gif_index = (gif_index + 1) % len(gif_frames)
            gif_timer = 0
        screen.blit(gif_frames[gif_index], (700, 610))
        screen.blit(gif_frames[gif_index], (0 ,610))
        screen.blit(gif_frames[gif_index], (355, 610))

    pygame.display.flip()

pygame.quit()