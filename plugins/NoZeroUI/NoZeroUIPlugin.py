import re
from Plugin import PluginManager

@PluginManager.registerTo("UiRequest")
class UiRequestPlugin(object):
    def renderWrapper(self, *args, **kwargs):
        body = super(UiRequestPlugin, self).renderWrapper(*args, **kwargs)  # Get the wrapper frame output

        #a small message for devs looking at the source code
        info='<!-- This Site/Zite is hosted in the ZeroNet and this is just a static proxy (call it the tip of an iceberg) | More @ https://zeronet.io -->'
        #remove most of the zeronet ui
        inject_html = '<style>.loadingscreen,.loadingscreen>*,.fixbutton {display:none !important}body{background:white !important}</style>'+info+'</body></html>'

        return re.sub("</body>\s*</html>\s*$", inject_html, body)
