from PyQt5.QtWidgets import QToolBar, QAction
class Toolbar(QToolBar):
    def __init__(self,MainMenu):
        super().__init__()
        self.MainMenu = MainMenu
        self.action_buttons = {
            'file': QAction("File", self),
            'edit': QAction("Edit", self),
            'action': QAction("Action", self),
            'view': QAction("View", self)
        }

        self.menus = {
            'file': {
                'new': QAction("New connection", self),
                'open': QAction("Import SQL from flie", self),
                'close': QAction("Close", self),
            },
            'edit': {
                'duplicate': QAction("Duplicate row", self),
                'duplicate_few': QAction("Duplicate row x times", self),
                'delete': QAction("Remove", self),
            },

            'action': {
                'run': QAction("Run", self),
                'stop': QAction("Stop", self),
            },
            'view': {
                'show': QAction("Show", self),
                'hide': QAction("Hide", self),
            }
        }
        
        #self.app.setStatusTip("Manage your connection and app settings")
        #button_action.triggered.connect(self.onMyToolBarButtonClick)
        self.initButtons()

 
        


    def initButtons(self):
        for name,menu in self.action_buttons.items():
            self.addAction(menu)
            self.addSeparator()

            section = self.MainMenu.addMenu("&"+name.capitalize())
            for action in self.menus[name].values():
                    section.addAction(action)
