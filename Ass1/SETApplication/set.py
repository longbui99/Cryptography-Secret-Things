from ui import UI as UserInterface
from alg import Algorithms as Al
import threading


class Application:
    def __init__(self):
        self.ui = UserInterface()
        self.cryp = Al(self.ui)
        self.addCommandForUI()
        self.isThread = False
        self.stop_event = threading.Event()
        self.algThread = None
        self.ui.root.protocol("WM_DELETE_WINDOW", self.stopProgram)

    def stopProgram(self):
        if self.algThread:
            if self.algThread.isAlive():
                self.ui.messageBoxShow()
            else:
                self.ui.updateAndTerminate(True)
                self.ui.close()
        else:
            self.ui.close()
        

    def runUI(self):
        self.ui.runUI()

    def runAlgorithsm(self, ):
        self.algThread = threading.Thread(target=self.cryp.runField)
        self.algThread.start()

    def addCommandForUI(self):
        self.ui.ActiveBtn["command"] = self.runAlgorithsm

if __name__ == "__main__":
    app = Application()
    app.runUI();