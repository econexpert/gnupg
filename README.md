# Python script for GPG
Simple Program to Use Linux GPG with Tkinter for Synchronous Encryption

Please note that this method requires a passphrase and should not be used for encrypting sensitive data.

Instructions:
To use this program, download public-synroencryptionGPG.py and save them into a single folder.

To run file:
```
python3 public-synroencryptionGPG.py   
```
Please don't user to encrypt data, you will lose your data.

Note: it saves passphrase in settings.py file. Delete that file or edit.

# Python script for GnuPG
Simple Program to Use GnuPG Python Module with Tkinter for Synchronous Encryption

This program demonstrates how to use the GnuPG Python module with Tkinter for synchronous encryption.      
Please note that this method requires a passphrase and should not be used for encrypting sensitive data.      

To see a demonstration, please check out the Twitter video linked below.

<blockquote class="twitter-tweet"><a href="https://twitter.com/econexpert/status/1639548054196854784">Twitter video link</a></blockquote> 

**Instructions:**    
To use this program, download the three necessary files and save them into a single folder. 

Before running the program, make sure to install the required dependencies.

```
pip3 install -r requirements.txt
```
To run file:
```
python3 public-synroencryption.py
```
Please don't user to encrypt data, you will lose your data.


**Note:** it saves passphrase in settings.py file. Delete that file or edit. 

## To decrypt in Linux terminal with GPG     
will be promted for passphrase after entering command below into Linux terminal, file contents displayed in terminal screen:
```
gpg -d filename.gpg
```
instead of terminal screen to save into file:
```
gpg --output filename.txt -d filename.txt.gpg
```

**Let's enjoy open source encryption!**
