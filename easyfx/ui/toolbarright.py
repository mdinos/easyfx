from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ToolbarRight(BoxLayout):
    """Class representing the top RHS toolbar for the application

    Currently placeholder section, important for keeping format.
    """

    def __init__(self, **kwargs):
        """Inits ToolbarRight class"""
        super(ToolbarRight, self).__init__(**kwargs)

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Inherited Attributes
        self.size_hint = (None, None)
        self.height = 68
        self.padding = 4
        self.spacing = 4

    def _update_rect(self, instance, value):
        """Private method for checking user input and triggering the save if input is OK."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size