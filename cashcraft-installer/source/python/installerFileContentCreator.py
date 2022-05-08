# INSTALLER FILE CONTET CREATOR
# Creates the an installerfile version content tag based off the files in the specified directory

from os import path, listdir
from json import dumps

dirPath = ''
while True:
    dirPath = input('What directory would you like to use for the content output? ')

    if path.exists(dirPath):
        break

    else:
        print('Invalid Path')

mcSubdir = input('What Minecraft subdirectory should these files be contained in? ') + '/'

urlPrefix = input('Where online where these files be stored? ')
if not urlPrefix[-1] == '/':
    urlPrefix += '/'

dirContents = listdir(dirPath)
contents = []
for content in dirContents:
    contents.append({
        'name': content,
        'files': [
            [mcSubdir + content, urlPrefix + content]
        ]
    })

print(dumps(contents, indent=4))
