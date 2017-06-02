import os
import json

from errbot import BotPlugin, botcmd
import config


class ExtraConfig(BotPlugin):
    
    def activate(self):
        super().activate()
        
        # Locate Extra Config File
        extra_conf = ""
        try:
            extra_conf = config.EXTRA_CONFIG_FILE
        except Exception as e:
            self.log.exception(e)
            curr_dir = os.path.dirname(os.path.realpath(__file__))
            extra_conf = os.path.join(curr_dir, "etc/config.json")
        
        # Load Json Data from Extra Config File
        if not os.path.exists(extra_conf):
            self.log.warning("No extra configuration file provided !")
        else:
            with open(extra_conf) as json_file:
                jsonData = json.load(json_file)
                # This example just stores value into persistent database, and
                #   other plugins could add this plugin as a dependence and use
                # this configuration data.
                self['jsonData'] = json.dumps(jsonData)
            