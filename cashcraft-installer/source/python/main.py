from cgi import test
from re import T
import threading
import tkinter as tk
from tkinter.constants import DISABLED
from json import loads, dumps
from os import environ, path, mkdir, system
from shutil import copyfile
import requests
from time import sleep

def internet_fail_screen():
    window = tk.Tk()
    window.title('Installer Failed')

    window.geometry("325x50")
    window.resizable(False, False)

    tk.Label(text="The installer failed to download metadata off the internet.").pack()

    tk.Button(window, text="Exit", command=quit).pack()

    window.mainloop()

def install_fail_screen():
    window = tk.Tk()
    window.title('Installer Failed')

    window.geometry("325x50")
    window.resizable(False, False)

    tk.Label(text="The install process has failed.").pack()

    tk.Button(window, text="Exit", command=window.destroy).pack()

    window.mainloop()

def test_screen():
    window = tk.Tk()
    window.title('Installer Failed')

    window.geometry("325x50")
    window.resizable(False, False)

    tk.Label(text="The install process has failed.").pack()

    tk.Button(window, text="Exit", command=window.destroy).pack()

    window.mainloop()

def update_info_label(text):
    info_label['text'] = text

def download_package():

    for file in addon_package['files']:
        print(file[0])
        update_info_label('Downloading {}'.format(file[0]))
        r = requests.get(file[1], allow_redirects=True)
        open(dataPath + '\\' + file[0], 'wb').write(r.content)

    try:
        confirm_window.destroy()
    except: pass

def confirm_package():

    global confirm_window
    global yes_btn
    global no_btn

    confirm_window = tk.Tk()
    confirm_window.title('Install addon?')

    confirm_window.geometry("400x100")
    confirm_window.resizable(True, False)

    tk.Label(confirm_window, text="Do you want to install this extra package?").pack()
    tk.Label(confirm_window, text=addon_package['name'], font='Helvetica 16 bold').pack()

    yes_btn = tk.Button(confirm_window, text="Yes", command=download_package).pack()
    no_btn = tk.Button(confirm_window, text="No", command=confirm_window.destroy).pack()

    confirm_window.mainloop()

installer_file = {}
try:
    if True:
        installer_file = loads(open('C:\\Users\\casht\\Projects\\mc-pinger-2000-discord-edition\\files\\cashcraft-installer\\client\\installer.json').read())

    else:
        print('Downloading installer file...')
        installer_file = loads(requests.get("https://github.com/CoolCash1/files/raw/main/cashcraft-installer/client/installer.json", allow_redirects=True).content)
except:
    print('Download Failed!')
    internet_fail_screen()

# installer_file = loads(open('client\installer.json', 'r').read())
print('Starting App...')

first_server_name = list(installer_file['servers'])[-1]
print(first_server_name)

selected_server = installer_file['servers'][first_server_name]
selected_version = list(selected_server['versions'])[-1]

server_list = []
for version in installer_file['servers']:
    server_list.append(version)

version_list = []
for version in selected_server['versions'].values():
    version_list.append(version['name'])

print('Server List: ', server_list)
print('Version List: ', version_list)

dataPath = "{}\\.cashcraft".format(environ.get('APPDATA'))
mcPath = "{}\\.minecraft".format(environ.get('APPDATA'))

def switch_server(new_server_name):

    global selected_server
    selected_server = installer_file['servers'][new_server_name]

    global selected_version
    selected_version = list(selected_server['versions'].values())[-1]
    version_clicked.set( selected_version['name'] )

    global version_list
    version_list = []
    for version in selected_server['versions'].values():
        version_list.append(version['name'])

    global version_drop
    version_drop['menu'].delete(0, 'end')

    for version in version_list:
        version_drop['menu'].add_command(label=version, command=lambda v=version: version_clicked.set(v))

def start_install():
    install_button['text'] = 'Installing...'
    install_button['state'] = 'disabled'
    install_thread = threading.Thread(target=try_install)
    install_thread.start()

def try_install():
    try:
        install()
        install_button['text'] = 'Install Finished!'

    except:
        print('Install Failed!')
        internet_fail_screen()
        install_button['text'] = 'Install Failed!'

