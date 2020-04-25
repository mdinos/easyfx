
from easyfx.ui.effectlistitem import EffectListItem
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class FXList(GridLayout):

    def __init__(self, controller, pedal_board, **kwargs):
        super(FXList, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.78, 0.08, 0.16, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.cols = 1
        self.padding = 10
        self.controller = controller
        self.pedal_board = pedal_board
        self.effect_names = self.get_effect_names()

        self.effect_list = []

        self.add_widget(Label(text='FXList'))

        for name in self.effect_names:
            self.effect_list.append(EffectListItem(name, self.pedal_board))
        
        for effect in self.effect_list:
            self.add_widget(effect)

    def get_effect_names(self):
        effects_meta = self.controller.load_patch_meta()
        return [fx['name'] for fx in effects_meta['effects']]

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size