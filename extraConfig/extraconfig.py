import os
import json

from errbot import BotPlugin
import config


class ExtraConfig(BotPlugin):
    
    def activate(self):
        super().activate()

        # Locate Extra Config File
        extra_conf = ""
        if not hasattr(config, "EXTRA_CONFIG_FILE"):
            curr_dir = os.path.dirname(os.path.realpath(__file__))
            extra_conf = os.path.join(curr_dir, "etc/config.json")
        else:
            extra_conf = config.EXTRA_CONFIG_FILE

        # Load Json Data from Extra Config File
        if not os.path.exists(extra_conf):
            self.log.warning("No extra configuration file provided !")
        else:
            with open(extra_conf) as json_file:
                jsonData = json.load(json_file)
                # This example just stores value into persistent database, and
                #   other plugins could add this plugin as a dependence and use
                # this configuration data.
                self['extraConfig'] = json.dumps(jsonData)

    def load(self, configType):
        # Type will decide which sections we provide, such as PagerDuty, Slack
        #   and so on.
        try:
            extraConfig = json.loads(self['extraConfig'])

            if configType in extraConfig:
                return extraConfig[configType]
            else:
                self.log.error("Type %s is not supported !" % configType)
                return None
        except Exception as e:
            self.log.exception(e)
            self.log.error("Loading Extra Config Failed !")
            return None