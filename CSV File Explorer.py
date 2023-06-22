import glob, os, threading, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk


animation = ["  ◜   ", "  ◝   ", "  ◞   ", "  ◟   "]
animation_index = 0
filesname = ["0"]


def update_dropdown_values(typed=""):
    all_files = glob.glob(getpath() + "/*.csv")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:  # type: ignore
        column_names = executor.map(get_column_names, all_files)

    unique_column_names = set()
    for columns in column_names:
        unique_column_names.update(columns)

    if typed == "":
        drop["values"] = list(unique_column_names)
    else:
        drop["values"] = [x for x in unique_column_names if typed.lower() in x.lower()]

    # If "Select Column Name" is in the values, remove it
    if "Select Column Name" in drop["values"]:
        drop["values"] = [x for x in drop["values"] if x != "Select Column Name"]

    # If the type area is blank, add "Select Column Name" back to the values
    if drop.get() == "":
        drop["values"] = list(unique_column_names) + ["Select Column Name"]


# ----------------------------------------------------------------------------------------------


# Remove "Select Column Name" from the dropdown when clicked
def on_dropdown_click(event):
    if "Select Column Name" in drop["values"]:
        drop["values"] = [x for x in drop["values"] if x != "Select Column Name"]


# ----------------------------------------------------------------------------------------------


# Filter the dropdown options based on user input
def on_dropdown_key_release(event):
    typed = drop.get()
    if typed == "":
        update_dropdown_values()
    else:
        if "Select Column Name" in drop["values"] and typed != "":
            drop["values"] = [x for x in drop["values"] if x != "Select Column Name"]
        update_dropdown_values(typed)
    # Open the dropdown menu while typing and keep the focus on the typing area
    drop.focus_set()


# ----------------------------------------------------------------------------------------------


# error handler
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            messagebox.showerror(
                "Error", "The specified file or folder could not be found."
            )
        except UnicodeDecodeError:
            messagebox.showerror(
                "Error",
                "The specified file cannot be read. Please ensure that the encoding is correct.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return None

    return wrapper


# ----------------------------------------------------------------------------------------------


def start_columnname_thread():
    threading.Thread(target=columnname).start()


# ----------------------------------------------------------------------------------------------


def start_findvalue_thread():
    threading.Thread(target=findvalue).start()


# ----------------------------------------------------------------------------------------------


def browsepath():
    folder_path = filedialog.askdirectory()
    if validate_folder_path(folder_path):
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)
        filename1 = folder_path.split("/").pop()
        filesname.insert(0, filename1)


# ----------------------------------------------------------------------------------------------


def animationLoadingRefresh():
    if loading:
        global animation_index
        animation_index = (animation_index + 1) % len(animation)
        refresh_button.config(text=animation[animation_index])
        csv_window.after(100, animationLoadingRefresh)
    else:
        refresh_button.config(text="Refresh", state=tk.NORMAL)


# ----------------------------------------------------------------------------------------------


def animationLoadingRun():
    if loading:
        global animation_index
        animation_index = (animation_index + 1) % len(animation)
        run_button.config(text=animation[animation_index])
        csv_window.after(100, animationLoadingRun)
    else:
        run_button.config(text="Run", state=tk.NORMAL)


# ----------------------------------------------------------------------------------------------


def confirm():
    answer = messagebox.askyesno(
        title="confirmation", message="Do you want to open the file location?"
    )
    if answer:
        path = os.path.realpath(os.getcwd())
        os.startfile(path)


# ----------------------------------------------------------------------------------------------


