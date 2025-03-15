######################################################################################
# You can add more status messages here
status = [
    "vrc osc",
    "My osc status",
    "Magic chat box lookalike on linux",
    "linux osc for vrchat",
]
######################################################################################


######################################################################################
# Do not change unless you know what you're doing

import os
import signal
import time
from pythonosc.udp_client import SimpleUDPClient
import threading

VRCHAT_IP = "127.0.0.1"
VRCHAT_PORT = 9000

client = SimpleUDPClient(VRCHAT_IP, VRCHAT_PORT)

chatbox_text = "/chatbox/input"
chatbox_visibility = "/chatbox/typing"

message_interval = 5

pause_script = False
custom_message = ""
def get_active_window():
    try:
        output = os.popen('xdotool getwindowfocus getwindowname').read().strip()
        return output if output else None
    except Exception:
        return None

def get_system_time():
    return time.strftime("%I:%M %p", time.localtime())


def handle_user_input():
    global pause_script, custom_message
    while True:
        user_input = input("Enter a message (or press 'ctrl + c' to quit): ")

        if not pause_script:
            pause_script = True
            custom_message = f"💬 {user_input}"

            time.sleep(10)
            pause_script = False

input_thread = threading.Thread(target=handle_user_input)
input_thread.daemon = True
input_thread.start()

last_sent_time = time.time()
message_index = 0

while True:
    current_time = time.time()

    if not pause_script:
        if current_time - last_sent_time >= message_interval:
            active_window = get_active_window()
            system_time = get_system_time()

            message = status[message_index]

            full_message = f"{message}"

            if active_window:
                full_message += f"\nOn desktop ⁱⁿ '{active_window}'\n {system_time} "
            else:
                full_message += f"\n {system_time} "

            client.send_message(chatbox_text, [full_message, True])

            message_index = (message_index + 1) % len(status)

            last_sent_time = current_time

    if pause_script and custom_message:
        print(f"Message sent: {custom_message}")

        client.send_message(chatbox_visibility, True)

        time.sleep(1)

        client.send_message(chatbox_text, [custom_message, True])

        client.send_message(chatbox_visibility, False)

        custom_message = ""

    time.sleep(0.1)

######################################################################################
