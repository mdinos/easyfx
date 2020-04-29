from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class SaveDialogueContent(BoxLayout):

    def __init__(self, gui, **kwargs):
        super(SaveDialogueContent, self).__init__(**kwargs)
        self.gui = gui
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.input = TextInput(multiline=False)
        self.error_message = Label(markup=True)
        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_press=self._send_filename)

        self.add_widget(self.input)
        self.add_widget(self.error_message)
        self.add_widget(self.submit_button)

    def _send_filename(self, instance):
        if self.input.text.isalnum():
            self.gui.save(self.input.text)
        else:
            self.error_message.text = '[color=ffffff]Your filename must be alphanumeric! [Aa-Zz|0-9][/color]'
            print('nay')
        print(self.input.text)

        