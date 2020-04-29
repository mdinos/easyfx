import kivy
import os
from kivy.app import App
from easyfx.ui.easyfxlayout import EasyFXLayout
from easyfx.pdcontroller import PDController


class EasyFX(App):
    def build(self): 
        self.icon = 'img/efx_icon.png'
        self.title = 'EFX'
        self.controller = PDController('patches/master.pd', 'patches/patch_meta.json')
        self.controller.clean_up()
        save_folder = os.path.join(self.user_data_dir, 'savedata')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        gui = EasyFXLayout(self.controller, self.user_data_dir)
        return gui
