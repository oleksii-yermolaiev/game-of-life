import pygame as pg


class Checkbox:
    NORMAL_COLOR = (200, 200, 200)
    ACTIVE_COLOR = (100, 180, 100)

    def __init__(self, rect):
        """Tworzy nowy przełącznik, opisany w rect."""
        self.rect = rect
        self.active = False
    
    def on_event(self, event):
        """Odpowiada na wydarzenia.
        Zwraca True jeżeli wydarzenie zostało przechwycone.
        """
        if event.type == pg.MOUSEBUTTONDOWN and \
            event.button == 1 and \
            self.rect.collidepoint(event.pos):
            self.active = not self.active
            return True

        return False

    def draw(self, screen):
        """Rysuje przełącznik."""
        color = Checkbox.ACTIVE_COLOR if self.active else Checkbox.NORMAL_COLOR
        pg.draw.rect(screen, color, self.rect)
