# import threading
import os, shutil
import time
# import pywinauto.findwindows
# from pywinauto import application
from perpetual_timer import PerpetualTimer
# from perpetualtimer import perpetualTimer

from config import *
from functions import *

screenshot_coords_web = (1781, 895)
screenshot_coords_app = (1781 -1, 895 -46 +15)

class Livecatan:
    # if __name__ == '__main__':
    # def __init__(self,t,hFunction):

    def __init__(self):
        self.action = None
        if len(sys.argv) > 1:
            self.action = sys.argv[1]
        # self.mode = None
        # if len(sys.argv) > 2:
        #     self.mode = sys.argv[2]
        self.interval = interval # sec
        self.nbmax = nbmax
        self.dirpath = dirpath

        self.lastfilename = ''
        self.nb = 0
        self.screenshot_coords = screenshot_coords_web


    # def find_catan_windows(self):   # unused yet, work in progress
    #     app = application.Application()
    #     # win = app.window(title='Untitled - Notepad')
    #     # win = app.CatanUniverse
    #     # win = app.window(title='Catan Universe')
    #     # win = app.connect(title='Catan Universe - Google Chrome')
    #     win = app.connect(best_match='Catan Universe')
    #     print(win)
    #     dlg = win.wrapper_object()
    #     print(dir(dlg))

    def init(self):
        print('--- Live Catan Universe C&K dice stats ---')
        # script's action argument
        if self.action != None:
            if self.action == 'start':
                clean_images(self.dirpath)
                self.start()
                exit()
                return True

            if self.action == 'app':
                self.screenshot_coords = screenshot_coords_app
                print('--- app mode ---')

        # User input
        while True:
            try:
                key = input('Start watching (s), Delete last images (d) Quit (q): ')
                if key == 's':
                    self.start()
                    # exit()
                    break
                elif key == 'd':
                    clean_images(self.dirpath)
                elif key == 'q':
                    exit()
                    break
            except Exception as e:
                print(e)

    def start(self):
        # clean_images(self.dirpath)
        print('started.')
        self.letimer = PerpetualTimer(self.interval, self.routine)
        self.letimer.start()

    def routine(self):
        # self.nb = self.nb + 1
        # print('%s/%s' % (self.nb, self.nbmax))
        res = watch(self.screenshot_coords, self.action, self.dirpath, self.lastfilename, self.nb)
        self.lastfilename = res['lastfilename']
        self.nb = res['nb']

        if( self.nb == self.nbmax ):
            print('Stopped!')
            self.letimer.cancel()
            # return True

def main():
    livecatan = Livecatan()
    livecatan.init()
    # livecatan.find_catan_windows()

if __name__ == "__main__":
    main()
