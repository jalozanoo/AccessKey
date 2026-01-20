# ui/gui.py

import tkinter as tk
from tkinter import messagebox, PhotoImage
from cryptography.fernet import InvalidToken

from core.crypto import CryptoManager
from core.vault import Vault
from core.models import Credential
from storage.filesystem import FileStorage
from utils.password_gen import generate_password
from utils.password_strength import evaluate_password_strength


class AccessKeyGUI:
    # ---------------- PARÁMETROS DE ESTILO ----------------
    BTN_COLOR = "#1e3a60"
    BTN_HOVER_DARK = "#3b5f91"
    BTN_FONT = ("Arial", 11, "bold")
    BG_WINDOW = "#e0e0e0"
    BG_LEFT = "#d9d9d9"
    BG_RIGHT = "#f0f0f0"
    LABEL_FONT_TITLE = ("Arial", 14, "bold")
    LABEL_FONT_NORMAL = ("Arial", 12)
    LABEL_FONT_ITALIC = ("Arial", 12, "italic")

    def __init__(self, root):
        self.root = root
        self.root.title("AccessKey")
        self.icon = PhotoImage(file="icons/acceskey.png")
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)
        self.center_window(600, 420)
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_WINDOW)
        self.login_attempts = 0

        # ---------------- STORAGE & VAULT ----------------
        self.storage = FileStorage()
        self.crypto = None
        self.salt = None
        self.vault = None

        # ---------------- MAIN FRAME ----------------
        self.main_frame = tk.Frame(self.root, bg=self.BG_WINDOW)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo
        self.left_frame = tk.Frame(self.main_frame, width=220, bg=self.BG_LEFT, bd=2, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(self.left_frame, text="Accesos", font=("Arial", 12, "bold"), bg=self.BG_LEFT).pack(pady=5)

        # Sub-frame para Listbox + Scrollbar
        list_frame = tk.Frame(self.left_frame, bg=self.BG_LEFT)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(list_frame, font=("Arial", 11), bg="white")
        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.show_view_access())

        # Botones debajo de la lista
        self.left_buttons = []
        btn_specs = [
            ("Nuevo acceso", self.show_new_access),
            ("Modificar acceso", self.show_modify_access),
            ("Cambiar clave maestra", self.show_change_master_password),
            ("Eliminar acceso", self.delete_access),
            ("Guardar y salir", self.save_and_exit)
        ]
        for text, cmd in btn_specs:
            btn = tk.Button(self.left_frame, text=text, width=20, command=cmd,
                            bg=self.BTN_COLOR, fg="white", font=self.BTN_FONT, relief=tk.RAISED)
            btn.pack(pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.BTN_HOVER_DARK))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.BTN_COLOR))
            btn.config(state="disabled")  # bloqueado hasta login/crear clave
            self.left_buttons.append(btn)

        # Panel derecho
        self.right_frame = tk.Frame(self.main_frame, bg=self.BG_RIGHT, bd=2, relief=tk.GROOVE)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Guardar al cerrar
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

        # ---------------- AUTH ----------------
        if not self.authenticate():
            self.root.destroy()
            return

        if self.vault:
            self.refresh_list()
            self.show_empty_panel()
            self._enable_left_buttons()

    # ---------------- CENTRAR VENTANA ----------------
    def center_window(self, width=600, height=420):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # ---------------- HABILITAR BOTONES ----------------
    def _enable_left_buttons(self):
        for btn in self.left_buttons:
            btn.config(state="normal")

    # ---------------- Toplevel personalizado ----------------
    def ask_master_password(self, prompt="Ingrese contraseña maestra:"):
        top = tk.Toplevel(self.root)
        top.title("Login")
        top.iconphoto(False, self.icon)
        top.resizable(False, False)
        top.grab_set()

        # Centrar ventana
        width, height = 350, 150
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        top.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(top, text=prompt, font=self.LABEL_FONT_NORMAL).pack(padx=20, pady=10)
        entry = tk.Entry(top, show="*", width=30)
        entry.pack(padx=20, pady=5)

        result = {"value": None}

        def ok():
            result["value"] = entry.get()
            top.destroy()

        def cancel():
            top.destroy()

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="OK", width=10, bg=self.BTN_COLOR, fg="white", command=ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", width=10, bg=self.BTN_COLOR, fg="white", command=cancel).pack(side=tk.RIGHT, padx=5)

        self.root.wait_window(top)
        return result["value"]

    # ---------------- AUTH ----------------
    def authenticate(self):
        loaded = self.storage.load()
        if loaded is None:
            self.show_setup_master_password()
            return True
        else:
            return self.show_login()

    def show_setup_master_password(self):
        self.clear_right_panel()

        tk.Label(
            self.right_frame,
            text="Crear contraseña maestra",
            font=self.LABEL_FONT_TITLE,
            bg=self.BG_RIGHT
        ).pack(pady=10)

        tk.Label(self.right_frame, text="Nueva contraseña:", bg=self.BG_RIGHT).pack(pady=2)
        password_entry = tk.Entry(self.right_frame, show="*", width=30)
        password_entry.pack(pady=2)

        strength_label = tk.Label(
            self.right_frame,
            text="Nivel de seguridad: Débil",
            font=self.LABEL_FONT_NORMAL,
            fg = "red",
            bg=self.BG_RIGHT
        )
        strength_label.pack(pady=4)

        def on_password_change(event=None):
            pw = password_entry.get()
            score, label, color = evaluate_password_strength(pw)
            strength_label.config(
                text=f"Nivel de seguridad: {label}",
                fg=color
            )

        password_entry.bind("<KeyRelease>", on_password_change)

        tk.Label(self.right_frame, text="Confirmar contraseña:", bg=self.BG_RIGHT).pack(pady=2)
        confirm_entry = tk.Entry(self.right_frame, show="*", width=30)
        confirm_entry.pack(pady=2)

        tk.Button(
            self.right_frame,
            text="Crear",
            width=15,
            bg=self.BTN_COLOR,
            fg="white",
            command=lambda: self._create_master(password_entry, confirm_entry)
        ).pack(pady=10)

    def _create_master(self, pw_entry, conf_entry):
        import os

        pw = pw_entry.get()
        conf = conf_entry.get()

        if not pw or pw != conf:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Verificar fuerza de la contraseña
        score, label, _ = evaluate_password_strength(pw)
        if score < 3:
            messagebox.showwarning(
                "Contraseña débil",
                "La contraseña maestra es demasiado débil.\n"
                "Use al menos:\n"
                "- 8 caracteres\n"
                "- Mayúsculas y minúsculas\n"
                "- Números y símbolos"
            )
            return

        # 1️⃣ Generar salt y crypto
        self.salt = os.urandom(16)
        self.crypto = CryptoManager(pw, self.salt)

        # 2️⃣ Crear vault vacío
        self.vault = Vault()

        # 3️⃣ Guardar inmediatamente el vault en archivo para que exista
        self.storage.save(self.salt, self.crypto.encrypt(self.vault.to_bytes()))

        # 4️⃣ Actualizar UI
        self.refresh_list()
        self.show_empty_panel()
        self._enable_left_buttons()


    def show_login(self):
        import time

        salt, encrypted = self.storage.load()

        while True:
            pw = self.ask_master_password("Ingrese contraseña maestra:")
            if pw is None:
                return False

            # Delay progresivo
            delay = min(2 ** self.login_attempts, 3)
            time.sleep(delay)

            try:
                self.crypto = CryptoManager(pw, salt)
                data = self.crypto.decrypt(encrypted)
                self.vault = Vault.from_bytes(data)
                self.salt = salt

                # Reset en éxito
                self.login_attempts = 0
                self._enable_left_buttons()
                return True

            except InvalidToken:
                self.login_attempts += 1
                messagebox.showerror(
                    "Error",
                    f"Contraseña incorrecta\nIntentos fallidos: {self.login_attempts}"
                )
    # ---------------- PANEL DINÁMICO ----------------
    def clear_right_panel(self):
        for w in self.right_frame.winfo_children():
            w.destroy()

    def show_empty_panel(self):
        self.clear_right_panel()
        tk.Label(self.right_frame, text="Seleccione una acción", font=self.LABEL_FONT_ITALIC,
                 bg=self.BG_RIGHT).pack(pady=20)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.vault.list_names():
            self.listbox.insert(tk.END, name)

    # ---------------- NUEVO ACCESO ----------------
    def show_new_access(self):
        self.clear_right_panel()
        tk.Label(self.right_frame, text="Nuevo acceso", font=self.LABEL_FONT_TITLE, bg=self.BG_RIGHT).pack(pady=10)
        tk.Label(self.right_frame, text="Nombre:", bg=self.BG_RIGHT).pack(anchor="w")
        name_entry = tk.Entry(self.right_frame, width=30)
        name_entry.pack(pady=2)
        tk.Label(self.right_frame, text="Usuario:", bg=self.BG_RIGHT).pack(anchor="w")
        user_entry = tk.Entry(self.right_frame, width=30)
        user_entry.pack(pady=2)
        tk.Label(self.right_frame, text="Correo:", bg=self.BG_RIGHT).pack(anchor="w")
        email_entry = tk.Entry(self.right_frame, width=30)
        email_entry.pack(pady=2)
        tk.Label(self.right_frame, text="Contraseña:", bg=self.BG_RIGHT).pack(anchor="w")
        pass_entry = tk.Entry(self.right_frame, show="*", width=30)
        pass_entry.pack(pady=2)

        show_var = tk.BooleanVar()
        tk.Checkbutton(self.right_frame, text="Mostrar contraseña", variable=show_var,
                       command=lambda: pass_entry.config(show="" if show_var.get() else "*"),
                       bg=self.BG_RIGHT).pack(pady=2)

        tk.Button(self.right_frame, text="Generar contraseña", bg=self.BTN_COLOR, fg="white",
                  command=lambda: [pass_entry.delete(0, tk.END),
                                   pass_entry.insert(0, generate_password())]).pack(pady=5)

        tk.Button(self.right_frame, text="Guardar", bg=self.BTN_COLOR, fg="white",
                  command=lambda: self._save_new_access(name_entry, user_entry, email_entry, pass_entry)).pack(pady=10)

    def _save_new_access(self, name_entry, user_entry, email_entry, pass_entry):
        name = name_entry.get()
        username = user_entry.get()
        correo = email_entry.get()
        password = pass_entry.get()
        if not name or self.vault.get(name):
            messagebox.showerror("Error", "Nombre inválido o ya existe")
            return
        self.vault.add(Credential(name, username, password, correo))
        self.refresh_list()
        self.show_view_access()

    # ---------------- VER ACCESO ----------------
    def show_view_access(self):
        sel = self.listbox.curselection()
        self.clear_right_panel()
        if not sel:
            tk.Label(self.right_frame, text="Seleccione un acceso", font=self.LABEL_FONT_ITALIC,
                    bg=self.BG_RIGHT).pack(pady=10)
            return

        name = self.listbox.get(sel[0])
        cred = self.vault.get(name)

        tk.Label(self.right_frame, text=f"Acceso: {name}", font=self.LABEL_FONT_TITLE, bg=self.BG_RIGHT).pack(pady=5)
        tk.Label(self.right_frame, text=f"Usuario: {cred.username}", font=self.LABEL_FONT_NORMAL, bg=self.BG_RIGHT).pack(pady=2)
        tk.Label(self.right_frame, text=f"Correo: {cred.correo}", font=self.LABEL_FONT_NORMAL, bg=self.BG_RIGHT).pack(pady=2)
        tk.Label(self.right_frame, text="Contraseña:", font=self.LABEL_FONT_NORMAL, bg=self.BG_RIGHT).pack(pady=2)

        pass_entry = tk.Entry(self.right_frame, show="*", width=30)
        pass_entry.insert(0, cred.password)
        pass_entry.config(state="readonly")
        pass_entry.pack(pady=2)

        # Mostrar contraseña
        show_var = tk.BooleanVar()
        tk.Checkbutton(self.right_frame, text="Mostrar contraseña", variable=show_var,
                    command=lambda: pass_entry.config(show="" if show_var.get() else "*"),
                    bg=self.BG_RIGHT).pack(pady=2)

        # Botón copiar al portapapeles
        tk.Button(self.right_frame, text="Copiar contraseña", bg=self.BTN_COLOR, fg="white",
                command=lambda: self._copy_to_clipboard(cred.password)).pack(pady=5)

    def _copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        # Limpieza automática a los 10 segundos
        self.root.after(10000, self.root.clipboard_clear)

        messagebox.showinfo("Copiado", "Contraseña copiada.")
        
    # ---------------- MODIFICAR ACCESO ----------------
    def show_modify_access(self):
        sel = self.listbox.curselection()
        self.clear_right_panel()
        if not sel:
            tk.Label(self.right_frame, text="Seleccione un acceso para modificar", bg=self.BG_RIGHT).pack()
            return
        name = self.listbox.get(sel[0])
        cred = self.vault.get(name)

        tk.Label(self.right_frame, text=f"Modificar acceso: {name}", font=self.LABEL_FONT_TITLE, bg=self.BG_RIGHT).pack(pady=5)
        tk.Label(self.right_frame, text="Usuario:", bg=self.BG_RIGHT).pack(anchor="w")
        user_entry = tk.Entry(self.right_frame, width=30)
        user_entry.insert(0, cred.username)
        user_entry.pack(pady=2)

        tk.Label(self.right_frame, text="Correo:", bg=self.BG_RIGHT).pack(anchor="w")
        email_entry = tk.Entry(self.right_frame, width=30)
        email_entry.insert(0, cred.correo)
        email_entry.pack(pady=2)

        tk.Label(self.right_frame, text="Contraseña:", bg=self.BG_RIGHT).pack(anchor="w")
        pass_entry = tk.Entry(self.right_frame, show="*", width=30)
        pass_entry.insert(0, cred.password)
        pass_entry.pack(pady=2)

        show_var = tk.BooleanVar()
        tk.Checkbutton(self.right_frame, text="Mostrar contraseña", variable=show_var,
                       command=lambda: pass_entry.config(show="" if show_var.get() else "*"),
                       bg=self.BG_RIGHT).pack(pady=2)

        tk.Button(self.right_frame, text="Generar nueva contraseña", bg=self.BTN_COLOR, fg="white",
                  command=lambda: [pass_entry.delete(0, tk.END),
                                   pass_entry.insert(0, generate_password())]).pack(pady=5)

        tk.Button(self.right_frame, text="Guardar cambios", bg=self.BTN_COLOR, fg="white",
                  command=lambda: self._save_changes(cred, user_entry, email_entry, pass_entry)).pack(pady=10)

    def _save_changes(self, cred, user_entry, email_entry, pass_entry):
        new_user = user_entry.get()
        new_pass = pass_entry.get()
        new_correo = email_entry.get()
        if not new_pass:
            messagebox.showerror("Error", "La contraseña no puede estar vacía")
            return
        cred.username = new_user
        cred.password = new_pass
        cred.correo = new_correo
        self.refresh_list()
        self.show_view_access()

    # ---------------- CAMBIAR CLAVE MAESTRA ----------------
    def show_change_master_password(self):
        self.clear_right_panel()

        tk.Label(
            self.right_frame,
            text="Cambiar contraseña maestra",
            font=self.LABEL_FONT_TITLE,
            bg=self.BG_RIGHT
        ).pack(pady=10)

        tk.Label(self.right_frame, text="Contraseña actual:", bg=self.BG_RIGHT).pack(pady=2)
        current_entry = tk.Entry(self.right_frame, show="*", width=30)
        current_entry.pack(pady=2)

        tk.Label(self.right_frame, text="Nueva contraseña:", bg=self.BG_RIGHT).pack(pady=2)
        new_entry = tk.Entry(self.right_frame, show="*", width=30)
        new_entry.pack(pady=2)

        strength_label = tk.Label(
            self.right_frame,
            text="Nivel de seguridad: Débil",
            font=self.LABEL_FONT_NORMAL,
            fg="red",
            bg=self.BG_RIGHT
        )
        strength_label.pack(pady=4)

        def on_password_change(event=None):
            score, label, color = evaluate_password_strength(new_entry.get())
            strength_label.config(text=f"Nivel de seguridad: {label}", fg=color)

        new_entry.bind("<KeyRelease>", on_password_change)

        tk.Label(self.right_frame, text="Confirmar nueva contraseña:", bg=self.BG_RIGHT).pack(pady=2)
        confirm_entry = tk.Entry(self.right_frame, show="*", width=30)
        confirm_entry.pack(pady=2)

        tk.Button(
            self.right_frame,
            text="Cambiar",
            width=15,
            bg=self.BTN_COLOR,
            fg="white",
            command=lambda: self._change_master_password(
                current_entry, new_entry, confirm_entry
            )
        ).pack(pady=10)

    def _change_master_password(self, current_entry, new_entry, confirm_entry):
        import os

        current_pw = current_entry.get()
        new_pw = new_entry.get()
        confirm = confirm_entry.get()

        if not current_pw or not new_pw:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if new_pw != confirm:
            messagebox.showerror("Error", "Las contraseñas nuevas no coinciden")
            return

        score, _, _ = evaluate_password_strength(new_pw)
        if score < 3:
            messagebox.showwarning(
                "Contraseña débil",
                "La nueva contraseña maestra no es suficientemente segura"
            )
            return

        # 1. Validar clave actual
        try:
            salt, encrypted = self.storage.load()
            old_crypto = CryptoManager(current_pw, salt)
            decrypted_data = old_crypto.decrypt(encrypted)
        except Exception:
            messagebox.showerror("Error", "Contraseña actual incorrecta")
            return

        # 2. Crear nueva clave y salt
        new_salt = os.urandom(16)
        new_crypto = CryptoManager(new_pw, new_salt)

        # 3. Re-encriptar los mismos bytes descifrados
        new_encrypted = new_crypto.encrypt(decrypted_data)

        # 4. Guardar vault y actualizar estado
        self.crypto = new_crypto
        self.salt = new_salt
        # 🔹 No crear Vault.from_bytes() de nuevo, usar la existente
        self.storage.save(new_salt, new_encrypted)

        messagebox.showinfo("Éxito", "Contraseña maestra cambiada correctamente")
        self.show_empty_panel()


    # ---------------- ELIMINAR ACCESO ----------------
    def delete_access(self):
        sel = self.listbox.curselection()
        self.clear_right_panel()
        if not sel:
            tk.Label(self.right_frame, text="Seleccione un acceso para eliminar", bg=self.BG_RIGHT).pack()
            return
        name = self.listbox.get(sel[0])
        pw = self.ask_master_password(f"Ingrese clave maestra.")
        if pw is None:
            return
        try:
            salt, encrypted = self.storage.load()
            CryptoManager(pw, salt).decrypt(encrypted)
        except Exception:
            messagebox.showerror("Error", "Clave maestra incorrecta")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar acceso '{name}'?"):
            del self.vault._items[name]
            self.refresh_list()
            self.show_empty_panel()

    # ---------------- GUARDAR Y SALIR ----------------
    def save_and_exit(self):
        if self.crypto and self.vault:  # solo guardar si existen
            self.storage.save(self.salt, self.crypto.encrypt(self.vault.to_bytes()))
        self.root.destroy()