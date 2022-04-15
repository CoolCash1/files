from re import T
import tkinter as tk
from tkinter.constants import DISABLED
from json import loads, dumps
from os import environ, path, mkdir, system
from shutil import copyfile
import requests

def internet_fail_screen():
    window = tk.Tk()
    window.title('Installer Failed')

    window.geometry("325x50")
    window.resizable(False, False)

    tk.Label(text="The installer failed to download metadata off the internet.").pack()

    tk.Button(window, text="Exit", command=quit).pack()

    window.mainloop()

print('Loading installer file...')
installerFile = {}
try:
    installerFile = loads(requests.get("https://raw.githubusercontent.com/CoolCash1/CashCraft/main/client/installer.json?token=GHSAT0AAAAAABQTZA3SO24S3Z2OB5WNSHSYYPXLFFQ", allow_redirects=True).content)
except:
    print('Download Failed!')
    internet_fail_screen()

# installerFile = loads(open('client\installer.json', 'r').read())
print('Starting App...')
versionNames = []
for version in installerFile['versions'].values():
    versionNames.append(version['name'])
dataPath = "{}\\.cashcraft".format(environ.get('APPDATA'))
mcPath = "{}\\.minecraft".format(environ.get('APPDATA'))

def install():
    if not path.exists(mcPath + "\\launcher_profiles.json"):
        print('MC Launcher Not Detected! Quiting')
        return 
    print('Installing Cashtons Minecraft Server Client. Please Wait...')
    selectedVersion = installerFile['versions'][clicked.get()]
    if not path.exists(dataPath):
        print('\tCreating Data Folder... ({})'.format(dataPath))
        mkdir(dataPath)

    if not path.exists(mcPath + '\\versions\\' + selectedVersion['mcVersionId']):  
        print('\tDownloading Loader...')
        r = requests.get(selectedVersion['loaderInstall'], allow_redirects=True)
        open(dataPath + '\\' + 'loader.jar', 'wb').write(r.content)

        print('\tInstalling Loader...')
        system('java -jar "' + dataPath + '\\' + 'loader.jar" {}'.format(selectedVersion['loaderArgs']))

    else:
        print('\tLoader already installed. Skipping loader installation process.')

    print('\tPreping File System...')
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
            print('\t\t\t{}'.format(file[0]))
            r = requests.get(file[1], allow_redirects=True)
            open(dataPath + '\\' + file[0], 'wb').write(r.content)

    print('\n\tTime to install optional features.')
    print('\tPlease respond with "y" (yes) or "n" (no) to each question.')

    for contentItem in selectedVersion['content']['optional']:
        while True:
            resp = input('\t\tWould you like to install {}? '.format(contentItem['name']))
            if resp.lower() == 'y' or resp.lower() == 'yes':
                for file in contentItem['files']:
                    print('\t\t\t{}'.format(file[0]))
                    r = requests.get(file[1], allow_redirects=True)
                    open(dataPath + '\\' + file[0], 'wb').write(r.content)

                break

            elif resp.lower() == 'n' or resp.lower() == 'no':
                break

            else: 
                print('\t\tInvalid Response')
                print('\t\tPlease respond with "y" (yes) or "n" (no) to each question.\n')

    print('Adding profile to launcher')
    launcherJson = loads(open(mcPath + '\\launcher_profiles.json').read())
    launcherJson['profiles']['CashCraft'] = {
        "gameDir": dataPath,
        "icon": selectedVersion['icon'],
        "name": selectedVersion['name'],
        "lastVersionId": selectedVersion['mcVersionId'],
        "type": "custom"
    }
    open(mcPath + '\\launcher_profiles.json', 'w').write(dumps(launcherJson, indent=4))

    print('Finishing up...')
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


window = tk.Tk()
window.title('Installer')
# window.iconbitmap('icon.ico')
window.geometry("300x200")
window.resizable(False, False)

tk.Label(text="CashCraft Installer").pack()

clicked = tk.StringVar()
clicked.set( versionNames[-1] )
drop = tk.OptionMenu( window , clicked , *versionNames )
drop.pack()

frame = tk.Frame(window)  
frame.pack()
# tk.Button(frame, text="Optional Resources").pack(side=tk.RIGHT)
tk.Button(frame, text="Install", command=install).pack(side=tk.LEFT)

window.mainloop()