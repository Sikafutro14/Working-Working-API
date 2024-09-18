import customtkinter as ctk

def create_label_entry(parent, label_text, row):
    label = ctk.CTkLabel(parent, text=label_text)
    label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
    entry = ctk.CTkEntry(parent)
    entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
    return entry