def install():
    if not path.exists(mcPath + "\\launcher_profiles.json"):
        print('MC Launcher Not Detected! Quiting')
        update_info_label('Error: Minecraft launcher was not found.')
        return 
    print('Installing Cashtons Minecraft Server Client. Please Wait...')
    update_info_label('Installing...')
    selectedVersion = installer_file['servers'][server_clicked.get()]['versions'][version_clicked.get()]
    if not path.exists(dataPath):
        print('\tCreating Data Folder... ({})'.format(dataPath))
        mkdir(dataPath)

    if not path.exists(mcPath + '\\versions\\' + selectedVersion['mcVersionId']):  
        print('\tDownloading Loader...')
        update_info_label('Downloading Mod Loader...')
        r = requests.get(selectedVersion['loaderInstall'], allow_redirects=True)
        open(dataPath + '\\' + 'loader.jar', 'wb').write(r.content)

        print('\tInstalling Loader...')
        update_info_label('Installing Mod Loader...')
        system('java -jar "' + dataPath + '\\' + 'loader.jar" {}'.format(selectedVersion['loaderArgs']))

    else:
        print('\tLoader already installed. Skipping loader installation process.')

    print('\tPreping File System...')
    update_info_label('Preparing File System...')
    for folder in selectedVersion['deleteFolders']:
        folderLoaction = dataPath + '\\' + folder
        print('\t\tDELETE {}'.format(folderLoaction))
        system('rmdir /s /q {}'.format(folderLoaction))

    for folder in selectedVersion['createFolders']:
        folderLoaction = dataPath + '\\' + folder
        print('\t\tCREATE {}'.format(folderLoaction))
        try:
            mkdir(folderLoaction)
        except FileExistsError:
            print('\t\t\tAlready Exists')

    print('\n\tDownloading and Installing mandantory content...')
    for contentItem in selectedVersion['content']['required']:
        print('\t\t{}'.format(contentItem['name']))
        for file in contentItem['files']:
            update_info_label(file[0])
            r = requests.get(file[1], allow_redirects=True)
            open(dataPath + '\\' + file[0], 'wb').write(r.content)

    print('\n\tTime to install optional features.')

    for contentItem in selectedVersion['content']['optional']:
        update_info_label('Waiting for user input...')
        global addon_package
        addon_package = contentItem
        confirm_package()

    print('Adding profile to launcher')
    update_info_label('Adding profile to launcher')
    launcherJson = loads(open(mcPath + '\\launcher_profiles.json').read())
    launcherJson['profiles']['CashCraft'] = {
        "gameDir": dataPath,
        "icon": selectedVersion['icon'],
        "name": selected_server['name'] + ' ' + selectedVersion['name'],
        "lastVersionId": selectedVersion['mcVersionId'],
        "type": "custom",
        "javaArgs": selectedVersion['javaArgs'],
    }
    open(mcPath + '\\launcher_profiles.json', 'w').write(dumps(launcherJson, indent=4))

    print('Finishing up...')
    update_info_label('Finishing up...')
    if not path.exists(dataPath + '\\options.txt'):
        if path.exists(mcPath + '\\options.txt'):
            copyfile(mcPath + '\\options.txt', dataPath + '\\options.txt')

    if not path.exists(dataPath + '\\optionsof.txt'):
        if path.exists(mcPath + '\\optionsof.txt'):
            copyfile(mcPath + '\\optionsof.txt', dataPath + '\\optionsof.txt')

    if not path.exists(dataPath + '\\servers.dat'):
        if path.exists(mcPath + '\\servers.dat'):
            copyfile(mcPath + '\\servers.dat', dataPath + '\\servers.dat')

    print('Done!')
    update_info_label('Install Finished!')


window = tk.Tk()
window.title('Installer')
# window.iconbitmap('icon.ico')
window.geometry("300x200")
window.resizable(False, False)

tk.Label(text="CashCraft Installer").pack()

server_clicked = tk.StringVar()
server_clicked.set( server_list[-1] )
server_drop = tk.OptionMenu( window , server_clicked , *server_list, command=switch_server )
server_drop.pack()

version_clicked = tk.StringVar()
version_clicked.set( version_list[-1] )
version_drop = tk.OptionMenu( window , version_clicked , *version_list )
version_drop.pack()

info_label = tk.Label(text="Ready to install.")
info_label.pack()

frame = tk.Frame(window)  
frame.pack()
# tk.Button(frame, text="Optional Resources").pack(side=tk.RIGHT)
install_button = tk.Button(frame, text="Install", command=start_install)
install_button.pack(side=tk.RIGHT)

window.mainloop()