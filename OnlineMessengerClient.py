# NOTE: Server must be started first

import socket
import threading
import queue
from datetime import datetime
import tkinter
from tkinter import END

q = queue.Queue()

prev_message = 0

s = socket.socket()
port = 30110
s.connect(("127.0.0.1", port))

user = "local"
root = tkinter.Tk()
root.title("Online Messaging")
root.geometry("1000x600")
root.resizable(0, 0)
canvas = tkinter.Canvas(root, width=1000, height=600)
canvas.pack()


def current_time():
    time = datetime.now()
    time_formatted = time.strftime("%H:%M:%S")
    return time_formatted


def entry_button_click():
    global prev_message
    entered_text = text_entry.get("1.0", END)
    prev_message = entered_text
    if len(text_entry.get("1.0", "end-1c")) == 0 or str.isspace(text_entry.get("1.0", "end-1c")) is True:
        text_entry.delete("1.0", END)
        return "break"
    text_display.configure(state="normal")
    text_display.insert(END, current_time()+" - "+user+": "+"\n"+entered_text+"\n")
    text_display.configure(state="disabled")
    s.sendall(entered_text.encode())
    text_entry.delete("1.0", END)
    return "break"


def message_input(window, out_q):
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        if text == prev_message:
            continue
        out_q.put(text)
        window.event_generate("<<MessageReceived>>")


def message_print(in_q):
    message = in_q.get()
    text_display.configure(state="normal"),
    text_display.insert(END, current_time() + " - " + "online" + ": " + "\n" + message + "\n"),
    text_display.configure(state="disabled")


def on_closing():
    print("closing")
    s.close()
    root.destroy()


text_display = tkinter.Text(canvas, bg="#E0E0E0")
text_entry = tkinter.Text(canvas)
text_entry.pack()
entry_button = tkinter.Button(canvas, text="Send", command=entry_button_click)
text_entry.bind('<Return>', lambda event:entry_button_click())
text_entry.bind('<Shift-Return>')
text_display.configure(state="disabled")
root.bind("<<MessageReceived>>", lambda e: message_print(q))

# Positioning
canvas.create_window(480, 580, width=960, height=40, window=text_entry)
canvas.create_window(980, 580, width=40, height=40, window=entry_button)
canvas.create_window(500, 280, width=1000, height=560, window=text_display)


h = threading.Thread(target=message_input, args=(root, q))
h.daemon = True
h.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
