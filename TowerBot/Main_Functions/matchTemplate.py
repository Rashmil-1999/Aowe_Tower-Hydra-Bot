import cv2, pyautogui
import numpy as np


def findImg(
    image, P1, P2=None, _type="one", precision=0.8, im=None, centerPosition=True
):
    # print("Search for: {0}".format(image.split("/")[-1]))
    x1 = P1[0]
    y1 = P1[1]
    if im is None:
        x2 = P2[0]
        y2 = P2[1]
        im = region_grabber(region=(x1, y1, x2, y2))
        if is_retina():
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    else:
        x2, y2, _ = im.shape

    # Tratamento de Imagem e do template
    img_rgb = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    OldY, OldX = img_gray.shape
    # img_gray = cv2.resize(
    #     img_gray, (1033, 581)
    # )  # Para o matchTemplate funcionar com todos os tamanhos.
    template = cv2.imread(image, 0)
    if template is None:
        return False
    w, h = template.shape[::-1]
    # Pega a lista dos Matches em 'res'
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Verifico o Min e o Max dos matches para terminar o processo caso não encontre nada relevante.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # h, w = template.shape

    max_loc = (max_loc[0] + x1, max_loc[1] + y1)
    if centerPosition:
        max_loc = (max_loc[0] + w / 2, max_loc[1] + h / 2)

    # max_loc = (
    #     int((((max_loc[0] - x1) / 1033) * OldX)) + x1,
    #     int((((max_loc[1] - y1) / 581) * OldY) + y1),
    # )
    if (
        max_val < precision
    ):  # Valida se o melhor match encontrado é 'no minimo aceitavel'.
        return False

    if (
        _type == "one"
    ):  # Verifica se o tipo é 'one' para retornar apenas o melhor match.
        return max_loc

    elif _type == "many":
        match_locations = np.where(res >= precision)  # Filtro com base na precisão.

        hM = h * 1.05  # Apenas para margem de erro.
        wM = w * 1.05

        matches = []
        for (x, y) in zip(match_locations[1], match_locations[0]):
            x += w / 2 + x1  # w/2 e h/2 é para focar no centro do Template.
            y += h / 2 + y1  # x1 e y1 é para deslocar para onde foi selecionado.
            if all(
                (
                    (x > p[0] + wM / 2 or x < p[0] - wM / 2)
                    or (y < p[1] - hM / 2 or y > p[1] + hM / 2)
                )
                for p in matches
            ):
                matches.append((x, y))

        # lambFun = lambda x: (
        #     int((((x[0] - x1) / 1033) * OldX) + x1),
        #     int((((x[1] - y1) / 581) * OldY) + y1),
        # )  # Corrige o resize do inicio.
        # matches = list(map(lambFun, matches))

        return matches


def is_retina():
    return False


#     if platform.system() == "Darwin":
#         return subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True)
#     else: return False


def region_grabber(region):
    if is_retina():
        region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1
    return pyautogui.screenshot(region=(x1, y1, width, height))
