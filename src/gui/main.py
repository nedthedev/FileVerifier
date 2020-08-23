import PySimpleGUI as sg

class MainWindow:
    def __init__(self, algorithms, default_algo, hash_generator):
        # variable declarations
        self.kill_code = "Quit"
        self.about_label = "About..."
        self.hash_generator = hash_generator
        self.hash_algos = algorithms
        default_hash_algo = default_algo

        # window styling
        sg.theme('Dark Blue 3')

        # create the radio buttons for the hash algorithm
        hash_radio_buttons = []
        for hash_algo in self.hash_algos:
            if hash_algo == default_hash_algo:
                # make this button the default one
                button = sg.Radio(hash_algo, key='{}'.format(hash_algo), group_id="hash_algo", default=True)
            else:
                button = sg.Radio(hash_algo, key='{}'.format(hash_algo), group_id="hash_algo")

            # don't know how to get this working :(
            '''if hash_algo == default_hash_algo:
                button.default=True'''
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
        window = sg.Window('File Verifier', self.layout, margins=(25, 25))

        # window lifespan block
        while True:
            event, values = window.read()

            # if file and hash value provided then can continue
            if values['-FILE-INPUT-'] and values['-HASH-INPUT-']:
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)

            # handling the different event signals
            # if you exited, via wm or menubar
            if event in (sg.WIN_CLOSED, self.kill_code):
                break
            # if you pressed the ok button...
            elif event == "-OK-":
                hash_algo = None
                for hash_algo in self.hash_algos:
                    if values[hash_algo]:
                        break
                
                #
                result = self.hash_generator.compute(hash_algo, values['-FILE-INPUT-'])
                if not result['success']:
                    sg.popup("Error: {}".format(result['value']))
                else:
                    valid = False
                    if values['-HASH-INPUT-'] == result['value']:
                        valid = True
                    sg.popup("Equal: {}".format(valid), "Original: {}\nComputed: {}".format(values['-HASH-INPUT-'], result['value']), font='Courier 12')
            # this is a collection of menubar options
            # if you clicked the about option...
            elif event == self.about_label:
                sg.popup("About...", "File Verifier\nV1.0.0")

        window.close()