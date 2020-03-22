import time, pyautogui, random
import numpy as np
from tkinter import *
from TowerBot.Helper_Functions.helperFunctions import *
from TowerBot.Main_Functions.autoBattle import auto_battle

pyautogui.FAILSAFE = True


class TowerLogWindow:
    @classmethod
    def __init__(
        self, P1, P2, grindMode, grindAmount, grindGCReward, grindPath, grindTimes
    ):
        self.P1 = P1
        self.P2 = P2
        self.grindMode = grindMode
        self.grindAmount = grindAmount
        self.grindGCReward = True if grindGCReward == 1 else False
        self.grindPath = grindPath
        self.grindTimes = grindTimes
        self.enemies = 0
        self.chests = 0
        self.bosses = 0
        self.grindAmountSpent = 0
        self.TowerPriority = {"1": "Enemy", "3": "Chest", "2": "Boss"}
        self.bossFlag = 0
        # print(P1, P2, grindMode, grindAmount, self.grindGCReward, grindPath, grindTimes)

        TowerLogWindow.buildLogWindow()

    @classmethod
    def appendLog(self, string):
        self.logBox.insert("end", string + "\n")
        self.logBox.see("end")
        self.logBox.update()

    @classmethod
    def increseStatus(self, status):
        if status == "Enemy":
            self.enemies += 1
            self.sEne.configure(text="Enemy Killed: {0}".format(self.enemies))
        elif status == "Chest":
            self.chests += 1
            self.sCh.configure(text="Opened Chests: {0}".format(self.chests))
        elif status == "Boss":
            self.bosses += 1
            self.sBss.configure(text="Boss Killed: {0}".format(self.bosses))

    @classmethod
    def buildLogWindow(self):
        towerLog = Toplevel()
        towerLog.title("Tower Bot")
        towerLog.geometry("750x810+50+50")

        logBox_label = Label(towerLog, text="Log:")
        logBox_label.grid(row=0, column=0)

        statusLabel = Label(towerLog, text="Status")
        statusLabel.grid(row=1, column=5, sticky="n", padx=15)

        self.sEne = Label(
            towerLog, text="Enemy Killed: {0}".format(self.enemies), anchor="w"
        )
        self.sEne.grid(row=2, column=5, sticky="n", padx=15)

        self.sCh = Label(
            towerLog, text="Opened Chests: {0}".format(self.chests), anchor="w"
        )
        self.sCh.grid(row=3, column=5, sticky="n", padx=15)

        self.sBss = Label(
            towerLog, text="Boss Killed: {0}".format(self.bosses), anchor="w"
        )
        self.sBss.grid(row=4, column=5, sticky="n", padx=15)

        self.logBox = Text(towerLog, height=45, width=55)
        self.logBox.grid(row=1, column=0, padx=15, rowspan=50)
        self.logBox_Scroll = Scrollbar(
            towerLog, orient="vertical", command=self.logBox.yview
        )
        self.logBox.configure(yscrollcommand=self.logBox_Scroll.set)
        self.logBox_Scroll.grid(row=1, column=3, sticky="ns", rowspan=50)

        bt1 = Button(towerLog, text="Start", command=self.startBot)
        bt1.grid(row=2, column=6, rowspan=2, padx=15)

        bt2 = Button(towerLog, text="Stop", command=self.startBot)
        bt2.grid(row=3, column=6, rowspan=2, padx=15)
        towerLog.mainloop()

    @classmethod
    def status(self):
        pass

    @classmethod
    def startBot(self):
        i = 1
        if len(self.grindPath) != 1:
            for path in self.grindPath:
                time.sleep(5)
                pyautogui.click(path)
                self.appendLog("Entering Arena.")
                self.appendLog("Round: {0}".format(i))
                i = self.startTowerBot(i)
                self.appendLog(50 * "#" + "\n" + 50 * "#" + "\n" + 50 * "#")
        else:
            while i <= self.grindTimes:
                time.sleep(5)
                pyautogui.click(self.grindPath[0])
                self.appendLog("Entering Arena.")
                self.appendLog("Round: {0}".format(i))
                i = self.startTowerBot(i)

    @classmethod
    def startTowerBot(self, times):
        time.sleep(1.5)
        player = False
        keepBottin = True
        while keepBottin:
            time.sleep(0.5)
            enemy = 0
            chest = 0
            boss = 0
            while not player:
                player = findPlayer(self.P1, self.P2)
            self.appendLog(
                "Player Position: {}".format(converPos(player, self.P1, self.P2))
            )

            for i in range(1, 4):
                if self.bossFlag == 1:
                    i = 2
                if self.TowerPriority[str(i)] == "Enemy":
                    enemy = self.TowerEnemies(player)
                    if enemy != player:
                        player = enemy
                        break
                elif self.TowerPriority[str(i)] == "Chest":
                    chest = self.TowerChests(player)
                    if chest != player:
                        player = chest
                        break
                elif self.TowerPriority[str(i)] == "Boss":
                    keepBottin = self.TowerBoss()
                    self.bossFlag = 0
                    if not keepBottin:
                        break

            self.appendLog("End of turn.")
            self.appendLog("\n" + 50 * "-" + "\n")
        return times + 1

    ##### Priorities Functions #####

    @classmethod
    def TowerEnemies(self, player):
        enemies = findEnemy(self.P1, self.P2)
        if enemies:
            lambFun = lambda coord: np.sqrt(
                (player[0] - coord[0]) ** 2 + (player[1] - coord[1]) ** 2
            )
            enemies = sorted(enemies, key=lambFun)
            self.appendLog(
                "Enemies: {}".format([converPos(e, self.P1, self.P2) for e in enemies])
            )
            for enemy in enemies:
                pyautogui.click(enemy)
                self.appendLog(
                    "\tAttacking Enemy: {0}".format(converPos(enemy, self.P1, self.P2))
                )
                time.sleep(1)
                auto_battle(self.P1, self.P2, enemy, self.grindMode, self.grindAmount)
                self.increseStatus("Enemy")
                time.sleep(1)
                boss = findBoss(self.P1, self.P2)
                if boss:
                    self.bossFlag = 1
                    break
            return enemy
        else:
            return player

    @classmethod
    def TowerChests(self, player):
        chests = findChests(self.P1, self.P2)
        if chests:
            lambFun = lambda coord: np.sqrt(
                (player[0] - coord[0]) ** 2 + (player[1] - coord[1]) ** 2
            )
            chests = sorted(chests, key=lambFun)
            self.appendLog(
                "Chests: {}".format([converPos(cx, self.P1, self.P2) for cx in chests])
            )
            for chest in chests:
                pyautogui.click(chest)
                self.appendLog(
                    "\tGathering Chest: {0}".format(converPos(chest, self.P1, self.P2))
                )
                time.sleep(4)
                if isOutOfEnergy(self.P1, self.P2, self.grindMode, self.grindAmount):
                    time.sleep(0.5)
                    pyautogui.click(chest)
                    time.sleep(0.8)
                self.increseStatus("Chest")
                break
            return chest
        else:
            return player

    @classmethod
    def TowerBoss(self):
        boss = findBoss(self.P1, self.P2)
        if boss:
            self.appendLog("Boss: {}".format(converPos(boss, self.P1, self.P2)))
            pyautogui.click(boss)
            self.appendLog("\tAttacking Boss.")
            time.sleep(1)
            auto_battle(self.P1, self.P2, boss, self.grindMode, self.grindAmount)
            self.increseStatus("Boss")
            time.sleep(1)
            pyautogui.click()
            time.sleep(0.5)
            bossChests = findBossChests(self.P1, self.P2)
            while not bossChests:
                pyautogui.click()
                bossChests = findBossChests(self.P1, self.P2)

            bossChests = sorted(bossChests, key=lambda x: x[0])
            randChoice = random.choice(bossChests)
            pyautogui.click(randChoice)
            time.sleep(2)
            # button = findConfirmButon(self.P1, self.P2)
            # if button:
            #     if self.grindGCReward:
            #         button = findGCButton(self.P1, self.P2)
            #         pyautogui.click(button)
            #     else:
            #         pyautogui.click(button)

            return False

        else:
            return True
