from easyfx.ui.toolbutton import ToolButton
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ToolbarLeft(BoxLayout):

    def __init__(self, gui, **kwargs):
        super(ToolbarLeft, self).__init__(**kwargs)
        self.gui = gui
        with self.canvas.before:
            Color(0.1, 0.1, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.size_hint = (None, None)
        self.height = 68
        self.padding = 4
        self.spacing = 4

        self.load_button = ToolButton(source='img/load_icon.png')
        self.load_button.bind(on_press=self._do_load)
        self.add_widget(self.load_button)

        self.save_button = ToolButton(source='img/save_icon.png')
        self.save_button.bind(on_press=self._do_save)
        self.add_widget(self.save_button)

    def _do_save(self, instance):
        self.gui.save_dialogue()

    def _do_load(self, instance):
        self.gui.load_dialogue()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size