import pygame as pg

from gui import Checkbox


class Menu:
    CHECKBOX_COL_NUMBER = 9
    CHECKBOX_ROW_NUMBER = 2
    CHECKBOX_SIZE = 30
    CHECKBOX_SPACING = 10

    CHECKBOX_OFFSET = CHECKBOX_SIZE + CHECKBOX_SPACING
    CHECKBOXES_WIDTH = CHECKBOX_COL_NUMBER * CHECKBOX_SIZE + (CHECKBOX_COL_NUMBER - 1) * CHECKBOX_SPACING
    CHECKBOXES_HEIGHT = CHECKBOX_ROW_NUMBER * CHECKBOX_SIZE + (CHECKBOX_ROW_NUMBER - 1) * CHECKBOX_SPACING

    def __init__(self, win_size):
        """Tworzy nowe menu. Standardowa reguła - reguła Conwaya."""
        start_x = (win_size[0] - Menu.CHECKBOXES_WIDTH) / 2
        start_y = (win_size[1] - Menu.CHECKBOXES_HEIGHT) / 2

        self.rule_checkboxes = [
            Checkbox(pg.Rect(
                start_x + Menu.CHECKBOX_OFFSET * x,
                start_y + Menu.CHECKBOX_OFFSET * y,
                Menu.CHECKBOX_SIZE,
                Menu.CHECKBOX_SIZE
            ))
            for y in range(Menu.CHECKBOX_ROW_NUMBER)
            for x in range(Menu.CHECKBOX_COL_NUMBER)
        ]

        self.rule_checkboxes[2].active = True
        self.rule_checkboxes[3].active = True
        self.rule_checkboxes[Menu.CHECKBOX_COL_NUMBER + 3].active = True

        self.update_rule()

    def update_rule(self):
        """Updatuje self.rule opeirając się na stanie przełączników."""
        self.rule = [
            [
                self.rule_checkboxes[state * Menu.CHECKBOX_COL_NUMBER + neighbor_count].active
                for neighbor_count in range(Menu.CHECKBOX_COL_NUMBER)
            ]
            for state in range(Menu.CHECKBOX_ROW_NUMBER)
        ]

    def on_event(self, event):
        """Odpowiada na wydarzenia.
        Zwraca True jeżeli wydarzenie zostało przechwycone.
        """
        for checkbox in self.rule_checkboxes:
            if checkbox.on_event(event):
                self.update_rule()
                return True

        return False
    
    def draw(self, screen):
        """Rysuje menu."""
        for checkbox in self.rule_checkboxes:
            checkbox.draw(screen)
