from customtkinter import *
import socket
import threading

HOST = '7.tcp.eu.ngrok.io'#
PORT = 15848#

class MainWindow(CTk):
    def __init__(self):#self  - screen
        super().__init__()
        self.geometry('600x450')
        self.minsize(600, 450)
        set_appearance_mode('system')

        #menu  - ui
        self.menu = CTkFrame(self, width = 200, height= 400)
        self.label_userName = CTkLabel(self.menu,text='User Name',
                                  font=('Times New Roman', 18, 'normal'),
                                  anchor='w',
                                  width = 190)
        self.entry_userName = CTkEntry(self.menu, placeholder_text='...',width = 190)
        self.btn_name = CTkButton(self.menu,text='Change name', 
                                  font=('Times New Roman',16,'normal'),
                                  width=190,
                                  command=self.change_name)
        self.theme = CTkOptionMenu(self.menu, values=['system', 'dark','light'], 
                                   width = 190, 
                                   font=('Times New Roman',16,'normal'),
                                   dropdown_font=('Times New Roman', 14),
                                   command=self.change_theme)
        #menu - pos
        self.label_userName.pack(pady = (150, 10), padx = 5)
        self.entry_userName.pack(padx = 5)
        self.btn_name.pack(padx=5,pady=(5,0))
        self.theme.pack(pady=(50,0), padx=5)
        #
        self.menu.place(x=0, y =0)
        self.menu.pack_propagate(False)
        #
        self.menu.configure(width=0)
        #chat ui
        self.btn_menu = CTkButton(self, text='☰', width = 30, height = 30,
                                  command=self.change_state)
        self.chat = CTkTextbox(self,state="disable", fg_color='white')
        self.message = CTkEntry(self, placeholder_text='щось пиши...')
        self.send_message = CTkButton(self, text='▶', width = 50, height =30,
                                      command=self.send_message_)
        #chat pos
        self.send_message.place(x = 545, y = 365)
        self.btn_menu.place(x = 5, y = 5)
        self.chat.place(x = 5, y = 40)
        self.message.place(x = 5, y = 365)
        #burger_menu
        self.max_size = 200
        self.speed = 20
        self.menu_state = False
        self.size_menu = 0 
        #
        self.user_name = '007'
        #client
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((
                HOST, PORT
            ))
            hello = f'TEXT@{self.user_name}@[SYSTEM] {self.user_name} приєднався(лась) до чату!\n'
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except:
            self.add_message('Зв\'язок з сервером втрачено')


        self.adaptive_ui()

    def add_message(self, text):
        self.chat.configure(state='normal')
        self.chat.insert(END, text + '\n')# \n - ENTER
        self.chat.configure(state='disable')

    def send_message_(self):
        message = self.message.get()
        if message:
            self.add_message(f'{self.user_name}: {message}')#можна буде закоментувати
            data = f'TEXT@{self.user_name}@{message}\n'
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message.delete(0, 'end')

    def recv_message(self):
        buffer = ''
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split('@',3)
        if parts[0] == 'TEXT':
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f'{author}: {message}')
        else:
            self.add_message(line)

    def change_theme(self, value):
        set_appearance_mode(value)

    def change_name(self):
        name = self.entry_userName.get()
        if name:
            self.user_name = name
            self.entry_userName.delete(0, 'end')
            print(self.user_name)

    def show_menu(self):
        if self.size_menu <= self.max_size:
            if self.size_menu > 30:
                self.btn_menu.configure(text='MENU ☰')
            self.size_menu += self.speed
            self.btn_menu.configure(width = self.size_menu - 10)
            self.menu.configure(width = self.size_menu)
        if self.menu_state:
            self.after(20, self.show_menu)
    
    def hide_menu(self):
        if self.size_menu > 0:
            if self.size_menu <30:
                self.btn_menu.configure(text='☰')
                self.btn_menu.configure(width=30)
            else:
                self.btn_menu.configure(width=self.size_menu)
            self.size_menu -= self.speed
            self.menu.configure(width = self.size_menu)
        if not self.menu_state:
            self.after(20, self.hide_menu)

    def change_state(self):
        if self.menu_state:
            self.menu_state = False
            self.hide_menu()
            
        else:
            self.menu_state = True
            self.show_menu()
            
    def adaptive_ui(self):
        k = 1.25
        w_w = self.winfo_width() / k
        w_h = self.winfo_height() / k
        btn_w = w_w / 12
        btn_h = w_h / 13.3
        #size
        self.send_message.configure(width = btn_w, height = btn_h)
        self.menu.configure(height = w_h)
        self.chat.configure(width = w_w - 10 - self.size_menu,
                            height = w_h - btn_h - 20 - 30)
        self.message.configure(width = w_w - btn_w - 10 - self.size_menu, height = btn_h)
        #place
        self.send_message.place(x = w_w - btn_w, y = w_h - btn_h)
        self.message.place(y = w_h - btn_h, x = self.size_menu + 5)
        self.chat.place(x = self.size_menu + 5)
        self.after(50, self.adaptive_ui)


app = MainWindow()
app.mainloop()