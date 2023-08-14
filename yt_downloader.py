import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
from os import rename, path
from threading import Thread
import io
import requests
from PIL import Image

# Custom Tkinter Object
class GUI:
    URL = ''
    def __init__(self):
        # Screen Proprieties:
        self.window = ctk.CTk()
        self.size = self.window.geometry('750x300')
        self.title = self.window.title('YouTube Downloader')
        self.theme = ctk.set_appearance_mode('Dark')
        
        # Widgets:
        self.top_label = ctk.CTkLabel(text='Enter the URL:', master=self.window)
        self.main_entry = ctk.CTkEntry(master=self.window, width=500)
        self.submit = ctk.CTkButton(master=self.window, text='Submit', command=self.submit_button)
        self.opt_1 = ctk.CTkCheckBox(master=self.window, text='Download audio only', font=('', 12), width=50, height=10)
        
        # Widgets placed by download functions to track progress
        self.download_bar = ctk.CTkProgressBar(master=self.window, mode='indeterminate', width=100, indeterminate_speed=3)
        self.completed = ctk.CTkLabel(master=self.window, text='Downloaded Successfully!', text_color='green', font=('', 15))

        # Set Position on Grid:
        self.top_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        self.main_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.submit.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        # Main Loop:
        self.main_loop = self.window.mainloop()



    def submit_button(self):
        GUI.URL = self.main_entry.get()
        self.main_entry.delete(0, 'end')
        yt = YouTube(GUI.URL)
        
        self.completed.place_forget() # To clean completed message of previous downloaded video, if any

        # Get Image from url as bytes object and pass it to im variable
        r = requests.get(yt.thumbnail_url, stream=True)
        im = Image.open(io.BytesIO(r.content))
        
        # Widgets of submit button that shows the thumbnail, author and title of the video
        self.image = ctk.CTkImage(dark_image=im, size=(100, 100))
        self.thumb = ctk.CTkLabel(master=self.window, image=self.image, height=50, width=50, text='')
        self.v_title = ctk.CTkLabel(master=self.window, text=yt.title)
        self.v_channel = ctk.CTkLabel(master=self.window, text=yt.author)
        
        # Download button
        self.download = ctk.CTkButton(master=self.window, text='Download', command=self.download_button)

        # Placement of this function's UI
        self.thumb.place(relx=0.04, rely=0.49)
        self.v_title.place(relx=0.2, rely=0.49)
        self.v_channel.place(relx=0.2, rely=0.58)
        self.opt_1.place(relx=0.4, rely=0.71)
        self.download.place(relx=0.2, rely=0.70)
        



    def download_button(self):
        self.main_entry.delete(0, 'end')
        if self.opt_1.get() == 0:
            th_vid = Thread(target=self.yt_download_video).start()
        elif self.opt_1.get() == 1:
            th_aud = Thread(target=self.yt_download_audio).start()
        
    
    def yt_download_video(self):
        self.download_bar.place(relx=0.04, rely=0.9)
        self.download_bar.start()
        yt = YouTube(GUI.URL)
        yt.streams.get_highest_resolution().download()
        self.download_bar.place_forget()
        self.completed.place(relx=0.04, rely=0.9)

    
    def yt_download_audio(self):
        self.download_bar.place(relx=0.04, rely=0.9)
        self.download_bar.start()
        yt = YouTube(GUI.URL)
        yt.streams.get_audio_only().download()
        out_file = yt.streams.get_audio_only().download()
        base, ext = path.splitext(out_file)
        new_file = base + '.mp3'
        rename(out_file, new_file)
        self.download_bar.place_forget()
        self.completed.place(relx=0.04, rely=0.9)



if __name__ == '__main__':
    GUI()
