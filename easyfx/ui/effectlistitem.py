from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

class EffectListItem(BoxLayout):
    """Class representing a list element within FXList class.

    Attributes:
        pedal_board: The PedalBoard which contains the effects
        name: The name of the effect
        checkbox: Toggleable checkbox to activate effects via the pedal board.
    """

    def __init__(self, name: str, pedal_board, **kwargs):
        """Inits EffectListItem class

        Args:
            name: The name of the effect
            pedal_board: The currently active pedal board
        """
        super(EffectListItem, self).__init__(**kwargs)

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0.55, 0.08, 0.16, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Instance attributes
        self.pedal_board = pedal_board
        self.name = name

        # Create checkbox and bind to function
        self.checkbox = CheckBox()
        self.checkbox.color = (255, 231, 90, 1)
        self.checkbox.bind(active=self.toggle_effect)

        # Add child widgets
        self.add_widget(self.checkbox)
        self.add_widget(Label(text=name))

    def toggle_effect(self, checkbox: CheckBox, value: bool):
        """Turns an effect on/off via the accociated pedal board.

        Places the pedal at the end of the current signal chain.

        Args:
            checkbox: The checkbox object
            value: boolean of whether the checkbox was selected or deselected
        """
        if value:
            self.pedal_board.turn_on_effect(self.name, len(self.pedal_board.pedals) + 1)
        else:
            self.pedal_board.turn_off_effect(self.name)

    def _update_rect(self, instance, value):
        """Update the shape of the background of this object when the view size changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size