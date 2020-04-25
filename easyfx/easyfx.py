import kivy
from kivy.app import App
from easyfx.ui.easyfxlayout import EasyFXLayout
from easyfx.pdcontroller import PDController

class EasyFX(App):
    def build(self): 
        self.controller = PDController('patches/master.pd', 'patches/patch_meta.json')
        self.controller.clean_up()
        gui = EasyFXLayout(self.controller)
        return gui 