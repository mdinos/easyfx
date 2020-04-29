from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ToolbarRight(BoxLayout):

    def __init__(self, gui, **kwargs):
        super(ToolbarRight, self).__init__(**kwargs)
        self.gui = gui
        with self.canvas.before:
            Color(0.1, 0.6, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.size_hint = (None, None)
        self.height = 68
        self.padding = 4
        self.spacing = 4

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size