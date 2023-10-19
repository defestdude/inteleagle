#!/usr/bin/env python
import PySimpleGUI as sg
from pathlib import Path

from modules.live_person_finder import live_person_finder
from modules.model_trainer import encode_known_faces


"""
IntelEaghe
"""
DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")
def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Helvetica 12'

    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'), sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]], element_justification='r', key='-C-', grab=True,
                   pad=(0, 0), background_color=bc)]


def main():

    sg.theme('Black')
    intelbox_logo = sg.Image(filename='logo.png', key='intelboxlogo', subsample=3)
    menu_def = [["File", ["Live Person Finder", "Train Model"]],
                ["Help", ["About"]]]
    
    
    background_layout = [[sg.MenubarCustom(menu_def, tearoff=False)],
                        
                         [sg.Column([[intelbox_logo]], justification='center')],
                         [sg.Image(r'images/bg2.png')],
                         [sg.Text('Bottom ', key='statusbar', text_color='white')]]

    window_background = sg.Window('Background', background_layout, no_titlebar=False, resizable=True, finalize=True, margins=(0, 0), element_padding=(0,0))
    #window_background.send_to_back()

    
    while True:
        event, values = window_background.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            #cap.release()
            return
        elif event == 'Live Person Finder':
            live_person_finder()
        elif event == 'Train Model':
            sg.popup_quick_message('Training the model, please wait...', background_color='green', text_color='white', font='_ 20')
            encode_known_faces()
            window_background['statusbar'].update("Training Complete")

    


main()