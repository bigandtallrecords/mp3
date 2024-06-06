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

layout = [
    [sg.Text('Select WAV Files:'), sg.InputText(key='FILE_LIST'), sg.FilesBrowse(file_types=(("WAV Files", "*.wav"),), target='FILE_LIST')],
    [sg.Text('Destination Folder:'), sg.InputText(key='DEST_FOLDER'), sg.FolderBrowse(target='DEST_FOLDER')],
    [sg.Text('Bitrate:'), sg.Combo(['320', '256', '128'], default_value='320', size=(5, 1), key='BITRATE'), sg.Text('kbps')],
    [sg.Button('Convert'), sg.Button('Exit')],
    [sg.Text('Progress:'), sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), key='progressbar')]
]

window = sg.Window('WAV to MP3', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Convert':
        files = values['FILE_LIST'].split(';')
        destination = values['DEST_FOLDER']
        bitrate = values['BITRATE']
        convert_files(files, destination, bitrate, window, window['progressbar'])

window.close()
