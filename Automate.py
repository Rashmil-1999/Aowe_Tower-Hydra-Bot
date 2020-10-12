
from pprint import pprint
from TowerBot.Helper_Functions.clickListener import ClickListener as CL
from TowerBot.Helper_Functions import helperFunctions as HL
import pyautogui, time
import argparse

position_recorder = []

def getScreenPoints():
    return CL.getClicks(nr=2)


def automate(p1,p2,epochs):
    # print("click mid mouse btn on field:")
    # pos = CL.getClicks(1)
    for i in range(epochs):
        print("Occupy: {}".format(i+1))
        # pyautogui.click(pos[0])
        field = False

        while not field:
            field = HL.findField(p1,p2)
        pyautogui.click(field)
        hasLoaded = HL.findHasLoaded(p1,p2)
        while not hasLoaded:
            pyautogui.click(field)
            hasLoaded = HL.findHasLoaded(p1,p2)
        # time.sleep(0.8)
        abandonBtn = HL.findAbandonBtn(p1,p2)
        if not abandonBtn:
            while not abandonBtn:
                abandonBtn = HL.findAbandonBtn(p1,p2)
        pyautogui.click(abandonBtn)
        # time.sleep(0.9)    
        confirmBtn = HL.findConfirmButon(p1,p2)
        if not confirmBtn:
            while not confirmBtn:
                confirmBtn = HL.findConfirmButon(p1,p2)
        while confirmBtn:
            pyautogui.click(confirmBtn)
            confirmBtn = HL.findConfirmButon(p1,p2)
        
        time.sleep(1)
        field = False

        while not field:
            field = HL.findField(p1,p2)
        pyautogui.click(field)
        hasLoaded = HL.findHasLoaded(p1,p2)
        while not hasLoaded:
            pyautogui.click(field)
            hasLoaded = HL.findHasLoaded(p1,p2)
        # time.sleep(0.9)
        occupyBtn = HL.findOccupyBtn(p1,p2)
        if not occupyBtn:
            while not occupyBtn:
                occupyBtn = HL.findOccupyBtn(p1,p2)
        while occupyBtn:
            pyautogui.click(occupyBtn)
            occupyBtn = HL.findOccupyBtn(p1,p2)
        autoConfigBtn = HL.findAutoConfigBtn(p1,p2)
        if not autoConfigBtn:
            while not autoConfigBtn:
                autoConfigBtn = HL.findAutoConfigBtn(p1,p2)
        pyautogui.click(autoConfigBtn)
        # time.sleep(0.9)
        marchBtn = HL.findMarchBtn(p1,p2)
        if not marchBtn:
            while not marchBtn:
                marchBtn = HL.findMarchBtn(p1,p2)
        pyautogui.click(marchBtn)
        time.sleep(3)


# record_action()
print("get Screen Corner by mid mouse clicks:")
p1 = (3, 52)
p2 = (883, 545)
P1, P2 = getScreenPoints()
epochs = int(input("number of repetitions:\n"))
# attack_time = int(input("attack time :\n"))
automate(P1,P2,epochs)
