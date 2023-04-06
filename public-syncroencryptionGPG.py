import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import os
import subprocess
import ftplib
import datetime
from tqdm import tqdm
from io import BytesIO
try:
    import settings
except:
    print("settings file not found")
    settings_file = 'settings.py'
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as f:
            f.write('FTP = \'\'\n')
            f.write('USERNAME = \'\'\n')
            f.write('PASSWORD = \'\'\n')
            f.write('GNURECIPIENT = \'\'\n')
            f.close()
        import settings

class App(tk.Tk):
  def __init__(self):
    super().__init__()
    print("testing for GPG presence in the system.")
    try:
        command3 = ["gpg", "--version"]
        checkversion = subprocess.check_output(command3)
        print(checkversion.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print("some problem with gpg")
        os.abort()

    # configure the root window
    self.title('Encrypt files')
    self.geometry('300x400')
    self.notebook = ttk.Notebook(self)
    self.notebook.pack(pady=10, expand=True)
    self.notebook.option_add('*Dialog.msg.font', 'Arial 11')

    # create frames
    self.frame1 = ttk.Frame(self, width=300, height=380)
    self.frame2 = ttk.Frame(self, width=300, height=380)
    self.frame3 = ttk.Frame(self, width=300, height=380)

    self.frame1.pack(fill='both', expand=True)
    self.frame2.pack(fill='both', expand=True)
    self.frame3.pack(fill='both', expand=True)

# add frames to notebook
    self.notebook.add(self.frame1, text='Encrypt files')
    self.notebook.add(self.frame2, text='Decrypt files')
    self.notebook.add(self.frame3, text='FTP settings')
# ----- frame 1
    self.exit_button = tk.Button(self.frame1, text="Exit", command=self.destroyall)
    self.exit_button.pack(side="bottom")
    self.file_path_label = tk.Label(self.frame1, text='File Path:')
    self.file_path_label.pack()
    self.file_path_entry = tk.Entry(self.frame1, width=30)
    self.file_path_entry.pack()
    self.select_file_button = tk.Button(self.frame1, text='Select File', command=self.select_file)
    self.select_file_button.pack()

    self.recipient_label = tk.Label(self.frame1, text='Passphrase \n(saved in settings.py!!!)')
    self.recipient_label.pack()
    self.recipient_entry = tk.Entry(self.frame1, width=30, show ="*")
    self.recipient_entry.insert(-1,settings.GNURECIPIENT) 
    self.recipient_entry.pack()

    self.encrypt_button = tk.Button(self.frame1, text='Encrypt File', command=self.encrypt_file)
    self.encrypt_button.pack()
    self.upload_button = tk.Button(self.frame1, text='Upload File', command=self.upload_file)
    self.upload_button.pack()

# ----- frame 2 
    self.connect_button = tk.Button(self.frame2, text="Connect to FTP", command=self.connect)
    self.connect_button.grid(row=0, column=0)
    self.file_list = tk.Listbox(self.frame2, width=35, height=6)
    self.file_list.grid(row=1, column=0) 
    self.download_button = tk.Button(self.frame2, text="Download", command=self.download)
    self.download_button.grid(row=6, column=0)
    self.file_path_label = tk.Label(self.frame2, text='File Path:')
    self.file_path_label.grid(row=7, column=0)
    self.file_path_entry2 = tk.Entry(self.frame2, width=35)
    self.file_path_entry2.grid(row=8, column=0)
    self.file_select_button = tk.Button(self.frame2, text='Select File', command=self.select_file2)
    self.file_select_button.grid(row=9, column=0)

    # Create passphrase label and entry
    self.passphrase_label = tk.Label(self.frame2, text='Passphrase:')
    self.passphrase_label.grid(row=10, column=0)
    self.passphrase_entry = tk.Entry(self.frame2, width=35, show='*')
    self.passphrase_entry.grid(row=11, column=0)

    self.decrypt_button = tk.Button(self.frame2, text='Decrypt File', command=self.decrypt_file)
    self.decrypt_button.grid(row=12, column=0)
    self.exit_button = tk.Button(self.frame2, text="Exit", command=self.destroyall)
    self.exit_button.grid(row=13, column=0)

# frame 3 ---------------------------
    self.firstlabel = tk.Label(self.frame3, text='FTP Settings')
    self.firstlabel.grid(row=0, column = 0)
    self.L1 = tk.Label(self.frame3, text="Server")
    self.L1.grid(row=1, column = 0)
    self.server = tk.Entry(self.frame3)
    self.server.insert(-1,settings.FTP)
    self.server.grid(row=1, column = 1)
    self.L2 = tk.Label(self.frame3, text="User Name")
    self.L2.grid(row=2, column = 0)
    self.username = tk.Entry(self.frame3)
    self.username.insert(-1,settings.USERNAME)
    self.username.grid(row=2, column = 1)
    self.L3 = tk.Label(self.frame3, text="Password")
    self.L3.grid(row=3, column = 0)
    self.password = tk.Entry(self.frame3, show='*')
    self.password.insert(-1,settings.PASSWORD)
    self.password.grid(row=3, column = 1)
    self.save_settings_button = tk.Button(self.frame3, text='Save', command=self.save_settings)
    self.save_settings_button.grid(row=5, column = 1)
    self.exit_button = tk.Button(self.frame3, text="Exit", command=self.destroyall)
    self.exit_button.grid(row=6, column = 1)

  def destroyall(self):
      app.destroy()
      if hasattr(app,'ftp'): 
          print("closing FTP connection. Return from FTP: ", self.ftp.close())

  def connect(self):
    self.host = settings.FTP
    self.user = settings.USERNAME
    self.passwd = settings.PASSWORD

    try:
        self.ftp = ftplib.FTP(self.host)
        self.ftp.login(self.user, self.passwd)
        self.ftp.cwd("/")
        self.file_list.delete(0, tk.END)
        self.file_list.insert(tk.END, "Connected to FTP server successfully.")
        print(self.ftp.getwelcome())
        self.file_list.insert(tk.END, "Current directory: /")
        self.populate_file_list()
    except Exception as e:
        self.file_list.delete(0, tk.END)
        self.file_list.insert(tk.END, str(e))

  def populate_file_list(self):
        files = self.ftp.nlst()
        self.file_list.delete(0, tk.END)
        self.file_list.insert(tk.END, "Current directory: " + self.ftp.pwd())
        for f in files:
            self.file_list.insert(tk.END, f)

  def download(self):
      # check if
        if self.file_list.get(tk.ACTIVE) == "":
            print("nothing selected")
            return
        filename = self.file_list.get(tk.ACTIVE)
        local_path = filedialog.askdirectory()
        if local_path:
            local_path = local_path + "/" + filename
            # check if file exists locally
            try:
                local_file_system = os.path.basename(local_path)
                local_file_time = os.path.getmtime(local_path)
                print("locally saved before:", local_file_system, local_file_time)
                new_name_download = self.rename_file_dialog(local_path,"") 
                if new_name_download:  #
                    print("new name to save: ",new_name_download) #
                    local_path = new_name_download #
            except:
                print("file not exists on local syteem")
            print("attempting download...")
            with open(local_path, "wb") as f:   
                self.ftp.retrbinary("RETR " + filename, f.write)
                print("downloaded file", local_path) 
                self.file_path_entry2.delete(0, tk.END)
                self.file_path_entry2.insert(0, local_path)
                tk.messagebox.showinfo("Download complete",f"Downloaded {filename} successfully\nin {local_path} ")

  def save_settings(self):
    # Define the name of the variable you want to change
    def updatesettings(variable_name, new_value):
        new_value = "'" + new_value + "'"
        print("updating:", new_value)
        settings_file_path = "settings.py"
        with open(settings_file_path, "r") as f:
            settings_contents = f.read()

    # Search for the line that defines the variable
        lines = settings_contents.split("\n")
        variable_line = None
        for i, line in enumerate(lines):
            if line.startswith(variable_name):
                variable_line = i
                break
        if variable_line is not None:
            lines[variable_line] = f"{variable_name} = {new_value}"
        with open(settings_file_path, "w") as f:
            f.write("\n".join(lines))

    if self.server.get() != settings.FTP:
        updatesettings("FTP",self.server.get())
    if self.username.get() != settings.USERNAME:
        updatesettings("USERNAME",self.username.get())
    if self.password.get() != settings.PASSWORD:
        updatesettings("PASSWORD",self.password.get())
    if self.recipient_entry.get() != settings.GNURECIPIENT:
        updatesettings("GNURECIPIENT",self.recipient_entry.get())
        return # not show confirmation
    showinfo(title='Information', message='Settings saved')

  def button_clicked(self):
    showinfo(title='Information', message='Hello!')

  def select_file(self):
  # Get current working directory and open file dialog
    current_dir = os.getcwd()
    self.file_path = filedialog.askopenfilename(initialdir=current_dir, title='Select File')
    print("select file path:", self.file_path)
    self.file_path_entry.delete(0, tk.END)
    self.file_path_entry.insert(0, self.file_path)

  def select_file2(self):  # for second frame
    current_dir = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=current_dir, title='Select File')
    print("selected file path:",file_path)
    self.file_path_entry2.delete(0, tk.END)
    self.file_path_entry2.insert(0, file_path)

  def encrypt_file(self):
    self.file_path = self.file_path_entry.get()
    print(self.file_path)
    if self.file_path == "":
        print("no file selected")
        return
    self.file_name = os.path.basename(self.file_path)

    # Use GPG 
    command = ["gpg", "--symmetric", "--armor", "--batch", "--passphrase", self.recipient_entry.get()]
    # Encrypt file using signer's private key
    with open(self.file_path, 'rb') as f:
        file_data = f.read()
        encryptedoutput = subprocess.check_output(command, input=file_data, universal_newlines=False)

    # Upload encrypted file to FTP server
    if encryptedoutput:
        tk.messagebox.showinfo('Success','Encryption done!')
        if self.recipient_entry.get() != settings.GNURECIPIENT:
            self.save_settings()
    else:
        tk.messagebox.showinfo('Error',encryptedoutput.status)
        return
    self.file_path = self.file_path + ".gpg"
    self.file_path = self.check_file_exists(self.file_path, ".gpg")
    with open(self.file_path, 'wb') as f:
        f.write(encryptedoutput)
        self.file_path = self.file_path
        print("file saved:", self.file_path)
    # update file path

  def check_file_exists(self, file_path, extension):
    if os.path.isfile(file_path):
        print("file " + file_path +" already exists")
        file_path = self.rename_file_dialog(file_path, extension)
        print("new path", file_path)
    if file_path == "":
        print("no file name given")
        return 
    print("file path:", file_path)
    return file_path

  def rename_file_dialog(self, file_path, extension):
    answer = tk.messagebox.askyesno("File Exists", f"The file {file_path} already exists.\nDo you want to overwrite it?")
    if not answer:
        new_file_path = filedialog.asksaveasfilename(defaultextension=extension)
        if new_file_path == "":
            print("nothing selected")
            return
        print(new_file_path)
        # Rename the file
        file_path = new_file_path
        print("selection:",file_path)
    return(file_path)    

  def upload_file(self):
    try:
        if self.file_path == "":
            print("no file selected")
            return
        print("selected: ",self.file_path)
    except:
        print("no file selected")
        return   # exit if no file selected
    self.file_name = os.path.basename(self.file_path)
    self.local_file_time = os.path.getmtime(self.file_path)
    self.local_file_time = datetime.datetime.utcfromtimestamp(self.local_file_time).strftime('%Y-%m-%d %H:%M:%S')
    print("local file time:", self.local_file_time)
    try:
        print("FTP upload attempt, server:" , settings.FTP)
        ftp = ftplib.FTP(settings.FTP, settings.USERNAME, settings.PASSWORD)
