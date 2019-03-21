#!/usr/bin/python
import sys
import os
import os.path
import mutagen
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify 
import glob
import pickle


Notify.init("cmus")

d = dict(zip(sys.argv[1::2], sys.argv[2::2]))

if d.get('status') != 'playing':
    sys.exit()

title = d.get('title')
artist = d.get('artist','Unknown')
album = d.get('album')
file_path = d.get('file')
splitfile = file_path.split('/')
folder = ""
for i in splitfile[:-1]:
    folder += i + '/'


files = os.listdir(folder)
image_file = ""
extensions = ['jpg', 'png', 'jpeg']
for i in files:
    for e in extensions:
        if glob.glob(folder + "*." + e) != [] and glob.glob(folder + "*." + e)[0] == folder + i:
            image_file = folder + i
if image_file == "":
    mut_file = mutagen.File(file_path)
    image = mut_file.tags.get('covr')[0]
    with open("/tmp/image", "wb") as img:
        img.write(image)
    image_file = "/tmp/image"


if os.path.isfile("/tmp/song.pickle"):
    with open("/tmp/song.pickle", "rb") as f:
        last_path = pickle.load(f)
    if last_path != file_path:
        notification = Notify.Notification.new(title, artist, image_file)
        notification.props.id = 6502
        notification.show()
else:
    notification = Notify.Notification.new(title, artist, image_file)
    notification.props.id = 6502
    notification.show()
with open("/tmp/song.pickle", "wb") as f:
    pickle.dump(file_path, f)
