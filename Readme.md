#ipaHack

It's my little script for hacking **Info.plist** file in some IOS application file.
Now it can change minimally required iOS version, but could be easy modified 
for your needs.

##Requires:
[a] (http://packages.ubuntu.com/ru/oneiric/python-plist "python-plist") package
(I hope to change it later on something that can be installed via pip)
To install it in Debian-based systems you should do:
`$ sudo apt-get install python-plist`

##Using:
It's easier than appears:
`$ python ipaMinimusOSVersionChanger.py <pathToYourIpaFile>`
