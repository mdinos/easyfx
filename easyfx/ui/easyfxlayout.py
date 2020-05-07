import datetime
from easyfx.pdcontroller import PDController
from easyfx.ui.pedalboard import PedalBoard
from easyfx.ui.fxlist import FXList
from easyfx.ui.toolbarright import ToolbarRight
from easyfx.ui.toolbarleft import ToolbarLeft
from easyfx.ui.savedialoguecontent import SaveDialogueContent
from easyfx.ui.importdialoguecontent import ImportDialogueContent
from json import dumps as dump_json
from json import load as load_json
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from os.path import join as join_path
from os import popen

class EasyFXLayout(GridLayout):
    """
    This class represents the entire application window - all other widgets are children of this one.

    Attributes:
        controller: An instance of PDController
        root_dir: The directory for which we have access to files in
    """

    def __init__(self, controller: PDController, root_dir: str, **kwargs):
        """Inits EasyFXLayout and adds required child widgets."""
        super(EasyFXLayout, self).__init__(**kwargs)

        # Instance attributes
        self.controller = controller
        self.root_dir = root_dir

        # GridLayout properties
        self.cols = 2
        self.rows = 2

        # GUI elements
        self.toolbar_left = ToolbarLeft(self)
        self.toolbar_right = ToolbarRight()
        self.pedal_board = PedalBoard(self.controller, self)
        self.fx_list = FXList(self.controller, self.pedal_board)

        # Allow a scrolling view of the FXList, incase there are too
        # many effects to show
        self.scrollView = ScrollView()
        self.scrollView.size_hint = (0.2, 1)
        self.scrollView.do_scroll_x = False
        self.scrollView.add_widget(self.fx_list)

        # Add widgets to the GridLayout
        self.add_widget(self.toolbar_left)
        self.add_widget(self.toolbar_right)
        self.add_widget(self.scrollView)
        self.add_widget(self.pedal_board)

    def save_dialogue(self):
        """Opens a dialogue to enter a filename"""
        content = SaveDialogueContent(self)
        self.dialogue = Popup(
            content=content,
            title='Please enter a filename: (alphanumeric only)',
            size_hint=(0.3, None),
            height=300)
        self.dialogue.open()

    def save(self, filename: str):
        """Gathers parameters from program, creates a dict, writes JSON to file.

        Is called by a function in SaveDialogueContent.

        Args:
            filename: The name of the file to be saved.
        """

        self.dialogue.dismiss()
        try:
            ts = int(datetime.datetime.now().timestamp())

            # Format save data
            save_data = dict(
                saved_at=ts,
                patch_file=self.controller.patch_file_name,
                patch_meta_file=self.controller.patch_meta_file,
                pedals=[])

            # Get current pedal parameter values, and place them in the dictionary.
            for pedal in self.pedal_board.pedals:
                effect_name = pedal.effect_name
                parameter_values = pedal.effect_parameter_values
                entry = dict(
                    effect=effect_name,
                    parameter_values=parameter_values)

                save_data['pedals'].append(entry)

            # Save the file
            save_file_path = join_path(self.root_dir, f'savedata/{filename}.json')
            file_contents = dump_json(save_data, indent=4)
            with open(save_file_path, 'w+') as f:
                f.write(file_contents)

            self.alert_user(f'Successfully saved your pedalboard at {save_file_path}')

        except Exception as e:
            self.alert_user('Something went wrong saving your file - please try again!')

    def load_dialogue(self):
        """Opens a FileChooserListView widget to choose a file to load."""
        default_directory = join_path(self.root_dir, 'savedata')
        content = FileChooserListView(path=default_directory)
        self.dialogue = Popup(
            content=content,
            title='Choose a file',
            size_hint=(0.5, 0.5))
        self.dialogue.open()
        content.bind(on_submit=self.load)

    def load(self, event, selection, touch):
        """Load state from saved JSON file.

        Loads a JSON file from disk and replaces GUI elements with those with
        state from saved file.

        Args:
            event: The type of event recieved, always will be on_submit in current use case (not used)
            selection: A list of objects selected in the FileChooserListView (first always selected)
            touch: Mouse coordinates of the event (not used)
        """
        self.dialogue.dismiss()
        try:
            # Access file
            with open(selection[0], 'r') as f:
                savedata = load_json(f)

            # Remove currently loaded pedals
            self.controller.clean_up(clear_connections=True)

            # Replace current GUI objects with objects created with data from file
            self.controller = PDController(savedata['patch_file'], savedata['patch_meta_file'])
            self.remove_widget(self.pedal_board)
            self.pedal_board = PedalBoard(self.controller, self)
            self.scrollView.remove_widget(self.fx_list)
            self.fx_list = FXList(self.controller, self.pedal_board)
            self.scrollView.add_widget(self.fx_list)
            self.add_widget(self.pedal_board)

            # Activate effects and send saved parameters to each effect
            for pedal in savedata['pedals']:
                for effect in self.fx_list.effect_list:
                    if effect.name == pedal['effect']:
                        # Activate effect
                        effect.checkbox.active = True
                        # Send saved parameters to pure-data
                        self.pedal_board.load_parameters(effect.name, pedal['parameter_values'])

        except Exception as e:
            self.alert_user(
                'Something went wrong while loading the file - '
                'make sure the file was intended for this program!')

    def import_dialogue(self):
        """Opens a FileChooserListView widget to choose a PD Patch file to import."""
        content = FileChooserListView(path=self.root_dir)
        self.dialogue = Popup(
            content=content,
            title='Choose a Pure Data patch file to import',
            size_hint=(0.5, 0.5))
        self.dialogue.open()
        content.bind(on_submit=self.get_patch_meta_from_user)

    def get_patch_meta_from_user(self, event, selection, touch):
        """Second step of importing new user effect; creates input fields to gather patch metadata.
        
        Args:
            event: The type of event recieved, always will be on_submit in current use case (not used)
            selection: A list of objects selected in the FileChooserListView (first always selected)
            touch: Mouse coordinates of the event (not used)"""
        self.dialogue.dismiss()
        try:
            file = selection[0]
            popen(f'cp {file} ./patches')
            content = ImportDialogueContent(self)
            self.dialogue = Popup(
                title='Please enter information regarding the pedal configuration.',
                content=content
            )
            self.dialogue.open()
        except Exception as e:
            print(e)
            self.alert_user('We\'re sorry! Something went wrong!'
                            'Please ensure you entered the correct information.')

    def add_patch_meta(self, entry: dict):
        """Adds the patch metadata to the file."""
        self.dialogue.dismiss()
        try:
            self.controller.add_imported_effect_to_master(entry)
        except Exception as e:
            print(e)
            self.alert_user('Something went wrong in applying your new patch.')
    
    def alert_user(self, message: str, title='Error'):
        """Send an alert popup to the user"""
        content = Button(text=str(message))
        popup = Popup(title=title,
            size_hint=(0.3, None),
            height=400,
            content=content)
        content.bind(on_press=popup.dismiss)
        popup.open()