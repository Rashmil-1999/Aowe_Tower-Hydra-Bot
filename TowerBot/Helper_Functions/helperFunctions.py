import pyautogui, cv2, time
import os
from TowerBot.Main_Functions.matchTemplate import findImg

picDirTowerBot = os.path.join(os.getcwd(), "TowerBot", "pic")


def isOutOfEnergy(P1, P2, grindMode, grindAmount):
    gringAmountSpent = 0
    img = findOutOfEnergy(P1, P2)
    if img:
        if grindMode == "Wait":
            image = cv2.imread(os.path.join(picDirTowerBot, "outOfEnergy.jpg"))
            xButton = findXButton(P1, P2)
            pyautogui.click(xButton)
            time.sleep(250 * grindAmount)
            return gringAmountSpent
        if grindMode == "Gold Coin":
            if gringAmountSpent <= grindAmount:
                if gringAmountSpent == 25:
                    gringAmountSpent += 10
                else:
                    gringAmountSpent += 5
                image = cv2.imread(os.path.join(picDirTowerBot, "outOfEnergy.jpg"))
                gcButton = findGCButton(P1, P2)
                pyautogui.click(gcButton)
                time.sleep(0.3)
                return gringAmountSpent
            else:
                return "Not enough."
        if grindMode == "Item":
            if gringAmountSpent <= grindAmount:
                image = cv2.imread(os.path.join(picDirTowerBot, "outOfEnergy.jpg"))
                scrollButton = findScrollEnergyItem(P1, P2)
                useButton = findUseButton(P1, P2)
                # pyautogui.mouseDown(
                #     button="right", x=scrollButton[0], y=scrollButton[1]
                # )
                # pyautogui.mouseUp(button="right", x=useButton[0], y=useButton[1])
                pyautogui.click(scrollButton)
                time.sleep(0.4)
                pyautogui.click(useButton)
                time.sleep(1)
                gringAmountSpent += 3
                return gringAmountSpent
            else:
                return "Not enough."
    else:
        False


def converPos(coord, P1, P2):
    X = coord[0]
    Y = coord[1]

    X = ((X - P1[0]) * 100) / (P2[0] - P1[0])
    if X >= 16 and X <= 33:
        X = 1
    elif X >= 35 and X <= 42:
        X = 2
    elif X >= 43 and X <= 51:
        X = 3
    elif X >= 52 and X <= 60:
        X = 4
    elif X >= 61 and X <= 68:
        X = 5
    elif X >= 70 and X <= 77:
        X = 6

    Y = ((Y - P1[1]) * 100) / (P2[1] - P1[1])
    if Y >= 13 and Y <= 26:
        Y = 1
    elif Y >= 30 and Y <= 42:
        Y = 2
    elif Y >= 45 and Y <= 58:
        Y = 3
    elif Y >= 61 and Y <= 74:
        Y = 4
    elif Y >= 77 and Y <= 90:
        Y = 5

    return (X, Y)


def moveTo(coord, s=0.2):
    pyautogui.moveTo(coord[0], coord[1], duration=s)


def moveToM(coords, s=0.2):
    for coord in coords:
        pyautogui.moveTo(coord[0], coord[1], duration=s)


def percent(nr, tudo, mode="percent"):
    if mode == "percent":
        return (nr * tudo) / 100.0
    elif mode == "numeric":
        return (nr * 100) / tudo


def findNextLvl(P1, P2):
    return findImg(picDirTowerBot + "nextLvl.jpg", P1, P2)


def findPlayer(P1, P2):
    player = findImg(os.path.join(picDirTowerBot, "player.jpg"), P1, P2)
    if player:
        return player
    else:
        return findImg(os.path.join(picDirTowerBot, "player2.jpg"), P1, P2)


def findEnemy(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "enemy.jpg"), P1, P2, _type="many")


def findChests(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "chest.jpg"), P1, P2, _type="many")


def findBossChests(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "boss_chest.jpg"), P1, P2, _type="many")


def findBoss(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "boss.jpg"), P1, P2)


def findFightButton(P1, P2):
    return findImg(
        os.path.join(picDirTowerBot, "troop_choose_fight_button.jpg"), P1, P2
    )


def findFightStarted(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "fight_part_recognize.jpg"), P1, P2)


def findHurryBattle(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "hurry_Battle_recognize.jpg"), P1, P2)


def findOutOfEnergy(P1, P2):
    return findImg(
        os.path.join(picDirTowerBot, "outOfEnergy.jpg"), P1, P2, centerPosition=False
    )


def findConfirmButon(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "confirmButton.jpg"), P1, P2)


def findGCButton(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "GoldCoinButton.jpg"), P1, P2)


def findXButton(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "xButton.jpg"), P1, P2)


def findScrollEnergyItem(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "scrollEnergyItem2.jpg"), P1, P2)


def findUseButton(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "useButton.jpg"), P1, P2)


def findChestOrb(P1, P2):
    return findImg(os.path.join(picDirTowerBot, "chest_orb.jpg"), P1, P2)
