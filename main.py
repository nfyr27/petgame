import random
import os
import pygame as pg
import json

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

DOG_WIDTH = 310
DOG_HEIGHT = 510

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

ICON_SIZE = 80
PADDING = 8

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

TOY_SIZE = 100

font = pg.font.Font(None, 40)
maxi_font = pg.font.Font(None, 100)
mini_font = pg.font.Font(None, 15)


def load_image(file, widht, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (widht, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0, happiness=0):
        self.name = name
        self.price = price
        self.image = load_image(file, DOG_WIDTH // 1.2, DOG_WIDTH // 1.2)
        self.satiety = satiety
        self.medicine_power = medicine_power
        self.happiness = happiness


class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Food("Яблоко", 15, "images/food/apple.png", 5, 2, 2),
                      Food("Кость", 20, "images/food/bone.png", 7, 0, 3),
                      Food("Мясо", 40, "images/food/meat.png", 20, 3 , 5),                      Food("Собачий корм", 40, "images/food/dog food.png", 30, 0, 10),
                      Food("Элитный корм", 50, "images/food/dog food elite.png", 40, 0, 15),
                      Food("Лекарство", 30, "images/food/medicine.png", 0, 20, -10)]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH,
                                  SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                  func=self.to_next)
        self.previous_button = Button("Назад", MENU_NAV_YPAD,
                                      SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                      func=self.to_previous)
        self.eat_button = Button("Съесть", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                 SCREEN_HEIGHT // 2 + 95,
                                 width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                 func=self.buy_and_eat)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def buy_and_eat(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100
            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100
            self.game.happiness += self.items[self.current_item].happiness
            if self.game.happiness > 100:
                self.game.happiness = 100

    def update(self):
        self.next_button.update()
        self.previous_button.update()
        self.eat_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.previous_button.is_clicked(event)
        self.eat_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.eat_button.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)


class Item:
    def __init__(self, name, price, file, is_bought=False, is_put_on=False):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on
        self.file = file

        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []
        for item in data:
            self.items.append(Item(*item.values()))

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.next_button = Button("Вперёд", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH,
                                  SCREEN_HEIGHT - MENU_NAV_YPAD,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                  func=self.to_next)
        self.previous_button = Button("Назад", MENU_NAV_YPAD,
                                      SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                      func=self.to_previous)
        self.buy_button = Button("Купить", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                 SCREEN_HEIGHT // 2 + 95,
                                 width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                 func=self.buy)
        self.use_button = Button("Надеть", SCREEN_WIDTH // 2 - int(BUTTON_WIDTH // 1.5) // 2,
                                 SCREEN_HEIGHT // 2 + 135,
                                 width=int(BUTTON_WIDTH // 1.5), height=int(BUTTON_HEIGHT // 1.5),
                                 func=self.use_item)

        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH - 150, 130)

        self.buy_text = text_render("Куплено")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH - 150, 200)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def use_item(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

    def update(self):
        self.next_button.update()
        self.previous_button.update()
        self.buy_button.update()
        self.use_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.previous_button.is_clicked(event)
        self.buy_button.is_clicked(event)
        self.use_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.buy_button.draw(screen)
        self.use_button.draw(screen)

        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.price_text, self.price_text_rect)


