import customtkinter as ctk


def show_pop_up_window(view: ctk.CTk, message: str, title: str):
    playlist_added_window = ctk.CTkToplevel(view)
    playlist_added_window.title(title)
    playlist_added_label = ctk.CTkLabel(playlist_added_window, text=message)
    playlist_added_label.pack(padx=10, pady=10)
    ok_button = ctk.CTkButton(playlist_added_window, text="OK", command=playlist_added_window.destroy)
    ok_button.pack(pady=10)
    playlist_added_window.grab_set()
    playlist_added_window.wait_window()
    playlist_added_window.destroy()