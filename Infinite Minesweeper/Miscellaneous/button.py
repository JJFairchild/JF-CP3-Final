import pygame

class Button:
    """Generic and customizable pygame button class"""
    def __init__(self, x, y, w, h, color=(200, 200, 200), text="", text_color=(0,0,0), size=32):
        """Initialized necessary values"""
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, size)

        # Track if mouse was pressed earlier (to detect release)
        self._pressed_inside = False

    def handleEvent(self, event):
        """Detects if the mouse was clicked and released inside the box."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self._pressed_inside = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self._pressed_inside and self.rect.collidepoint(event.pos):
                self._pressed_inside = False
                return True  # Click detected

            self._pressed_inside = False

        return False
    
    def collidepoint(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        return False

    def draw(self, screen):
        """Creates the button on the screen"""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)

        text_surface = self.font.render(self.text, True, self.text_color)
        tx = self.rect.x + (self.rect.w - text_surface.get_width()) // 2
        ty = self.rect.y + (self.rect.h - text_surface.get_height()) // 2
        screen.blit(text_surface, (tx, ty))