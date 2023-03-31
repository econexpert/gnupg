# Python script for gnupg
Simple program to use gnupg Python module with tkinter. This uses synchronous encryption (will passphrase)

See demonstration in Twitter video:  

<blockquote class="twitter-tweet"><a href="https://twitter.com/econexpert/status/1639548054196854784">Twitter video link</a></blockquote> 

Please don't user to encrypt data, you will lose your data.

Suggested usage:
1. Download three files into one folder
2. Install requirements: 
```
pip3 install -r requirements.txt
```
3. Run file:
```
python3 public-synroencryption.py
```

**Note:** it saves passphrase in settings.py file. Delete that file or edit. 

## to decrypt in Linux terminal with GPG     
will be promted for passphrase after entering command below into Linux terminal, file contents displayed in terminal screen:
```
gpg -d filename.gpg
```
instead of terminal screen to save into file:
```
gpg --output filename.txt -d filename.txt.gpg
```

**Let's enjoy open source encryption!**
