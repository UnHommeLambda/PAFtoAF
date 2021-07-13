# -*- coding: utf-8 -*-
"""
Created on Tue Jun 8 2021

@author: Eyal Cohen
"""

import os
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import sys
import tkinter as tk
from tkinter import DISABLED, NORMAL
from tkinter import BOTTOM, TOP, LEFT, RIGHT#, CENTER
from tkinter import ttk
import networkx as nx
from networkx import NetworkXException
import TkinterDnD2 as tkd
import PAFtoAF as paf
import platform
from PAFtoAF import UnsupportedFormatException, FormatSyntaxException,  PreferenceException#, FormatException, CommandLineException, FindingSolverException, UnsupportedOSException
from datetime import (date, datetime)

system = platform.system()
if system not in ["Windows", "Linux", "Darwin"]:
    root = tk.Tk()
    root.withdraw()
    msg = tk.messagebox.showinfo("Error", "It looks like you system is not supported.\nSupported systems : Windows, Linux, Darwin(MacOS)\nYour system : {}".format(system))
    while msg != "ok":
        continue
    sys.exit()

inputfile = ''
fileformat = ''
query_bool = False
outs = []
tempFile = []
solverPath = ''
reduction = 0
fig = Figure()

if os.path.exists("temp"):
    for file in os.scandir("temp"):
        os.remove(file)
    os.rmdir("temp")
os.mkdir("temp")

def try_toPaf(file, fileformat = ''):
    """
    This method is just a toPaf that can manage the different possible Exceptions.
    It is invoked every time we want to convert something to the PAF format in PAFtoAF : (set, dict, dict).
    str * str -> None
    """
    
    assert type(file) is str, "The first argument must be the name of the file. (type String)"
    assert type(fileformat) is str, "The second argument must be the format of the file. (type String)"
    
    if fileformat == '':
        try:
            paf.toPaf(file, "ptgf" if file.endswith(".ptgf") or file.endswith(".tgf") else "papx")
        except FileNotFoundError:
            print("It seems that the file you used as input can not be found anymore.")
            textarea.delete("1.0", "end")
            textarea.insert("end", "It seems that the file you used as input can not be found anymore.")
        except (IOError, OSError) as e:
            print("System Error")
            
            def fatal_closing():
                fatal_window.destroy()
                on_closing()
            
            fatal_window = tk.Tk()
            fatal_window.title("System Error")
            fatal_frame = tk.Frame(fatal_window)
            fatal_frame.pack(side = tk.CENTER)
            fatal_label = tk.Label(fatal_frame, text = "System Error :\n{}".format(e))
            fatal_label.pack(side = TOP)
            fatal_button = tk.Button(fatal_frame, text = "Ok", command = fatal_closing)
            fatal_button.pack(side = BOTTOM)
            fatal_window.protocol("WM_DELETE_WINDOW", fatal_closing)
            
        except FormatSyntaxException as e:
            textareaReduc["state"] = NORMAL
            textareaReduc.delete("1.0", "end")
            textareaReduc.insert("end", "Format syntax error :\n"+str(e))
            textareaReduc["state"] = DISABLED
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED
        except PreferenceException as e:
            textareaReduc["state"] = NORMAL
            textareaReduc.delete("1.0", "end")
            textareaReduc.insert("end", "Preferences error :\n"+str(e))
            textareaReduc["state"] = DISABLED
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED
        except UnsupportedFormatException as e:
            textarea.delete("1.0", "end")
            textarea.insert("end", "Unsupported format exception :\n", str(e))
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED
    else:
        try:
            paf.toPaf(file, "ptgf" if fileformat in ["ptgf", "tgf"] else "papx")
        except FileNotFoundError:
            print("It seems that the file you used as input can not be found anymore.")
            textarea.delete("1.0", "end")
            textarea.insert("end", "It seems that the file you used as input can not be found anymore.")
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED
        except (IOError, OSError) as e:
            print("System Error")
            
            def fatal_closing():
                fatal_window.destroy()
                on_closing()
            
            fatal_window = tk.Tk()
            fatal_window.title("System Error")
            fatal_frame = tk.Frame(fatal_window)
            fatal_frame.pack(side = tk.CENTER)
            fatal_label = tk.Label(fatal_frame, text = "System Error :\n{}".format(e))
            fatal_label.pack(side = TOP)
            fatal_button = tk.Button(fatal_frame, text = "Ok", command = fatal_closing)
            fatal_button.pack(side = BOTTOM)
            fatal_window.protocol("WM_DELETE_WINDOW", fatal_closing)
            
        except FormatSyntaxException as e:
            textareaReduc["state"] = NORMAL
            textareaReduc.delete("1.0", "end")
            textareaReduc.insert("end", "Format syntax error :\n"+str(e))
            textareaReduc["state"] = DISABLED
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED
        except PreferenceException as e:
            textareaReduc["state"] = NORMAL
            textareaReduc.delete("1.0", "end")
            textareaReduc.insert("end", "Preferences error :\n"+str(e))
            textareaReduc["state"] = DISABLED
            problem_box.set("")
            semantic_box.set("")
            problem_box["state"] = DISABLED
            semantic_box["state"] = DISABLED
            solver.delete(0, tk.END)
            solver["state"] = DISABLED
            solver_select_button["state"] = DISABLED
            solver_find_button["state"] = DISABLED
            button0["state"] = DISABLED
            button1["state"] = DISABLED
            button2["state"] = DISABLED
            button3["state"] = DISABLED
            button4["state"] = DISABLED
            graph_check["state"] = DISABLED

