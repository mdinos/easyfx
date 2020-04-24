#!/usr/bin/env python

from json import load as load_json

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.properties  import NumericProperty

from pd_controller import PDController

class EffectContainer(GridLayout): 

    def __init__(self, effect_name, controller, **kwargs):
        super(EffectContainer, self).__init__(**kwargs)

        self.controller = controller
        self.effect_name = effect_name
        self.get_effect_info()
        self.cols = 1
        self.col_default_width = 250
        self.row_default_height = 10
        self.sliders = []
        self.slider_display_labels = []
        self.effect_parameter_values = []

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

    def get_effect_info(self):
        with open('patches/patch_meta.json', 'r') as f:
            effects_meta = load_json(f)
        effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == self.effect_name][0]
        self.effect_port = effect_entry['port']
        self.effect_parameters = effect_entry['parameters']

class MainLayout(GridLayout):

    def __init__(self, controller, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 4
        self.controller = controller
    
    def turn_on_effect(self, effect_name, position):
        self.add_widget(EffectContainer(effect_name, self.controller))
        self.controller.enable_effect(effect_name, position)
        self.controller.create_connections_in_file()
        self.controller.reload_patch()

class EasyFx(App): 
    def build(self): 
        self.controller = PDController('patches/master.pd', 'patches/patch_meta.json')
        self.controller.clean_up()
        gui = MainLayout(self.controller)
        gui.turn_on_effect("Phasor", 1)
        gui.turn_on_effect("Delay", 2) # case sensitive, must match name value in patches/patch_meta.json
        return gui 

if __name__ == '__main__':
    root = EasyFx()
    root.run()
    root.controller.clean_up(True)