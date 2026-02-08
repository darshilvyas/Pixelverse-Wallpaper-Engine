from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QGridLayout, QStackedWidget,QLineEdit,QProgressBar,QSystemTrayIcon,QMenu
)
from PySide6.QtCore import Qt , QTimer, QSettings ,QObject, Signal, QThread 
from PySide6.QtGui import QPixmap , QIcon
import sys
import wall as wl
import category as cat
import os
import winreg
import storage as sg
from pyqttoast import Toast, ToastPreset
from PySide6.QtNetwork import QNetworkInformation



APP_NAME = "PixelverseWallpaper"

FLAG_FILE = os.path.join(os.getenv("APPDATA"), APP_NAME, "first_run.txt")

def is_first_run():
    return not os.path.exists(FLAG_FILE)


def add_to_startup():
    exe_path = sys.executable  # 

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)


def mark_first_run_done():
    os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
    with open(FLAG_FILE, "w") as f:
        f.write("done")



if is_first_run():
    add_to_startup()
    mark_first_run_done()


# Qt threds for api key validation
class ApiWorker(QObject):
    finished = Signal(bool)

    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def run(self):
        result = wl.check_api(self.api_key)
        self.finished.emit(result)

# intialize the Main Component
app = QApplication(sys.argv)
# Create a Main BG Container
window = QWidget()
window.setWindowTitle("Pixelverse 8k Wallpaper")
app.setOrganizationName("DarshilSoft")
app.setApplicationName("Pixelverse")
window.resize(900, 500)

# Load storage
path_wal=sg.get_loc()

# logo loading
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

app.setWindowIcon(QIcon(resource_path("asset/logo.ico")))




# LOAD SETTINGS VARIABLES
settings = QSettings("DarshilVyas", "Pixelverse Wallpaper")   
last_cat = settings.value("last_cat","landscape",type=str)
api_key = settings.value("api",None,type=str)

# Check internet func

def is_internet_available():
    #Initialize the network backend
    QNetworkInformation.loadDefaultBackend()
    
    # get the singleton instance
    info = QNetworkInformation.instance()
    
    # Check if the reachability is online
    return info.reachability() == QNetworkInformation.Reachability.Online




# Create A GRID Layout FOR  for Two part 1 sidebar 2 main page
main_grid = QGridLayout(window)

# LEFT SIDEBAR
sidebar = QWidget()
sidebar.setFixedWidth(180)
# sidebar.setStyleSheet("background-color:#000000;")

# Create A Vertical STACK OF sidebar Options
sidebar_layout = QVBoxLayout(sidebar)

btn_home = QPushButton("Home")
btn_setting = QPushButton("Settings")
btn_change = QPushButton("Change-Wallpaper")
btn_change.setCursor(Qt.PointingHandCursor)

sidebar_layout.addWidget(btn_home)
sidebar_layout.addWidget(btn_setting)
sidebar_layout.addWidget(btn_change)
sidebar_layout.addStretch()

# MAIN-CONTENT AREA (RIGHT) 

content = QWidget()
content_layout = QVBoxLayout(content)

# TO SHOW ALL PAGE ONE BY ONE IN STACK BY CLICKING SIDE BAR BUTTON

stack = QStackedWidget()


# HOME PAGE
print(api_key)
home_page = QWidget()
home_layout = QVBoxLayout(home_page)

lbl_api = QLabel("*Please Enter Your PIXABAY API key for Further Process")
lbl_api.setAlignment(Qt.AlignLeft)
lbl_api.setStyleSheet("font-size:15px; color:red;")


lbl_err = QLabel("API KEY IS WRONG PLEASE TRY AGIAN...")
lbl_err.setAlignment(Qt.AlignCenter)
lbl_err.setStyleSheet("font-size:15px; color:red;")


input_box = QLineEdit()
input_box.setPlaceholderText("Enter Your Api KEY....")
submit_btn = QPushButton("Submit")
loader = QProgressBar()
loader.setRange(0, 0)     # make it infinite
loader.setAlignment(Qt.AlignCenter)


label_A = QLabel('<a href="https://example.com">HOW TO GET PIXABAY API ? CLICK HERE...</a>')
label_A.setOpenExternalLinks(True)  # makes link clickable
label_A.setAlignment(Qt.AlignCenter)
label_A.setStyleSheet("color:#0000FF; font-size:15px;")

lbl = QLabel()
lbl.setFixedSize(500, 300)
lbl.setAlignment(Qt.AlignCenter)
lbl.setStyleSheet("""
        border-radius: 20px;
        text-align:center;
        padding:0px;
""")
btn_category = QLabel("Image By PIXABAY....")
btn_category.setAlignment(Qt.AlignLeft)
home_layout.addWidget(lbl_api)
home_layout.addWidget(input_box)
home_layout.addWidget(submit_btn)
home_layout.addWidget(loader)
home_layout.addWidget(label_A)
home_layout.addWidget(lbl_err)
home_layout.addWidget(lbl)
home_layout.addWidget(btn_category)
home_layout.addStretch()

# CHECK API BEFORE SETTING PAGE INITIALIZATION FOR RESET BUTTON
def  api_check():
    if not api_key:
        submit_btn.show()
        input_box.show()
        lbl_api.show()
        label_A.show()
        lbl.hide()
        btn_category.hide()


QTimer.singleShot(100, lambda: update_image(f"{path_wal}/temp.jpg"))





# SETTINGS PAGE

settings_page = QWidget()
settings_layout = QVBoxLayout(settings_page)

