import win32gui, win32com.client, win32con

def print_GetForegroundWindow():
    hwnd_active = win32gui.GetForegroundWindow()
    print('hwnd_active hwnd:',hwnd_active)
    print('hwnd_active text:',win32gui.GetWindowText(hwnd_active))
    print('hwnd_active class:',win32gui.GetClassName(hwnd_active))

print_GetForegroundWindow()
print('------------------------------------------')
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')
win32gui.SetForegroundWindow(win32gui.FindWindow("Dielectric dog","Dielectric dog"))
print_GetForegroundWindow()
win32gui.ShowWindow(win32gui.FindWindow("Dielectric dog","Dielectric dog"), win32con.SW_SHOW)