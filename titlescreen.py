import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
#import thorpy
#import eyetracker
import MyAnnoyingPartner


RED = (229, 60, 33)
WHITE = (255, 255, 255)
TRANS = (1, 1, 1)
TRACKERFILE = MyAnnoyingPartner
# TRACKERFILE = eyetracker
def create_surface_with_text(text, font_size, rgb, bg_rgb):
    font = pygame.freetype.SysFont("Calibri", font_size, bold=True)
    surface, _=font.render(text=text, fgcolor=rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    START = 1

class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, rgb, action=None):
        self.mouse_over = False 
        default_image = create_surface_with_text(
            text=text, font_size=font_size, rgb=rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, rgb=rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]
        self.action = action
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)
        super().__init__()


def title_screen(screen):
    start_btn = UIElement(
        center_position=(640, 400),
        font_size=30,
        bg_rgb=WHITE,
        rgb=RED,
        text="Start",
        action=GameState.START,
    )
    quit_btn = UIElement(
        center_position=(640, 500),
        font_size=30,
        bg_rgb=WHITE,
        rgb=RED,
        text="Quit",
        action=GameState.QUIT,
    )
    # slider = thorpy.SliderX(length=100, limvals=(0, 100), text="Patience Meter", initial_value=25, type_=int)

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(WHITE)
        screen.blit(pygame.image.load("logo1.jpg").convert(), (325, 50))
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    game_state=GameState.TITLE
    # main loop
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        
        if game_state == GameState.START:
            TRACKERFILE.start()
            game_state = GameState.TITLE
        
        if game_state == GameState.QUIT:
            pygame.quit()
            return

# call main when the script is run
if __name__ == "__main__":
    main()