
from easyfx.ui.pedalboard import PedalBoard
from easyfx.ui.fxlist import FXList
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class EasyFXLayout(GridLayout):

    def __init__(self, controller, **kwargs):
        super(EasyFXLayout, self).__init__(**kwargs)
        self.cols = 2
        self.pedal_board = PedalBoard(controller, self)
        self.fx_list = FXList(controller, self.pedal_board)
        self.add_widget(self.fx_list)
        self.add_widget(self.pedal_board)
    
    def alert_user(self, title, message):
        print(message)
        content = Button(text=str(message))
        popup = Popup(title=title, size=(200, 200), content=content)
        content.bind(on_press=popup.dismiss)