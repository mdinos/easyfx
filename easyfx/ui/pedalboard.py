from easyfx.ui.effectcontainer import EffectContainer
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

class PedalBoard(GridLayout):
    """Class representing the pedal board area of the UI.

    Attributes:
        controller: The PDController instance to use for communication with pure-data
        gui: The parent EasyFXLayout object accociated with this pedal board
        pedals: The ordered list of currently active pedals
    """

    def __init__(self, controller, gui, **kwargs):
        """Inits PedalBoard class

        Args:
            controller: PDController instance currently active
            gui: The current EasyFXLayout instance, for which this object is a child of
        """
        super(PedalBoard, self).__init__(**kwargs)

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0.33, 0.43, 0.48, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Inherited attributes (shape, format)
        self.size_hint = (0.8, 1)
        self.cols = 4
        self.rows = 2
        self.spacing = 10
        self.padding = 10
        self.col_force_default = True
        self.row_force_default = True

        # Initialise attributes
        self.controller = controller
        self.gui = gui
        self.pedals = []
    
    def turn_on_effect(self, effect_name: str, position: int):
        """Turn on a specific effect

        Args:
            effect_name: The name of the effect to turn on
            position: The position in the signal chain to insert this effect (>1)

        Raises:
            ValueError if position argument is less than 1
        """
        try:
            pedal = EffectContainer(effect_name, self.controller, self)

            if position > len(self.pedals):
                self.pedals.append(pedal)
            elif position < 1:
                raise(ValueError("Position value must be greater than or equal to 1."))
            else:
                self.pedals.insert(position-1, pedal)

            self.add_widget(pedal)
            self.controller.enable_effect(effect_name, position)
            self.controller.rewrite_patch_file(create_new_connections=True)
            self.controller.reload_patch()
        except Exception as e:
            self.gui.alert_user(e)

    def turn_off_effect(self, effect_name: str):
        """Turn off a specific effect

        Args:
            effect_name: The name of the effect to turn off
        """
        try:
            pedal = [(i, p) for i, p in enumerate(self.pedals) if p.effect_name == effect_name][0]
            del(self.pedals[pedal[0]])
            self.remove_widget(pedal[1])
            self.controller.disable_effect(effect_name)
            self.controller.rewrite_patch_file(create_new_connections=False)
            self.controller.reload_patch()
        except Exception as e:
            self.gui.alert_user(e)

    def load_parameters(self, effect_name: str, parameters: list):
        """Load effect parameters for a specific effect

        Args:
            effect_name: The name of the effect to update the parameter values
            parameters: List of numbers to update the effect
        """
        pedal = [pedal for pedal in self.pedals if pedal.effect_name == effect_name][0]
        try:
            pedal.load_parameter_values(parameters)
            self.reload_all_pedal_parameters()
        except Exception as e:
            raise(e)

    def reload_all_pedal_parameters(self):
        """Send all pedal parameters to pure-data"""
        for pedal in self.pedals:
            pedal.send_all_to_pd()

    def _update_rect(self, instance, value):
        """Update the shape of the background of this object when the view size changes."""
        self.col_default_width = instance.size[0] / 4
        self.row_default_height = instance.size[1] / 2
        self.rect.pos = instance.pos
        self.rect.size = instance.size