def load_text(event):
    """
    This method is binded to the drag and drop text area, it is invoked when someone drop a file,
    and just load the text inside the file if the format is right and write an error message in the area if the format is not accepted.
    Event -> None
    """
    
    textarea.delete("1.0","end")
    textareaReduc.delete("1.0","end")
    button0["bg"] = "white"
    button1["bg"] = "white"
    button2["bg"] = "white"
    button3["bg"] = "white"
    button4["bg"] = "white"
    global inputfile
    global fileformat
    if event.data.endswith(".ptgf") or event.data.endswith(".papx"):
        inputfile = event.data
        fileformat = "ptgf" if event.data.endswith(".ptgf") else "papx"
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        button0["bg"] = "red"
        button0["state"] = DISABLED
        button1["state"] = NORMAL
        button2["state"] = NORMAL
        button3["state"] = NORMAL
        button4["state"] = NORMAL
        graph_check["state"] = NORMAL
        try_toPaf(event.data)
    elif event.data.endswith(".tgf") or event.data.endswith(".apx"):
        inputfile = event.data
        fileformat = "tgf" if event.data.endswith(".tgf") else "apx"
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        button0["bg"] = "red"
        button0["state"] = DISABLED
        button1["state"] = NORMAL
        button2["state"] = NORMAL
        button3["state"] = NORMAL
        button4["state"] = NORMAL
        graph_check["state"] = NORMAL
        try_toPaf(event.data)
    else:
        button0["state"] = DISABLED
        button1["state"] = DISABLED
        button2["state"] = DISABLED
        button3["state"] = DISABLED
        button4["state"] = DISABLED
        graph_check["state"] = DISABLED
        paf.args.clear()
        paf.attacksFrom.clear()
        paf.preferences.clear()
        textarea.insert("end","Sorry this document format is not\naccepted.\nPlease use .ptgf .papx .tgf or .apx\nformats.\n\nFor help please click on the help button and to see the available formats click onthe formats button.")
    global graph_check_value
    if graph_check_value.get() == 1:
        show_graph()
        
def load_text_selection():
    """
    This method is the one used by the button open on the GUI.
    It opens a window allowing the user to browse its file and then reads and load the selected file.
    """
    
    typeslist = [("PTFG file", ".ptgf"), ("PAPX file", ".papx"), ("TGF file", ".tgf"), ("APX file", ".apx")]
    Sfile = tk.filedialog.askopenfilename(title = "Sélectionnez un fichier ..." , filetypes = typeslist)
    load_text_file(Sfile)
    
def select_solver():
    """
    This method is the one used by the button open on the GUI.
    It opens a window allowing the user to browse its file and then reads and load the selected file.
    """
    global solverPath
    typeslist = [("Executable", ".exe"), ("Python", ".py"), ("Java", ".jar"), ("Other", ".*")]
    Sfile = tk.filedialog.askopenfilename(title = "Sélectionnez un fichier ..." , filetypes = typeslist)
    solverPath = Sfile
    solver.delete(0, tk.END)
    solver.insert(tk.END, Sfile)
    
def find_solver():
    global solverPath
    found = True
    solver_name = solver_value.get()
    if os.path.exists(solver_name):
        if os.path.isdir(solver_name):
            found = False
            for file in os.scandir(solver_name):
                if os.fsdecode(file) in ["mu-toksia", "mu-toksia.exe", "JargSemSAT.jar"]:
                    solverPath = os.path.abspath(solver_name + os.fsdecode(file))
                    found = True
        else:
            solverPath = os.path.abspath(solver_name)
    else:
        found = False
    if not found:
        solver.delete(0,tk.END)
        solver.insert(tk.END, "Not found")
    else:
        solver.delete(0,tk.END)
        solver.insert(tk.END, solverPath)

