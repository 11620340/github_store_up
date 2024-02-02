import time, os, threading, subprocess, shutil, requests

import win32con, win32gui
from pywinauto.application import Application
import spawn_lisence
from PyQt5 import QtCore ,QtWidgets

home_path = os.path.expanduser('~')
class login(QtCore.QThread):
    signal_login = QtCore.pyqtSignal(str)
    def __init__(self, user_password):
        super().__init__()
        self.user_password = {"key":user_password}

    def run(self):
        self.response = requests.get(
            'https://97a7ea5e244c4a1d801166104cef719e.apig.cn-east-3.huaweicloudapis.com/jcms_studio',
            params=self.user_password)
        self.signal_login.emit(self.response.text)


class install_studio(QtCore.QThread):
    signal_progressBar = QtCore.pyqtSignal(int)
    def __init__(self, select_option):
        super().__init__()
        self.select_option = select_option

    def run(self):
        if self.select_option == 1:
            print('kaishianzhuang')
            self.install()
            self.activate()
        elif self.select_option == 101:
            self.install()
        elif self.select_option == 102:
            self.activate()
        elif self.select_option == 103:
            self.uninstall()
        elif self.select_option == 104:
            self.deactivate()
        else:
            print('option wrong')


    def install(self):
        try:
            print("开始安装")
            self.signal_progressBar.emit(9)
            subprocess.run([r".\install_datas\SetupStudioOne6v6.5.0.exe", "/verysilent"])
            # subprocess.run(r".\install_datas\SetupStudioOne6v6.5.0.exe")
            self.signal_progressBar.emit(24)
            print("安装完成")

        except Exception as e:
            print('安装失败')
            print(e)
    def activate(self):
        def activate():

            # 关闭登录页面:win32获取句柄，判断窗口类型，切换到离线激活页面，并复制激活码
            hwnd = None
            while not hwnd:
                hwnd = win32gui.FindWindow('CCLDialogClass', None)
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

                if win32gui.GetWindowText(hwnd) == 'Studio One 最终用户许可协议':
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    hwnd = None
                    print("关闭协议")
                    self.signal_progressBar.emit(28)
                elif win32gui.GetWindowText(hwnd) == 'PreSonus 登录':
                    win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    print('关闭登录窗口')
                    self.signal_progressBar.emit(35)
                    hwnd = None
                elif win32gui.GetWindowText(hwnd) == '激活Studio One':
                    for i in range(9):
                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_TAB, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                    print("切换到离线激活")
                    self.signal_progressBar.emit(47)
                    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
                    for i in range(4):
                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_TAB, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                    print("复制激活码")
                    self.signal_progressBar.emit(59)

                    spawn_lisence.spawn()
                    print("lisence生成成功")
                    self.signal_progressBar.emit(72)

                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_TAB, 0)

                    thread_select = threading.Thread(target=select_license)
                    self.signal_progressBar.emit(84)
                    thread_select.start()


                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                    self.signal_progressBar.emit(92)

                    break
                else:
                    time.sleep(0.1)

        def select_license():
            # 选择license win32找不到控件，所以将就用winauto
            while True:
                try:
                    app = Application().connect(title='打开')
                    print('获取到选择授权窗口')
                    break
                except:
                    print("in capture: select")
                    time.sleep(0.3)

            # 通过winauto获取句柄，再用win32发送文字
            select_handle = app['打开']['文件名(&N):Edit'].handle
            win32gui.SendMessage(select_handle, win32con.WM_SETTEXT, None,
                                 f'{home_path}\Desktop\studioapp6.pro.license')

            app['打开']['打开(O)'].click()

            jihuo_hwnd = None
            while not jihuo_hwnd:
                jihuo_hwnd = win32gui.FindWindow(None, 'Studio One')
                print('in capture: studio')
                time.sleep(0.1)
            win32gui.SendMessage(jihuo_hwnd, win32con.WM_CLOSE, 0, 0)

        def clear_activate():
            try:
                for file_name in os.listdir(f'{home_path}\\Desktop\\'):
                    if file_name.endswith('.license'):
                        os.remove(f'{home_path}\\Desktop\\{file_name}')

                print('cleared activate')
            except Exception as e:
                print(e)

        subprocess.Popen('"C:\Program Files\PreSonus\Studio One 6\Studio One.exe"')
        self.signal_progressBar.emit(24)
        activate()
        clear_activate()
        self.signal_progressBar.emit(100)
    def uninstall(self):
        print('开始卸载')
        try:
            subprocess.run([r"C:\Program Files\PreSonus\Studio One 6\unins000.exe", "/verysilent"])
            print("卸载完成")
        except:
            print("卸载失败")
    def deactivate(self):
        try:
            shutil.rmtree(r"C:\ProgramData\PreSonus\Studio One 6")
            print(r"清楚完成：C:\ProgramData\PreSonus\Studio One 6")
        except:
            print("没有这个残留或者清楚失败：C:\ProgramData\PreSonus\Studio One 6")
        try:
            shutil.rmtree(f"{home_path}\\AppData\\Roaming\\PreSonus\\Studio One 6")
            print(f"清楚完成：{home_path}\\AppData\\Roaming\\PreSonus\\Studio One 6")
        except:
            print(f"没有这个残留或者清楚失败：{home_path}\\AppData\\Roaming\\PreSonus\\Studio One 6")
        try:
            shutil.rmtree(f"{home_path}\\Documents\\Studio One")
            print(f"清楚完成：{home_path}\\Documents\\Studio One")
        except:
            print(f"没有这个残留或者清楚失败：{home_path}\\AppData\\Roaming\\PreSonus\\Studio One 6")