@handle_errors
def findvalue():
    global loading
    loading = True

    loading_thread = threading.Thread(target=animationLoadingRun)
    loading_thread.start()

    if var.get() == "Select Column Name":
        messagebox.showinfo("Warning", "No data loaded. Please refresh the file list.")
    else:
        find = text_area.get("1.0", tk.END)
        line = find.splitlines()
        lines = []

        for i in line:
            try:
                c = int(i)
                lines.append(c)
            except ValueError:
                c = i
                lines.append(c)

        print(lines)
        all_files = glob.glob(getpath() + "/*.csv")
        li = []

        total_loops = len(all_files) + len(lines)
        progress_bar.config(maximum=total_loops)

        total_execution_time = 0

        for idx, filename in enumerate(all_files):
            if stop_search.get():
                break
            start_time = time.time()
            df = pd.read_csv(
                filename,
                index_col=None,
                header=0,
                on_bad_lines="skip",
                low_memory=False,
            )
            if var.get() not in df.columns:
                messagebox.showerror(
                    "Error",
                    f"The selected column '{var.get()}' does not exist in the file '{filename}'. Skipping this file.",
                )
                continue
            li.append(df)

            progress_var.set(idx + 1)
            progress_bar_per.config(
                text="{}%".format(int(100 * progress_var.get() / total_loops))
            )
            progress_bar.update()

            step_execution_time = time.time() - start_time
            total_execution_time += step_execution_time

            step_remaining_time = (
                total_execution_time * (total_loops - idx - 1) / (idx + 1)
            )

            minutes, seconds = divmod(step_remaining_time, 60)
            if progress_var.get() != total_loops:
                estimated_time_label.config(
                    text="Estimated Time Remaining: {:02.0f}:{:02.0f}".format(
                        minutes, seconds
                    )
                )

        df = pd.concat(li, axis=0, ignore_index=True)

        result_df = pd.DataFrame(columns=df.columns)
        for i, line in enumerate(lines):
            if stop_search.get():
                break
            start_time = time.time()
            result_df = pd.concat(
                [result_df, df[df[var.get()] == line]], axis=0, ignore_index=True
            )

            progress_var.set(len(all_files) + i + 1)
            progress_bar_per.config(
                text="{}%".format(int(100 * progress_var.get() / total_loops))
            )
            progress_bar.update()

            step_execution_time = time.time() - start_time
            total_execution_time += step_execution_time

            step_remaining_time = (
                total_execution_time * (total_loops - len(all_files) - i - 1) / (i + 1)
            )

            minutes, seconds = divmod(step_remaining_time, 60)
            if progress_var.get() != total_loops:
                estimated_time_label.config(
                    text="Estimated Time Remaining: {:02.0f}:{:02.0f}".format(
                        minutes, seconds
                    )
                )

        now = filesname[0] + " " + datetime.now().strftime("%d%m%Y")
        result_df.to_csv(now + ".csv", index=False)
        confirm()

        text_area.delete("1.0", tk.END)
        loading = False
        run_button.config(text="Run", state=tk.NORMAL)
        estimated_time_label.config(text="Estimated Time Remaining: --")


# ----------------------------------------------------------------------------------------------


def validate_folder_path(path):
    if not os.path.isdir(path):
        messagebox.showerror(
            "Error", "Invalid folder path. Please enter a valid folder path."
        )
        return False
    return True


def getpath():
    path = path_entry.get()
    if not validate_folder_path(path):
        return ""
    else:
        return path


# ----------------------------------------------------------------------------------------------


def get_column_names(file):
    df = pd.read_csv(file, low_memory=False, nrows=0)
    return df.columns.values


# ----------------------------------------------------------------------------------------------


@handle_errors
def columnname():
    global loading
    loading = True

    loading_thread = threading.Thread(target=animationLoadingRefresh)
    loading_thread.start()

    all_files = glob.glob(getpath() + "/*.csv")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        column_names = executor.map(get_column_names, all_files)

    unique_column_names = set()
    for columns in column_names:
        unique_column_names.update(columns)

    drop["values"] = list(unique_column_names)

    loading = False
    refresh_button.config(text="Refresh", state=tk.NORMAL)


# ----------------------------------------------------------------------------------------------
def stop_search_process():
    stop_search.set(True)


