import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from config.constant import IMAGE_FILE_PATH, ENV_FILE_PATH



class InstallatorWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.root = UserInterface(self.window)

    def run_app(self):
        self.root.setup_ui()
        self.window.mainloop()


class UserInterface:
    def __init__(self, root, title='Prosta aplikacja'):
        self.root = root
        self.root.title(title)
        self.label = None
        self.button = None
        self.image = None
        self.api_field = None

    def setup_ui(self):
        # Set constant parameter for window
        self.constant_window()
        # Add first view

        # Add image to installer
        self.add_label_image(root=self.root, image_path=self.add_image(IMAGE_FILE_PATH))

        # Add welcome label
        self.add_label_text(root=self.root, side='top', pady=20, text='Witaj w instalatorze prostej aplikacji. \n'
                                                      'Dziękuje za poświęcony dla mnie czas. \n'
                                                      'Postępuj według instrukcji poniżej.')
        # Add information label
        self.add_label_text(root=self.root, side='top', pady=20, text='Przygotuj sobie twoj klucz API do OpenAI, \n'
                                                          'i wpisz go w pole poniżej aby zapisać zmienną '
                                                                      'środowiskową.')

        # Add title label for field
        self.add_label_text(root=self.root, side='top', pady=20, text='Możesz użyć Ctrl+V aby wkleić\n'
                                                                      'lub jeśli ci sie chce to możesz przepisywać,'
                                                                      'powodzenia.')

        # Add field do get API key
        self.api_field = self.add_text_field(root=self.root, side='top', pady=20)

        # Add button "Instaluj"
        self.add_button(root=self.root, side='right', name='Wgraj', command=self.on_click_install)

        # Add button "Anuluj"
        self.add_button(root=self.root, side='right', name='Anuluj', command=self.on_click_cancel)

        # Add button command main.py
        self.add_button(root=self.root, side='right', name='Uruchom', command=self.on_click_command)

    def constant_window(self):
        self.root.geometry('600x400')
        self.root.resizable(False, False)

    def add_label_text(self, root=None, padx=0, pady=0, side='left', text=None):
        _label = tk.Label(root, text=text)
        _label.pack(side=side, padx=padx, pady=pady)
        return _label

    def add_label_image(self, root=None, padx=0, pady=0, side='left', image_path=None):
        _label = tk.Label(root, image=image_path)
        _label.pack(side=side, padx=padx, pady=pady)
        _label.image = image_path
        return _label

    def add_button(self, root=None, name=None, command=None, side='left', padx=0, pady=0):
        _button = tk.Button(root, text=name, command=command)
        _button.pack(side=side, padx=padx, pady=pady)
        return _button

    def on_click_install(self):
        _api_key = self.api_field.get()

        if _api_key:
            with open(ENV_FILE_PATH, 'w') as env_file:
                _api_key_write_valid = env_file.write(f'OPENAI_API_KEY={_api_key}')
                if _api_key_write_valid:
                    action = messagebox.showinfo(title='Sukces',
                                    message='Klucz został zainstalowany w pliku .env')

    def on_click_cancel(self):
        self.root.quit()

    def on_click_command(self):
        """Uruchamia główny skrypt main.py we wirtualnym środowisku"""
        python_path = os.path.join('.venv', "Scripts", "python") if os.name == "nt" else os.path.join('.venv', "bin",
                                                                                                      "python")
        print(f"Uruchamianie skryptu {'main.py'} w wirtualnym środowisku...")
        messagebox.showinfo(title='Ładowanie',
                            message='Naciśnij Ok, aby zatwierdzić.')
        subprocess.check_call([python_path, 'main.py'])
        messagebox.showinfo(title='Zakończono',
                            message='Proces został zakończony.')

    def add_text_field(self, root, side='left', padx=0, pady=0):
        _field = tk.Entry(root)
        _field.pack(side=side, padx=padx, pady=pady)
        return _field

    @classmethod
    def add_image(cls, image_path):
        try:
            # Otwieramy obrazek za pomocą Pillow
            image = Image.open(image_path)
            tk_image = ImageTk.PhotoImage(image)
            return tk_image
        except Exception as e:
            print(f"Błąd podczas otwierania obrazu: {e}")
            return None


if __name__ == '__main__':
    app = InstallatorWindow()
    app.run_app()


