import unittest

from octoprint_sidebar_macros import SidebarMacrosPlugin


class Settings:
    def __init__(self, data):
        self.data = data

    def get(self, path):
        return self.data[path[0]]

    def set(self, path, value):
        self.data[path[0]] = value


class Logger:
    def info(self, *args):
        pass


class SettingsMigrationTest(unittest.TestCase):
    def test_migrates_unversioned_settings_to_current_version(self):
        plugin = SidebarMacrosPlugin()
        plugin._settings = Settings(
            {
                "macros": [
                    {
                        "name": "Home",
                        "macro": "G28",
                        "active": True,
                    }
                ]
            }
        )
        plugin._logger = Logger()

        plugin.on_settings_migrate(target=2, current=None)

        self.assertEqual(plugin._settings.get(["column"]), 1)
        self.assertEqual(
            plugin._settings.get(["macros"]),
            [
                {
                    "name": "Home",
                    "macro": "G28",
                    "active": True,
                    "type": "default",
                    "dop": False,
                }
            ],
        )
