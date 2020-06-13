from easyfx.pdcontroller import PDController
from json import JSONDecodeError
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

class EffectContainer(GridLayout):
    """This class represents an effect pedal.

    Contains methods for manipulating the effect (sending messages to pure-data via the controller)

    Attributes:
        controller: The PDController instance to use for communication with pure-data
        pedal_board: The parent PedalBoard instance for which this EffectContainer is a widget
        effect_name: The name of the effect
        effect_port: The port over which UDP communication occurs with pure-data for this effect
        effect_parameters: A list of adjustable parameters for which sliders will be made
        sliders: A list of sliders which will adjust the effect parameters
        slider_display_labels: A list of slider labels, adjusted when slider values change
        effect_parameter_values: The list of parameters which will be sent to pure-data.
    """
    def __init__(self, effect_name: str, controller: PDController, pedal_board, **kwargs):
        super(EffectContainer, self).__init__(**kwargs)
        self.controller = controller
        self.pedal_board = pedal_board
        self.effect_name = effect_name
        self.effect_port, self.effect_parameters = self._get_effect_info()
        self.effect_parameter_values = []
        self.sliders = []
        self.slider_display_labels = []

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0.15, 0.8, 0.48, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Inherited attributes relating to layout
        self.cols = 1
        self.row_force_default = True
        self.row_default_height = 45

        # Pedal header (name)
        self.add_widget(
            Label(
                text=f'[b]{effect_name}[/b]',
                font_size=44,
                max_lines=1,
                markup=True,
                padding_y=10))

        # Create sliders from parameters
        for parameter in self.effect_parameters:
            self.effect_parameter_values.append(parameter['default'])
            self._create_slider(
                parameter['min_value'],
                parameter['max_value'],
                parameter['default'],
                parameter['name'],
                parameter['step'])
  
        # Bind slider functionality
        for i, slider in enumerate(self.sliders):
            slider.bind(value=lambda slider, tmp_val=slider.value, fx_id=i: self._update_parameter_value(slider, tmp_val, fx_id))

        # Send current effect parameter values to pure data
        for i in range(0, len(self.effect_parameter_values)):
            self.send_param_to_pd(i)

    def send_param_to_pd(self, fx_id: int):
        """Send current parameter values to pure data"""
        value = self.effect_parameter_values[fx_id]
        message = f'{fx_id} {value}'
        self.controller.send_message(self.effect_port, message)

    def load_parameter_values(self, new_values: list):
        """Public function for loading pedal parameter values from a saved file.

        Invokes _update_parameter_value for each slider implicitly.

        Args:
            new_values: list of numbers to load into pure-data

        Raises:
            ValueError if incorrect quantiy of values passed to function
        """
        n = len(new_values)
        m = len(self.effect_parameter_values)
        if n != m:
            raise(ValueError(
                f'Incorrect quantity of values ({n}) passed to effect: {self.effect_name},'
                f'Correct quantity of values is {m}'))
        for i, slider in enumerate(self.sliders):
            slider.value = new_values[i]

    def _create_slider(self, min_value, max_value, default, name: str, step_size):
        """Private function for creating slider widgets.

        Args:
            min_value: The minimum value of the slider
            max_value: The maximum value of the slider
            default: The default value of the slider
            name: The name of the parameter accociated with the slider
            step_size: The step size of the slider
        """
        try:
            self.sliders.append(
                Slider(
                    min=min_value,
                    max=max_value,
                    value=default,
                    step=step_size))
            self.slider_display_labels.append(Label(text=f'{default}'))
            self.add_widget(self.sliders[-1])
            self.add_widget(Label(text=f'{name}: '))
            self.add_widget(self.slider_display_labels[-1])
        except Exception as e:
            self.pedal_board.gui.alert_user(e)

    def _get_effect_info(self) -> tuple:
        """Private function for pulling effect data from patch metadata file.

        Returns:
            Tuple in the format of (effect_port: int, effect_parameters: list of dict)"""
        try:
            effects_meta = self.controller.load_patch_meta()
        except JSONDecodeError:
            self.pedal_board.gui.alert_user('Error in JSON file formatting - please check patch metadata file.')
        except FileNotFoundError:
            self.pedal_board.gui.alert_user('Patch metadata file not found!')
        except Exception as e:
            self.pedal_board.gui.alert_user(e)

        try:
            effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == self.effect_name][0]
        except Exception as e:
            self.pedal_board.gui.alert_user('Issue reading patch metadata file, please check the format.')
        return effect_entry['port'], effect_entry['parameters']

    def _update_parameter_value(self, instance: Slider, value: float, fx_id: int):
        """Private function for updating the parameter values on slider value change

        Args:
            instance: The slider with a new value
            value: The value of the slider
            fx_id: The index in class attribute effect_parameter_values which refers to the slider
        """
        self.effect_parameter_values[fx_id] = value
        try:
            self.send_param_to_pd(fx_id)
        except Exception:
            self.pedal_board.gui.alert_user('Issue sending pedal parameters to pure-data.')
        for i, value in enumerate(self.slider_display_labels):
            value.text = str(self.effect_parameter_values[i])

    def _update_rect(self, instance, value):
        """Update the shape of the background of this object when the view size changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size