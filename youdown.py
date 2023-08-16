from pytube import*
from tkinter import*
from tkinter import ttk
from tkinter import filedialog
from threading import *
import os

class start:
    def __init__(self,window):    
        window.geometry('600x200')
        window.resizable(0,0)
        window.title("Youtube Downloader")
        self.location=StringVar()
        self.comb1_var=StringVar()

        self.lab=Label(window,width='4',height='2', text='url :',fg='black')
        self.lab.place(x=10,y=46)
        self.ent=Entry(window,bg='red',width='36',text="",font='arial, 14')
        self.ent.place(x=45,y=50)
        self.lab1=Label(window,width='51',height='1',borderwidth=2, relief="groove", text='Youtube Downloader',anchor=W,fg='green',font='arial, 13')
        self.lab1.place(x=15,y=10)
        self.lab2=Label(window,width=35, height=1,borderwidth=2, relief="groove",text="Welcome to ack downloader",fg="blue")
        self.lab2.place(x=110,y=102)
    
        self.comb1=ttk.Combobox(window,textvariable=self.comb1_var,font=("times new roman", 13, "bold"),state="readonly")
        self.comb1["values"]=("Select size from here",)
        self.comb1.current(0)                           
        self.comb1.place(x=405,y=102,width=180)
        
        self.pro=Label(window,width=22,anchor=W,height=1,borderwidth=2,font=("times new roman", 14),relief="groove",text="            progress bar",fg="blue")
        self.pro.place(x=10,y=152)

        self.btd=Button(window,text='Download', width=8, height=1, command=lambda:self.download())
        self.btd.place(x=220,y=150)

        self.bt4=Button(window,text='Browse', width=4, height=1, command=lambda:[self.Browse()])
        self.bt4.place(x=525,y=150)

        self.bro=Label(window,width=22,anchor=E,height=1,borderwidth=2,font=("times new roman", 14),relief="groove",fg="blue")
        self.bro.place(x=316,y=152)

        self.bt3=Button(window,text='Clear',width=8, height=1,command=lambda:self.cls())
        self.bt3.place(x=10,y=97)

        self.bt=Button(window,text='Fetch',width=8, height=1, command=lambda:self.go())
        self.bt.place(x=492,y=49)
        self.download_Directory=os.getcwd()
        self.bro.config(text=self.download_Directory )

    def Browse(self):
        self.download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
        self.bro.config(text=self.download_Directory )


    def go(self):
        if self.ent.get()=="":
            self.lab1.config(text="Enter url then press Go button")
        else:
            t2=Thread(target=self.gos)
            t2.start()
    def gos(self):
        self.bt["state"] = "disabled"
        self.bt["text"] = "wait"
        try:
            global ar
            urs= self.ent.get()
            ar=YouTube(urs)
            self.lab1.config(text=ar.title)
            stream = str(ar.streams.filter(progressive=True))
            stream = stream[1:]
            stream = stream[:-1]
            streamlist = stream.split(", ")
            pr=[]
            for i in range(0, len(streamlist)):
                    st = streamlist[i].split(" ")
                    pr.append(st[1]+">"+st[3])
            it=[]
            re=[]
            vt=""
            for i in pr:
                re.append(i[-5:-2])
                it.append(i[6:8])
                self.size=str(((ar.streams.get_by_itag(i[6:8]).filesize)//10000)/100)
                vt=vt+self.size+"mb=>!"+i[-5:-2]+"!Pixel"+" "
            self.lab2.config(text="Please selct resolution =>")
            self.comb1["values"]=(vt)
            self.comb1.current(1)

        except:
            self.lab2.config(text="Error in URL!!!!!")
            self.lab1.config(text="Error in URL!!!!!")
        self.bt["state"] = "normal"
        self.bt["text"] = "Fetch"
    def progress(self):
        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            #print("total size",total_size)
            #print("remaining",bytes_remaining)
            #print(percentage_of_completion)
            status="            progress bar"
            if percentage_of_completion<25:
                status="|"*10
            if percentage_of_completion>25 and percentage_of_completion<50:
                status="|"*20
            if percentage_of_completion>50 and percentage_of_completion<75:
                status="|"*30
            if percentage_of_completion>75 and percentage_of_completion<99:
                status="|"*40
            if percentage_of_completion==100:
                status="          DOWNLOADED"
            self.pro.config(text=status)
        ar.register_on_progress_callback(on_progress)
                   
    def download(self):
        if self.comb1_var.get()=="Select size from here":
            self.lab1.config(text="Cant get fetched data! Try again")
        else:
            self.lab2.config(text="Downloading.....")     
            t2=Thread(target=self.down)
            t2.start()
            t3=Thread(target=self.progress)
            t3.start()
    def cleans(self):
        val=self.comb1_var.get()
        words = val.split('!')
        return words[1]

    def down(self):
        self.btd["state"] = "disabled"
        self.va=""
        try:
            val=self.cleans()
            if val=="144":
                self.va="17"
                down=ar.streams.get_by_itag(self.va)
            if val=="360":
                self.va="18"
                down=ar.streams.get_by_itag(self.va)
            if val=="720":
                self.va="22"
                down=ar.streams.get_by_itag(self.va)
            print(down)
            print("start download")
            down.download(self.download_Directory)
            print("completed download")
            newtitle="Downloaded! "+ar.title
            self.lab1.config(text=newtitle)
            self.lab2.config(text="Download in another resolution =>")
            self.btd["state"] = "normal"
        except:
            self.lab1.config(text="Cant download!! please try again")
            self.btd["state"] = "normal"

    def cls(self):
        self.ent.delete(0,END)
        self.lab1.config(text='Youtube Downloader')
        self.lab2.config(text="Welcome to ack downloader")
        self.bro.config(text=self.download_Directory )
        self.comb1["values"]=("Select size from here",)
        self.comb1_var.set("Select size from here")
        self.pro.config(text="            progress bar")
        
            

if __name__=="__main__":
    window=Tk()
    app=start(window)
    window.mainloop()





