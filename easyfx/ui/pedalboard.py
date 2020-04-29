from easyfx.ui.effectcontainer import EffectContainer
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

class PedalBoard(GridLayout):

    def __init__(self, controller, gui, **kwargs):
        super(PedalBoard, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.33, 0.43, 0.48, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.cols = 4
        self.rows = 2
        self.controller = controller
        self.gui = gui
        self.pedals = []
    
    def turn_on_effect(self, effect_name, position):
        try:
            pedal = EffectContainer(effect_name, self.controller)

            if position > len(self.pedals):
                self.pedals.append(pedal)
            elif position < 1:
                raise(ValueError("Position value must be greater than or equal to 1."))
            else:
                self.pedals.insert(position-1, pedal)

            self.add_widget(pedal)
            self.controller.enable_effect(effect_name, position)
            self.controller.create_connections_in_file()
            self.controller.reload_patch()
        except Exception as e:
            print(e)
            print('turn on effect error')
            self.gui.alert_user('Error', e)

    def turn_off_effect(self, effect_name):
        try:
            pedal = [(i, p) for i, p in enumerate(self.pedals) if p.effect_name == effect_name][0]
            del(self.pedals[pedal[0]])
            self.remove_widget(pedal[1])
            self.controller.disable_effect(effect_name)
            self.controller.create_connections_in_file()
            self.controller.reload_patch()
        except Exception as e:
            self.gui.alert_user(e)

    def load_parameters(self, effect_name: str, parameters: list):
        pedal = [pedal for pedal in self.pedals if pedal.effect_name == effect_name][0]
        pedal.load_parameter_values(parameters)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size