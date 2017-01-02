import re
import sys

from Config import config
from Plugin import PluginManager
from Crypt import CryptBitcoin
import UserPlugin


@PluginManager.registerTo("UiRequest")
class UiRequestPlugin(object):
    def __init__(self, *args, **kwargs):
        self.user_manager = sys.modules["User.UserManager"].user_manager
        super(UiRequestPlugin, self).__init__(*args, **kwargs)

    # Create new user
    # Return: back_generator
    def actionWrapper(self, path, extra_headers=None):
        print "Serve "+path
        # Prevent accessing anything but the Zite specified
        if not re.match("/[A-Za-z0-9\._-]*"+config.homepage+"[/]*.*", path):
            return False
        match = re.match("/(?P<address>[A-Za-z0-9\._-]+)(?P<inner_path>/.*|$)", path)
        if not match:
            return False
        inner_path = match.group("inner_path").lstrip("/")
        html_request = "." not in inner_path or inner_path.endswith(".html")  # Only inject html to html requests

        user_created = False
        if html_request:
            user = self.getCurrentUser()  # Get user from cookie
            if not user:  # No user found by cookie
                user = self.user_manager.create()
                user_created = True

        if user_created:
            if not extra_headers:
                extra_headers = []
            extra_headers.append(('Set-Cookie', "master_address=%s;path=/;max-age=2592000;" % user.master_address))  # = 30 days

        loggedin = self.get.get("login") == "done"

        back_generator = super(UiRequestPlugin, self).actionWrapper(path, extra_headers)  # Get the wrapper frame output

        if not extra_headers:
            extra_headers = []

        if not back_generator:  # Wrapper error or not string returned, injection not possible
            return False
        return back_generator



    # Get the current user based on request's cookies
    # Return: User object or None if no match
    def getCurrentUser(self):
        cookies = self.getCookies()
        user = None
        if "master_address" in cookies:
            users = self.user_manager.list()
            user = users.get(cookies["master_address"])
        return user


@PluginManager.registerTo("UiWebsocket")
class UiWebsocketPlugin(object):
    # Let the page know we running in multiuser mode
    def formatServerInfo(self):
        server_info = super(UiWebsocketPlugin, self).formatServerInfo()
        server_info["static"] = True
        #server_info["multiuser"] = True
        #if "ADMIN" in self.site.settings["permissions"]:
        #    server_info["master_address"] = self.user.master_address
        return server_info

    # Disable not Multiuser safe functions
    def actionSiteDelete(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "This function is disabled on this proxy"])
        else:
            return super(UiWebsocketPlugin, self).actionSiteDelete(to, *args, **kwargs)

    def actionConfigSet(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "This function is disabled on this proxy"])
        else:
            return super(UiWebsocketPlugin, self).actionConfigSet(to, *args, **kwargs)

    def actionServerShutdown(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "This function is disabled on this proxy"])
        else:
            return super(UiWebsocketPlugin, self).actionServerShutdown(to, *args, **kwargs)

    def actionServerUpdate(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "This function is disabled on this proxy"])
        else:
            return super(UiWebsocketPlugin, self).actionServerUpdate(to, *args, **kwargs)

    def actionSiteClone(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "This function is disabled on this proxy"])
        else:
            return super(UiWebsocketPlugin, self).actionSiteClone(to, *args, **kwargs)

    #Disable anything "non-static"
    def actionCertAdd(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "Please use a local ZeroNet client"])
        else:
            return super(UiWebsocketPlugin, self).actionCertAdd(to, *args, **kwargs)

    def actionCertSelect(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "Please use a local ZeroNet client"])
        else:
            return super(UiWebsocketPlugin, self).actionCertSelect(to, *args, **kwargs)

    def actionFileDelete(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "Please use a local ZeroNet client"])
        else:
            return super(UiWebsocketPlugin, self).actionFilqDelete(to, *args, **kwargs)

    def actionFileWrite(self, to, *args, **kwargs):
        if not config.less_restricted:
            self.cmd("notification", ["info", "Please use a local ZeroNet client"])
        else:
            return super(UiWebsocketPlugin, self).actionFileWrite(to, *args, **kwargs)



@PluginManager.registerTo("ConfigPlugin")
class ConfigPlugin(object):
    def createArguments(self):
        group = self.parser.add_argument_group("Multiuser plugin")
        group.add_argument('--less_restricted', help="Enable unsafe Ui functions, write users to disk and allow actions like certSelect", action='store_true')

        return super(ConfigPlugin, self).createArguments()
