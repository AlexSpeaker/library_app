from core.classes.app import Library
from core.menu import main_menu
from settings.settings import app_settings

if __name__ == "__main__":
    lib_app = Library(main_menu, app_settings)
    lib_app.run()
