from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

class EffectListItem(BoxLayout):

    def __init__(self, name, pedal_board, **kwargs):
        super(EffectListItem, self).__init__(**kwargs)
        self.pedal_board = pedal_board
        self.name = name
        with self.canvas.before:
            Color(0.55, 0.08, 0.16, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.checkbox = CheckBox()
        self.checkbox.color = (255, 231, 90, 1)
        self.checkbox.bind(active=self.toggle_effect)
        self.add_widget(self.checkbox)
        self.add_widget(Label(text=name))

    def toggle_effect(self, checkbox, value):
        if value:
            self.pedal_board.turn_on_effect(self.name, len(self.pedal_board.pedals) + 1)
        else:
            self.pedal_board.turn_off_effect(self.name)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size