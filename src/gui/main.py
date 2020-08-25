import PySimpleGUI as sg
import datetime
from ..hash.main import HashGenerator


class MainWindow:
    def __init__(self):
        '''
        MainWindow constructor. Configures the layout, menubar,
        instance variables, etc.

        :returns: an instance of PySimpleGUI
        '''
        # variable declarations
        self.kill_code = "Quit"
        self.about_label = "About..."
        self.history_label = "History"
        self.hash_algos = ['MD5', 'SHA1', 'SHA256', 'SHA512']
        self.hash_generator = HashGenerator()
        default_hash_algo = "SHA256"

        # window styling
        sg.theme('Dark Blue 3')

        # create the radio buttons for the hash algorithm
        hash_radio_buttons = []
        for hash_algo in self.hash_algos:
            if hash_algo == default_hash_algo:
                # make this button the default one
                button = sg.Radio(hash_algo,
                                  key='{}'.format(hash_algo),
                                  group_id="hash_algo",
                                  default=True)
            else:
                button = sg.Radio(hash_algo,
                                  key='{}'.format(hash_algo),
                                  group_id="hash_algo")

            # don't know how to get this working :(
            '''if hash_algo == default_hash_algo:
                button.default=True'''
            hash_radio_buttons.append(button)

        # Window layout
        menubar = [['&File',
                   [  # '&{}'.format(self.history_label), '---',
                    '&{}'.format(self.kill_code)]],
                   ['&Help', '&{}'.format(self.about_label)]]
        self.layout = [[sg.Menu(menubar)],
                       [sg.T("Choose file to verify")],
                       [sg.In(key="-FILE-INPUT-", enable_events=True)],
                       [sg.FileBrowse(target="-FILE-INPUT-")],
                       [sg.Text('_'*45)],
                       [sg.T("Choose your hash algorithm")],
                       hash_radio_buttons,
                       [sg.Text('_'*45)],
                       [sg.T("Enter the hash value to check against")],
                       [sg.In(key="-HASH-INPUT-", enable_events=True)],
                       [sg.OK(key="-OK-", disabled=True)]]

    def get_hash_algo(self, values):
        '''
        Find out what the specified hash algorithm is

        :returns: a string representing the desired hash algorithm
        '''
        hash_algo = None
        for hash_algo in self.hash_algos:
            if values[hash_algo]:
                break
        return hash_algo

    def do_analysis(self, values):
        '''
        Make call to get hash of the specified file

        :param values: the values specified in the window
        :returns: void
        '''
        hash_algo = self.get_hash_algo(values)

        # compute the hash of the file
        start = datetime.datetime.now()
        result = self.hash_generator.compute(hash_algo, values['-FILE-INPUT-'])
        finish = datetime.datetime.now()

        # display the result, be it an error or success
        if not result['success']:
            sg.popup("Error: {}".format(result['value']))
        else:
            valid = False
            if values['-HASH-INPUT-'] == result['value']:
                valid = True
            sg.popup("Equal: {}".format(valid),
                     "Original: {}\n"
                     "Computed: {}\n\n"
                     "Time taken: {}".format(
                     values['-HASH-INPUT-'], result['value'], finish-start),
                     font='Courier 10')

    def draw(self):
        '''
        Draw the window
        :returns: void
        '''
        window = sg.Window('File Verifier', self.layout, margins=(25, 25))

        # window lifespan block
        while True:
            event, values = window.read()

            # if file and hash value provided then enable OK button
            if values['-FILE-INPUT-'] and values['-HASH-INPUT-']:
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)

            ######################################

            # handling the different event signals
            if event in (sg.WIN_CLOSED, self.kill_code):
                # closed out or pressed the quit button
                break
            elif event == "-OK-":
                # pressed the ok button to do the hashing
                self.do_analysis(values)
            elif event == self.about_label:
                # pressed the about button
                sg.popup("About...", "File Verifier\nV1.0.0")
            elif event == self.history_label:
                # pressed the history button
                sg.popup("History", "None")

        window.close()
