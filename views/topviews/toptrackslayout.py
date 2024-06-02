import customtkinter as ctk
import pygame


class BaseView(ctk.CTkFrame):
    """
    A base class for creating views using CustomTkinter and Pygame.

    This class provides a template for creating views with buttons to display short, medium, and long-term data.
    It also includes a mechanism to handle user input for setting data limits and updating the view accordingly.

    Attributes:
        sp (SpotifyUser): The Spotify user object for retrieving data.
        current_limit (int): The current limit for the number of items to display.
        previous_limit (int): The previous limit for the number of items to display.
        short_term_data (dict): Cached data for short-term items.
        medium_term_data (dict): Cached data for medium-term items.
        long_term_data (dict): Cached data for long-term items.
    """

    def __init__(self, parent, bg_color="#8AA7A9", spotify_user=None):
        """
        Initialize the BaseView.

        Parameters:
            parent (tkinter.Tk or tkinter.Frame): The parent widget.
            bg_color (str): The background color of the frame.
            spotify_user (SpotifyUser): The Spotify user object.
        """
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
        self.to_be_shown_label = ctk.CTkLabel(self, text=f'To be shown: {self.current_limit}', font=("Arial", 12))
        self.limit_entry = ctk.CTkEntry(self, width=100, font=("Arial", 12), placeholder_text="Enter limit")

        self.limit_entry.bind("<Return>", self.handle_enter)

        short_term_button.grid(row=0, column=1, pady=10, padx=10, sticky='e')
        medium_term_button.grid(row=0, column=2, pady=10, padx=10)
        long_term_button.grid(row=0, column=3, pady=10, padx=10)
        self.to_be_shown_label.grid(row=0, column=4, pady=10, padx=10)
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
        """
        Handle the Enter key event to update the data limit.

        Parameters:
            event (tkinter.Event): The event object.
        """
        limit = self.limit_entry.get()
        self.to_be_shown_label.configure(text=f'To be shown: {limit}')
        self.limit_entry.delete(0, 'end')
        if limit.isdigit():
            self.previous_limit = self.current_limit
            self.current_limit = int(limit)

    def add_table_headers(self):
        """
        Add headers to the table displaying data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def add_table_data(self, data):
        """
        Add data to the table.

        This method should be implemented by subclasses.

        Parameters:
            data (dict): Data to be displayed in the table.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def show_short_term(self):
        """
        Show the short-term data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def show_medium_term(self):
        """
        Show the medium-term data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def show_long_term(self):
        """
        Show the long-term data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def show_info(self, item_id):
        """
        Show detailed information for a selected item.

        This method should be implemented by subclasses.

        Parameters:
            item_id (str): The ID of the item to display information for.
        """
        raise NotImplementedError("Subclasses should implement this method")
