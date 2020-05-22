from json import load as load_json
from json import dumps as dump_json
from os import popen, rename, remove
import psutil
import datetime

class PDController():
    """This class is a controller responsible for communicating with pure data

    Attributes:
        patch_file_name: The file location of the master patch file
        patch_meta_file: The file location of the master patch metadata file
        adc_id: The ID in the master patch file which the ADC object is
        dac_id: The ID in the master patch file which the DAC object is
        current_conns: The list of current connections between pedals, as a list of tuples
    """
    def __init__(self, patch_file_name: str, patch_meta_file: str):
        """Inits PDController, backs up the current patch file, and initiates attributes

        Args:
            patch_file_name: The file location of the master patch file
            patch_meta_file: The file location of the master patch metadata file
        """
        self.patch_file_name = patch_file_name
        self.patch_meta_file = patch_meta_file
        self.backup_patch()
        self.adc_id = 0
        self.dac_id = 1
        self.current_conns = []

    def enable_effect(self, effect_name: str, position: int):
        """Insert an effect into the list of current connections, at a given position.

        In order to activate the effect after using this method, we still need to use
        the "rewrite_patch_file" and "reload_patch" methods.

        Args:
            effect_name: The name of the effect to be enabled (must match name exactly in p
                atch meta file)
            position: The position in the pedal chain to be placed, starts at 1
        """
        try:
            if position < 1:
                raise(ValueError("Position value must be greater than 1."))
            effects_meta = self.load_patch_meta()
            effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == effect_name][0]
            patch_id = effect_entry['patch_identifier']
            
            if len(self.current_conns) == 0:
                previous_object = self.adc_id
                next_object = self.dac_id
                self.current_conns.append((previous_object, patch_id))
                self.current_conns.append((patch_id, next_object))
            else:
                previous_conn = self.current_conns[position-1]
                new_conn_1 = (previous_conn[0], patch_id)
                new_conn_2 = (patch_id, previous_conn[1])

                del(self.current_conns[position-1])
                self.current_conns.insert(position-1, new_conn_1)
                self.current_conns.insert(position, new_conn_2)
        except Exception as e:
            raise(e)

    def disable_effect(self, effect_name: str):
        """Remove an effect from the list of current connections.

        Like enable_effect, we still need to use "rewrite_patch_file" and "reload_patch"
        in order to have the desired effect.

        Args:
            effect_name: The name of the effect to be disabled (must match name exactly in
                patch meta file)
        """
        try:
            effects_meta = self.load_patch_meta()
            effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == effect_name][0]
            patch_id = effect_entry['patch_identifier']

            connectors = [(i, conn) for i, conn in enumerate(self.current_conns) if patch_id in conn]
            if len(connectors) != 2:
                raise(Exception("There is an error with discovering current enabled effects, please restart the program - this may have happened due to a DSP Loop, i.e. an effect was initiated multiple times somehow."))
            for i in range(2):
                del(self.current_conns[connectors[0][0]])

            new_connector = (connectors[0][1][0], connectors[1][1][1])
            insert_position = connectors[0][0]
            self.current_conns.insert(insert_position, new_connector)

        except Exception as e:
            raise(e)

    def rewrite_patch_file(self, create_new_connections: bool):
        """Create the connections listed in self.current_conns attribute in the patch file.

        In order to load this new file, "reload_patch" method must still be called.

        Args: 
            create_new_connections: Whether the current connections should simply be cleared (False)
                or if they should be created as in self.current_conns
        """
        try: 
            with open(self.patch_file_name, "r") as f:
                file_lines = f.readlines()
            # Find and remove all connection lines
            print(file_lines)
            current_connectors = [i for i, line in enumerate(file_lines) if ("#X connect" in line)]
            print(current_connectors)
            file_lines = [line for i, line in enumerate(file_lines) if i not in current_connectors]
            file_lines = [line for line in file_lines if line != '\n']

            # Rewrite connection lines with respect to class state (self.current_conns)
            if create_new_connections:
                connector_strs = []
                for conn in self.current_conns:
                    conn_str = f'\n#X connect {conn[0]} 0 {conn[1]} 0;'
                    connector_strs.append(conn_str)
                file_lines.extend(connector_strs)

            print(file_lines)

            # Write to new file, and replace the old one.
            with open(self.patch_file_name + '.bak', 'w') as f:
                f.writelines(file_lines)
            remove(self.patch_file_name)
            rename(self.patch_file_name + '.bak', self.patch_file_name)
        except Exception as e:
            raise(e)

    def add_imported_effect_to_master(self, entry: dict):
        """Adds an imported effect to the master patch.
        
        Also add the entry supplied into the patch_meta.json file

        Args:
            entry: The dictionary generated by the ImportDialogueContent popup"""
        try:
            # Remove current connections in file
            self.rewrite_patch_file(False)

            # Add new object to patch file
            with open(self.patch_file_name, "r") as f:
                file_lines = f.readlines()
            objects_in_patch = [line for line in file_lines if ("obj" in line)]
            patch_identifier = len(objects_in_patch)
            entry['patch_identifier'] = patch_identifier

            canvas_loc = int(file_lines[-1].split(' ')[3]) + 70
            effect_name = entry['name']

            obj_string = f'#X obj {canvas_loc} 64 {effect_name};'
            file_lines.append(obj_string)

            with open(self.patch_file_name + '.bak', 'w') as f:
                f.writelines(file_lines)
            remove(self.patch_file_name)
            rename(self.patch_file_name + '.bak', self.patch_file_name)

            # Write out new patch metadata file
            effects_meta = self.load_patch_meta()
            effects_meta['effects'].append(entry)

            with open(self.patch_meta_file + '.bak', 'w') as f:
                f.write(dump_json(effects_meta, indent=4))
            remove(self.patch_meta_file)
            rename(self.patch_meta_file + '.bak', self.patch_meta_file)

            self.rewrite_patch_file(True)
        except Exception as e:
            raise(e)

    def reload_patch(self):
        """Loads patch file into PD from the patches folder, and starts running pd"""
        try:
            self.clean_up()
            process = popen("./pure-data/bin/pd -nogui -send \"{}\" -open \"{}\" &".format("pd dsp 1", self.patch_file_name))
        except Exception as e:
            raise(e)

    def backup_patch(self):
        """Backup the current patch file to the backups folder with a timestamp"""
        ts = int(datetime.datetime.now().timestamp())
        try:
            filename = self.patch_file_name.split('/')[-1]
            backup_path = 'patches/backups/'
            backup_filename = "{}-{}".format(filename, ts)
            popen("cp {} {}".format(self.patch_file_name, backup_path))
            popen("mv {} {}".format(backup_path + filename, backup_path + backup_filename))
        except Exception as e:
            raise(e)

    def clean_up(self, clear_connections=False):
        """Ensure no existing pure-data processes

        Args:
            clear_connections: Whether or not the patch file connections should be removed."""
        if clear_connections == True:
            self.rewrite_patch_file(create_new_connections=False)
        try:
            # Try and kill off any pure-data instances already running.
            processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'username']) if (p.info['name'] == 'pd' or p.info['name'] == 'Wish')}
            for p in processes:
                print('Killing process {}'.format(p))
                popen('kill {}'.format(p))
        except Exception as e:
            raise(e)

    def load_patch_meta(self) -> dict:
        """Retrieve patch meta file

        Returns:
            A dict containing a list of effects available in the patch file.
        """
        try:
            with open(self.patch_meta_file, 'r') as f:
                effects_meta = load_json(f)
        except Exception as e:
            raise(e)
        return effects_meta

    @staticmethod
    def send_message(port: int, message: str):
        """Pushes a generic message up to PD via pdsend"""
        try:
            print('sending {} message to pd on port {}'.format(message, port))
            popen("echo '{}' | ./pure-data/bin/pdsend {} localhost udp".format(message, port))
        except Exception as e:
            raise(e)
        