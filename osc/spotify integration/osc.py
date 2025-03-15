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
import time
import threading
from pythonosc.udp_client import SimpleUDPClient

VRCHAT_IP = "127.0.0.1"
VRCHAT_PORT = 9000

client = SimpleUDPClient(VRCHAT_IP, VRCHAT_PORT)

chatbox_text = "/chatbox/input"
chatbox_visibility = "/chatbox/typing"

message_interval = 5

pause_script = False
custom_message = ""

def get_spotify_song():
    try:
        song = os.popen('playerctl -p spotify metadata --format "{{artist}} - {{title}}"').read().strip()
        return song if song else "No song playing"
    except Exception:
        return "Spotify not detected"

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

last_status_message = ""
last_sent_time = time.time()
message_index = 0

while True:
    current_time = time.time()

    if not pause_script:
        if current_time - last_sent_time >= message_interval:
            system_time = get_system_time()
            message = status[message_index]

            if message != last_status_message:
                song = get_spotify_song()
                full_message = f"{message}\n🎵 {song}\n {system_time} "
                client.send_message(chatbox_text, [full_message, True])

                last_status_message = message
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
