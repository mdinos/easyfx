from json import load as load_json
from os import popen, rename, remove
import psutil
import datetime

class PDController():

    def __init__(self, patch_file_name: str, patch_meta_file: str):
        self.patch_file_name = patch_file_name
        self.patch_meta_file = patch_meta_file
        self.backup_patch()
        self.adc_id = 0
        self.dac_id = 3
        self.current_conns = []

    """
        Enable an effect, position starts at 1.
    """
    def enable_effect(self, effect_name: str, position: int):
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
            print(e)
            raise(e)

    def disable_effect(self, effect_name: str):
        try:
            effects_meta = self.load_patch_meta()
            effect_entry = [fx for fx in effects_meta['effects'] if fx['name'] == effect_name][0]
            patch_id = effect_entry['patch_identifier']

            connectors = [(i, conn) for i, conn in enumerate(self.current_conns) if patch_id in conn]
            if len(connectors) != 2:
                raise(Exception("There is an error with discovering current enabled effects, please restart the program."))
            for i in range(2):
                del(self.current_conns[connectors[0][0]])

            new_connector = (connectors[0][1][0], connectors[1][1][1])
            insert_position = connectors[0][0]

            self.current_conns.insert(insert_position, new_connector)

        except Exception as e:
            print(e)
            raise(e)

    def create_connections_in_file(self):
        try: 
            with open(self.patch_file_name, "r") as f:
                file_lines = f.readlines()
            dac_idx = [i for i, line in enumerate(file_lines) if ("dac~" in line)][0]
            current_connectors = [dac_idx + i for i, line in enumerate(file_lines[dac_idx:len(file_lines)]) if ("#X connect" in line)]
            file_lines = [line for i, line in enumerate(file_lines) if i not in current_connectors]

            connector_strs = []
            for conn in self.current_conns:
                conn_str = "#X connect {} 0 {} 0;\n".format(conn[0], conn[1])
                connector_strs.append(conn_str)
            
            file_lines.extend(connector_strs)

            with open(self.patch_file_name + '.bak', 'w') as f:
                f.writelines(file_lines)
            
            remove(self.patch_file_name)
            rename(self.patch_file_name + '.bak', self.patch_file_name)
        except Exception as e:
            print(e)
            raise(e)

    def clear_connections_from_file(self):
        try:
            with open(self.patch_file_name, "r") as f:
                file_lines = f.readlines()
            dac_idx = [i for i, line in enumerate(file_lines) if ("dac~" in line)][0]
            current_connectors = [dac_idx + i for i, line in enumerate(file_lines[dac_idx:len(file_lines)]) if ("#X connect" in line)]
            file_lines = [line for i, line in enumerate(file_lines) if i not in current_connectors]

            with open(self.patch_file_name + '.bak', 'w') as f:
                f.writelines(file_lines)

            self.current_conns = []
            remove(self.patch_file_name)
            rename(self.patch_file_name + '.bak', self.patch_file_name)

        except Exception as e:
            print(e)
            raise(e)

    """
        Loads patch file into PD from the patches folder, and starts running pd
    """
    def reload_patch(self):
        try:
            self.clean_up()
            print('Attempting to load {} with pure data.'.format(self.patch_file_name))
            process = popen("./pure-data/bin/pd -nogui -send \"{}\" -open \"{}\" &".format("pd dsp 1", self.patch_file_name))
        except Exception as e:
            print(e)
            raise(e)

    """
        Backup the current patch file to the backups folder with a timestamp
    """
    def backup_patch(self):
        ts = int(datetime.datetime.now().timestamp())
        try:
            filename = self.patch_file_name.split('/')[-1]
            backup_path = 'patches/backups/'
            backup_filename = "{}-{}".format(filename, ts)
            popen("cp {} {}".format(self.patch_file_name, backup_path))
            popen("mv {} {}".format(backup_path + filename, backup_path + backup_filename))
        except Exception as e:
            print(backup_filename)
            print(e)
            raise(e)
    """
        ensure no existing pd processes
    """
    def clean_up(self, clear_connections=False):
        if clear_connections == True:
            self.clear_connections_from_file()
        try:
            # Try and kill off any pure-data instances already running.
            processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'username']) if (p.info['name'] == 'pd' or p.info['name'] == 'Wish')}
            for p in processes:
                print('Killing process {}'.format(p))
                popen('kill {}'.format(p))
        except Exception as e:
            print(e)
            raise(e)

    def load_patch_meta(self):
        with open(self.patch_meta_file, 'r') as f:
            effects_meta = load_json(f)
        return effects_meta

    """
        Pushes a generic message up to PD via pdsend
    """
    @staticmethod
    def send_message(port: int, message: str):
        try:
            print('sending {} message to pd on port {}'.format(message, port))
            popen("echo '{}' | ./pure-data/bin/pdsend {} localhost udp".format(message, port))
        except Exception as e:
            print(e)
            raise(e)
        