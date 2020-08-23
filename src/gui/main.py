import PySimpleGUI as sg

class MainWindow:
    def __init__(self):
        # class vars
        self.kill_code = "Quit"
        self.about_label = "About..."
        self.hash_algos = ['MD5', 'SHA1', 'SHA256', 'SHA512']
        default_hash_algo = 'SHA256'

        # window styling
        sg.theme('Dark Blue 3')

        hash_radio_buttons = []
        for hash_algo in self.hash_algos:
            if hash_algo == default_hash_algo:
                button = sg.Radio(hash_algo, key='{}'.format(hash_algo), group_id="hash_algo", default=True)
            else:
                button = sg.Radio(hash_algo, key='{}'.format(hash_algo), group_id="hash_algo")

            # don't know how to get this working :(
            # if hash_algo == default_hash_algo:
            #     button.default=True
            hash_radio_buttons.append(button)

        # Window layout
        menubar =  [['&File', ['&Check new file', '&History', '---', '&{}'.format(self.kill_code),]],
                    ['&Help', '&{}'.format(self.about_label)],]
        self.layout = [ [sg.Menu(menubar)],
                    [sg.T("Choose file to verify")],
                    [sg.In(key="-FILE-INPUT-", enable_events=True)],
                    [sg.FileBrowse(target="-FILE-INPUT-")],
                    [sg.Text('_'*45)],
                    [sg.T("Choose your hash algorithm")],
                    hash_radio_buttons,
                    [sg.Text('_'*45)],
                    [sg.T("Enter the hash value to check against")],
                    [sg.In(key="-HASH-INPUT-", enable_events=True)],
                    [sg.OK(key="-OK-", disabled=True)] ]

    def draw(self):
        # Create the Window
        window = sg.Window('File Verifier', self.layout, margins=(25, 25))

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()

            # if there is a potential file path, then ok button enabled
            if values['-FILE-INPUT-'] and values['-HASH-INPUT-']:
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)

            if event in (sg.WIN_CLOSED, self.kill_code):
                break
            elif event == "-OK-":
                hash_algo = None
                for hash_algo in self.hash_algos:
                    if values[hash_algo]:
                        break
                sg.popup("Computing the {} of {}".format(hash_algo, values['-FILE-INPUT-']))
            elif event == self.about_label:
                sg.popup("About...", "File Verifier\nV1.0.0")

        window.close()