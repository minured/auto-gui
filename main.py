import threading
import time
from autoclick import get_xy, auto_Click, switchToWindow
from tk2 import logger


def startTask():
    time.sleep(3)
    switchToWindow('Google Chrome')
    xy = get_xy("./pic/new-post.png")
    auto_Click(xy)
    

def main():
    threading.Thread(target=startTask).start()
    logger.start()


if __name__ == "__main__":
    main()
