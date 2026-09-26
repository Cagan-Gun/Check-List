import customtkinter as ctk
import os

DATAFOLDER = "CheckListGroups"

if not os.path.exists(DATAFOLDER):
    os.makedirs(DATAFOLDER)

textnamespath = os.path.join(DATAFOLDER, "Textnames.txt")
if not os.path.exists(textnamespath):
    with open(textnamespath, "w", encoding="utf-8") as f:
        pass

def get_path(filename):
    return os.path.join(DATAFOLDER, filename)

window = ctk.CTk()
window.title("Check-List")
window.geometry("550x400")
window.resizable(False, False)

createtext = ctk.CTkTextbox(window, width=200, height=10)
createtext.grid(row=0, column=0, padx=10, pady=10)

def create():
    textdata = createtext.get("1.0", ctk.END).strip()
    createtext.delete("1.0", ctk.END)

    if textdata:
        with open(get_path("Textnames.txt"), "a+", encoding="utf-8") as file:
            file.write(textdata + "\n")
        
        groupfile = get_path(textdata)
        if not os.path.exists(groupfile):
            with open(groupfile, "w", encoding="utf-8") as f:
                pass
                
        addbutton()

def deletefile():
    textdata = createtext.get("1.0", ctk.END).strip()
    createtext.delete("1.0", ctk.END)

    if not textdata:
        return

    filepath = get_path(textdata)
    t_path = get_path("Textnames.txt")

    if os.path.exists(filepath):
        os.remove(filepath)

    if os.path.exists(t_path):
        with open(t_path, "r", encoding="utf-8") as file:
            files = [line.strip() for line in file.readlines() if line.strip()]

        updatedfiles = [f for f in files if f != textdata]

        with open(t_path, "w", encoding="utf-8") as file:
            for f in updatedfiles:
                file.write(f + "\n")

    for widget in scrollablecheck.winfo_children():
        widget.destroy()

    addbutton()

createbutton = ctk.CTkButton(window, text="Create", width=70, command=create)
createbutton.grid(row=0, column=1, padx=5, pady=10)

deletefilebutton = ctk.CTkButton(
    window, 
    text="Delete", 
    width=70, 
    fg_color="red", 
    hover_color="darkred", 
    command=deletefile
)
deletefilebutton.grid(row=0, column=2, padx=5, pady=10)

frame = ctk.CTkFrame(window, width=460, height=310)
frame.place(x=10, y=60)

scrollableframe = ctk.CTkScrollableFrame(frame, width=100, height=300)
scrollableframe.grid(row=0, column=0, padx=10, pady=10)

scrollablecheck = ctk.CTkScrollableFrame(frame, width=340, height=300)
scrollablecheck.grid(row=0, column=1, padx=10, pady=10)

def savecheckboxstates(filename, checkboxlist):
    filepath = get_path(filename)
    with open(filepath, 'w', encoding="utf-8") as file:
        for cb in checkboxlist:
            text = cb.cget("text")
            state = cb.get()
            file.write(f"{text};{state}\n")

def buttonclicked(buttontext):
    for widget in scrollablecheck.winfo_children():
        widget.destroy()

    cleanbuttontext = buttontext.strip()
    if not cleanbuttontext:
        return

    filepath = get_path(cleanbuttontext)
    lines = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding="utf-8") as filename:
            lines = [line.strip() for line in filename.readlines() if line.strip()]

    checkboxlist = []

    for i, line in enumerate(lines):
        if ";" in line:
            text, state = line.rsplit(";", 1)
            ischecked = int(state) if state.isdigit() else 0
        else:
            text = line
            ischecked = 0

        checkbox = ctk.CTkCheckBox(
            scrollablecheck, 
            text=text,
            command=lambda: savecheckboxstates(cleanbuttontext, checkboxlist)
        )
        if ischecked == 1:
            checkbox.select()
        else:
            checkbox.deselect()

        checkbox.grid(row=i, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        checkboxlist.append(checkbox)

    rowidx = len(lines)

    addchecktext = ctk.CTkTextbox(scrollablecheck, width=150, height=30)
    addchecktext.grid(row=rowidx, column=0, padx=(10, 5), pady=10, sticky="w")

    addcheck = ctk.CTkButton(
        scrollablecheck,
        text='Add Check',
        width=80,
        command=lambda: addchecks(cleanbuttontext, addchecktext, checkboxlist)
    )
    addcheck.grid(row=rowidx, column=1, padx=5, pady=10, sticky="w")

    deletecheck = ctk.CTkButton(
        scrollablecheck,
        text='Delete',
        width=60,
        fg_color="red",
        hover_color="darkred",
        command=lambda: deletecheckeditems(cleanbuttontext, checkboxlist)
    )
    deletecheck.grid(row=rowidx, column=2, padx=5, pady=10, sticky="w")

def addbutton():
    for widget in scrollableframe.winfo_children():
        widget.destroy()
    
    t_path = get_path("Textnames.txt")
    if not os.path.exists(t_path):
        return

    with open(t_path, "r", encoding="utf-8") as file:
        files = file.readlines()    

    for i in range(len(files)):
        cleanname = files[i].strip()
        if cleanname:
            button = ctk.CTkButton(
                scrollableframe,
                text=cleanname,
                width=80,
                command=lambda sentence=cleanname: buttonclicked(sentence)
            )
            button.grid(row=i, column=0, padx=10, pady=10, sticky="w")

def addchecks(filename, textbox, checkboxlist):
    savecheckboxstates(filename, checkboxlist)
    
    textdata = textbox.get("1.0", ctk.END).strip()
    if textdata:
        filepath = get_path(filename)
        with open(filepath, 'a+', encoding="utf-8") as file:
            file.write(f"{textdata};0\n")
        textbox.delete("1.0", ctk.END)
        buttonclicked(filename)

def deletecheckeditems(filename, checkboxlist):
    remainingcheckboxes = [check for check in checkboxlist if check.get() == 0]
    savecheckboxstates(filename, remainingcheckboxes)
    buttonclicked(filename)

addbutton()

window.mainloop()