from core.classes.app import Library
from core.menu import main_menu
from settings.settings import app_settings

settings = app_settings
lib_app = Library(main_menu, settings)

lib_app.run()
