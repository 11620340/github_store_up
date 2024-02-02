import win32con, win32gui, win32clipboard
import time, subprocess, threading,os

home_path = os.path.expanduser('~')


def select_dir():
    # 捕获选择框并用Home键盘选择桌面
    select_handle = None
    while not select_handle:
        select_handle = win32gui.FindWindow(None, '浏览文件夹')
        time.sleep(0.1)
    select_child_handle = None
    while not select_child_handle:
        select_child_handle = win32gui.FindWindowEx(select_handle, None, 'SysTreeView32', None)

    win32gui.SendMessage(select_child_handle, win32con.WM_KEYDOWN, win32con.VK_HOME, 0)
    win32gui.SendMessage(select_child_handle, win32con.WM_KEYUP, win32con.VK_HOME, 0)

    # 选择框中点击确认
    confirm_button_handle = None
    while not confirm_button_handle:
        confirm_button_handle = win32gui.FindWindowEx(select_handle, None, None, '确定')
    print(confirm_button_handle)
    win32gui.SendMessage(confirm_button_handle, win32con.WM_LBUTTONDOWN, 0, 0)
    win32gui.SendMessage(confirm_button_handle, win32con.WM_LBUTTONUP, 0, 0)

def close_AD():
    # 定义关闭那个傻鸡巴软件的广告页面的函数，你妈的比这软件做的真鸡巴傻逼！
    AD_handle = None
    while not AD_handle:
        AD_handle = win32gui.FindWindow('#32770', 'StudioOne KeyGen v3.54.0')
        time.sleep(0.3)
    print(AD_handle)
    win32gui.SendMessage(AD_handle, win32con.WM_CLOSE, 0, 0)

def spawn():
    # 获取剪切板中的内容，并启动激活软件
    win32clipboard.OpenClipboard()
    key_data = win32clipboard.GetClipboardData()
    # key_data = '4324324324234324324'
    subprocess.Popen('install_datas\StudioOne_Keygen.exe')

    # 定义专门隐藏这个傻逼软件的函数，并在后边实例化为进程，循环2秒
    def hide_window():
        for i in range(10):
            win32gui.ShowWindow(main_handle, win32con.SW_HIDE)
            time.sleep(0.1)
            # print(i)

    # # 捕获激活软件主窗口，并找到输入激活码的edit3
    main_handle = None
    while not main_handle:

        main_handle = win32gui.FindWindow('hspwnd0', None)
        time.sleep(0.1)

    thread_hide = threading.Thread(target=hide_window)
    thread_hide.start()

    edit1_handle = None
    while not edit1_handle:

        edit1_handle = win32gui.FindWindowEx(main_handle, None, 'Edit', None)
    edit2_handle = None
    while not edit2_handle:
        edit2_handle = win32gui.FindWindowEx(main_handle, edit1_handle, 'Edit', None)
    edit3_handle = None
    while not edit3_handle:
        edit3_handle = win32gui.FindWindowEx(main_handle, edit2_handle, 'Edit', None)
    win32gui.SendMessage(edit3_handle, win32con.WM_SETTEXT, None, key_data)
    print(edit3_handle)
    print(key_data)
    print("粘贴激活码")


    generate_handle = None
    while not generate_handle:
        generate_handle = win32gui.FindWindowEx(main_handle, None, None, 'GENERATE')

    win32gui.SendMessage(generate_handle, win32con.WM_LBUTTONDOWN, 0, 0)
    win32gui.SendMessage(generate_handle, win32con.WM_LBUTTONUP, 0, 0)
    select_dir()


    while True:
        if os.path.isfile(f'{home_path}\\Desktop\\studioapp6.pro.license') == True:
            break
        time.sleep(0.1)
    # 关闭激活软件，提前定义关闭广告函数，提前创建关闭广告线程，要不然会阻塞主程序
    thread_close_AD = threading.Thread(target=close_AD)
    thread_close_AD.start()
    win32gui.SendMessage(main_handle, win32con.WM_CLOSE, 0, 0)


def spwan():
    spawn()




