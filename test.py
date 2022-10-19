from tkinter import *
from tkinter import filedialog
import requests 
import tkinter.font as font
from PIL import ImageTk, Image  
from tkinter import ttk
import matplotlib

def openFile():
    tf = filedialog.askopenfilename(
        filetypes=(("Mp3 Files","*.mp3 .wav"),)
        )
    txtarea.delete('1.0',END) # Delete from position 0 till end 
    txtarea.update()
    pathh.delete(END,'0')
    pathh.update()
    pathh.insert(END, tf)
    tf = open(tf, "rb")
    UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
    TRANSCRIPTION_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
    api_key = "24cb91bdd2264679bf0f35e89430dab9"
    headers = {"authorization": api_key, "content-type": "application/json"}
    def read_file(filename):
        while True:
            data = filename.read(5242880)
            if not data:
                break
            yield data
    upload_response = requests.post(UPLOAD_ENDPOINT, headers=headers,data=read_file(tf),verify=True)
    tf.close()
    audio_url = upload_response.json()["upload_url"]
    transcript_request = {'audio_url': audio_url,"speaker_labels": True}
    transcript_response = requests.post(TRANSCRIPTION_ENDPOINT, json=transcript_request, headers=headers,verify=True)
    _id = transcript_response.json()["id"]
    while True:
        polling_response = requests.get(TRANSCRIPTION_ENDPOINT + "/" + _id, headers=headers,verify=True)
        if polling_response.json()['status'] == 'completed':
            break
        elif polling_response.json()['status'] == 'error':
            raise Exception("Transcription failed. Make sure a valid API key has been used.")

    for speaker in polling_response.json()['utterances']:
        note=f'Speaker {speaker.get("speaker")} : {speaker.get("text")}'
        txtarea.insert(END,'\n')
        txtarea.insert(END,'\n')
        txtarea.insert(END,note)
ws = Tk()
width= ws.winfo_screenwidth()
height= ws.winfo_screenheight()
ws.geometry("%dx%d" % (width, height))
ws.title("AUDIO TO TEXT CONVERTER ")
ws['bg']='#3677f7'
l1=label = Label(ws, text="AUDIO TO TEXT CONVERTER 🎤🔜📝",bg='#3677f7',fg='#ffffff',font="bold 23",wraplength=200, justify="center",)
l1.place(x=20,y=160)
p1 = PhotoImage(file = 'C:\\Users\\mukeshkannan.d\\Documents\\pyinstaller\\icon.png')   
# Icon set for program window
ws.iconphoto(True, p1)  
# loading the image
img = ImageTk.PhotoImage(Image.open("C:\\Users\\mukeshkannan.d\\Documents\\pyinstaller\\logo1-removebg-preview.png").resize((190,90)))
  
# reading the image
panel = Label(ws, image = img,bg='#3677f7')
  
# setting the application
panel.place(x=20,y=30)

button_font = font.Font(family='Monospace', size=20)
b1=Button(
    ws, 
    text=" 📁 Open File", 
    command=openFile,
    bg='#45b592',
    fg='#ffffff',
    font=button_font
    )
b1.pack(side=LEFT, expand=True, fill=X, padx=20)
b2=Button(
    ws, 
    text="❎ Exit", 
    command=lambda:ws.destroy(),
    bg='#e33529',
    fg='#ffffff',
    font=button_font
    )#.pack(side=LEFT, expand=True, fill=X, padx=20, pady=20)
b2.place(x=100,y=550)


frame = Frame(ws)
frame.pack(pady=5)

# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)
pathh = Entry(ws,disabledbackground='#9fa0a1')
pathh.pack(expand=True, fill=X, padx=15)
# adding writing space
txtarea = Text(frame, width=160, height=40)
txtarea.pack(side=RIGHT)

# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)

# adding path showing box
def save_text():
    my_str1=txtarea.get("1.0",END)
    fob=filedialog.asksaveasfile(filetypes=[('text file','*.txt')],
        defaultextension='.txt',
        mode='w')
    try:
        fob.write(my_str1)
        fob.close()
        txtarea.delete('1.0',END) # Delete from position 0 till end 
        txtarea.update()  
    except :
        print (" There is an error...")
# adding buttons 
b3=Button(
    ws, 
    text="💾 Save File", 
    command=save_text,
    bg='#6d7fb5',
    fg='#ffffff',
    font=button_font
    )
b3.place(x=40,y=480)

ws.mainloop()