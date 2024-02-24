from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
import random


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)

        self.snake_size = 20
        self.snake_pos = [(100, 100)]
        self.food_pos = self.generate_food_pos()
        self.direction = (1, 0)
        self.score = 0

        with self.canvas:
            Color(1, 1, 1, 1)
            self.snake_body = Rectangle(pos=self.snake_pos[0], size=(self.snake_size, self.snake_size))
            Color(1, 0, 0, 1)
            self.food = Rectangle(pos=self.food_pos, size=(self.snake_size, self.snake_size))

        self.bind(on_touch_down=self.on_touch_down)
        Clock.schedule_interval(self.update, 0.1)

    def generate_food_pos(self):
        x = random.randint(0, (Window.width - self.snake_size) // self.snake_size) * self.snake_size
        y = random.randint(0, (Window.height - self.snake_size) // self.snake_size) * self.snake_size
        return x, y

    def on_touch_down(self, touch):
        dx = touch.dx
        dy = touch.dy

        if abs(dx) > abs(dy):
            self.direction = (dx, 0)
        else:
            self.direction = (0, dy)

    def update(self, dt):
        new_x = self.snake_pos[0][0] + self.direction[0] * self.snake_size
        new_y = self.snake_pos[0][1] + self.direction[1] * self.snake_size

        # Check if snake hits the wall or itself
        if new_x < 0 or new_x >= Window.width or new_y < 0 or new_y >= Window.height or (
        new_x, new_y) in self.snake_pos:
            self.snake_pos = [(100, 100)]
            self.direction = (1, 0)
            self.score = 0
            self.update_score()

        self.snake_pos.insert(0, (new_x, new_y))

        # Check if snake eats the food
        if self.snake_pos[0] == self.food_pos:
            self.food_pos = self.generate_food_pos()
            self.food.pos = self.food_pos
            self.score += 1
            self.update_score()
        else:
            self.snake_pos.pop()

        self.snake_body.pos = self.snake_pos[0]

    def update_score(self):
        self.parent.score_label.text = f"Score: {self.score}"


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        self.score_label = Label(text="Score: 0", font_size=30, pos=(0, Window.height - 50), size=(Window.width, 50))
        game.add_widget(self.score_label)
        return game


if __name__ == '__main__':
    SnakeApp().run()
