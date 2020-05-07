from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class ImportDialogueContent(BoxLayout):
    """Custom layout for import dialogue popup.

    Attributes:
        gui: The current EasyFXLayout instance
        error_message: A text Label for displaying issues with user input
        submit_button: A Button object to submit the input data, and trigger the import.
    """

    def __init__(self, gui, **kwargs):
        """Inits ImportDialogueContent class

        Args:
            gui: The current EasyFXLayout instance
        """
        super(ImportDialogueContent, self).__init__(**kwargs)
        # Inherited attributes
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.size_hint = (0.3, 1)

        # Attributes
        self.gui = gui
        self.name_field_label = Label(text='Name of effect (Must match patch filename!)')
        self.name_field = TextInput(multiline=False)
        self.port_field_label = Label(text='Network Port')
        self.port_field = TextInput(multiline=False)
        self.parameter_name_fields = []
        self.parameter_min_value_fields = []
        self.parameter_max_value_fields = []
        self.parameter_default_value_fields = []
        self.parameter_step_fields = []

        self.add_parameter_button = Button(text='Add effect parameter')
        self.add_parameter_button.bind(on_press=self._add_parameter)

        self.error_message = Label(markup=True)

        self.submit_button = Button(text='Submit')
        self.submit_button.bind(on_press=self._send_data)

        # Add child widgets
        self.add_widget(self.add_parameter_button)
        self.add_widget(self.name_field_label)
        self.add_widget(self.name_field)
        self.add_widget(self.port_field_label)
        self.add_widget(self.port_field)
        self.add_widget(self.error_message)
        self.add_widget(self.submit_button)

    def _send_data(self, instance):
        """Private method for structuring and sending data collected in this form to the patch_meta_file"""
        effect_entry = dict()
        
        try:
            effect_entry = dict(
                name=self.name_field.text,
                port=int(self.port_field.text),
                patch_identifier=-1,
                parameters = []
            )
        except Exception as e:
            self.error_message.text = '[color=ffffff]There was an issue with your parameter entry data! Please check it.[/color]'

        parameter_entries = self.generate_parameter_entries()
        while True:
            try:
                entry = next(parameter_entries)
                effect_entry['parameters'].append(entry)
            except StopIteration:
                break
        
        self.gui.add_patch_meta(effect_entry)

    def generate_parameter_entries(self):
        for i, field in enumerate(self.parameter_name_fields):
            try:
                entry = dict(
                    name=field.text,
                    min_value=float(self.parameter_min_value_fields[i].text),
                    max_value=float(self.parameter_max_value_fields[i].text),
                    default=float(self.parameter_default_value_fields[i].text),
                    step=float(self.parameter_step_fields[i].text)
                )
                yield entry
            except Exception as e:
                self.error_message.text = '[color=ffffff]There was an issue with your parameter entry data! Please check it.[/color]'

    def _add_parameter(self, instance):
        """Private method for adding parameter form elements to the layout"""
        # Keep these at the end of the form
        self.remove_widget(self.error_message)
        self.remove_widget(self.submit_button)

        # Create widgets
        name_field_label = Label(text='Name of effect parameter')
        name_field = TextInput(multiline=False)
        min_value_label = Label(text='Minimum parameter value')
        min_value_field = TextInput(multiline=False)
        max_value_label = Label(text='Maximum parameter value')
        max_value_field = TextInput(multiline=False)
        default_value_label = Label(text='Default parameter value')
        default_value_field = TextInput(multiline=False)
        step_label = Label(text='Size of step')
        step_field = TextInput(multiline=False)

        # Keep track of the input fields
        self.parameter_name_fields.append(name_field)
        self.parameter_min_value_fields.append(min_value_field)
        self.parameter_max_value_fields.append(max_value_field)
        self.parameter_default_value_fields.append(default_value_field)
        self.parameter_step_fields.append(step_field)

        # Add widgets
        self.add_widget(name_field_label)
        self.add_widget(name_field)
        self.add_widget(min_value_label)
        self.add_widget(min_value_field)
        self.add_widget(max_value_label)
        self.add_widget(max_value_field)
        self.add_widget(default_value_label)
        self.add_widget(default_value_field)
        self.add_widget(step_label)
        self.add_widget(step_field)
        self.add_widget(self.error_message)
        self.add_widget(self.submit_button)
