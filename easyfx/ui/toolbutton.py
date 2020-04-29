from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image

class ToolButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(ToolButton, self).__init__(**kwargs)
        self.size = (64, 64)
        self.always_release = True