from .context import easyfx
from easyfx import EasyFX
from easyfx import PDController
from easyfx.ui import EasyFXLayout
from unittest import TestCase
from mock import patch, MagicMock
import os

class TestEasyFXApp(TestCase):
    def setUp(self):
        self.app = EasyFX()
        self.gui = self.app.build()
        os.path.exists = MagicMock(return_value=False)
        os.makedirs = MagicMock()

    def test_creates_attributes(self):
        self.assertEqual(self.app.title, 'EFX')
        self.assertEqual(self.app.icon, 'img/efx_icon.png')
        
    def test_creates_pdcontroller(self):
        self.assertIsInstance(self.app.controller, PDController)

    def test_returns_gui(self):
        self.assertIsInstance(self.gui, EasyFXLayout)


    

    


