from easyfx.pdcontroller import PDController
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

class EffectContainer(GridLayout): 

    def __init__(self, effect_name: str, controller: PDController, **kwargs):
        super(EffectContainer, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.15, 0.8, 0.48, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.controller = controller
        self.effect_name = effect_name
        self.effect_port, self.effect_parameters = self.get_effect_info()
        self.sliders = []
        self.slider_display_labels = []
        self.effect_parameter_values = []
        self.cols = 1
        self.row_force_default = True
        self.row_default_height = 45

        self.add_widget(Label(text="[b]{}[/b]".format(effect_name), font_size=44, max_lines=1, markup=True, padding_y=10))

        for parameter in self.effect_parameters:
            self.effect_parameter_values.append(parameter['default'])
            self.create_slider(parameter['min_value'], parameter['max_value'], parameter['default'], parameter['name'], parameter['step'])
  
        for i, slider in enumerate(self.sliders):
            slider.bind(value=lambda slider, tmp_val=slider.value, tmp_id=i: self.send_to_pd(slider, tmp_val, tmp_id))

    def send_to_pd(self, instance, value, fx_id):
        self.effect_parameter_values[fx_id] = value
        parameters = ';'.join(str(s) for s in self.effect_parameter_values)
        self.controller.send_message(self.effect_port, parameters)
        for i, value in enumerate(self.slider_display_labels):
            value.text = parameters.split(';')[i]

    def create_slider(self, min_value, max_value, default, name, step_size):
        self.sliders.append(Slider(min=min_value, max=max_value, value=default, step=step_size))
        self.slider_display_labels.append(Label(text='{}'.format(default)))
        self.add_widget(self.sliders[-1])
        self.add_widget(Label(text='{}: '.format(name)))
        self.add_widget(self.slider_display_labels[-1])

    def load_parameter_values(self, new_values: list):
        for i, slider in enumerate(self.sliders):
            slider.value = new_values[i]

    def get_effect_info(self):
        effects_meta = self.controller.load_patch_meta()
        effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == self.effect_name][0]
        return effect_entry['port'], effect_entry['parameters']

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size