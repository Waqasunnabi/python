import tkinter as tk

# Define the main window style
MAIN_WINDOW_STYLE = {
    "bg": "#353535",
}

# Define the frame style
FRAME_STYLE = {
    "bg": "#353535",
    "padx": 10,
    "pady": 10,
}

# Define the label style
LABEL_STYLE = {
    "bg": "#353535",
    "font": ("Arial", 12,"bold"),
    "fg": "white",  # Set font color to white
}

# Define the text widget style
TEXT_WIDGET_STYLE = {
    "height": 9,
    "wrap": tk.WORD,
    "font": ("Arial", 12),
    "borderwidth": 2,
    "relief": tk.GROOVE,
    "bg": "#353535",  # Set background color to #353535
    "fg": "white",  # Set font color to white
}

# Define the scrollbar style
SCROLLBAR_STYLE = {
    "bg": "#353535",
}

# Define the button style
BUTTON_STYLE = {
    "font": ("Arial", 12,"bold"),
    "bg": "black",  # Set button color to black
    "fg": "white",  # Set font color to white
    "padx": 20,
    "pady": 10,
    "borderwidth": 1,
}

def convert():
    # Get the input text from the input_text widget
    input_string = input_text.get("1.0", tk.END).strip()

    # Get the options
    delimiter = delimiter_entry.get()
    add_quotes = add_quotes_var.get()
    add_double_slash = add_double_slash_var.get()

    # Convert the input string to a list of items
    if add_quotes:
        items = [f'"{x}"' for x in input_string.split("\n")]
    elif add_double_slash:
        items = [f"'{x}'" for x in input_string.split("\n")]
    else:
        items = [x for x in input_string.split("\n")]

    # Generate the output string
    output_string = delimiter.join(items)

    # Insert the result string into the output_text widget
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output_string)
    output_text.config(state=tk.DISABLED)


# Create the main window
Comma_window = tk.Tk()
Comma_window.title("Comma Separated Value Editor")
Comma_window.geometry("450x600")
Comma_window.configure(**MAIN_WINDOW_STYLE)


# Create a frame for the input text widget and label
input_frame = tk.Frame(Comma_window, **FRAME_STYLE)
input_frame.pack(fill=tk.BOTH, expand=True)

# Add a label for the input text widget
input_label = tk.Label(input_frame, text="Input Text:", **LABEL_STYLE)
input_label.pack(side=tk.TOP, padx=10, pady=10)

# Add the input text widget and scrollbar
input_scrollbar = tk.Scrollbar(input_frame, **SCROLLBAR_STYLE)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
input_text = tk.Text(input_frame, **TEXT_WIDGET_STYLE, yscrollcommand=input_scrollbar.set)
input_text.pack(fill=tk.BOTH, expand=True)
input_scrollbar.config(command=input_text.yview)

# Create a frame for the options
options_frame = tk.Frame(Comma_window, **FRAME_STYLE)
options_frame.pack(fill=tk.X)

# Add the delimiter option
delimiter_label = tk.Label(options_frame, text="Delimiter:", font=("Arial", 12,"bold"),bg="#353535",foreground="white")
delimiter_label.pack(side=tk.LEFT, padx=2, pady=2)
delimiter_entry = tk.Entry(options_frame, font=("Arial", 12,"bold"), width=1,foreground="white")
delimiter_entry.pack(side=tk.LEFT, padx=2, pady=2)
delimiter_entry.insert(0, ",")


# Add the add quotes option
add_quotes_var = tk.BooleanVar()
add_quotes_check = tk.Checkbutton(options_frame, text="Add quotes", font=("Arial", 12,"bold"), variable=add_quotes_var,bg="#353535",foreground="white")
add_quotes_check.pack(side=tk.LEFT, padx=2, pady=2)

# Add the add double slash option
add_double_slash_var = tk.BooleanVar()
add_double_slash_check = tk.Checkbutton(options_frame, text="Add double slash", font=("Arial", 12,"bold"), variable=add_double_slash_var,bg="#353535",foreground="white")
add_double_slash_check.pack(side=tk.LEFT, padx=2, pady=2)

options_frame.configure(width=450)

# Create a frame for the output text widget and label
output_frame = tk.Frame(Comma_window, padx=10, pady=10,bg="#353535")
output_frame.pack(fill=tk.BOTH, expand=True)

# Set the width of the output frame
output_frame.configure(width=450)

# Add a label for the output text widget
output_label = tk.Label(output_frame, text="Output Text:", foreground="white",font= ("Arial", 12,"bold"),bg="#353535")
output_label.pack(side=tk.TOP, padx=10, pady=10)

# Add the output text widget and scrollbar
output_scrollbar = tk.Scrollbar(output_frame,**SCROLLBAR_STYLE)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text = tk.Text(output_frame, height=9, wrap=tk.WORD, font=("Arial", 12),background="#353535", borderwidth=2, relief=tk.GROOVE, state=tk.DISABLED, yscrollcommand=output_scrollbar.set)
output_text.pack(fill=tk.BOTH, expand=True)
output_scrollbar.config(command=output_text.yview)

# Create a frame for the button
button_frame = tk.Frame(Comma_window,bg="#353535")
button_frame.pack(fill=tk.X, pady=10)

# Add the button
button = tk.Button(button_frame, text="Convert", foreground="White", font=("Arial", 12, "bold"), background="Black", padx=20, pady=10, borderwidth=0,command=convert)
button.pack(fill=tk.X, padx=10, pady=10)

# Allow the window to be resized
Comma_window.resizable(False, False)

# Run the main loop
Comma_window.mainloop()

