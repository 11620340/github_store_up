# netsh advfirewall firewall set rule name="0_ps2_in" new enable=yes
# netsh advfirewall firewall set rule name="0_ps2_out" new enable=yes
# netsh advfirewall firewall set rule name="0_ps2_in" new enable=no
# netsh advfirewall firewall set rule name="0_ps2_out" new enable=no

import keyboard, win32gui, win32con
import subprocess, time


def block_internet():
    try:
        subprocess.run('netsh advfirewall firewall set rule name="0_ps2_in" new enable=yes',
                       creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        subprocess.run('netsh advfirewall firewall set rule name="0_ps2_out" new enable=yes',
                       creationflags=subprocess.CREATE_NO_WINDOW, check=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    print('blocked')


def allow_internet():
    try:
        subprocess.run('netsh advfirewall firewall set rule name="0_ps2_in" new enable=no',
                       creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        subprocess.run('netsh advfirewall firewall set rule name="0_ps2_out" new enable=no',
                       creationflags=subprocess.CREATE_NO_WINDOW, check=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    print('allowed')


def set_top():
    hwnd = None
    while not hwnd:
        hwnd = win32gui.FindWindow('ConsoleWindowClass', None)
        print(hwnd)
        time.sleep(0.1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 100, 120, 0)

# 注册快捷键事件处理函数
# keyboard.add_hotkey('/', block_internet)
# keyboard.add_hotkey('*', allow_internet)
keyboard.add_hotkey('F3', allow_internet)
keyboard.add_hotkey('F4', block_internet)


# 开始监视键盘事件
set_top()

try:
    print("PS2灵魂出窍V240126 等待快捷键触发")
    keyboard.wait()
# except KeyboardInterrupt:
#     # 当 'esc' 键被按下时，会引发 KeyboardInterrupt 异常
#     print("等待被中断，程序继续执行。")
finally:
    # 在退出程序前取消所有键盘挂钩
    keyboard.unhook_all()
    print('clear done')
