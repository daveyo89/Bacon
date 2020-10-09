import tkinter as tk
from tkinter import messagebox, ttk

from Bacon.Cypher import BaconSpider, DecodeBaconSpider


class Window:

    def __init__(self):
        self.master = tk.Tk()
        self._geom = '1426x400+100+0'
        self.container = ttk.Frame(self.master)
        self.canvas = tk.Canvas(self.container, width=400, height=400)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.secret_message = ""
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.scrollable_frame.bbox("all")
            )
        )
        pad = 3
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth() - pad, self.master.winfo_screenheight() - pad))

        self.master.bind('<Control-space>', self.toggle_geom)

        self.app_ui_buttons()
        self.secret_message_box()
        self.text_box()
        self.result_box()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.container.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", expand=False)

        self.master.title("BaconCypher")
        self.master.iconbitmap("icon.ico")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind('<Escape>', func=lambda e: self.master.destroy())
        self.master.bind('<Control-s>', func=lambda e: self.secret_message_box())
        self.master.mainloop()

    def app_ui_buttons(self):
        fr_buttons = tk.Frame(self.scrollable_frame, relief=tk.RAISED, bd=3)
        btn_load = tk.Button(fr_buttons, text="Load", command=self.get_input)
        btn_add_secret_message = tk.Button(fr_buttons, text="Secret Message", command=self.secret_message_box)

        setattr(self, 'checkCmd', tk.IntVar())
        self.checkCmd.set(0)

        btn_function = tk.Checkbutton(fr_buttons, variable=self.checkCmd, onvalue=1, offvalue=0, text="Decode")

        btn_load.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_function.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        btn_add_secret_message.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        fr_buttons.grid(row=0, column=0, sticky="ns")

    def hide(self):
        self.master.withdraw()

    def show(self):
        self.master.update()
        self.master.deiconify()

    def get_input(self):
        setattr(self, 'message', [])
        self.result_box.delete(1.0, tk.END)
        setattr(self, 'input', self.text_box.get("1.0", "end"))
        self.result_box.insert("1.0", self.translate())

    def translate(self):
        if not bool(self.checkCmd.get()):
            bs = BaconSpider(self.input, self.secret_message)
            bs.to_binary()
            bs.to_be_encoded()
            bs.make_it_upper()
            bs.encode_in_poem()
            return bs.encode_in_poem_result
        else:
            dbs = DecodeBaconSpider(self.input)
            dbs.get_code_words()
            dbs.get_letters()
            dbs.translate()
            return dbs.translate_result

    def secret_message_box(self):
        if hasattr(self, 'recipient'):
            self.recipient.destroy()

        def check():
            secret_message_input = self.add_secret_message.get()
            if secret_message_input:
                setattr(self, 'secret_message', secret_message_input)
                self.recipient.destroy()

        setattr(self, 'recipient', tk.Toplevel(width=100, height=100))
        self.recipient.wm_title("Secret message")

        setattr(self, 'add_secret_message', tk.Entry(self.recipient))
        recipient_label = tk.Label(self.recipient, text="Secret Message")

        self.add_secret_message.grid(row=0, column=1)
        recipient_label.grid(row=0, column=0)

        b = ttk.Button(self.recipient, text="Okay", command=check)
        b.grid(row=1, column=0)
        self.recipient.bind('<Enter>', func=lambda e: check())

    def text_box(self):
        setattr(self, 'text_box', tk.Text(self.scrollable_frame, relief=tk.RAISED, bd=3))
        self.text_box.grid(row=0, column=1, sticky="ewns")

    def result_box(self):
        setattr(self, 'result_box', tk.Text(self.scrollable_frame, state="normal", relief=tk.RAISED, bd=3))
        self.result_box.grid(row=0, column=2, sticky="ewns")

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom = geom

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()
