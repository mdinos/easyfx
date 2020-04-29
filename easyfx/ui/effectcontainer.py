from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

class EffectContainer(BoxLayout):

    def __init__(self, effect_name, controller, **kwargs):
        super(EffectContainer, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (0.25, 0.5)

        self.controller = controller
        self.effect_name = effect_name
        self.get_effect_info()
        self.sliders = []
        self.slider_display_labels = []
        self.effect_parameter_values = []

        self.add_widget(Label(text=effect_name, font_size=54, max_lines=1))

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
        self.effect_port = effect_entry['port']
        self.effect_parameters = effect_entry['parameters']