lbl_settings = QLabel("🛑Settings")
lbl_settings.setAlignment(Qt.AlignCenter)
lbl_settings.setStyleSheet("font-size:20px;")

lbl_set_api = QLabel("Click RESET Remove Api KEY")
lbl_set_api.setStyleSheet("font-size:15px;")
reset_btn = QPushButton("RESET")
lbl_reset = QLabel("NOW! You Can Change Your API_KEY BY Going To THE Home Page.")
lbl_reset.setStyleSheet("color:#c7ddd1; background-color:#1c3327; padding:10px;")

settings_layout.addWidget(lbl_settings)
settings_layout.addWidget(lbl_set_api)
settings_layout.addWidget(reset_btn)
settings_layout.addWidget(lbl_reset)
lbl_reset.hide()
settings_layout.addStretch()


#  API NONE FUNCTION
def api_none():
    settings.setValue("api",None)
    lbl_reset.show()
    api_check()
reset_btn.clicked.connect(api_none)

# CHANGE WALL PAGE

# change_page = QWidget()
# change_layout = QVBoxLayout(change_page)

# lbl_change = QLabel("CHANGE WALL PAGE")
# lbl_change.setAlignment(Qt.AlignCenter)
# lbl_change.setStyleSheet("font-size:20px;")

# change_layout.addWidget(lbl_change)
# change_layout.addStretch()





# ADD PAGES TO STACK

stack.addWidget(home_page)      # index 0
stack.addWidget(settings_page)  # index 1
# stack.addWidget(change_page)    # index 2

content_layout.addWidget(stack)


# ADD TO GRID

main_grid.addWidget(sidebar, 0, 0)
main_grid.addWidget(content, 0, 1)


# BUTTON ACTIONS

btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))
btn_setting.clicked.connect(lambda: stack.setCurrentIndex(1))
def change_and_refresh():
    if is_internet_available():
        toast = Toast()
        toast.setDuration(5000)  # 5 seconds
        toast.setTitle("Changing Wallpaper")
        toast.setText("We Are Changing Your Wallpaper 😊.")
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()
    # FETCH CATEGORY AND ADD IT TO SETTING VARIABLE AND ALSO SEND AS SEARCH PARAMETER
    cate = cat.get_category()
    if(cate == last_cat):
        # CHECK FOR ONCE IT NOT SAME AS PRIVIOUS OR ACCEPT IF IT AGAIN GIVE SAME AS LAST
        # ALTERNATIVE SOLUTION IS LOOP ,UNTILL I GOT UNIQE ONE BUT IT NOT EFFICIENT WAY IT LEAD CRASHES
        cate = cat.get_category()
    settings.setValue("last_cat",cate)
    if is_internet_available():
         wl.main(cate)
    else:
          toast = Toast()
    toast.setDuration(5000)  # 5 seconds
    toast.setTitle("No Internet Connection...")
    toast.setText("Please Turn On Internet For Changing Wallpaper 🫠")
    toast.applyPreset(ToastPreset.ERROR_DARK)
    toast.show()

    QTimer.singleShot(200, lambda: update_image(f"{path_wal}/temp.jpg"))

btn_change.clicked.connect(change_and_refresh)


def update_image(path):
    pixmap = QPixmap(path)

    if pixmap.isNull():
        return

    pixmap = pixmap.scaled(
        lbl.size(),
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
    lbl.setPixmap(pixmap)
    lbl.setScaledContents(True) 
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setStyleSheet("""
        border-radius: 20px;
        text-align:center;
        padding:0px;
""")
    lbl.setPixmap(pixmap)


wall_timer = QTimer()
wall_timer.timeout.connect(change_and_refresh)
wall_timer.start(900_000)  # 15 minutes 900 * 1000 = 900000 ms


#API KEY-INPUT BOX                     
input_box.hide()
submit_btn.hide()
lbl_err.hide()
lbl_api.hide()
loader.hide()
label_A.hide()
api_check()
def api_result(success):
    loader.hide()

    if success:
        settings.setValue("api", input_box.text().strip())

        input_box.hide()
        submit_btn.hide()
        lbl_api.hide()
        label_A.hide()
        lbl.show()
        btn_category.show()
    else:
        lbl_err.show()
        submit_btn.show()


def api_submit():
    api_key_value = input_box.text().strip()
    if not api_key_value:
        return

    loader.show()
    submit_btn.hide()
    lbl_err.hide()

# create qt thread for handle api request without ui stuck
    global thread, worker
    thread = QThread()
    worker = ApiWorker(api_key_value)

    worker.moveToThread(thread)
    thread.started.connect(worker.run) # start request api
    worker.finished.connect(api_result) # call api result 
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    thread.start()

# test api KEY
submit_btn.clicked.connect(api_submit)
# SHOW APP


tray = QSystemTrayIcon(QIcon(resource_path("asset/logo.ico")), app)

tray_menu = QMenu()
tray_menu.addAction("Open", window.show)
tray_menu.addAction("Exit", app.quit)

tray.setContextMenu(tray_menu)
tray.show()

window.show()
app.exec()


# now missing things are network handling and setting time management feture and api_key giveing feture and last category and 
# final software pacakge with path management ans one temp image for errors control


# path change is done [done]
# now add api configuration in setting [done]
# add animation while clicking to change btn [done]
# one wallpaer for fallback controll [done]
# website link or tutorial for how to get pixabay api_key
# no-internet handling also not completed [done]
# setup for startup app
