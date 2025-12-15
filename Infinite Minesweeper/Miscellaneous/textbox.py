import pygame

class TextBox:
    """Generic and customizable pygame text box"""
    def __init__(self, x, y, w, h, mutable, text="", color=(200, 200, 200), text_color=(0, 0, 0), limit=20, size=32):
        """Initializes necessary values"""
        self.rect = pygame.Rect(x, y, w, h)
        self.mutable = mutable
        self.text = text
        self.text_color = text_color
        self.color = color
        self.limit = limit

        self.font = pygame.font.Font(None, size)
        self.active = False  # Whether the box is selected

    def handleEvent(self, event):
        """Handles input events for the text box"""
        if self.mutable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isprintable() and len(self.text) < self.limit:
                        self.text += event.unicode

    def draw(self, screen):
        """Creates the text box on the screen"""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)

        text_surface = self.font.render(self.text, True, self.text_color)
        tx = self.rect.x + (self.rect.w - text_surface.get_width()) // 2
        ty = self.rect.y + (self.rect.h - text_surface.get_height()) // 2
        screen.blit(text_surface, (tx, ty))