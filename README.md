# Public-Synchronous Encryption Using GnuPG and Python

This project demonstrates two simple methods for public-synchronous encryption using GnuPG and Python with Tkinter. Please note that these methods require a passphrase and should not be used for encrypting sensitive data.

## Using GPG Without Python Module

Instructions:
1. Download the public-synroencryptionGPG.py file and save it to a folder.
2. To run the file, enter the following command in the terminal:

```
python3 public-synroencryptionGPG.py   
```

Note: This method saves the passphrase in the settings.py file. You can delete or edit this file.

# Using GnuPG Python Module
Simple Program to Use GnuPG Python Module with Tkinter for Synchronous Encryption

This program demonstrates how to use the GnuPG Python module with Tkinter for synchronous encryption.      
Please note that this method requires a passphrase and should not be used for encrypting sensitive data.      

To see a demonstration, please check out the Twitter video linked below.

<blockquote class="twitter-tweet"><a href="https://twitter.com/econexpert/status/1639548054196854784">Twitter video link</a></blockquote> 

Instructions:

1. Download the three necessary files (public-synroencryption.py, settings.py, and requirements.txt) and save them to a folder.
2. Before running the program, install the required dependencies by entering the following command in the terminal:

```
pip3 install -r requirements.txt
```
To run file:
```
python3 public-synroencryption.py
```
Please don't user to encrypt data, you will lose your data.


**Note:** it saves passphrase in settings.py file. Delete that file or edit. 

## Decrypting in the Linux Terminal with GPG
   
To decrypt a file using GPG in the Linux terminal and display the contents in the terminal screen, enter the following command:
   
```
gpg -d filename.gpg
```
To save the decrypted contents to a file, enter the following command: 

```
gpg --output filename.txt -d filename.txt.gpg
```

Demonstration in Twitter video: 

<blockquote class="twitter-tweet"><a href="https://twitter.com/econexpert/status/1643880707901607936">Twitter video link</a></blockquote> 

**Let's enjoy open source encryption!**
