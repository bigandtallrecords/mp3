import PySimpleGUI as sg
import os
import subprocess

def convert_files(files, destination, bitrate, window, progress_bar):
    total_files = len(files)
    for count, file in enumerate(files, 1):
        output_file = os.path.join(destination, os.path.splitext(os.path.basename(file))[0] + '.mp3')
        command = ['ffmpeg', '-i', file, '-ab', f'{bitrate}k', output_file]
        subprocess.run(command)
        progress = (count / total_files) * 100
        window['progressbar'].update_bar(progress)

# Custom color definitions
background_color = '#000000'
text_color = '#ffffff'  # White color
input_text_color = '#ffffff'  # White color for input text
button_color = ('black', '#00ffff')  # Text, Background
progress_bar_color = ('#f2f2f2', '#00ffff')  # (border_color, bar_color)

# Set the theme colors for the window
sg.theme('Dark')
sg.set_options(
    background_color=background_color,
    text_element_background_color=background_color,
    element_background_color=background_color,
    input_elements_background_color=background_color,  # Use background color for input elements
    progress_meter_color=progress_bar_color,
    button_color=button_color,
    text_color=text_color,
    input_text_color=input_text_color,
    scrollbar_color=None
)

# Define the layout of the GUI
layout = [
    [sg.Text('Select WAV Files:', text_color=text_color), sg.InputText(key='FILE_LIST', text_color=input_text_color, background_color=background_color), sg.FilesBrowse(file_types=(("WAV Files", "*.wav"),), target='FILE_LIST', button_color=button_color)],
    [sg.Text('Destination Folder:', text_color=text_color), sg.InputText(key='DEST_FOLDER', text_color=input_text_color, background_color=background_color), sg.FolderBrowse(target='DEST_FOLDER', button_color=button_color)],
    [sg.Text('Bitrate:', text_color=text_color), sg.Combo(['320', '256', '128'], default_value='320', size=(5, 1), key='BITRATE', text_color=text_color, background_color=background_color), sg.Text('kbps', text_color=text_color)],
    [sg.Button('Convert', button_color=button_color), sg.Button('Exit', button_color=button_color)],
    [sg.Text('Progress:', text_color=text_color), sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), key='progressbar', bar_color=progress_bar_color)]
]

# Create the window
window = sg.Window('WAV to MP3', layout, grab_anywhere=True)

# Event loop to process events and get input values
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Convert':
        files = values['FILE_LIST'].split(';')
        destination = values['DEST_FOLDER']
        bitrate = values['BITRATE']
        convert_files(files, destination, bitrate, window, window['progressbar'])

# Close the window
window.close()
