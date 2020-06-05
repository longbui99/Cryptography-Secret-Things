# easy_install http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win32-py2.7.exe
import tkinter as tk
from tkinter import filedialog
import threading
import time
class UI:
    def __init__(self):
        #Root application ui
        self.root = tk.Tk()
        self.root.title("Application Cryptography")
        self.root.resizable(False,False)
        self.consoleAreaMode = False
        # self.root.protocol("WM_DELETE_WINDOW", lambda : self.updateAndTerminate(True))
        self.LOOPCONSTRAINT = 0.1
        self.widthConstraint = 850

        self.isActive = False
        self.percent = 0

        self.mainObject=[
            "AES",#Algorithms
            True,#Crypto
            False,#Type
            None,#Input Url
            False,#Auto
            None,#Key URL
            None#Save url
        ]
        self.constraintAlgorithms = (
            ("AES","Advanced Encryption Standard"),
            ("DES","Data Encryption Standard"),
            ("3DES","Triple Data Encryption Standard"),
        )
        # Constraint color
        self.historyShow = False
        #Application Frame control function
        self.App = None
        self.Title = None
        self.AlgorithmsFrame = None
        self.controlFrame = None
        self.MainActiveFrame = None
        self.ActiveFrame = None
        self.ProcessingFrame = None
        self.HistoryFrame=None
        #
        self.ActiveBtn = None
        self.EncodeBtn = None
        self.DecodeBtn = None
        self.ConsoleMainActive = None
        self.initAppFrame()
        self.initTitleFrame()
        self.initControlFrame()
        self.initAlgorithmsFrame()
        self.initMainActiveFrame()
        self.initConsoleActive()
        self.initActiveFrame()
        self.initCommand()
        self.initHistory()
        self.initProcessingFrame()
        self.initFistConsole()
        # self.controlProcessingFrame(True)
    
    def initAppFrame(self):
        self.App = tk.Frame(self.root,width="720px", height  ="380px", bg='white')
        self.Title = tk.Frame(self.App, width='720px',height='50px',  borderwidth=1, relief='ridge' )
        self.controlFrame = tk.Frame(self.App, width='500px',height='50px', borderwidth="2px", relief="ridge",highlightthickness=1)
        self.AlgorithmsFrame = tk.Frame(self.App, width="200px", height="400px",highlightthickness=1)
        self.MainActiveFrame = tk.Frame(self.App, height='300px',borderwidth="2px", relief="ridge")
        self.ActiveFrame = tk.Frame(self.App,width='118px',height='151px',borderwidth="1px", relief="ridge")
        self.ConsoleMainActive = tk.Frame(self.App, width="500px",height="98px", borderwidth="2px",relief="groove", bg="white")
        self.HistoryFrame =tk.Frame(self.App,width='720px',height='120px', bg='white', borderwidth="2px",relief="groove")
        self.ProcessingFrame = tk.Frame(self.App, width='179px',height="380px", bg="white", borderwidth=1, relief='solid')

        self.App.pack()
        self.Title.place(x=0,y=0)
        self.controlFrame.place(x='220px',y='50px')
        self.AlgorithmsFrame.place(x='0px', y='50px')
        self.MainActiveFrame.place(x='220px',y='120px')
        self.ActiveFrame.place(x='600px',y='123px')
        self.ConsoleMainActive.place(x='220px',y="280px")
        
        # ----------------------------------------------------------------
    
    def initTitleFrame(self):
        self.labelTitle = tk.Label(self.Title,text="Application Cryptography", font=('Helvetia',16))

        self.labelTitle.place(x=125,y=10,width='500px',height='30px')

    def initControlFrame(self):
        self.EncodeBtn = tk.Button(self.controlFrame,text='ENCODE',
        cursor='hand2' ,padx='90px',pady=15, relief="flat", font=("Helvetica",12),highlightthickness=1)
        self.DecodeBtn = tk.Button(self.controlFrame,text="DECODE", 
        cursor='hand2',padx='90px',pady=15, relief="flat", font=("Helvetica",12),highlightthickness=1)
        labelDivide = tk.Label(self.controlFrame, borderwidth=2,relief='groove')

        self.EncodeBtn.place(x="3px",y=0)
        self.DecodeBtn.place(x="250px",y=0)
        labelDivide.place(x=40,y=65,width='450px',height="2px")


    def initHistory(self):
        self.percentageProcess = tk.Frame(self.HistoryFrame,bg="green2",width=0,height="28px")
        # labelHistory = tk.Label(self.HistoryFrame, text="Operational history", font=("Helvetica",10), bg="white")
        scrollHistory = tk.Scrollbar(self.HistoryFrame)
        self.listHistory = tk.Listbox(self.HistoryFrame,yscrollcommand=scrollHistory.set, relief = "flat")

        self.percentageProcess.place(x=0,y=0)
        # labelHistory.place(x="200px",y="5px")
        scrollHistory["command"]= self.listHistory.yview
        self.listHistory.place(x=0,y="29px",width="700px", height="120px")
        scrollHistory.place(x="700px",y=0,height="120px")


    def initProcessingFrame(self):
        tk.Label(self.ProcessingFrame, text="Queue processing", bg='white', fg='green', font=('Helvetica',12)).place(x=0,y=0, width="175px")

        scrollProcessing = tk.Scrollbar(self.ProcessingFrame)
        self.ProcessingList = tk.Listbox(self.ProcessingFrame, yscrollcommand = scrollProcessing.set, relief='flat')
        
        self.ProcessingList.delete(0)

        scrollProcessing["command"] = self.ProcessingList.yview
        self.ProcessingList.place(y="20px",width="165px", height="360px")
        scrollProcessing.place(x="165px",y="20px", height="360px")

    def initAlgorithmsFrame(self):
        labelAlgorithms = tk.Label(self.AlgorithmsFrame,text='Algorithms', font=('Helvetica',12))
        self.listAlgorithms = [tk.Button(self.AlgorithmsFrame,text=tex[1],cursor='hand2') for tex in self.constraintAlgorithms]

        labelAlgorithms.place(x="25px",y=0,width="145px",height="30px")
        paddingY = 30
        for x in range(0,len(self.listAlgorithms)):
            self.listAlgorithms[x].place(x=2,y=str(paddingY)+"px",width="195px",height="40px")
            paddingY+=40


    def initMainActiveFrame(self):
        # Encode input
        InputBtn = tk.Frame(self.MainActiveFrame, width="495px",height="50px", borderwidth="0px",relief="groove")
        labelInputFile = tk.Label(InputBtn, text="Input", font=('Helvetica',12))
        labelDivideVertical = tk.Label(InputBtn, borderwidth="2px", relief="ridge")
        RadioFrame = tk.Frame(InputBtn,highlightthickness=1)
        self.Radiovar = tk.BooleanVar()
        self.fileRadioBtn = tk.Radiobutton(RadioFrame,variable=self.Radiovar,value=True,  text="File", cursor="hand2", font=('Helvetica',12))
        self.folderRadioBtn = tk.Radiobutton(RadioFrame,variable=self.Radiovar,value=False, text="Folder", cursor="hand2", font=('Helvetica',12))
        self.InputOpenBtn = tk.Button(InputBtn, text="Open",cursor="hand2",highlightthickness=1)
        labelDivide = tk.Label(self.controlFrame, borderwidth=2,relief='solid')

        InputBtn.pack()
        labelInputFile.place(x="30px",y=0,width="100px",height="42px")
        labelDivideVertical.place(x="150px",y=0,width="4px",height="42px")
        RadioFrame.place(x="155px",height="42px",width="100px")
        self.fileRadioBtn.place(x=0,y="0px", width="100px", height="20px")
        self.folderRadioBtn.place(x=10,y="25px", width="100px", height="20px")
        self.InputOpenBtn.place(x="280px",y="6px",height="30px",width="80px")
        labelDivide.place(x=40,y=65,width='450px',height="2px")
        # Key input
        KeyInput = tk.Frame(self.MainActiveFrame, width="495px",height="50px", borderwidth="0px",relief="groove")
        labelKeyFile = tk.Label(KeyInput, text="Key file", font=('Helvetica',12))
        labelDivideVertical = tk.Label(KeyInput, borderwidth="2px", relief="ridge")
        self.autoVar = tk.BooleanVar()
        self.AutoKeyBtn = tk.Checkbutton(KeyInput,text="Automatic",cursor="hand2", font=("Helvetica",10),variable=self.autoVar, onvalue=True,offvalue=False)
        self.keyOpenBtn = tk.Button(KeyInput, text="File",cursor="hand2",highlightthickness=1)
        labelDivide = tk.Label(self.controlFrame, borderwidth=2,relief='groove')

        KeyInput.pack()
        labelKeyFile.place(x="30px",y=0,width="100px",height="42px")
        labelDivideVertical.place(x="150px",y=0,width="4px",height="42px")
        self.AutoKeyBtn.place(x="170px",y="10px",width="100px")
        self.keyOpenBtn.place(x="280px",y="6px",height="30px",width="80px")
        labelDivide.place(x=40,y=65,width='450px',height="2px")
        
        #Save Output
        saveOutput = tk.Frame(self.MainActiveFrame, width="495px",height="50px", borderwidth="0px",relief="groove")
        labelSaveFile = tk.Label(saveOutput, text="Save folder", font=('Helvetica',12))
        labelDivideVertical = tk.Label(saveOutput, borderwidth="2px", relief="ridge")
        self.saveOpenBtn = tk.Button(saveOutput, text="Folder",cursor="hand2",highlightthickness=1)
        labelDivide = tk.Label(self.controlFrame, borderwidth=2,relief='groove')

        saveOutput.pack()
        labelSaveFile.place(x="30px",y=0,width="100px",height="42px")
        labelDivideVertical.place(x="150px",y=0,width="4px",height="42px")
        self.saveOpenBtn.place(x="180px",y="6px",height="30px",width="180px")
        labelDivide.place(x=40,y=65,width='450px',height="2px")
        #Log console

    def initActiveFrame(self):
        self.ActiveBtn = tk.Button(self.ActiveFrame,text="Start", cursor="hand2", font=("Helvetica",11))
        labelDivideVertical = tk.Label(self.ActiveFrame,borderwidth="2px", relief="ridge")


        self.ActiveBtn.place(x="35px",y="50px", width="50px", height="50px")
        labelDivideVertical.place(x=0,y=0, height="151px", width="2px")

    def initConsoleActive(self):
        self.labelConsoleActive = tk.Label(self.ConsoleMainActive, text="",
        font=("Helvetica",10), wraplengt="400px",bg="white")
        
        scrollConsole = tk.Scrollbar(self.ConsoleMainActive)
        self.listConsole = tk.Listbox(self.ConsoleMainActive, yscrollcommand= scrollConsole.set, relief="flat")


        self.listConsole.place(x=0,y="20px",height="78px", width="480px")
        scrollConsole.place(x="481px", height="95px")
        scrollConsole.config(command =self.listConsole.yview)
        self.labelConsoleActive.place(x="40px",y=0, width="400px")
        
    def bindMouseAlg(self, Option, Obj):
        if Obj.cget("bg") != 'black':
            if Option:
                Obj.configure(bg="grey",fg="white")
            else:
                Obj.configure(bg="white",fg="black")

    def bindMouseCont(self,Option, Obj):
        if Obj.cget("bg") != 'black':   
            if Option:
                Obj.configure(bg="grey",fg="white")
            else:
                Obj.configure(bg="white",fg="black")

    def bindMouseActive(self,Option,Obj):
        if Obj.cget('bg') != '#59ff00':
            if Option:
                Obj.configure(bg="grey",fg="white")
            else:
                Obj.configure(bg="#f04d4d",fg="black")

    def initCommand(self):
        # EncodeBtn
        self.EncodeBtn["command"]=lambda:self.ProcessEncodeDecode( True)
        self.EncodeBtn.bind("<Enter>", lambda x: self.bindMouseCont(True,self.EncodeBtn))
        self.EncodeBtn.bind("<Leave>", lambda x: self.bindMouseCont(False,self.EncodeBtn))
        self.EncodeBtn.configure(bg='black',fg='white')
        # DecodeBtn
        self.DecodeBtn["command"]=lambda:self.ProcessEncodeDecode( False)
        self.DecodeBtn.bind("<Enter>", lambda x: self.bindMouseCont(True,self.DecodeBtn))
        self.DecodeBtn.bind("<Leave>", lambda x: self.bindMouseCont(False,self.DecodeBtn))

        # List Algorithms
        for index in range(0,len(self.listAlgorithms)):
            self.listAlgorithms[index].configure(command=lambda x=index: self.algorithmsProcess(x))
            self.listAlgorithms[index].bind('<Enter>', lambda a,x=index: self.bindMouseAlg(True, self.listAlgorithms[x]))
            self.listAlgorithms[index].bind('<Leave>', lambda a,x=index: self.bindMouseAlg(False, self.listAlgorithms[x]))
        self.listAlgorithms[0].configure(bg='black', fg='white')

        # Input Button
        self.InputOpenBtn["command"]=lambda:self.fileInputProcess()
        self.InputOpenBtn.bind("<Enter>", lambda x: self.bindMouseActive(True,self.InputOpenBtn))
        self.InputOpenBtn.bind("<Leave>", lambda x: self.bindMouseActive(False,self.InputOpenBtn))
        # Radio file
        self.fileRadioBtn["command"]=lambda:self.radioTypeProcess()
        # Radio folder
        self.folderRadioBtn["command"]=lambda:self.radioTypeProcess()
        # Checkbox Automatic
        self.AutoKeyBtn["command"]=lambda: self.autoKeyProcess()
        # Key folder
        self.keyOpenBtn["command"]=lambda: self.fileKeyProcess()
        self.keyOpenBtn.bind("<Enter>", lambda x: self.bindMouseActive(True,self.keyOpenBtn))
        self.keyOpenBtn.bind("<Leave>", lambda x: self.bindMouseActive(False,self.keyOpenBtn))

        self.saveOpenBtn["command"]=lambda:self.folderSavingProcess()
        self.saveOpenBtn.bind("<Enter>", lambda x: self.bindMouseActive(True,self.saveOpenBtn))
        self.saveOpenBtn.bind("<Leave>", lambda x: self.bindMouseActive(False,self.saveOpenBtn))
        # self.ActiveBtn["command"]=lambda:self.ActiveFunction
        
    def initFistConsole(self):
        self.listConsole.insert(0,"Input: None")
        self.listConsole.insert(1,"Key: None")
        self.listConsole.insert(2,"Save: None")
        self.listConsole.itemconfig(0,fg='orange')
        self.listConsole.itemconfig(1,fg='orange')
        self.listConsole.itemconfig(2,fg='orange')

    def displayHistory(self):
        if not self.historyShow:
            # print("OK")
            self.App["height"]="500px"
            self.HistoryFrame.place(x='0px',y='385px')
            self.historyShow = True
            self.initHistory()
        
    def addHistory(self, data):
        (typeCrypto,state,url, time) = data
        crypString = time+ ("ENCODE " if typeCrypto else "DECODE ")
        stringState = "success " if state else "failed "
        self.listHistory.insert(0, crypString + stringState + ": path= " +url )
        self.listHistory.itemconfigure(0, fg= "green" if state else "red")

    def algorithmsProcess(self, typeAl=0):
        self.listAlgorithms[typeAl].config(bg="black",fg="white")
        for index,x in enumerate(self.listAlgorithms):
            if index is not typeAl:
                self.listAlgorithms[index].config(bg="white",fg="black")
        self.mainObject[0] = self.constraintAlgorithms[typeAl][0]
    
    def ProcessEncodeDecode(self, ENCODE=True):
        self.mode = ENCODE
        self.mainObject[1] = ENCODE
        if ENCODE:
            self.AutoKeyBtn.configure(state=tk.NORMAL, cursor="hand2")
            self.EncodeBtn.config(bg="black",fg="white")
            self.DecodeBtn.config(bg="white",fg="black")
        else:
            self.autoVar.set(False)
            self.autoKeyProcess()
            if self.keyOpenBtn.cget('bg') =='#59ff00':
                self.keyOpenBtn.configure(bg='#f04d4d')
            self.mainObject[5] = None
            self.AutoKeyBtn.configure(state=tk.DISABLED,cursor="arrow")
            self.DecodeBtn.config(bg="black",fg="white")
            self.EncodeBtn.config(bg="white",fg="black")

    def radioTypeProcess(self):
        self.mainObject[2] = self.Radiovar.get()

    def updateWorking(self, c = True):
        if c:
            self.labelTitle.config(text="The application is working......", fg="red")
            self.ActiveBtn.configure(cursor='arrow', state="disable")
        else:
            self.labelTitle.config(text="Application Cryptography", fg="black")
            self.ActiveBtn.configure(cursor='hand2', state="normal")

    def fileInputProcess(self):
        url=None
        try:
            if self.mainObject[2]:
                url=filedialog.askopenfilename(
            filetypes=[
    		("All files", "*")])
            else:
                url=filedialog.askdirectory() + "/"
        except :
            return
        finally:
            self.mainObject[3] = url if url is not '' else None
            self.listConsole.delete(0)
            if url == None or url == '' or url == '/':
                self.InputOpenBtn.configure(bg='#f04d4d')
                self.listConsole.insert(0,"Input : None")
                self.listConsole.itemconfig(0,fg='red')
            else:
                self.InputOpenBtn.configure(bg='#59ff00')
                self.listConsole.insert(0,"Input : " + url + ("" if self.mainObject[2] else "/"))
                self.listConsole.itemconfig(0,fg='#00b330')
                

    def autoKeyProcess(self):
        self.mainObject[4]= self.autoVar.get()
        if self.mainObject[4]:
            self.keyOpenBtn["text"]="Folder"
        else:
            self.keyOpenBtn["text"]="File"

    def fileKeyProcess(self):
        url = None
        try:
            if self.mainObject[4]:
                url = filedialog.askdirectory()
            else:
                url = filedialog.askopenfilename(
                filetypes=[
                ("All files", "*")])
        except:
            return
        finally:
            self.mainObject[5] = url if url is not '' else None
            self.listConsole.delete(1)
            if url == None or url == '' or url == '/':
                self.keyOpenBtn.configure(bg='#f04d4d')
                self.listConsole.insert(1,"Key : None")
                self.listConsole.itemconfig(1,fg='red')
            else:
                self.keyOpenBtn.configure(bg='#59ff00')
                self.listConsole.insert(1,"Key : " + url)
                self.listConsole.itemconfig(1,fg='#00b330')

    def folderSavingProcess(self):
        url = None
        try:
            url = filedialog.askdirectory()+"/"
        except:
            return
        self.mainObject[6] = url if url is not '' else None
        self.listConsole.delete(2)
        if url == None or url == ''  or url == '/':
            self.saveOpenBtn.configure(bg='#f04d4d')
            self.listConsole.insert(2,"Saving : None")
            self.listConsole.itemconfig(2,fg='red')
        else:
            self.saveOpenBtn.configure(bg='#59ff00')
            self.listConsole.insert(2,"Saving : " + url)
            self.listConsole.itemconfig(2,fg='#00b330')
    
    def raiseError(self, tple):
        (index, typeErr) = tple
        if index == 0:
            c = True
            errAlgorithms = "Algorithms: "
            if typeErr is None:
                # self.AlgorithmsFrame["highlightbackground"]="red"
                errAlgorithms += "You have select algorithms"
                c = False
            else:
                # self.AlgorithmsFrame["highlightbackground"]="gray"
                errAlgorithms += "Satisfy"
                c = True
            return (errAlgorithms,c)
            
        elif index==1:
            c = True
            errENDEType = "Cryptography: "
            if typeErr is None:
                # self.controlFrame["highlightbackground"]="red"
                errENDEType += "You have select Encode or Decode"
                c = False
            else:
                # self.controlFrame["highlightbackground"]="gray"
                errENDEType += "Satisfy"
                c = True
            return (errENDEType,c)
        elif index==2:
            c=True
            errInputType = "Type: "
            if typeErr is None:
                errInputType += "You have select input type"
                c=False
            else:
                errInputType += "Satisfy"
                c=True
            return (errInputType,c)
        elif index==3:
            c=True
            errInputBtn = "Input:"
            if typeErr is None:
                # self.InputOpenBtn["highlightbackground"]="red"
                errInputBtn += "No input choosen"
                c=False
            else:
                # self.InputOpenBtn["highlightbackground"]="gray"
                errInputBtn += "Satisfy"
                c=True
            return (errInputBtn,c)
        elif index == 4:
            c= True
            errAutoKey = "Autokey:"
            if typeErr is None:
                errAutoKey+="No input choosen"
                c=False
            else:
                errAutoKey += "Satisfy"
                c=True
            return (errAutoKey,c)

        elif index==5:
            c=True
            errInputKey = "Key:"
            if typeErr is None:
                # self.keyOpenBtn["highlightbackground"]="red"
                errInputKey += "No key choosen"
                c=False
            else:
                # self.keyOpenBtn["highlightbackground"]="gray"
                errInputKey += "Satisfy"
                c=True
            return (errInputKey,c)
            pass
        elif index==6:
            c=True
            errSaveFol = "Save folder:"
            if typeErr is None:
                # self.saveOpenBtn["highlightbackground"]="red"
                errSaveFol += "No folder saving choosen"
                c=False
            else:
                # self.saveOpenBtn["highlightbackground"]="gray"
                errSaveFol += "Satisfy"
                c=True
            return (errSaveFol,c)
        
    def showActiveConsole(self,lst):
        self.listConsole.delete(4,tk.END)
        for index,x in enumerate(lst):
            if x[1]:
                self.listConsole.insert(tk.END,x[0])
                self.listConsole.itemconfig(tk.END,fg='green')
            else:
                self.listConsole.insert(0,x[0])
                self.listConsole.itemconfig(0,fg='red')

    def AlertConsole(self,data, bools = True, boo = False):
        if boo:
            self.labelConsoleActive["text"]+=data
            return
        if bools:
            self.updateWorking(False)
            self.labelConsoleActive["fg"]="red"
            self.labelConsoleActive["text"] = data
        else:
            self.labelConsoleActive["fg"]="green"
            self.labelConsoleActive["text"] += data
        
        self.listConsole["height"]=self.ConsoleMainActive.cget("height")
    
    def showFileandKey(self, lst, c, expand=""):
        if c:
            self.labelConsoleActive["fg"]="green"
        else: 
            self.labelConsoleActive["fg"]="red"
        self.labelConsoleActive["text"] = "Done: " +expand+ str(lst[0]) + " files  -  Key: " +str(lst[1])+ " keys  "

    def initActive(self):
        self.isActive=False
        
        def threadLoopSize():
            while not self.isActive:
                self.percentageProcess["width"]= int(self.percentageProcess.cget("width"))+int(self.percent*self.widthConstraint)
                time.sleep(self.LOOPCONSTRAINT) 

        threading.Thread(target=threadLoopSize).start()

    def updateAndTerminate(self, c=True, data = None):
        if c:
            self.isActive = True
            self.percentageProcess["width"]=800
            time.sleep(0.1)
            self.percentageProcess["width"]=0
        else:
            self.percentageProcess["width"]=800
            time.sleep(0.01)
            self.percentageProcess["width"]=0
            self.percent = self.LOOPCONSTRAINT/data if data > 0 else 0

    def insertNotificationConsole(self, data, c = True):
        fileName = data[0].split('/')[-1]
        if c:
            self.listConsole.insert(tk.END,fileName +data[1])
            self.listConsole.itemconfigure(tk.END,fg='green')
        else:
            self.listConsole.insert(0,fileName + data[1])
            self.listConsole.itemconfigure(0,fg='red')

    def messageBoxShow(self):
        self.labelTitle.config(text="Application is working, you cannot stop now......", fg="red")

        def reFixTitle():
            time.sleep(3)
            self.labelTitle.config(text="The application is working, .......", fg="red")

        threading.Thread(target=reFixTitle).start()


    def controlProcessingFrame(self, c):
        if c:
            self.ProcessingFrame.place(x='721px')
            self.App["width"]="900px"
        else:
            self.App["width"]="720px"

    def modifyProcessingList(self, option = True, data = None):
        if option:
            self.ProcessingList.delete(0)
            if self.ProcessingList.size() > 0:
                tempText= self.ProcessingList.get(0)[8:]
                self.ProcessingList.delete(0)
                self.ProcessingList.insert(0,'Processing : ' +tempText)
                self.ProcessingList.itemconfigure(0, fg='green')
            else:
                self.controlProcessingFrame(False)
        else:
            # List must be reverse
            data = data[::-1]
            for x in data[:-1]:
                self.ProcessingList.insert(0, "Waiting: " + x[0].split('/')[-1] + " - {:5.2f} MB".format(x[1]/1048576))
                self.ProcessingList.itemconfigure(0, fg='orange')
                
            tempText= data[-1][0].split('/')[-1]    
            self.ProcessingList.insert(0,'Processing : ' +tempText + " - {:5.2f} MB".format(data[-1][1]/1048576))
            self.ProcessingList.itemconfigure(0, fg='green')

    def close(self):
        self.root.destroy()

    def runUI(self):
        self.root.mainloop()