class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_font=font, func=None):
        self.func = func
        self.idle_image = load_image("images/button.png", width, height)
        self.pressed_image = load_image("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Toy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        file = random.choice(os.listdir("images/toys"))
        self.image = load_image(f"images/toys/{file}", TOY_SIZE, TOY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - TOY_SIZE)
        self.rect.y = MENU_NAV_YPAD - TOY_SIZE

    def update(self):
        self.rect.y += 1


class Dog(pg.sprite.Sprite):
    def __init__(self, file):
        self.file = file
        super().__init__(),
        self.image = pg.image.load("images/dog.png")
        self.image = pg.transform.scale(self.image, (DOG_WIDTH // 2, DOG_HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.rect.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT - MENU_NAV_YPAD

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= 1
        if keys[pg.K_d]:
            self.rect.x += 1


class MiniGame:
    def __init__(self, game):
        self.game = game
        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog("images/dog.png")

        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 20000

    def new_game(self):
        self.dog = Dog("images/dog.png")
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 20000

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.dog.image, self.dog.rect)
        self.toys.draw(screen)
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))

    def is_clicked(self, event):
        ...

    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0, 100) == 0:
            self.toys.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = "Main"


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mode = "Main"
        pg.display.set_caption("Виртуальный питомец")
        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]

        self.money = data["money"]
        self.coin_per_second = data["coin_per_second"]

        self.costs_of_upgrade = {}
        for key, value in data["cost_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value

        self.INCREASE_MONEY = pg.USEREVENT + 1
        self.DECREASE = pg.USEREVENT + 2
        pg.time.set_timer(self.INCREASE_MONEY, 1000)
        pg.time.set_timer(self.DECREASE, 1000)

        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)
        self.satiety_image = load_image("images/satiety.png", ICON_SIZE, ICON_SIZE)
        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)
        self.dog_image = load_image("images/dog.png", DOG_WIDTH, DOG_HEIGHT)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button("Еда", button_x, PADDING + ICON_SIZE, func=self.food_menu_on)
        self.clothes_button = Button("Одежда", button_x, PADDING + ICON_SIZE * 2, func=self.clothes_menu_on)
        self.play_button = Button("Игры", button_x, PADDING + ICON_SIZE * 3, func=self.mini_game_on)
        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_font=mini_font, func=self.increase_money)

        self.buttons = [self.eat_button, self.clothes_button, self.play_button, self.upgrade_button]

        self.clothes_menu = ClothesMenu(self, data["clothes"])
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def mini_game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if self.money >= cost and not check:
                self.coin_per_second += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True
                break

    def event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = {
                        "happiness": 100,
                        "satiety": 100,
                        "health": 100,
                        "money": 10,
                        "coin_per_second": 1,
                        "cost_of_upgrade": {
                            "100": False,
                            "500": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "clothes": []
                    }

                    for item in self.clothes_menu.items:
                        data["clothes"].append(
                            {"name": item.name,
                             "price": item.price,
                             "file": item.file,
                             "is_bought": False,
                             "is_put_on": False
                             }
                        )
                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coin_per_second": self.coin_per_second,
                        "cost_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "500": self.costs_of_upgrade[500],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]

                        },
                        "clothes": []
                    }

                    for item in self.clothes_menu.items:
                        data["clothes"].append(
                            {"name": item.name,
                             "price": item.price,
                             "file": item.file,
                             "is_bought": item.is_bought,
                             "is_put_on": item.is_put_on
                             }
                        )
                with open("save.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                pg.quit()
                exit()
            if self.mode == "Main":
                for button in self.buttons:
                    button.is_clicked(event)
            elif self.mode == "Clothes menu":
                self.clothes_menu.is_clicked(event)
            elif self.mode == "Food menu":
                self.food_menu.is_clicked(event)
            elif self.mode == "Mini game":
                self.mini_game.is_clicked(event)

            if self.mode != "Game over":
                if event.type == self.INCREASE_MONEY:
                    self.money += self.coin_per_second
                if event.type == self.DECREASE:
                    chance = random.randint(1, 10)
                    if chance <= 5:
                        self.satiety -= 1
                    elif 5 < chance < 9:
                        self.happiness -= 1
                    else:
                        self.health -= 1

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.money += self.coin_per_second

    def update(self):
        if self.mode == "Main":
            for button in self.buttons:
                button.update()
        elif self.mode == "Clothes menu":
            self.clothes_menu.update()
        elif self.mode == "Food menu":
            self.food_menu.update()
        elif self.mode == "Mini game":
            self.mini_game.update()

        if self.satiety <= 0 or self.health <= 0 or self.happiness <= 0:
            self.mode = "Game over"

    def draw(self):
        pg.display.flip()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.health_image, (PADDING, PADDING + 60))
        self.screen.blit(self.satiety_image, (PADDING, PADDING + 120))
        self.screen.blit(self.money_image, (800, PADDING))
        self.screen.blit(self.dog_image, (300, 100))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING * 4))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 12))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 20))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - 125, PADDING * 5))

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, (300, 100))

        if self.mode == "Main":
            for button in self.buttons:
                button.draw(self.screen)
        elif self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)
        elif self.mode == "Food menu":
            self.food_menu.draw(self.screen)
        elif self.mode == "Mini game":
            self.mini_game.draw(self.screen)
        elif self.mode == "Game over":
            text = maxi_font.render("ИГРА ОКОНЧЕНА", True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)


if __name__ == "__main__":
    Game()
