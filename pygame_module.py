import pygame
import chorder

"""这个文件定义了和pygame有关的模块，包括按钮，黑白键，输入框。"""


def prt(screen, message, size, xc, yc, background=(230, 230, 230)):
    fol = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', size)
    text0 = fol.render(message, True, (0, 0, 0), background)
    text_rect0 = text0.get_rect()
    text_rect0.center = (xc, yc)
    screen.blit(text0, text_rect0)
    pygame.display.flip()


# 按钮
class Button:
    def __init__(self, text='按钮', left=20, top=706, width=100, height=30):
        self.text = text
        self.rect = pygame.Rect(left, top, width, height)
        self.font = pygame.font.Font(r'C:/Windows/Fonts/simhei.ttf', 20)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.active = False
        self.function = None

    def draw(self, scr):
        pygame.draw.rect(scr, (160, 160, 160), self.rect, 3)
        scr.blit(self.text_surface, self.text_rect)


# 白键
class WKey:
    # 这里的note_v是从0开始到51计算的
    def __init__(self, note_v, top=130):
        self.rect = pygame.Rect(51.5 + note_v * 26.93, top, 25.5, 49)
        self.n_v = int(note_v)
        self.active = False
        self.function = None

    def selected(self, scr, eve):
        if 51.5 + self.n_v * 26.93 <= eve.pos[0] <= 77 + self.n_v * 26.93 and 130 <= eve.pos[1] <= 155:
            pygame.draw.rect(scr, (160, 160, 200), self.rect)
            pygame.display.flip()
            # 返回可用于mido的音符数值
            return self.n_v + 21

    def mouse_on(self, scr, eve):
        if self.n_v * 26.9 <= eve.pos[0] <= 58 + self.n_v * 26.9 and 130 <= eve.pos[1] <= 155:
            pygame.draw.rect(scr, (200, 200, 240), self.rect)
            pygame.display.flip()

    def play(self, screen, active=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if active is True:
                pygame.draw.rect(screen, (100, 100, 130), self.rect)
                pygame.display.flip()
