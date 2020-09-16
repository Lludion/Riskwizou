import pygame
from collections import defaultdict
from math import floor

def s(t): return pygame.time.wait(floor(t * 1000))
# do not use time.sleep() - return should be useless.

class Displayer:

    def __init__(self):
        pygame.init()
        self.load_images()
        self.launch_display()

    def load_images(self):
        with open("data/img/img.json", "r", encoding="utf-8-sig") as read_file:
            self.raw_img = json.load(read_file)

        dflt = pygame.image.load("data/img/default.png")
        def return_dflt(*_):
            return dflt
        self.img = defaultdict(return_dflt)

        for k,v in self.raw_img.items():
            self.img[k] = pygame.image.load("data/img/"+v)

    def launch_display(self):
        self.mode = 0#mode = 0 ou FULLSCREEN
        self.win = pygame.display.set_mode((1400, 1000),self.mode)
        pygame.display.set_icon(self.img["R"])
        pygame.display.set_caption("Riskwizou")
        self.win.blit(self.img["Riskwizou"],(0,0))
        pygame.display.flip()
        s(5)

    def close(self):
        pygame.display.quit()
        pygame.quit()
