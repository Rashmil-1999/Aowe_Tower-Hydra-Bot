from tkinter import *

from TowerBot.Helper_Functions.clickListener import ClickListener as CL

from TowerBot.TowerLogWindow import TowerLogWindow


class TowerConfig:
    @classmethod
    def __init__(self):
        self.P1 = (0, 0)
        self.P2 = (0, 0)
        self.grindPath = []

    @classmethod
    def getPoints(self):
        self.curStatus[
            "text"
        ] = "Click on the upper left corner\nand on the right bottom. with middle button"
        self.curStatus.update()
        self.P1, self.P2 = CL.getClicks(nr=2)
        self.curStatus["text"] = "Selected points:\nP1:{0}\nP2:{1}".format(
            self.P1, self.P2
        )

    @classmethod
    def getGrindPath(self):
        self.curStatus[
            "text"
        ] = "Select as many maps you\nwant with middle button.\nPress right button to stop."
        self.curStatus.update()
        self.grindPath = CL.getClicks(nr=1)
        self.curStatus["text"] = "Selected {0} maps.".format(len(self.grindPath))
        self.curStatus.update()
        if len(self.grindPath) == 1:
            self.grindTimes_Label.place(x=25, y=250)
            self.e3.place(x=120, y=250)
        else:
            self.grindTimes_Label.place_forget()
            self.e3.place_forget()

    @classmethod
    def startBot(self):
        self.config.destroy()
        self.TC = TowerLogWindow(
            self.P1,
            self.P2,
            self.grindModeStr,
            self.grindAmount.get(),
            self.grindGCReward.get(),
            self.grindPath,
            self.grindTimes.get(),
        )

    @classmethod
    def configWindow(self):
        self.config = Toplevel()
        self.config.title("Tower Configuration")
        self.config.geometry("250x550+100+100")

        self.GM_label = Label(self.config, text="Grind Mode:")
        self.GM_label.place(x=25, y=25)

        self.grindMode = StringVar()
        self.grindMode.set("Item")
        self.grindModeStr = "Item"
        self.modeList = ["Wait", "Gold Coin", "Item"]
        om1 = OptionMenu(
            self.config, self.grindMode, *self.modeList, command=self.setGrindMode
        )
        om1.place(x=125, y=20)

        GA_label = Label(self.config, text="Amount of resources:")
        GA_label.place(x=25, y=75)

        self.grindAmount = IntVar()
        self.grindAmount.set(20)
        e2 = Entry(self.config, textvariable=self.grindAmount, width=3)
        e2.place(x=175, y=75)

        self.grindGCReward = IntVar()
        grindGCReward_checkbox = Checkbutton(
            self.config, variable=self.grindGCReward, text="Use GC to get boss rewards."
        )
        grindGCReward_checkbox.place(x=25, y=115)

        self.getLoc = Button(
            self.config,
            width=20,
            height=1,
            text="Select screen margin.",
            command=TowerConfig.getPoints,
        )
        self.getLoc.place(x=25, y=165)

        getPath = Button(
            self.config,
            width=20,
            height=1,
            text="Select Levels.",
            command=TowerConfig.getGrindPath,
        )
        getPath.place(x=25, y=215)

        self.grindTimes_Label = Label(self.config, text="Farm times:")

        self.grindTimes = IntVar()
        self.grindTimes.set(10)
        self.e3 = Entry(self.config, textvariable=self.grindTimes, width=3)

        self.startButton = Button(
            self.config, text="Start", width=20, height=1, command=TowerConfig.startBot
        )
        self.startButton.place(x=25, y=350)

        self.curStatus = Label(self.config, text="Configure o seu bot.")
        self.curStatus.place(x=40, y=450)

        self.config.mainloop()

    @classmethod
    def setGrindMode(self, value):
        self.grindModeStr = value
