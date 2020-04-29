import datetime
from easyfx.pdcontroller import PDController
from easyfx.ui.pedalboard import PedalBoard
from easyfx.ui.fxlist import FXList
from easyfx.ui.toolbarright import ToolbarRight
from easyfx.ui.toolbarleft import ToolbarLeft
from easyfx.ui.savedialoguecontent import SaveDialogueContent
from json import dumps as dump_json
from json import load as load_json
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from os.path import join as join_path

class EasyFXLayout(GridLayout):

    def __init__(self, controller, root_dir, **kwargs):
        super(EasyFXLayout, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.controller = controller
        self.root_dir = root_dir
        self.toolbar_left = ToolbarLeft(self)
        self.toolbar_right = ToolbarRight(self)
        self.pedal_board = PedalBoard(self.controller, self)
        self.fx_list = FXList(self.controller, self.pedal_board)
        self.scrollView = ScrollView()
        self.scrollView.size_hint = (0.2, 1)
        self.scrollView.do_scroll_x = False
        self.scrollView.add_widget(self.fx_list)
        self.add_widget(self.toolbar_left)
        self.add_widget(self.toolbar_right)
        self.add_widget(self.scrollView)
        self.add_widget(self.pedal_board)

    def save_dialogue(self):
        content = SaveDialogueContent(self)
        self.dialogue = Popup(content=content, title='Please enter a filename: (alphanumeric only)', size_hint=(0.3, None), height=300)
        self.dialogue.open()

    def save(self, filename):
        self.dialogue.dismiss()
        try:
            ts = int(datetime.datetime.now().timestamp())
            save_data = dict(saved_at=ts, patch_file=self.controller.patch_file_name, patch_meta_file=self.controller.patch_meta_file, pedals=[])
            pedals = self.pedal_board.pedals
            for pedal in pedals:
                effect_name = pedal.effect_name
                parameter_values = pedal.effect_parameter_values
                entry = dict(effect=effect_name, parameter_values=parameter_values)
                save_data['pedals'].append(entry)

            with open(join_path(self.root_dir, 'savedata/{}.json'.format(filename)), 'w+') as f:
                f.write(dump_json(save_data, indent=4))
        except Exception as e:
            print(e)
            self.alert_user('Something went wrong saving your file - please try again!')

    def load_dialogue(self):
        content = FileChooserListView(path=join_path(self.root_dir, 'savedata'))
        self.dialogue = Popup(content=content, title='Choose a file', size_hint=(0.5, 0.5))
        self.dialogue.open()
        content.bind(on_submit=self.load)

    def load(self, event, selection, touch):
        self.dialogue.dismiss()
        try:
            with open(selection[0], 'r') as f:
                savedata = load_json(f)
            self.controller.clean_up(clear_connections=True)
            self.controller = PDController(savedata['patch_file'], savedata['patch_meta_file'])
            self.remove_widget(self.pedal_board)
            self.pedal_board = PedalBoard(self.controller, self)
            self.scrollView.remove_widget(self.fx_list)
            self.fx_list = FXList(self.controller, self.pedal_board)
            self.scrollView.add_widget(self.fx_list)
            self.add_widget(self.pedal_board)
            for pedal in savedata['pedals']:
                for effect in self.fx_list.effect_list:
                    if effect.name == pedal['effect']:
                        effect.checkbox.active = True
                        self.pedal_board.load_parameters(effect.name, pedal['parameter_values'])
        except Exception as e:
            print(e)
            self.alert_user('Something went wrong while loading the file - make sure the file was intended for this program!')
    
    def alert_user(self, message, title='Error'):
        content = Button(text=str(message))
        popup = Popup(title=title, size_hint=(0.4, 0.4), content=content)
        content.bind(on_press=popup.dismiss)
        popup.open()