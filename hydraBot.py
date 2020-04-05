from TowerBot.Helper_Functions.clickListener import ClickListener as CL
from TowerBot.Helper_Functions import helperFunctions as HL
import pyautogui, time


def getScreenPoints():
    return CL.getClicks(nr=2)


arena = [
    [(267.5, 169.5), (353.5, 169.5), (440.5, 169.5), (526.5, 169.5), (613.5, 169.5)],
    [(267.5, 256.5), (353.5, 256.5), (440.5, 256.5), (526.5, 256.5), (613.5, 256.5)],
    [(267.5, 343.5), (353.5, 343.5), (440.5, 343.5), (526.5, 343.5), (613.5, 343.5)],
    [(267.5, 429.5), (353.5, 429.5), (440.5, 429.5), (526.5, 429.5), (613.5, 429.5)],
]

roi = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]

rof = [(0, 0), (0, 4), (4, 0), (4, 4)]


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def convertCoord(point):
    found = False
    for row_index, row in enumerate(arena):
        for col_index, col in enumerate(row):
            if distance(point, col) <= 10:
                found = True
                break
        if found:
            break
    return (row_index, col_index)


def auto_battle(P1, P2):
    arrow = (
        HL.percent(96, (P2[0] - P1[0])) + P1[0],
        HL.percent(96, (P2[1] - P1[1])) + P1[1],
    )  # Define que a Arrow está a 99% em X e 97% em Y
    time.sleep(0.5)
    button = HL.findFightButton(P1, P2)
    while not button:
        button = HL.findFightButton(P1, P2)
    while button:
        pyautogui.click(button)
        button = HL.findFightButton(P1, P2)
    time.sleep(0.5)
    while not HL.findHydraHurryBattle(P1, P2):
        continue
    pyautogui.click(arrow)
    time.sleep(1)
    victory_status = HL.findVictory(P1, P2)
    time.sleep(0.5)
    pyautogui.click(arrow)
    return victory_status


def auto_battleM(P1, P2, position):
    for pos in position:
        pyautogui.click(pos)
        time.sleep(2)
        btn = HL.findHydraHeroSelectBtn(P1, P2)
        if btn:
            victory = auto_battle(P1, P2)
            if not victory:
                return not victory
    return victory


def block_battle(P1, P2, hydraPos, playerPos, enemiesPos):
    if hydraPos == (0, 0):
        position = [arena[1][1], arena[0][1], arena[0][0]]
    elif hydraPos == (0, 4):
        position = [arena[1][3], arena[0][3], arena[0][4]]
    elif hydraPos == (3, 0):
        position = [arena[2][1], arena[3][1], arena[3][0]]
    else:
        position = [arena[2][3], arena[3][3], arena[3][4]]
    victory = auto_battleM(P1, P2, position)
    return victory


def fight(p1, p2, num_fights=10):
    # function that emulates fight. It is the main fight function that executes all battles
    for i in range(num_fights):
        FIGHT = True
        count = 0
        block_break = False
        block_battle_f = False
        victory_flag = True
        print("Hydra number: ", i + 1)
        while FIGHT:
            count += 1
            print("Round: ", count)
            player = HL.findPlayer(p1, p2)
            if not player:
                print("Player not found!")
                break
            hydraBoss = HL.findHydraBoss(p1, p2)
            if not hydraBoss:
                enemies = HL.findHydraEnemy(p1, p2)
                enmy_in_roi = []
                for enemy in enemies:
                    # print("enemy: ", enemy)
                    for pos in roi:
                        temp = arena[pos[0]][pos[1]]
                        # print(
                        #     "enemy,pos and dist: ", enemy, temp, distance(temp, enemy)
                        # )
                        if distance(temp, enemy) <= 10:
                            enmy_in_roi.append(temp)
                if len(enmy_in_roi) != 0:
                    nearest_enmy = sorted(
                        enmy_in_roi, key=lambda x: distance(player, x)
                    )[0]
                else:
                    nearest_enmy = sorted(enemies, key=lambda x: distance(player, x))[0]
                print("nearest: ", nearest_enmy)
                pyautogui.click(nearest_enmy)
                time.sleep(2)
                btn = HL.findHydraHeroSelectBtn(p1, p2)
                if not btn:
                    time.sleep(5)
                    btn = HL.findHydraHeroSelectBtn(p1, p2)
                    if not btn:
                        print("blockage:")
                        FIGHT = False
                        block_break = True
                time.sleep(0.8)
                victory = auto_battle(p1, p2)
                if not victory:
                    victory_flag = False
                    break
            else:
                print("Found Boss at: ", hydraBoss)
                pyautogui.click(hydraBoss)
                time.sleep(2)
                btn = HL.findHydraHeroSelectBtn(p1, p2)
                if not btn:
                    time.sleep(5)
                    btn = HL.findHydraHeroSelectBtn(p1, p2)
                    if not btn:
                        print("blockage:")
                        player = HL.findPlayer(p1, p2)
                        enemies = HL.findHydraEnemy(p1, p2)
                        enemies = sorted(enemies, key=lambda x: distance(player, x))
                        enemiesPos = list(map(convertCoord, enemies))
                        playerPos = convertCoord(player)
                        hydraPos = convertCoord(hydraBoss)
                        victory = block_battle(p1, p2, hydraPos, playerPos, enemiesPos)
                        block_battle_f = True
                        if not victory:
                            victory_flag = False
                            break
                if not block_battle_f:
                    time.sleep(0.8)
                    victory = auto_battle(p1, p2)
                    if not victory:
                        victory_flag = False
                        break
                FIGHT = False
        if (block_break) or (not victory_flag):
            break


fight((3, 52), (883, 545), num_fights=51)