# tkinter gui
if __name__ == "__main__":
    csv_window = tk.Tk()
    csv_window.title("CSV File Explorer")
    csv_window.geometry("450x658")
    csv_window.resizable(False, False)
    csv_window.configure(bg="#353535", padx=20, pady=20)

    style = ttk.Style()
    style.configure(
        "My.TLabel", font=("Arial", 12), background="#353535", foreground="#333333"
    )
    style.configure(
        "My.TButton",
        font=("Arial", 10, "bold"),
        background="#353535",
        foreground="black",
        borderwidth=0,
        borderradius=5,
    )

    # Create a frame for the path label and entry box
    path_frame = tk.Frame(csv_window, bg="#353535")
    path_frame.pack(fill=tk.X)

    # Add a label for the path entry
    path_label = tk.Label(
        path_frame,
        text="CSV Path:",
        font=("Arial", 10),
        bg="#353535",
        fg="#fafafa",
        padx=7,
    )
    path_label.pack(side=tk.LEFT)

    # Add an entry box for the path
    path_entry = ttk.Entry(path_frame, font=("Arial", 12))
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    browesbutton = ttk.Button(
        path_frame,
        text="browse",
        style="My.TButton",
        padding=(5, 5),
        command=browsepath,
    )
    browesbutton.pack(side=tk.RIGHT)

    options = ["Select Column Name"]
    var = tk.StringVar(value=options[0])

    # Create a frame for the drop-down and refresh button
    form_frame = tk.Frame(csv_window, bg="#353535")
    form_frame.pack(fill=tk.X, pady=10)

    # Add the dropdown to the form frame
    drop = ttk.Combobox(form_frame, textvariable=var, state="normal")
    drop.config(width=45, height=10)
    drop.pack(side=tk.LEFT, padx=10, expand=True)

    drop.bind("<<ComboboxSelected>>", on_dropdown_click)
    drop.bind("<KeyRelease>", on_dropdown_key_release)

    # Add a refresh button to the form frame
    refresh_button = ttk.Button(
        form_frame,
        text="Refresh",
        style="My.TButton",
        padding=(5, 5),
        command=start_columnname_thread,
    )
    refresh_button.pack(side=tk.RIGHT)

    text_frame = tk.Frame(csv_window, bg="#353535")
    text_frame.pack(fill=tk.BOTH, expand=True)

    # Add a scrolled text widget to the text frame
    text_area = scrolledtext.ScrolledText(
        text_frame, wrap=tk.WORD, font=("Arial", 10), bg="#353532", fg="white"
    )
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the text frame
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area["yscrollcommand"] = scrollbar.set

    # Create a frame for the run and close buttons
    button_frame = tk.Frame(csv_window, bg="#353535")
    button_frame.pack(fill=tk.X, pady=20, padx=50)

    # Add a "Run" button
    run_button = ttk.Button(
        button_frame,
        text="Run",
        style="My.TButton",
        padding=(5, 5),
        command=start_findvalue_thread,
    )
    run_button.pack(side=tk.LEFT, padx=2)

    # Add a "Stop" button
    stop_search = tk.BooleanVar()
    stop_button = ttk.Button(
        button_frame,
        text="Stop",
        style="My.TButton",
        padding=(5, 5),
        command=stop_search_process,
    )
    stop_button.pack(side=tk.LEFT, padx=8)

    # Add a "Close" button
    close_button = ttk.Button(
        button_frame,
        text="Close",
        style="My.TButton",
        padding=(5, 5),
        command=csv_window.destroy,
    )
    close_button.pack(side=tk.RIGHT, padx=2)

    # Add a progress bar
    progress_frame = tk.Frame(csv_window, bg="#353535")
    progress_frame.pack(fill=tk.X, expand=True, pady=(0, 20))

    progress_bar_per = tk.Label(
        progress_frame,
        text="0%",
        font=("Arial", 10),
        bg="#353535",
        fg="#fafafa",
        padx=7,
    )
    progress_bar_per.pack(side=tk.LEFT, anchor="ne")

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        progress_frame, variable=progress_var, mode="determinate"
    )
    progress_bar.pack(fill=tk.X, expand=True)

    estimated_time_label = tk.Label(
        progress_frame,
        text="Estimated Time Remaining: --",
        background="#353535",
        foreground="White",
    )
    estimated_time_label.pack()

    csv_window.mainloop()
