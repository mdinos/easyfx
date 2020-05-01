from easyfx.ui.toolbutton import ToolButton
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ToolbarLeft(BoxLayout):
    """Class representing the top LHS toolbar of the application.

    Attributes:
        gui: The current EasyFXLayout instance
        load_button: ToolButton for activating the file loading sequence
        save_button: ToolButton for activating the file saving sequence
    """

    def __init__(self, gui, **kwargs):
        """Inits ToolbarLeft class

        Args:
            gui: The current EasyFXLayout to be accociated with this toolbar.
        """
        super(ToolbarLeft, self).__init__(**kwargs)

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0.1, 0.1, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Inherited attributes
        self.size_hint = (None, None)
        self.height = 68
        self.padding = 4
        self.spacing = 4

        # Class attributes
        self.gui = gui

        # Create and add child widgets
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
        """Private method for checking user input and triggering the save if input is OK."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size