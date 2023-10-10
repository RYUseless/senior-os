from tkinter import *
import configurationActions as ryuconf
from screeninfo import get_monitors
from configurationActions import readFile
import logging

logger = logging.getLogger(__file__)
logger.info("initiated logging")


class menuBarButtons:
    def __init__(self, menuFrame: Frame, root: Tk, heightDivisor: int, height: int, width: int):
        self.height = height
        self.width = width
        self.root = root
        self.menuFrame = menuFrame
        self.heightDivisor = heightDivisor
        self.xValue = 0
        self.options = ryuconf.testRead("careConf", "menuButtonsList")
        self.buttonDictionary = {}
        # calls section
        self.buttons()
        self.callOPT = configFrame(self.root, self.width, self.height)

    def buttons(self):
        counter = 0
        self.options.append("EXIT")  # add exit as a last button
        for i in self.options:
            def getButtonNum(y=counter):
                if y == 0:
                    self.callOPT.globalConfig(y)
                elif y == 1:
                    self.callOPT.mailConfig(y)
                elif y == 2:
                    self.callOPT.webConfig(y)
                elif y == 3:
                    self.callOPT.viewLogs(y)
                elif y == int(len(self.options) - 1):
                    exit(0)

            self.buttonDictionary[counter] = Button(self.menuFrame)
            self.buttonDictionary[counter]['text'] = i
            self.buttonDictionary[counter]['bg'] = '#696969'
            self.buttonDictionary[counter]['fg'] = 'white'
            self.buttonDictionary[counter]['activebackground'] = '#373737'
            self.buttonDictionary[counter]['activeforeground'] = 'white'
            self.buttonDictionary[counter]['relief'] = 'solid'
            self.buttonDictionary[counter]['command'] = getButtonNum
            self.buttonDictionary[counter]['font'] = "Helvetica 36 bold"
            if counter == 0:
                self.buttonDictionary[counter].place(x=0, y=0, width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            else:
                self.xValue = self.xValue + int(self.width / len(self.options))
                self.buttonDictionary[counter].place(x=self.xValue, y=0,
                                                     width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            counter += 1
        logger.info("created buttons")


class configFrame:
    def __init__(self, root: Tk, width: int, height: int):
        self.width = width
        self.height = height
        self.root = root
        self.heightDivisor = 7
        self.numberOfFrames = 4
        self.whichFrameIsON = None
        self.configFrameHeight = self.height - (self.height / self.heightDivisor)
        self.langaugeOPT = ('Czech', 'English', 'Deutsch')
        self.frameDict = {}
        self.createFrame()

    """
    Defs that are used later:
    """

    def refreshLogFrame(self, x):
        for widgets in self.frameDict[x].winfo_children():
            widgets.destroy()
        self.viewLogs(x)

    """
    Creating base frame for all of the options:
    """

    def createFrame(self):
        valueOfI = 0
        while valueOfI <= self.numberOfFrames:
            self.frameDict[valueOfI] = Frame(self.root)
            self.frameDict[valueOfI].pack_propagate(False)
            self.frameDict[valueOfI]['bg'] = "#1e1f22"
            self.frameDict[valueOfI]['width'] = self.width
            self.frameDict[valueOfI]['height'] = self.configFrameHeight
            valueOfI += 1

    """
    Configuration for each options Frame:
    """

    def viewLogs(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:  # close whatever frame is on AppFrame section
            # destroy all widget from frame, if there is any present (for refreshing data values)
            for widgets in self.frameDict[x].winfo_children():
                widgets.destroy()
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:  # just open frame for this option
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        # some setup
        B = Button(self.frameDict[x], text="REFRESH", command=lambda: self.refreshLogFrame(x))
        B.pack(side=TOP)
        textThing = Text(self.frameDict[x], height=self.height - (self.height / 7),
                         width=self.width,
                         bg="gray")
        scroll = Scrollbar(orient=VERTICAL, )
        scroll.config(command=textThing.yview, )
        textThing["yscrollcommand"] = scroll.set
        textThing.pack()
        file = ryuconf.readLog()
        for f in file:
            textThing.insert(END, f)
        textThing.config(state=DISABLED)  # disable editing

    def globalConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()

        var = StringVar()
        label = Label(self.frameDict[x], textvariable=var, relief=RAISED)
        var.set("Pick language: (default: English)")
        label['font'] = "Helvetica 12 bold"
        label.place(x=0, y=10, width=600, height=100)

        options = ["Czech", "English", "German"]
        dictionary = {}
        counter = 1
        var = IntVar()
        self.pickedButton = None
        width = 200
        height = 100
        iks = 610
        y = 10

        def changeColor(var):
            if not self.pickedButton is None:
                dictionary[self.pickedButton].configure(bg="#D3D3D3", activebackground="#D3D3D3")
                dictionary[var].configure(bg="green", activebackground="green")
                self.pickedButton = var
            else:
                dictionary[var].configure(bg="green", activebackground="green")
                self.pickedButton = var

        for opt in options:
            dictionary[counter] = Radiobutton(self.frameDict[x], text=opt, variable=var, value=counter)
            dictionary[counter]['font'] = "Helvetica 12 bold"
            dictionary[counter].configure(bg="#D3D3D3", activebackground="#D3D3D3")
            dictionary[counter]['command'] = lambda: changeColor(var.get())
            if counter == 1:
                dictionary[counter].place(x=iks, y=y, width=width, height=height)
            else:
                iks = iks + width + 10  # 5 is here for some space
                dictionary[counter].place(x=iks, y=y, width=width, height=height)
            counter += 1
        logger.info("opened global config frame")

    def mailConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        logger.info("opened mail config frame")

    def webConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        logger.info("opened web config frame")


class AppBase:
    def __init__(self, root: Tk):
        self.root = root
        self.heightDivisor = 7
        self.screenWidth = get_monitors()[readFile("resolution_info", "numOfScreen")].width  # screen width
        self.screenHeight = get_monitors()[readFile("resolution_info", "numOfScreen")].height  # screen height
        self.rootSetup()  # def for root window
        self.menuBarFrameSetup()  # def for creating menu bar frame

    def rootSetup(self):
        self.root.title("Caregiver Configuration v:0.0.1")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="#1e1f22")
        logger.info("created root window")

    def menuBarFrameSetup(self):
        masterFrame = Frame(self.root)  # creating menu bar frame (tkinter.Frame)
        masterFrame.pack_propagate(False)
        masterFrame['width'] = self.screenWidth
        masterFrame['height'] = self.screenHeight / self.heightDivisor
        masterFrame['bg'] = '#232323'
        masterFrame.pack(side=TOP)
        logger.info("created menuFrame")
        # calling class for creating objects
        menuBarButtons(masterFrame, self.root, self.heightDivisor, self.screenHeight, self.screenWidth)
