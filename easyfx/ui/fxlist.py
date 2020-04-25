
from easyfx.ui.effectlistitem import EffectListItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class FXList(BoxLayout):

    def __init__(self, controller, pedal_board, **kwargs):
        super(FXList, self).__init__(**kwargs)
        self.add_widget(Label(text='FXList'))
        self.controller = controller
        self.pedal_board = pedal_board
        self.effect_names = self.get_effect_names()
        self.orientation = 'vertical'

        self.effect_list = []

        for name in self.effect_names:
            self.effect_list.append(EffectListItem(name, self.pedal_board))
        
        for effect in self.effect_list:
            self.add_widget(effect)

    def get_effect_names(self):
        effects_meta = self.controller.load_patch_meta()
        return [fx['name'] for fx in effects_meta['effects']]