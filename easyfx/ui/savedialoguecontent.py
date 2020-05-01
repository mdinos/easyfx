from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class SaveDialogueContent(BoxLayout):
    """Custom layout for save dialogue popup.

    Attributes:
        gui: The current EasyFXLayout instance
        input: A TextInput object for users to enter their save file name
        error_message: A text Label for displaying issues with user input
        submit_button: A Button object to submit the input data, and trigger the save.
    """

    def __init__(self, gui, **kwargs):
        """Inits SaveDialogueContent class

        Args:
            gui: The current EasyFXLayout instance
        """
        super(SaveDialogueContent, self).__init__(**kwargs)
        # Inherited attributes
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Attributes
        self.gui = gui
        self.input = TextInput(multiline=False)
        self.error_message = Label(markup=True)
        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_press=self._send_filename)

        # Add child widgets
        self.add_widget(self.input)
        self.add_widget(self.error_message)
        self.add_widget(self.submit_button)

    def _send_filename(self, instance):
        """Private method for checking user input and triggering the save if input is OK."""
        if self.input.text.isalnum():
            self.gui.save(self.input.text)
        else:
            self.error_message.text = '[color=ffffff]Your filename must be alphanumeric! [Aa-Zz|0-9][/color]'

        