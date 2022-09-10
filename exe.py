
# Notes:
# https://www.baeldung.com/jar-windows-executables
# https://medium.com/javarevisited/creating-executable-exe-file-from-java-archive-jar-file-9e83f42baade

import os
import easygui
import requests

msg = "Load application..."
title="Rambunctious Turtles application"

choices = ["Google Chrome","PuTTY"]
reply = easygui.buttonbox(msg, title,  choices=choices)

if reply == "Google Chrome":
   os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
elif reply == "PuTTY":
    os.system("putty")
else:
    print("Done")

def read_csv():


def hash_identifiers():

# more notes
# https://www.tomshardware.com/how-to/create-python-executable-applications
# https://www.geeksforgeeks.org/convert-python-script-to-exe-file/
