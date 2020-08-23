from src.gui.main import MainWindow
from src.hash.main import HashGenerator
# from src.gui.popup import AlertWindow, PopupWindow

if __name__ == "__main__":

    algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512']

    hash_generator = HashGenerator(algorithms)
    # create and draw the main window
    MainWindow(algorithms, 'SHA256', hash_generator).draw()