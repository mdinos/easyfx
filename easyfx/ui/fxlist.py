
from easyfx.ui.effectlistitem import EffectListItem
from easyfx.ui.pedalboard import PedalBoard
from easyfx.pdcontroller import PDController
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class FXList(GridLayout):
    """Class for laying out a list of toggleable effects available.

    Attributes:
        controller: The PDController instance currently active
        pedal_board: The current PedalBoard instance
        effect_names: List of all available effects
    """

    def __init__(self, controller: PDController, pedal_board: PedalBoard, **kwargs):
        """Inits FXList class

        Args:
            controller: The PDController instance currently active
            pedal_board: The PedalBoard instance currently active
        """
        super(FXList, self).__init__(**kwargs)

        # For a custom coloured background for this GUI object
        with self.canvas.before:
            Color(0.78, 0.08, 0.16, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Inherited attributes
        self.row_force_default = True
        self.row_default_height = 50
        self.cols = 1
        self.padding = 10
        self.spacing = 10

        # Initialise attributes
        self.controller = controller
        self.pedal_board = pedal_board
        self.effect_names = self.get_effect_names()
        self.effect_list = []

        # Add title label
        self.add_widget(
            Label(
                text='[b]Available Effects[/b]',
                size=(3,3),
                markup=True))

        # Create child list items
        for name in self.effect_names:
            list_item = EffectListItem(name, self.pedal_board)
            self.effect_list.append(list_item)
            self.add_widget(list_item)

    def get_effect_names(self) -> list:
        """Via controller, extracts effect names from patch metadata file
        Returns:
            List of effect names.
        """
        try:
            effects_meta = self.controller.load_patch_meta()
        except JSONDecodeError:
            self.pedal_board.gui.alert_user('Error in JSON file formatting - please check patch metadata file.')
        except FileNotFoundError:
            self.pedal_board.gui.alert_user('Patch metadata file not found!')
        except Exception as e:
            self.pedal_Board.gui.alert_user(e)
        return [fx['name'] for fx in effects_meta['effects']]

    def _update_rect(self, instance, value):
        """Update the shape of the background of this object when the view size changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size