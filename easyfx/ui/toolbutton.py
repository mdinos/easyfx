from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image

class ToolButton(ButtonBehavior, Image):
    """Class representing a button on a toolbar.

    Class inherits button like behavior while also being an image.
    """

    def __init__(self, **kwargs):
        """Inits ToolButton class"""
        super(ToolButton, self).__init__(**kwargs)
        self.size = (64, 64)
        self.always_release = True