import urlparse

from errbot import BotPlugin


class UtilsFunc(BotPlugin):

    def activate(self):
        super().activate()
        
        self.extraConfig = self.get_plugin("ExtraConfig")
        self.slackConf = self.extraConfig.load("Slack")

    def send_msg(self, msg=None, color="#0abab5", title="", body=""):
        self.send_card(in_reply_to=msg,
                       color=color,
                       title=title,
                       body=body)

    def get_slack_user(self, username):
        
        slack_user = self.slackConf['default_user']
        
        if not username:
            self.log.warnning("No Username provided !")
        elif username not in self.bbConfig['managed_bbg_team']:
            self.log.warnning("User %s not in BlueBox.managed_bbg_team !" % username)
        else:
            slack_user = self.bbConfig['managed_bbg_team'][username]
        return slack_user

    def replace_url_domain(self, current_url, expected_domain):
        try:
            parsed_url = urlparse.urlparse(current_url)
            replaced_url = parsed_url._replace(netloc=expected_domain)
            return replaced_url.geturl()
        except Exception as e:
            self.log.exception(e)
            return "www.google.com"