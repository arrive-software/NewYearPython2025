#This program is released under license GNU GENERAL PUBLIC LICENSEv3
#Copyright 2024,2025 Jason Lee(p299-dev),arrive Corporation(arrive-software)
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
import pygame
import random
import math
import time
import winsound
import threading
 
# Initialize pygame
pygame.init()
 
# Set up display
WIDTH, HEIGHT = 1280, 932
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("python2025")
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

soundoff = True
 
# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.target_y = random.randint(100, 880)
        self.color = random.choice([RED, BLUE, GREEN, PURPLE, ORANGE, YELLOW])
        self.radius = 5
        self.exploded = False
        self.particles = []
 
    def update(self):
        if not self.exploded:
            self.y -= 5
            if self.y <= self.target_y:
                self.explode()
        else:
            new_particles = []
            for px, py, vx, vy, p_radius, p_color in self.particles:
                px += vx
                py += vy
                vy += 0.05  # Gravity effect
                p_radius -= 0.05
                if p_radius > 0:
                    new_particles.append((px, py, vx, vy, p_radius, p_color))
            self.particles = new_particles
 
    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        else:
            for px, py, _, _, p_radius, p_color in self.particles:
                pygame.draw.circle(surface, p_color, (int(px), int(py)), int(p_radius))
 
    def explode(self):
        self.exploded = True
        num_particles = 50
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            px = self.x
            py = self.y
            p_radius = random.uniform(3, 5)
            p_color = random.choice([RED, BLUE, GREEN, PURPLE, ORANGE, YELLOW])
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append((px, py, vx, vy, p_radius, p_color))
def sound():
    for i in range(2025):
        winsound.PlaySound('python2025.wav',winsound.SND_ASYNC)
        time.sleep((random.randint(22,28))/10)
    print("你发现彩蛋了，2025蛇年快乐！")
thread = threading.Thread(target=sound)
# Main loop
def main():
    img = pygame.image.load('python2025.png')
    clock = pygame.time.Clock()
    running = True
    fireworks = [Firework() for _ in range(8)]
    fade_alpha = 5  # For fading effect
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    thread.daemon = True
    thread.start()
    while running:
        screen.fill(BLACK)
        rect = img.get_rect()
        rect.center = 640, 466
        screen.blit(img,rect)
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        # Add fading effect
        overlay.set_alpha(fade_alpha)
        screen.blit(overlay, (0, 0))
        
        pygame.display.flip()
        clock.tick(30)
        
        # Check if all fireworks have exploded and particles have disappeared, then reset
        if all(firework.exploded and not firework.particles for firework in fireworks):
            time.sleep(1)
            fireworks = [Firework() for _ in range(10)]
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    soundoff = False    
    # os.system("taskkill /f /im python.exe /t")
if __name__ == "__main__":
    main()
