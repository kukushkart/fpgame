import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color): # Метод инициализации кнопок
        self.rect = pygame.Rect(x, y, width, height) # Прямоугольник, который определяет границы кнопки
        self.text = text # Ну очевидно текст на этой кнопке
        self.color = color # Основной цвет этой шляпы
        self.hover_color = hover_color # Цвет этой твари если мы на нее наводим мышкой
        self.is_hovered = False # Флаг, по которому мы и определяем на нашу штуку навели или нет

    def draw(self, screen): # Ясен пень отрисовка кнопки
        color = self.hover_color if self.is_hovered else self.color # Определяется какой цвет установить в зависимости от флага
        pygame.draw.rect(screen, color, self.rect, border_radius = 10) # Рисуется закругленный прямоугольник
        # (border_radius = 10 отвечает за это) с выбранным цветом
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius = 10) # Рисует чёрную обводку в 2 пикселя

        if not pygame.font.get_init():
            pygame.font.init()
        font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10) # Имя и размер шрифта
        text_surface = font.render(self.text, True, WHITE) # Белый текст
        shadow_surface = font.render(self.text, True, BLACK) # Черная тень

        text_rect = text_surface.get_rect(center=self.rect.center) # Это прямоугольник, центрированный
        # внутри кнопки O_o
        shadow_rect = text_rect.copy() # Копия, которая является тенью кнопки, смещенная на 2 пикселя
        shadow_rect.x += 2 # Вот
        shadow_rect.y += 2 # И вот

        screen.blit(shadow_surface, shadow_rect) # Сначала рисуем тень
        screen.blit(text_surface, text_rect) # Затем саму надпись, чтобы был эффект тени

    def check_hover(self, mouse_pos): # Метод проверки наведения (mouse_pos - текущие корды курсора)
        self.is_hovered = self.rect.collidepoint(mouse_pos) # Штука справа возвращает тру если курсор внутри кнопки
        return self.is_hovered # Ну понятно, возвращает новое значение

    def is_clicked(self, mouse_pos, mouse_click): # mouse_click - флаг клика
        return self.rect.collidepoint(mouse_pos) and mouse_click # Возвращает тру если курсор на кнопке и нажата кнопка


def draw_menu(screen, buttons): # Отрисовка меню
    if not pygame.font.get_init():
        pygame.font.init()
    title_font = pygame.font.Font(FONT_NAME, FONT_SIZE + 20) # Устанавливаем шрифт и размер
    title_text = title_font.render("Zombie Survival", True, WHITE) # Записываем отрисовку текста
    title_shadow = title_font.render("Zombie Survival", True, BLACK) # Записываем отрисовку тени

    title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2 # Центрируем заголовок по иксу
    title_y = 100 # Зафиксировал игрик

    screen.blit(title_shadow, (title_x + 3, title_y + 3)) # Сначала рисуем тень, как и с кнопками было
    screen.blit(title_text, (title_x, title_y)) # Затем саму надпись

    for button in buttons: # Перебирает все кнопки из списка и рисует их елки палки
        button.draw(screen)