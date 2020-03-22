from pynput.mouse import Listener, Button, Controller


class ClickListener:
    def __init__(self):
        self.ClickTimes = 0
        self.CurrentClick = 0
        self.ClickPositions = []

    @classmethod
    def on_click(cls, x, y, button, pressed):
        mouse = Controller()
        if pressed and button == Button.middle:
            cls.ClickPositions.append(mouse.position)
            cls.CurrentClick += 1
            if cls.ClickTimes <= cls.CurrentClick:
                return False
        elif button == Button.right:
            return False

    @classmethod
    def getClicks(cls, nr):
        cls.ClickPositions = []
        cls.CurrentClick = 0
        cls.ClickTimes = nr
        with Listener(on_click=cls.on_click) as listener:
            listener.join()
        return cls.ClickPositions
