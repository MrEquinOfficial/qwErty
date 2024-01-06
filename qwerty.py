import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import re

class ChatAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("qwErty Chat Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#282c34')

        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, fg='white', bg='black', font=('Helvetica', 12), state=tk.DISABLED)
        self.chat_history.pack(pady=10)

        self.entry = tk.Entry(root, fg='black', bg='white', font=('Helvetica', 12))
        self.entry.pack(pady=10, padx=10, fill=tk.X)  # X ekseni boyunca genişlet
        self.entry.bind("<Return>", self.show_response)  # Enter tuşuna basıldığında show_response fonksiyonunu çağır

        self.send_button = tk.Button(root, text="Send", command=self.show_response, fg='black', bg='#61dafb', font=('Helvetica', 12))
        self.send_button.pack()

        self.response_text = tk.StringVar()
        self.response_label = tk.Label(root, textvariable=self.response_text, fg='white', bg='#282c34', font=('Helvetica', 12), wraplength=700)
        self.response_label.pack()

        self.greet_user()

    def calculate_expression(self, expression):
        try:
            # İfadeyi değerlendirirken "x" yerine "*" kullan
            expression = expression.replace("x", "*")
            result = eval(expression)
            return str(result)
        except Exception as e:
            return "Error: " + str(e)

    def greet_user(self):
        greeting = "Hello! I am qwErty, your virtual assistant. How can I assist you today?"
        self.add_to_chat_history(greeting)

    def add_to_chat_history(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state=tk.DISABLED)

    def show_response(self, event=None):
        user_input = self.entry.get().strip().lower()

        if user_input and not user_input.isspace():
            # Eğer kullanıcıdan alınan giriş boşluktan ibaret değilse devam et
            if "bye" in user_input or "goodbye" in user_input or "exit" in user_input or "quit" in user_input:
                self.ask_exit_confirmation()
            elif "calculate" in user_input or "calc" in user_input:
                # Kullanıcılar "x" yerine "*" yazarak işlem yapabilir
                user_input = user_input.replace("x", "*")
                match = re.search(r'\d+(\s*[+\-*/]\s*\d+)+', user_input)
                if match:
                    expression = match.group()
                    expression = expression.replace(" ", "")
                    result = self.calculate_expression(expression)
                    response = f"The result of {expression} is {result}."
                else:
                    response = "Invalid calculation format. Please enter a valid expression."
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)
            elif "hi" in user_input or "hello" in user_input:
                response = "Hi! How can I help you?"
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)
            elif "thanks" in user_input or "thank you" in user_input or "thank" in user_input:
                response = "You're welcome! If you have any more questions, feel free to ask."
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)
            elif "help me" in user_input:
                response = "Of course! I'm here to help. What do you need assistance with?"
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)
            elif "i don't need you" in user_input or "i dont need you" in user_input:
                response = "I understand. If you change your mind or have any questions later, feel free to ask. Have a great day!"
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)
            else:
                response = "I'm sorry, I didn't understand that question. Please ask something else."
                self.add_to_chat_history(user_input)
                self.add_to_chat_history(response)

            self.entry.delete(0, tk.END)

    def ask_exit_confirmation(self):
        # Onay ekranını özelleştir
        confirmation = messagebox.askyesno("Exit", "Are you sure you want to exit?", icon=messagebox.WARNING)
        if confirmation:
            response = "Goodbye! Have a great day!"
            self.add_to_chat_history(response)
            self.root.after(0, self.close_window)  # Pencereyi hemen kapat

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatAssistant(root)
    root.protocol("WM_DELETE_WINDOW", app.ask_exit_confirmation)  # Çıkış tuşuna basıldığında ask_exit_confirmation fonksiyonunu çağır
    root.mainloop()
