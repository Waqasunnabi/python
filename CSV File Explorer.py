from tkinter import scrolledtext, messagebox, ttk, filedialog
import tkinter as tk
import pandas as pd
import glob,os,threading
from datetime import datetime


def browsepath():
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)  
    path_entry.insert(0, folder_path)


animation = ["  ◜   ", "  ◝   ", "  ◞   ", "  ◟   "]
animation_index = 0

def animationLoadingRefresh():
    if loading:
        global animation_index
        animation_index = (animation_index + 1) % len(animation)
        refresh_button.config(text=animation[animation_index])
        csv_window.after(100, animationLoadingRefresh)


def animationLoadingRun():
    if loading:
        global animation_index
        animation_index = (animation_index + 1) % len(animation)
        run_button.config(text=animation[animation_index])
        csv_window.after(100, animationLoadingRun)



now = datetime.now().strftime("%d%m%Y-%H%M%S")

def confirm():
    answer = messagebox.askyesno(title='confirmation',
                    message='Do you want to open the file location?')
    if answer:
        path = os.path.realpath(os.getcwd())
        os.startfile(path)
        csv_window.destroy()
    else:
        csv_window.destroy()



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
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0,on_bad_lines = 'skip',low_memory=False)
            li.append(df)
        # combine all csv file
        df = pd.concat(li, axis=0, ignore_index=True)

        # find text file data in csv files
        result_df = df[df[var.get()].isin(lines)]
        # create new csv file
        result_df.to_csv(now + ".csv",index=False)
        confirm()

    text_area.delete('1.0', tk.END)
    loading = False
    run_button.config(text="Run",state=tk.NORMAL)

def getpath():
    path = path_entry.get()
    if path == "":
        messagebox.showinfo("Warning", "Invalid Path")
        csv_window.quit()
    else:
        return path
        

def columnname():
    global loading 
    loading = True

    loading_thread = threading.Thread(target=animationLoadingRefresh)
    loading_thread.start()

    
    header = []
    all_files = glob.glob(getpath() + "/*.csv")  # replace .csv with the file extension you want to concatenate
    df = pd.read_csv(all_files[0],low_memory=False)
    columnname = df.columns.values
    for i in columnname:
        header.append(i)
    drop['values'] = header


    loading = False
    refresh_button.config(text="Refresh",state=tk.NORMAL)


csv_window = tk.Tk()
csv_window.title("CSV File Explorer")
csv_window.geometry("450x600")
csv_window.resizable(False, False)
csv_window.configure(bg="#fafafa", padx=20, pady=20)

style = ttk.Style()
style.configure("My.TLabel", font=("Arial", 12), background="#fafafa", foreground="#333333")
style.configure("My.TButton", font=("Arial", 10))

# Create a frame for the path label and entry box
path_frame = tk.Frame(csv_window, bg="#fafafa")
path_frame.pack(fill=tk.X)

# Add a label for the path entry
path_label = tk.Label(path_frame, text="CSV Path:", font=("Arial", 10), bg="#fafafa",fg="#333333", padx=7)
path_label.pack(side=tk.LEFT)

# Add an entry box for the path
path_entry = ttk.Entry(path_frame, font=("Arial", 12))
path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True,padx=2)


browesbutton = ttk.Button(path_frame, text="browse", style="My.TButton", padding=(5, 5),command=browsepath)
browesbutton.pack(side=tk.RIGHT)



# Dropdown menu options
options = ["Select Column Name"]
var = tk.StringVar(value=options[0])

# Create a frame for the drop-down and refresh button
form_frame = tk.Frame(csv_window, bg="#fafafa")
form_frame.pack(fill=tk.X, pady=10)

# Add the dropdown to the form frame
drop = ttk.Combobox(form_frame, textvariable=var,state="readonly")
drop.config(width=45, height=10)
drop.pack(side=tk.LEFT, padx=10,expand=True)


# Add a refresh button to the form frame
refresh_button = ttk.Button(form_frame, text="Refresh", style="My.TButton", padding=(5, 5), command= threading.Thread(target=columnname).start)
refresh_button.pack(side=tk.RIGHT)


text_frame = tk.Frame(csv_window, bg="#fafafa")
text_frame.pack(fill=tk.BOTH, expand=True)

# Add a scrolled text widget to the text frame
text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Arial", 10))
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the text frame
scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area['yscrollcommand'] = scrollbar.set


# Create a frame for the run and close buttons
button_frame = tk.Frame(csv_window, bg="#fafafa")
button_frame.pack(fill=tk.X, pady=20,padx=50)

# Add a "Run" button
run_button = ttk.Button(button_frame, text="Run", style="My.TButton", padding=(5, 5), command=threading.Thread(target=findvalue).start)
run_button.pack(side=tk.LEFT,padx=20)

# Add a "Close" button
close_button = ttk.Button(button_frame, text="Close", style="My.TButton", padding=(5, 5), command=csv_window.destroy)
close_button.pack(side=tk.RIGHT,padx=10)


csv_window.mainloop()