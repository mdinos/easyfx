#!/usr/bin/env python

import kivy  
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.slider import Slider 
from kivy.uix.label import Label 
from kivy.properties  import NumericProperty 

from pd_controller import *
import json

class EffectContainer(GridLayout): 

    def __init__(self, file_name, **kwargs): 
        super(EffectContainer, self).__init__(**kwargs) 

        # temp code
        self.file_name = file_name
        load_patch('patches/{}.pd'.format(self.file_name))

        if not self.file_name:
            raise ValueError("No file name given to load effect.")

        self.get_effect_info()
        self.cols = 2 * len(self.effect_parameters)
        self.sliders = []
        self.slider_display_labels = []
        self.effect_parameter_values = []

        for parameter in self.effect_parameters:
            self.effect_parameter_values.append(parameter['default'])
            self.create_slider(parameter['min_value'], parameter['max_value'], parameter['default'], parameter['name'])
  
        for i, slider in enumerate(self.sliders):
            self.add_widget(slider)
            slider.bind(value=lambda slider, tmp_val=slider.value, tmp_id=i: self.send_to_pd(slider, tmp_val, tmp_id))

        for value in self.slider_display_labels:
            self.add_widget(value)

    def send_to_pd(self, instance, value, fx_id):   
        self.effect_parameter_values[fx_id] = value  
        tmp = [str(s) for s in self.effect_parameter_values]
        parameters = ';'.join(tmp)
        print(fx_id)
        print(parameters)
        send_message(self.effect_port, parameters)
        for i, value in enumerate(self.slider_display_labels):
            value.text = parameters.split(';')[i]

    def create_slider(self, min_value, max_value, default, name):
        self.sliders.append(Slider(min=min_value, max=max_value, value=default))
        self.add_widget(Label(text='{}: '.format(name)))
        self.slider_display_labels.append(Label(text='{}'.format(default)))

    def get_effect_info(self):
        with open('patches/{}.json'.format(self.file_name), 'r') as effect:
            effect_meta = json.load(effect)
        self.effect_name = effect_meta['name']
        self.effect_port = effect_meta['port']
        self.effect_parameters = effect_meta['parameters']

  
# The app class 
class EasyFx(App): 
    def build(self): 
        effectContainer = EffectContainer("delay001")
        return effectContainer 

root = EasyFx() 
root.run() 

