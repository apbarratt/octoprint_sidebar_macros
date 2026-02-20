import octoprint.plugin


class SidebarMacrosPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
):
    def get_settings_defaults(self):
        return {
            "column": 1,
            "macros": [
                {
                    "name": "Home",
                    "macro": "G28",
                    "active": True,
                    "type": "default",
                    "dop": True,
                }
            ],
        }

    def get_settings_version(self):
        return 2

    def on_settings_migrate(self, target, current=None):
        if current is None or current < 1:
            new_macros = []
            self._logger.info(self._settings.get(["macros"]))
            for macros in self._settings.get(["macros"]):
                macros["type"] = "default"
                new_macros.append(macros)
            self._settings.set(["macros"], new_macros)
            self._settings.set(["column"], 1)
        if current < 2:
            new_macros = []
            self._logger.info(self._settings.get(["macros"]))
            for macros in self._settings.get(["macros"]):
                macros["dop"] = False
                new_macros.append(macros)
            self._settings.set(["macros"], new_macros)

    def get_template_configs(self):
        return [
            {
                "type": "settings",
                "custom_bindings": True,
                "template": "sidebar_macros_settings.jinja2",
            },
            {
                "type": "sidebar",
                "icon": "rocket",
                "custom_bindings": True,
                "template": "sidebar_macros_sidebar.jinja2",
            },
        ]

    def is_template_autoescaped(self):
        return True

    def get_assets(self):
        return {
            "js": ["js/sidebar_macros.js", "js/sidebar_macros_settings.js"],
            "css": ["css/sidebar_macros.css"],
        }

    def get_update_information(self):
        return {
            "sidebarmacros": {
                "displayName": "Sidebar Macros",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "apbarratt",
                "repo": "octoprint_sidebar_macros",
                "current": self._plugin_version,
                "pip": "https://github.com/apbarratt/octoprint_sidebar_macros/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Sidebar Macros"
__plugin_pythoncompat__ = ">=3.7,<4"  # python 3 only


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = SidebarMacrosPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