def load_text_file(Sfile):
    """
    This method is the same as load_text but works without an event, 
    it just reads the file that the load_text_selection gave it and loads the text inside the same way, load_text does.
    """
    
    assert type(Sfile) is str, "The argument of this method is the name of the fileis has to load. (type String)"
    
    textarea.delete("1.0","end")
    textareaReduc["state"] = NORMAL
    textareaReduc.delete("1.0","end")
    textareaReduc["state"] = DISABLED
    button0["bg"] = "white"
    button1["bg"] = "white"
    button2["bg"] = "white"
    button3["bg"] = "white"
    button4["bg"] = "white"
    global inputfile
    global fileformat
    global reduction
    reduction = 0
    if Sfile.endswith(".ptgf") or Sfile.endswith(".papx"):
        inputfile = Sfile
        fileformat = "ptgf" if Sfile.endswith(".ptgf") else "papx"
        with open(Sfile, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        try_toPaf(Sfile)
        button0["bg"] = "red"
        button0["state"] = DISABLED
        button1["state"] = NORMAL
        button2["state"] = NORMAL
        button3["state"] = NORMAL
        button4["state"] = NORMAL
        graph_check["state"] = NORMAL
    elif Sfile.endswith(".tgf") or Sfile.endswith(".apx"):
        inputfile = Sfile
        fileformat = "tgf" if Sfile.endswith(".tgf") else "apx"
        with open(Sfile, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        try_toPaf(Sfile, fileformat)
        button0["bg"] = "red"
        button0["state"] = DISABLED
        button1["state"] = NORMAL
        button2["state"] = NORMAL
        button3["state"] = NORMAL
        button4["state"] = NORMAL
        graph_check["state"] = NORMAL
    else:
        button0["state"] = DISABLED
        button1["state"] = DISABLED
        button2["state"] = DISABLED
        button3["state"] = DISABLED
        button4["state"] = DISABLED
        graph_check["state"] = DISABLED
        paf.args.clear()
        paf.attacksFrom.clear()
        paf.preferences.clear()
        textarea.insert("end","Sorry this document format is not\naccepted.\nPlease use .ptgf .papx .tgf or .apx\nformats.\n\nFor help please click on the help button and to see the available formats click onthe formats button.")
    global graph_check_value
    if graph_check_value.get() == 1:
        show_graph()

def reload_text():
    """
    This method reads the text area and reload the text.
    It means that the user can now modify the text inside the area to modify the PAF they want to generate.
    """
    global inuptfile
    global fileformat
    if fileformat == '':
        textarea.get("1.0", "2.0")
        if line_is_int(textarea.get("1.0", "1.1")):
            fileformat = "ptgf"
        elif(textarea.get("1.0", "2.0")[0:3] == "arg"):
            fileformat = "papx"
        else:
            textareaReduc["state"] = NORMAL
            textareaReduc.delete("1.0","end")
            textareaReduc.insert("end", "\nThe text written in the box next to this one does not follow an accepted format.\nPlease consult the format option button for more information.\n")
            textareaReduc["state"] = DISABLED
            return 0
    inputfile = "temp/reloading_text.{}".format(fileformat)
    with(open(inputfile, "w+") as openfile):
        openfile.write(textarea.get("1.0", "end"))
        
    load_text_file(inputfile)
        
def line_is_int(line):
    """
    This method verify if the line it receives is an int, it is used to get the format if the user writes the file or writes directly on the text area.
    Object -> bool
    """
    if type(line) is int:
        return(True)
    elif type(line) is str:
        try:
            int(line)
        except:
            return(False)
        return(True)
    elif type(line) is float:
        if line%1==0:
            return(True)
    return(False)
    

window = tkd.TkinterDnD.Tk()
window.title('PAFtoAF')
window.geometry('750x600')
window.config(bg='#554356')

ws = tk.Frame(window)
ws.pack(side = TOP)

frame = tk.Frame(ws, height = 60, width = 82)
frame.pack()

optionframe = tk.Frame(frame, height = 10, width = 40)
optionframe.pack(side = TOP)

frameDnD = tk.Frame(frame, height = 23, width = 41)
frameDnD.pack(side = LEFT)

frameReduction = tk.Frame(frame, height = 23, width = 41)
frameReduction.pack(side = RIGHT)

taskframe = tk.Frame(ws)
taskframe.pack(side = BOTTOM)

solverframe = tk.Frame(ws)
solverframe.pack(side = BOTTOM)

buttonframe = tk.Frame(ws, height = 5, width = 40)
buttonframe.pack(side = BOTTOM)

queryframe = tk.Frame(taskframe)

def show_help():
    """
    The method linked to the help button, it creates a new window with nothing but a text area explaining the GUI.
    """
    help_window = tk.Tk()
    help_window.title("HELP")
    help_window.geometry("686x590")
    help_window.config(bg = "#dddddd")
    help_frame = tk.Frame(help_window, height = 38, width = 86)
    help_frame.pack()
    help_text = tk.Text(help_frame, height = 36, width = 84)
    help_text.pack(side = TOP)
    help_text.insert("end", "This is the GUI version of PAFtoAF Version 1.0, created by Eyal Cohen.\n")
    help_text.insert("end", "\nThis application allows you to use a Preference-based Argumentation Framework\n(PAF) and transform it into an Extension-based Argumentation Framework (AF).\n")
    help_text.insert("end", "\nTo do so, please choose a file in the ptgf, papx, tgf or apx format\n(for more information please click on the formats button in the main window).\n")
    help_text.insert("end", "\nDrag you file in the area specifying so or use the 'open' button to select one.\n(Don't forget to specify the format in the list or extensions)\nThe text in the file should now appear.\n")
    help_text.insert("end", "\nYou can generate the graph described in the file by checking the box under the\ntext area.\n")
    help_text.insert("end", "\nThen select the reduction you wish to apply, the resulting AF should\nappear in a ptg or apx format. The graph is dynamically modified to represent\nthe current AF.\n")
    help_text.insert("end", "\nIf you want to use a solver, please enter it's name in the specified line,\nor use the open button to find it, its path will automatically be written\nin the box.\nIn abscence of a name or path mu-toksia will be selected under Linux and\nJArgSemSAT under Windows.\n")
    help_text.insert("end", "\nFinally you can select the task you would like to carry out.\nAnd all the options that you want to apply, using the buttons under\n'Solver Options :'.\n")
    help_text.insert("end", "\nThe result should appear in the figure down below, if you want to dowload it\nplease indicate the path to the directory and then press the dowload button.\n")
    help_text.insert("end", "\nPlease do not alter the 'temp' directory. You can copy a file if needed, but\nremoving/deleting one could cause an error, maybe even crashing the application.\nAnd putting a new file in could rewrite it, and would delete it on the closing\nof the application.\n")
    help_text["state"] = DISABLED

def show_formats():
    """
    The method linked to the formats button, it creates a new window with nothing but a text explaining the formats and a button per format to see what each one means.
    """
    def show_ptgf():
        formats_text["state"] = NORMAL
        formats_text.delete("1.0", "end")
        formats_text.insert("end", "\nThe tgf (Trivial Graph Format) is a usualformat for files\ndescipting an AF.\n")
        formats_text.insert("end", "Here we add the preference side of a Preference-base AF (PAF).\n")
        formats_text.insert("end", "\nTo do so, we add on the tgf format a second # delimiting\na third area, where the prefernces are written as attacks.\n")
        formats_text.insert("end", "So arguments are written as their names, then a # is placed,\nfollowed by the attacks where 1 2 means that 1 attacks 2.\n")
        formats_text.insert("end", "Then a second # is placed and finally the preferences\nwhere 1 2 means 1 is prefered over 2.\n")
        formats_text.insert("end", "Here is an exemple :\n1\n2\n3\n#\n1 2\n2 1\n2 3\n#\n1 2\n\nMeans that 1 and 2 attack each other, 2 attack 3, 1 is preffered\nover 2.")
        p_tgfButton["bg"] = "red"
        p_tgfButton["state"] = DISABLED
        p_apxButton["bg"] = "white"
        p_apxButton["state"] = NORMAL
        formats_text["state"] = DISABLED
    def show_papx():
        formats_text["state"] = NORMAL
        formats_text.delete("1.0", "end")
        formats_text.insert("end", "\nThe apx (Aspartix) is a usualformat for files\ndescipting an AF.\n")
        formats_text.insert("end", "Here we add the preference side of a Preference-base AF (PAF).\n")
        formats_text.insert("end", "\nTo do so, we add on the apx format a new keyword\nfor the prefernces : pref.\n")
        formats_text.insert("end", "So arguments are written as arg(name) followed by\nthe attacks where att(1,2) means that 1 attacks 2.\n")
        formats_text.insert("end", "Finally the preferences written pref(1,2) if 1 is prefered\nover 2.\n")
        formats_text.insert("end", "Here is an exemple :\narg(1)\narg(2)\narg(3)\natt(1,2)\natt(2,1)\natt(2,3)\npref(1,2)\n\nMeans that 1 and 2 attack each other, 2 attack 3, 1 is preffered\nover 2.")
        p_apxButton["bg"] = "red"
        p_apxButton["state"] = DISABLED
        p_tgfButton["bg"] = "white"
        p_tgfButton["state"] = NORMAL
        formats_text["state"] = DISABLED
    formats_window = tk.Tk()
    formats_window.title("FORMATS")
    formats_window.geometry("686x480")
    formats_window.config(bg = "#dddddd")
    formats_frame = tk.Frame(formats_window, height = 30, width = 86)
    formats_frame.pack()
    accepted_formats_text = tk.Text(formats_frame, height = 4, width = 84)
    accepted_formats_text.pack(side = TOP)
    formats_text = tk.Text(formats_frame, height = 28, width = 84, state = DISABLED)
    buttonsframe = tk.Frame(formats_frame, height = 5, width = 84)
    buttonsframe.pack(side = TOP)
    p_tgfButton = tk.Button(buttonsframe, text = "tgf and ptgf", bg = "white", activebackground = "red", command = show_ptgf)
    p_apxButton = tk.Button(buttonsframe, text = "apx and papx", bg = "white", activebackground = "red", command = show_papx)
    p_tgfButton.pack(side = LEFT)
    p_apxButton.pack(side = LEFT)
    formats_text.pack(side = TOP)
    accepted_formats_text.insert("end", "The formats accepted are ptgf, papx, tgf, and apx.\n")
    
def show_problems():
    def CO():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Complete :\nS is in CO(F) iff :\n-S is in ADM(F)\n-for every a in A that is defended by S, a is in S.\n")
        sem_text.insert("end", "\nFor exemple in the following AF :\n1\n2\n3\n4\n5\n6\n7\n1 2\n2 3\n3 4\n4 3\n4 5\n5 6\n6 7\n7 5\nThe following sets are complete : {1,4,6}, {1, 3} or {1}.")
        sem_text["state"] = DISABLED
    def PR():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Prefered :\nS is in PR(F) iff :\n-S is a maximal admissible set.\n")
        sem_text("end", "\nFor exemple in the following AF :\n1\n2\n3\n4\n5\n6\n7\n1 2\n2 3\n3 4\n4 3\n4 5\n5 6\n6 7\n7 5\nThe following set is preferred : {1,4,6}.")
        sem_text["state"] = DISABLED
    def ST():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Stable :\n")
        sem_text("end", "\nFor exemple in the following AF :\n1\n2\n3\n4\n5\n6\n7\n1 2\n2 3\n3 4\n4 3\n4 5\n5 6\n6 7\n7 5\nThe following sets are stable : ")
        sem_text["state"] = DISABLED
    def SST():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Semi-Stable :\n")
        sem_text["state"] = DISABLED
    def STG():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Staged :\n")
        sem_text["state"] = DISABLED
    def GR():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Grounded :\n")
        sem_text["state"] = DISABLED
    def ID():
        sem_text["state"] = NORMAL
        sem_text.delete("1.0", "end")
        sem_text.insert("end", "Ideal :\n")
        sem_text["state"] = DISABLED
    def DC():
        task_text["state"] = NORMAL
        task_text.delete("1.0", "end")
        task_text.insert("end", "Decide Credulously :\n")
        task_text["state"] = DISABLED
    def DS():
        task_text["state"] = NORMAL
        task_text.delete("1.0", "end")
        task_text.insert("end", "Decide Skeptically :\n")
        task_text["state"] = DISABLED
    def SE():
        task_text["state"] = NORMAL
        task_text.delete("1.0", "end")
        task_text.insert("end", "Some Extension :\n")
        task_text["state"] = DISABLED
    def CE():
        task_text["state"] = NORMAL
        task_text.delete("1.0", "end")
        task_text.insert("end", "Count Extension :\n")
        task_text["state"] = DISABLED
    def EE():
        task_text["state"] = NORMAL
        task_text.delete("1.0", "end")
        task_text.insert("end", "Enumerate Extensions :\n")
        task_text["state"] = DISABLED
    switcher_semantics = {
        "" : print,
        "CO" : CO,
        "PR" : PR,
        "ST" : ST,
        "SST" : SST,
        "STG" : STG,
        "GR" : GR,
        "ID" : ID
        }
    switcher_tasks = {
        "" : print,
        "DC" : DC,
        "DS" : DS,
        "SE" : SE,
        "CE" : CE,
        "EE" : EE
        }
    def sem_select(event):
        switcher_semantics[sem_box.get()]() 
    def task_select(event):
        switcher_tasks[task_box.get()]()
    #I know it is weird to get from the box instead of from the StringVar()
    #But the sem_val and task_val are empty when I do a .get() and I don't know why
    #I even tried making the variable global but it does not change anything
        
    problems_window = tk.Tk()
    problems_window.title("PROBLEMS")
    problems_window.geometry("696x480")
    problems_window.config(bg = "#dddddd")
    
    problems_frame = tk.Frame(problems_window, height = 30, width = 86)
    problems_frame.pack()
    
    explication_text = tk.Text(problems_frame, height = 12, width = 84)
    explication_text.grid(row = 0, column = 0, columnspan = 10, rowspan = 6)
    explication_text.delete("1.0","end")
    explication_text.insert("end", "'Problems' are the computational problems that you want to submit to the program.\nA problem is composed of :\n-a semantic : a meaning, a logic\n-a task : that will be resolved with respect to the semantic.\n")
    explication_text.insert("end", "Now we must introduce 2 notions.\nGiven an AF F = <A,R>. With A the arguments and R (included in A x A) the attacks.\nS a set or arguments in A is :\n")
    explication_text.insert("end", "\n-Conflict-Free (CF) : iff for every a,b in S, (a,b) is not in R.\n")
    explication_text.insert("end", "\n-Admissible (ADM) : iff S is CF and for every a in S, S defends a from any b\n(not in S) attacking a.\n")
    explication_text["state"] = DISABLED
    
    boxframe = tk.Frame(problems_frame, width = 84)
    boxframe.grid(row = 6, column = 0, columnspan = 10)
    
    sem_val = tk.StringVar()
    sem_box = ttk.Combobox(boxframe, values = ["CO","PR","ST","SST","STG","GR","ID"], textvariable = sem_val, state = "readonly")
    sem_box.bind("<<ComboboxSelected>>", sem_select)
    sem_box.pack(side = LEFT)
    
    task_val = tk.StringVar()
    task_box = ttk.Combobox(boxframe, values = ["DC","DS","SE","CE", "EE"], textvariable = task_val, state = "readonly")
    task_box.bind("<<ComboboxSelected>>", task_select)
    task_box.pack(side = RIGHT)
    
    explicationframe = tk.Frame(problems_frame, height = 16, width = 84)
    explicationframe.grid(row = 7, column = 0, rowspan = 7, columnspan = 10)
    
    sem_text = tk.Text(explicationframe, height = 14, width = 40, state = DISABLED)
    sem_text.grid(row = 0, column = 0, rowspan = 7, columnspan = 5)
    
    task_text = tk.Text(explicationframe, height = 14, width = 40, state = DISABLED)
    task_text.grid(row = 0, column = 5, rowspan = 7, columnspan = 5)
    
    expli_empty_label = tk.Label(explicationframe, text = "", height = 1, width = 80)
    expli_empty_label.grid(row = 7, column = 0, rowspan = 1, columnspan = 10)

def ClickReduc0():
    """
    Linked to the 'no reduction' button. It clears the reduction text area and change the graph (if the checkbox is active to the PAF graph.
    """
    global reduction
    global inputfile
    global fileformat
    global graph_check_value
    reduction = 0
    try_toPaf(inputfile, fileformat)
    textareaReduc.configure(state = "normal")
    textareaReduc.delete("1.0","end")
    if graph_check_value.get() == 1:
        show_graph()
    button0["bg"] = "red"
    button0["state"] = DISABLED
    button1["bg"] = "white"
    button1["state"] = NORMAL
    button2["bg"] = "white"
    button2["state"] = NORMAL
    button3["bg"] = "white"
    button3["state"] = NORMAL
    button4["bg"] = "white"
    button4["state"] = NORMAL
    problem_box.set("")
    semantic_box.set("")
    problem_box["state"] = DISABLED
    semantic_box["state"] = DISABLED
    solver.delete(0, tk.END)
    solver["state"] = DISABLED
    solver_select_button["state"] = DISABLED
    solver_find_button["state"] = DISABLED
    download_button["state"] = DISABLED
    textareaReduc.configure(state = "disabled")

def ClickReduc1():
    """
    Linked to the 'reduction 1' button. It overwrite the reduction text area with the reduction 1.
    If the graph checkbox is active, it overwrites the graph with the resulting AF.
    """
    global reduction
    global inputfile
    global outs
    global tempFile
    global fileformat
    reduction = 1
    try_toPaf(inputfile, fileformat)
    textareaReduc.configure(state = "normal")
    file = "temp/Reduction1-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    paf.reduction1([file], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open(file,"r") as openfile:
        textareaReduc.delete("1.0", "end")
        for line in openfile:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    if file not in tempFile:
        tempFile.append(file)
    try_toPaf(file, fileformat)
    if graph_check_value.get() == 1:
        show_graph()
    button1["bg"] = "red"
    button1["state"] = DISABLED
    button0["bg"] = "white"
    button0["state"] = NORMAL
    button2["bg"] = "white"
    button2["state"] = NORMAL
    button3["bg"] = "white"
    button3["state"] = NORMAL
    button4["bg"] = "white"
    button4["state"] = NORMAL
    problem_box["state"] = "readonly"
    semantic_box["state"] = "readonly"
    solver["state"] = NORMAL
    solver_select_button["state"] = NORMAL
    solver_find_button["state"] = NORMAL
    download_button["state"] = NORMAL
    textareaReduc.configure(state = "disabled")

def ClickReduc2():
    """
    Linked to the 'reduction 2' button. It overwrite the reduction text area with the reduction 2.
    If the graph checkbox is active, it overwrites the graph with the resulting AF.
    """
    global reduction
    global inputfile
    global outs
    global tempFile
    global fileformat
    reduction = 2
    try_toPaf(inputfile, fileformat)
    textareaReduc.configure(state = "normal")
    file = "temp/Reduction2-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    paf.reduction2([file], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open(file,"r") as openfile:
        textareaReduc.delete("1.0", "end")
        for line in openfile:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    if file not in tempFile:
        tempFile.append(file)
    try_toPaf(file, fileformat)
    if graph_check_value.get() == 1:
        show_graph()
    button2["bg"] = "red"
    button2["state"] = DISABLED
    button0["bg"] = "white"
    button0["state"] = NORMAL
    button1["bg"] = "white"
    button1["state"] = NORMAL
    button3["bg"] = "white"
    button3["state"] = NORMAL
    button4["bg"] = "white"
    button4["state"] = NORMAL
    problem_box["state"] = "readonly"
    semantic_box["state"] = "readonly"
    solver["state"] = NORMAL
    solver_select_button["state"] = NORMAL
    solver_find_button["state"] = NORMAL
    download_button["state"] = NORMAL
    textareaReduc.configure(state = "disabled")

def ClickReduc3():
    """
    Linked to the 'reduction 3' button. It overwrite the reduction text area with the reduction 3.
    If the graph checkbox is active, it overwrites the graph with the resulting AF.
    """
    global reduction
    global inputfile
    global outs
    global tempFile
    global fileformat
    reduction = 3
    try_toPaf(inputfile, fileformat)
    textareaReduc.configure(state = "normal")
    file = "temp/Reduction3-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    paf.reduction3([file], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open(file,"r") as openfile:
        textareaReduc.delete("1.0", "end")
        for line in openfile:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    if file not in tempFile:
        tempFile.append(file)
    try_toPaf(file, fileformat)
    if graph_check_value.get() == 1:
        show_graph()
    button3["bg"] = "red"
    button3["state"] = DISABLED
    button0["bg"] = "white"
    button0["state"] = NORMAL
    button1["bg"] = "white"
    button1["state"] = NORMAL
    button2["bg"] = "white"
    button2["state"] = NORMAL
    button4["bg"] = "white"
    button4["state"] = NORMAL
    problem_box["state"] = "readonly"
    semantic_box["state"] = "readonly"
    solver["state"] = NORMAL
    solver_select_button["state"] = NORMAL
    solver_find_button["state"] = NORMAL
    download_button["state"] = NORMAL
    textareaReduc.configure(state = "disabled")

def ClickReduc4():
    """
    Linked to the 'reduction 4' button. It overwrite the reduction text area with the reduction 4.
    If the graph checkbox is active, it overwrites the graph with the resulting AF.
    """
    global reduction
    global inputfile
    global outs
    global tempFile
    global fileformat
    reduction = 4
    try_toPaf(inputfile, fileformat)
    file = "temp/Reduction4-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    textareaReduc.configure(state = "normal")
    paf.reduction4([file]+outs, "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open(file,"r") as openfile:
        textareaReduc.delete("1.0", "end")
        for line in openfile:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    if file not in tempFile:
        tempFile.append(file)
    try_toPaf(file, fileformat)
    if graph_check_value.get() == 1:
        show_graph()
    button4["bg"] = "red"
    button4["state"] = DISABLED
    button0["bg"] = "white"
    button0["state"] = NORMAL
    button1["bg"] = "white"
    button1["state"] = NORMAL
    button2["bg"] = "white"
    button2["state"] = NORMAL
    button3["bg"] = "white"
    button3["state"] = NORMAL
    problem_box["state"] = "readonly"
    semantic_box["state"] = "readonly"
    solver["state"] = NORMAL
    solver_select_button["state"] = NORMAL
    solver_find_button["state"] = NORMAL
    download_button["state"] = NORMAL
    textareaReduc.configure(state = "disabled")

def download_reduc():
    global inputfile
    today = date.today()
    now_time = datetime.now().strftime("%d-%m-%Y~%H_%M_%S")
    directory = f"PAFtoAF_downloads_{today}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        if not os.path.isdir(directory):
            directory = directory+"_dir"
            os.mkdir(directory)
    if inputfile.find("\\") != -1:
        filename = inputfile[inputfile.rfind("\\")+1:inputfile.rfind("".join([".", fileformat]))]
    elif inputfile.find("/") != -1:
        filename = inputfile[inputfile.rfind("/")+1:inputfile.rfind("".join([".", fileformat]))]
    else :
         filename = inputfile[:inputfile.rfind("".join([".", fileformat]))]
    with(open(f"{directory}/reduction{reduction}_{filename}_{now_time}.{('tgf', 'apx')[fileformat == 'papx']}", "w+") as openfile):
        openfile.write(textareaReduc.get("1.0", "end"))

def renew_query_frame():
    queryframe = tk.Frame(taskframe)
    
    query_label = tk.Label(queryframe, text = "query : ")
    query_label.grid(row = 0, column = 0)
    
    query_value= tk.StringVar()
    query_entry = tk.Entry(queryframe, textvariable = query_value)
    query_entry.grid(row = 0, column = 1)

def problem_selection(event):
    """
    Linked to the problem selection combo box, this method check the selected value in the box and manages the other box according to what was chosen.
    """
    global query_bool
    global queryframe
    if problem_value.get() in ["CE", "EE", "DC"]:
        semantic_box["values"] = ["CO","PR","ST","SST","STG","GR"]
    else:
        semantic_box["values"] = ["CO","PR","ST","SST","STG","GR", "ID"]
    if problem_value.get() in ["DC", "DS"] and not query_bool:
        query_bool = True
        task_label.grid(row = 0, column = 2)
        queryframe.grid(row = 1, column = 3)
    elif problem_value.get() in ["CE", "EE", "SE"] and query_bool:
        query_bool = False
        task_label.grid(row = 0, column = 1)
        queryframe.grid_remove()
        renew_query_frame()

def semantic_selection(event):
    """
    Linked to the semantic selection combo box, this method check the selected value in the box and manages the other box according to what was chosen.
    """
    if semantic_value.get() == "ID":
        problem_box["values"] = ["DS","SE"]
    else:
        problem_box["values"] = ["DC","DS","SE","CE", "EE"]

def show_graph():
    """
    Linked to the 'show graph' checkbox, this method creates a figure in which it draws the graph of the current reudction (PAF in case no reduction has been applied).
    """
    global fig
    global inputfile
    
    if graph_check_value.get() == 1:
        if fig == Figure():
            fig = plt.figure(dpi = 100)
        
        plt.clf()
        
        edgeList = []
        
        ax = plt.subplot(111)
        ax.set_title('Graph - {}'.format(inputfile), fontsize=10)
        graph = nx.DiGraph()
        
        for arg1 in paf.attacksFrom.keys():
            for arg2 in paf.attacksFrom[arg1]:
                edgeList.append((arg1,arg2))
        
        graph.add_edges_from(edgeList, color = "k", weight = 2)
        critical_edges = []
        
        for arg1 in paf.preferences.keys():
            for arg2 in paf.preferences[arg1]:
                if (arg2, arg1) in edgeList:
                    critical_edges.append((arg2,arg1))
                    
        graph.add_edges_from(critical_edges, color = "r", weight = 3)
        
        colors = nx.get_edge_attributes(graph,'color').values()
        weights = nx.get_edge_attributes(graph,'weight').values()
        try:
            pos = nx.planar_layout(graph)
        except(NetworkXException):
            pos = nx.spring_layout(graph)
        nx.draw(graph, pos, node_size=700, node_color='yellow', font_size=8, font_weight='bold', edge_color = colors, width = list(weights), arrowsize = 30, arrowstyle = "->", with_labels = True)
        
        plt.tight_layout()        

        plt.rcParams["figure.figsize"] = (10,9)
        
        plt.savefig("temp/Graph.png", format="PNG")

    else:
        os.remove("temp/Graph.png")
        plt.close()

def save():
    """
    This method is binded to the save button.
    On activation it reads every useful information in the user's choices and writes the corresponding command line.
    """
    global inputfile
    global fileformat
    global reduction
    global outs
    global task
    global query
    global solver 
    global solverPath
    with(open("PAFtoAFGUI-saved-{}-{}.txt".format(os.path.basename(inputfile).replace(".{}".format(fileformat),""), reduction), "w+")) as file:
        file.write("python3 PAFtoAF")
        if inputfile != '':
            file.write("-f {} -fo {}".format(inputfile, fileformat))
        if reduction != 0:
            file.write("-r {}".format(reduction))
        if outs != []:
            file.write("-outs {}".format(outs))
        if task != '':
            file.write("-p {}".format(task))
            if query != '':
                file.write("-a {}".format(query))
        if solver != '':
            file.write("-s {}".format(solver))
        if solverPath != '':
            file.write("-sp {}".format(solverPath))

def on_closing():
    """
    This is the closing protocol, it is activated on the closing of the main window.
    Its purpose is to delete every temporary file that has been created during the session and then to destroy the window.
    """
    global graph_value
    if graph_check_value.get() == 1:
        graph_check.toggle()
    if tempFile != []:
        for i in range(len(tempFile)):
            os.remove(tempFile[i])
        tempFile.clear()
    for file in os.scandir("temp"):
        os.remove(file)
    os.rmdir("temp")
    window.destroy()
    window.quit()

textarea = tk.Text(frameDnD, height=18, width=41)
textarea.grid(row = 1, column = 0, rowspan = 6, columnspan = 6)
textarea.drop_target_register(tkd.DND_FILES)
textarea.dnd_bind('<<Drop>>', load_text)
textarea.insert("end", "\n\nPlease drag a file here.\n\nOr click the 'open' button under this\nbox to select a file.\n\nAccepted formats are ptgf, papx,\ntgf or apx.")

sbv = tk.Scrollbar(frameDnD, orient=tk.VERTICAL)
sbv.grid(row = 1, column = 7, rowspan = 6, columnspan = 6, sticky = tk.NS)

textarea.configure(yscrollcommand=sbv.set)
sbv.config(command=textarea.yview)

open_button = tk.Button(frameDnD, activebackground = "blue", bg = "white", text = "open", command = load_text_selection)
open_button.grid(row = 7, column = 0, columnspan = 6)

reload_button= tk.Button(frameDnD, activebackground = "red", bg = "white", text = "reload", command = reload_text, width = 46)
reload_button.grid(row = 0, column = 0, columnspan = 6)

graph_check_value = tk.IntVar()
graph_check = tk.Checkbutton(frameDnD, disabledforeground = "yellow", text = "generate the graph", variable = graph_check_value, command = show_graph, onvalue = 1, state = DISABLED)
graph_check.grid(row = 7, column = 0)

help_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Help", command = show_help)
help_option.pack(side = LEFT)

formats_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Formats", command = show_formats)
formats_option.pack(side = LEFT)

problems_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Problems", command = show_problems)
problems_option.pack(side = LEFT)

save_option = tk.Button(optionframe, activebackground = "blue", bg = "white", text = "save", command = save)
save_option.pack(side = LEFT)

task_label = tk.Label(taskframe, text = "Tasks :", justify = tk.CENTER)
task_label.grid(row = 0, column = 1)

problem_value = tk.StringVar()
problem_box = ttk.Combobox(taskframe, values = ["DC","DS","SE","CE", "EE"], state = DISABLED, textvariable = problem_value)
problem_box.bind("<<ComboboxSelected>>", problem_selection)
problem_box.grid(row = 1, column = 0)

query_label = tk.Label(queryframe, text = "query : ")
query_label.grid(row = 0, column = 0)

query_value= tk.StringVar()
query_entry = tk.Entry(queryframe, textvariable = query_value)
query_entry.grid(row = 0, column = 1)

semantic_value = tk.StringVar()
semantic_box = ttk.Combobox(taskframe, values = ["CO","PR","ST","SST","STG","GR","ID"], state = DISABLED, textvariable = semantic_value)
semantic_box.bind("<<ComboboxSelected>>", semantic_selection)
semantic_box.grid(row = 1, column = 2)

solver_label = tk.Label(solverframe, text = "solver : ")
solver_label.grid(row = 0, column = 0)

solver_value = tk.StringVar()
solver = tk.Entry(solverframe, textvariable = solver_value)
solver.grid(row = 0, column = 1)

solver_select_button = tk.Button(solverframe, activebackground = "blue", bg = "white", text = "open", state = DISABLED, command = select_solver)
solver_select_button.grid(row = 0, column = 2)

solver_find_button = tk.Button(solverframe, activebackground = "red", bg = "white", text = "find", state = DISABLED, command = find_solver)
solver_find_button.grid(row = 1, column = 1)

button0 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "no reduction", state = DISABLED, command = ClickReduc0)
button0.pack(side = LEFT)

button1 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 1", state = DISABLED, command = ClickReduc1)
button1.pack(side = LEFT)

button2 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 2", state = DISABLED, command = ClickReduc2)
button2.pack(side = LEFT)

button3 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 3", state = DISABLED, command = ClickReduc3)
button3.pack(side = LEFT,)

button4 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 4", state = DISABLED, command = ClickReduc4)
button4.pack(side = LEFT)

textareaReduc = tk.Text(frameReduction, height=18, width=41)
textareaReduc.grid(row = 1, column = 0, rowspan = 6, columnspan = 6)
textareaReduc.configure(state = "disabled")

sbvR = tk.Scrollbar(frameReduction, orient=tk.VERTICAL)
sbvR.grid(row = 1, column = 7, rowspan = 6, columnspan = 6, sticky = tk.NS)

download_button= tk.Button(frameReduction, activebackground = "red", bg = "white", text = "download", command = download_reduc, width = 46, state = DISABLED)
download_button.grid(row = 0, column = 0, columnspan = 6)

empty_reduc_label = tk.Label(frameReduction, text = " ")
empty_reduc_label.grid(row = 7, column = 0)

textareaReduc.configure(yscrollcommand = sbvR.set)
sbvR.config(command = textareaReduc.yview)

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()