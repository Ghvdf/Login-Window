from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import string

conn = sqlite3.connect('Login.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS user (name TEXT NOT NULL, password TEXT NOT NULL)')

root = Tk()
root.title('Login')
root.geometry('400x250')
root.resizable(False, False)

entry_Name = Entry(root, justify='left', width=30)
entry_Password = Entry(root, justify='left', show='*', width=30)


def insert_data(name, password):
    conn = sqlite3.connect('Login.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user WHERE name = ? AND password = ?', (name, password))
    user = cur.fetchone()
    
    if user:
        messagebox.showinfo("Login", "Вы вошли")
    else:
        cur.execute('INSERT INTO user (name, password) VALUES (?, ?)', (name, password))
        messagebox.showinfo("Registration", "Регистрация успешна")
    
    conn.commit()
    conn.close()

def Sumbit():
    name_text = entry_Name.get().strip()
    password_text = entry_Password.get().strip()
    insert_data(name_text, password_text)
    entry_Name.delete(0, END)
    entry_Password.delete(0, END)

def Show_db():
    conn = sqlite3.connect('Login.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user')
    users = cur.fetchall()
    for user in users:
        print(user)
    conn.close()

def Show_Password():
    if entry_Password.cget('show') == '*':
        entry_Password.config(show='')
        button_show_password.config(text='Скрыть пароль')
    else:
        entry_Password.config(show='*')
        button_show_password.config(text='Показать пароль')

def Rand_Password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(15))
    entry_Password.delete(0, END)
    return entry_Password.insert(0, password)

button = Button(root, text='Подтвердить', command=Sumbit, width=25, state='disabled')
button_generate_password = Button(root, text='Сгенерировать пароль', command=Rand_Password, width=25)
button_show_password = Button(root, text='Показать пароль', command=Show_Password, width=25)
button_show_db = Button(root, text='База данных', command=Show_db, width=25)

entry_Name.pack(pady=10)
entry_Password.pack(pady=3)
button.pack(pady=3)
button_show_password.pack(pady=3)
button_generate_password.pack(pady=3)
button_show_db.pack(pady=3)

def update_button_state():
    name_text = entry_Name.get().strip()
    password_text = entry_Password.get().strip()
    if len(name_text) > 0 and len(password_text) >= 9:
        button['state'] = 'normal'
    else:
        button['state'] = 'disabled'

entry_Name_var = StringVar()
entry_Password_var = StringVar()

entry_Name.config(textvariable=entry_Name_var)
entry_Password.config(textvariable=entry_Password_var)

entry_Name_var.trace_add('write', lambda *args: update_button_state())
entry_Password_var.trace_add('write', lambda *args: update_button_state())

conn.commit()
conn.close()

mainloop()