# ----  check if file exists on FTP
        try:
            file_size = ftp.size(self.file_name)
            file_date_string = ftp.sendcmd('MDTM ' + self.file_name)[4:]
            file_date = datetime.datetime.strptime(file_date_string, '%Y%m%d%H%M%S')
            message = f"The file {self.file_name} exists \n with size {file_size} bytes, \n last modified on {file_date}. \n Your file modifed on {self.local_file_time}. Rewrite file on FTP?"
            answer = tk.messagebox.askyesno("File conflict on FTP", message)
            if answer:
                print("will replace file on FTP")
            else:
                print("Rename cancelled. The file has not been renamed.")
                return
        except ftplib.error_perm:
           print(f"The file {self.file_path} does not exist on the remote server. Proceeeding to upload")
# -----  continue with data upload
        file_size = os.path.getsize(self.file_path)
        # Upload the file in chunks and track the progress with tqdm
        chunk_size = 1024 * 1024 # 1 MB
        uploaded_size = 0
        with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading', miniters=1) as pbar:
            with open(self.file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    chunk_stream = BytesIO(chunk)
                    if not chunk:
                        break
                    ftp.storbinary('STOR ' + self.file_name, chunk_stream)
                    uploaded_size += len(chunk)
                    pbar.update(len(chunk))
        ftp.quit()
        tk.messagebox.showinfo('Success','File ' + self.file_name + ' uploaded')
    except ftplib.all_errors as e:
        print("some issue with FTP",  e)
        tk.messagebox.showerror("FTP error", f"Some issue with {settings.FTP} server.")

  def decrypt_file(self):
    self.file_path = self.file_path_entry2.get()   # get file name from second frame
    self.passphrase = self.passphrase_entry.get()   # get pass phrase from user
    try:
        if self.file_path == "":
            print("no file selected")
            return
        print("selected: ",self.file_path)
    except:
        print("no file selected")
        return   # exit if no file selected

    with open(self.file_path, 'rb') as f:
        self.filecontents = f.read()
    command2 = ["gpg", "--passphrase", self.passphrase_entry.get() , "-d","--batch"]
    try:
        self.decrypted_data = subprocess.check_output(command2, input=self.filecontents, universal_newlines=False)
    except subprocess.CalledProcessError as e:
        print(e.output) 
#        print(self.decrypted_data.output)  
        tk.messagebox.showerror('Decryption Failed',"Return code: " + str(e.returncode))
        return
    
    self.file_path = self.file_path + ".decrypted"
    # check if file exists 
    if os.path.isfile(self.file_path):
        print("files already exists")
        self.file_path = self.rename_file_dialog(self.file_path, ".decrypt")

    # Write decrypted data to new file
    with open(self.file_path, 'wb') as f:
        f.write(self.decrypted_data)
    
    # Show success message
    if self.decrypted_data: 
        tk.messagebox.showinfo('Success', f'File successfully decrypted and saved as \n' + self.file_path)
 
if __name__ == "__main__":

  app = App()
  app.mainloop()