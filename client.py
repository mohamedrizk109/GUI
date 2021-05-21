import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog



host = '127.0.0.1'
port = 9090


class client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring(
            "Nickname", "Please Choose a nickname", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):

        self.win = tkinter.Tk
        self.win.configure(self,bg='lightgray')

        self.chat_label = tkinter.Label(self.win, text="chat:", bg='lightgray')
        self.chat_label.config(font=("Arial", 16))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)

        # can't change the program content or text area
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(
            self.win, text="message:", bg='lightgray')
        self.msg_label.config(font=("Arial", 16))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(
            self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 16))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        # from starting to ending
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"
        # or get the whole text
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
        # this if we wanna delete the whole text from textbox

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def recieve(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        # the message will be append untill the end here
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')  # to scroll down
                        self.text_area.config(state='diabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")  # for any other Error
                self.sock.close()
                break


client = client(host, port)
