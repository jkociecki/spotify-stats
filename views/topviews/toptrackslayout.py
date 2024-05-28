import customtkinter as ctk
import pygame


class BaseView(ctk.CTkFrame):
    def __init__(self, parent, bg_color="#8AA7A9", spotify_user=None):
        super().__init__(parent, bg_color=bg_color)
        pygame.init()
        self.sp = spotify_user
        self.current_limit = 10
        self.previous_limit = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(1, weight=1)

        short_term_button = ctk.CTkButton(self, text="Short Term", command=self.show_short_term)
        medium_term_button = ctk.CTkButton(self, text="Medium Term", command=self.show_medium_term)
        long_term_button = ctk.CTkButton(self, text="Long Term", command=self.show_long_term)
        self.limit_entry = ctk.CTkEntry(self, width=100, font=("Arial", 12), placeholder_text="Enter limit")

        self.limit_entry.bind("<Return>", self.handle_enter)

        short_term_button.grid(row=0, column=1, pady=10, padx=10, sticky='e')
        medium_term_button.grid(row=0, column=2, pady=10, padx=10)
        long_term_button.grid(row=0, column=3, pady=10, padx=10)
        self.limit_entry.grid(row=0, column=4, pady=10, padx=10, sticky="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)
        self.scrollable_frame.grid_columnconfigure(3, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        self.add_table_headers()

        self.short_term_data = {}
        self.medium_term_data = {}
        self.long_term_data = {}

    def handle_enter(self, event):
        limit = self.limit_entry.get()
        self.limit_entry.delete(0, 'end')
        if limit.isdigit():
            self.previous_limit = self.current_limit
            self.current_limit = int(limit)

    def add_table_headers(self):
        raise NotImplementedError("Subclasses should implement this method")

    def add_table_data(self, data):
        raise NotImplementedError("Subclasses should implement this method")

    def show_short_term(self):
        raise NotImplementedError("Subclasses should implement this method")

    def show_medium_term(self):
        raise NotImplementedError("Subclasses should implement this method")

    def show_long_term(self):
        raise NotImplementedError("Subclasses should implement this method")

    def show_info(self, item_id):
        raise NotImplementedError("Subclasses should implement this method")