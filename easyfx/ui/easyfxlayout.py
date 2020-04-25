
from easyfx.ui.pedalboard import PedalBoard
from easyfx.ui.fxlist import FXList
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

class EasyFXLayout(GridLayout):

    def __init__(self, controller, **kwargs):
        super(EasyFXLayout, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.pedal_board = PedalBoard(controller, self)
        self.pedal_board.size_hint = (0.8, 1)
        self.fx_list = FXList(controller, self.pedal_board)
        self.scrollView = ScrollView()
        self.scrollView.size_hint = (0.2, 1)
        self.scrollView.do_scroll_x = False
        self.scrollView.add_widget(self.fx_list)
        self.add_widget(self.scrollView)
        self.add_widget(self.pedal_board)
    
    def alert_user(self, title, message):
        print(message)
        content = Button(text=str(message))
        popup = Popup(title=title, size=(200, 200), content=content)
        content.bind(on_press=popup.dismiss)