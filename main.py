#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
from multiprocessing import Lock, Queue
from datetime import datetime
import imutils


"""
IntelEaghe
"""

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


def findFaceInFrame(input_frames, output_frames):
    try:
        frame = input_frames.get_nowait()
        
    except:
        print('queue is empty')
        #return True
    else:
        face_cascade = cv2.CascadeClassifier('faceclassifier.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)
        processedgray = cv2.imencode('.png', gray)[1].tobytes()
        output_frames.put(processedgray)
    return

def live_person_finder():
    input_frames = Queue()
    output_frames = Queue()
    # define the window layout
    layout = [[sg.Text('Live Person Finder')],
              [sg.Image(filename='', key='liveimage'),  sg.Image(filename='', key='processedimage')],
              [sg.Column([[sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('Capture', size=(10, 1), font='Any 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]], justification='center')],
              ]

    # create the window and show it without the plot
    window = sg.Window('IntelEagle',
                       layout, keep_on_top=True, no_titlebar=True, modal=True, transparent_color=sg.theme_background_color(), resizable=True)

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = False
    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            cap.release()
            window.close()
            break

        elif event == 'Start':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((20, 20), 0)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['liveimage'].update(data=imgbytes)
            window['processedimage'].update(data=imgbytes)

        if recording:
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=320)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto

            if event == 'Capture':
                now = datetime.now()
                current_time = now.strftime("%y%m%d%H:%M:%S")
                filename = current_time+".png"
                cv2.imwrite(filename, frame)


            input_frames.put(frame)
            window['liveimage'].update(data=imgbytes)
            findFaceInFrame(input_frames, output_frames)
            window['processedimage'].update(data=output_frames.get())
        
    window.close()


def main():

    sg.theme('Black')
    intelbox_logo = sg.Image(filename='logo.png', key='intelboxlogo', subsample=3)
    menu_def = [["File", ["Live Person Finder", "Command 2"]],
                ["Help", ["About"]]]
    
    
    background_layout = [[sg.MenubarCustom(menu_def, tearoff=False)],
                        
                         [sg.Column([[intelbox_logo]], justification='center')],
                         [sg.Image(r'bg2.png')]]

    window_background = sg.Window('Background', background_layout, no_titlebar=False, resizable=True, finalize=True, margins=(0, 0), element_padding=(0,0))
    #window_background.send_to_back()

    
    while True:
        event, values = window_background.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            #cap.release()
            return
        elif event == 'Live Person Finder':
            live_person_finder()
    


main()