import customtkinter
import tkinter as tk
import os
from PIL import Image
import time
from ctypes import windll, Structure, c_long, byref
from PIL import Image
import webbrowser
from win32con import *
import hashlib
import sys
from keyauth import api
import psutil
import multiprocessing
from multiple_char_detection import m_thread
import subprocess as sp
import signal


#get mouse position for future reference
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
    

#start the class for the window
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #set random variables
        global fov_toggled
        fov_toggled = False
        
        self.attributes('-topmost',True)
        self.overrideredirect(True)
        
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("red")

        self.title("DO - NOT - SHARE")
        self.geometry("600x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        keys = {
            'Left Mouse': "0x01",
            'Right Mouse': "0x02",
            'Mouse 4': "0x05",
            'Mouse 5': "0x06",
        }

        
                
        #define all the functions for the buttons in the UI  
        def move_toggle():
            global move_toggle_val
            move_toggle_val = self.Global_Move_Button1.get()

            if move_toggle_val==1: 
                self.bind('<B1-Motion>',move)

                if move_toggle_val==0:
                    return


        def move(event):
            if move_toggle_val==0:
                return

            else:
                pt = POINT()
                windll.user32.GetCursorPos(byref(pt))
                self.geometry(f"+{pt.x}+{pt.y}")
                print("window >", self.winfo_x(), self.winfo_y())
                print("cursor >", pt.x, pt.y, "\n")



        global minimized
        minimized = False
        def minimize():
            global minimized

            if minimized == False:
                currentalpha = 1
                minimized = True

                while currentalpha > 0:
                    currentalpha -= 0.04
                    time.sleep(0.01)
                    self.attributes("-alpha", currentalpha)

            elif minimized == True:
                currentalpha = 0
                minimized = False
                
                while currentalpha < 1:
                    currentalpha += 0.06
                    time.sleep(0.01)
                    self.attributes("-alpha", currentalpha)

        bindings = [
            [["Insert"], None, minimize],
        ]
        


        #adding the value to the label of the slider

        def getchecksum():
            md5_hash = hashlib.md5()
            file = open(''.join(sys.argv), "rb")
            md5_hash.update(file.read())
            digest = md5_hash.hexdigest()
            return digest


        keyauthapp = api(
            name = "Panthium",
            ownerid = "GnZyq2Rfik",
            secret = "90c42ccbccea2b5fa2478199709a20cf1a3ef07972a891a419be90f4958350b0",
            version = "1.0",
            hash_to_check = getchecksum()
        )

        def keyenter():
            keyauthapp.license(self.Key_Enter.get())
            self.Aimbot_Enabled.configure(state="normal")
            self.Recoil_enabled.configure(state="normal")
            self.Triggerbot_enabled.configure(state="normal")
            self.apply_aimbot.configure(state="normal")
            self.apply_misc.configure(state="normal")
            self.apply_visual.configure(state="normal")
            self.apply_gen.configure(state="normal")


        def Smooth_val(val):
            val = round(val)
            self.Smoothing_Title.configure(text=f"Smoothing - {val}%")

        def FOV_val(val):
            val = round(val)
            self.FOV_Title.configure(text=f"FOV - {val} x {val}px")
        
        def Threshhold_val(val):
            val = round(val)
            self.Threshhold_Title.configure(text=f"Threshhold - {val}")

        def Core_count(val):
            val = round(val)
            self.core_count_title.configure(text=f"Active cores - {val}")
        
        def Dissable_on_headshot():
            print("dissabledonheadshot")
        
        def discord():
            webbrowser.open('https://panthium.xyz/')

        def force_quit():
            self.Aimbot_Enabled.toggle()
            exit()



        #disable all the buttons without the aim toggle enabled

        def repp():
            global p2
            global p3
            global p4
            global p5

            p2 = multiprocessing.Process(target=m_thread)
            p3 = multiprocessing.Process(target=m_thread)
            p4 = multiprocessing.Process(target=m_thread)
            p5 = multiprocessing.Process(target=m_thread)

            p2.start()
            print("running on core 2")
            p3.start()
            print("running on core 3")
            p4.start()
            print("running on core 4")
            p5.start()
            print("running on core 5")

        global apply_check
        apply_check = 0


        global extProc
        extProc = None


        def Aim_On():
            global extProc
            aimbval = self.Aimbot_Enabled.get()
            if aimbval==1:
                aimbval="normal"
                self.FOV_Slider.configure(state=aimbval)
                self.FOV_Title.configure(state=aimbval)
                self.Smoothing_Slider.configure(state=aimbval)
                self.Smoothing_Title.configure(state=aimbval)
                self.Aimbot_Key.configure(state=aimbval)
                self.Threshhold_Slider.configure(state=aimbval)
                self.Threshhold_Title.configure(state=aimbval)
                self.core_count.configure(state=aimbval)
                self.core_count_title.configure(state=aimbval)
                self.core_count_warning.configure(state=aimbval)
                self.Aimbone.configure(state=aimbval)
                self.alt_aimbone.configure(state=aimbval)
                self.ConfigList.configure(state=aimbval)
                self.ConfigInput.configure(state=aimbval)
                self.ConfigLoad.configure(state=aimbval)
                self.ConfigSave.configure(state=aimbval)
                self.ConfigDelete.configure(state=aimbval)
                self.ConfigCreate.configure(state=aimbval)
                self.BhopToggle.configure(state=aimbval)
                self.DebugToggle.configure(state=aimbval)
            else:
                aimbval="disabled"
                self.FOV_Slider.configure(state=aimbval)
                self.FOV_Title.configure(state=aimbval)
                self.Smoothing_Slider.configure(state=aimbval)
                self.Smoothing_Title.configure(state=aimbval)
                self.Aimbot_Key.configure(state=aimbval)
                self.Threshhold_Slider.configure(state=aimbval)
                self.Threshhold_Title.configure(state=aimbval)
                self.core_count.configure(state=aimbval)
                self.core_count_title.configure(state=aimbval)
                self.core_count_warning.configure(state=aimbval)
                self.Aimbone.configure(state=aimbval)
                self.alt_aimbone.configure(state=aimbval)
                self.ConfigList.configure(state=aimbval)
                self.ConfigInput.configure(state=aimbval)
                self.ConfigLoad.configure(state=aimbval)
                self.ConfigSave.configure(state=aimbval)
                self.ConfigDelete.configure(state=aimbval)
                self.ConfigCreate.configure(state=aimbval)
                self.BhopToggle.configure(state=aimbval)
                self.DebugToggle.configure(state=aimbval)

                
            if self.Aimbot_Enabled.get() == 1:
                extProc = sp.Popen(['python','robotty_zaddy.py', 
                                    str(int(self.Smoothing_Slider.get())), 
                                    str(int(self.FOV_Slider.get())), 
                                    keys[self.Aimbot_Key.get()], 
                                    self.Aimbone.get(),
                                    str(int(self.Threshhold_Slider.get())),
                                    str(self.BhopToggle.get()),
                                    str(self.alt_aimbone.get()),
                                    str(self.Triggerbot_enabled.get()),
                                    keys[self.triggerbot_key.get()],
                                    str(self.alt_aimbone.get()),
                                    str(self.alt_aimbone_select.get()),
                                    ])
            
            elif self.Aimbot_Enabled.get() != 1 and extProc is not None:
                sp.Popen("TASKKILL /F /PID {pid} /T".format(pid=extProc.pid))
                extProc = None

            

        def apply_aim():
            self.Aimbot_Enabled.toggle()
            self.Aimbot_Enabled.toggle()

            

        



            # if self.Aimbot_Enabled.get() == 1:
                
            #     aim_running = True
            #     print("aimbot on")  
            #     repp()
                
            
            # if self.Aimbot_Enabled.get() == 0:

            #     print("aimbot not running")
            #     aim_running = False      

            #     p2.terminate()
            #     p3.terminate()
            #     p4.terminate()
            #     p5.terminate()

            # print(self.Aimbot_Enabled.get())

        def alt_aimbone_enable():
            alt_aimbval = self.alt_aimbone.get()
            if alt_aimbval==1:
                alt_aimbval="normal"
                self.alt_aimbone_select.configure(state=alt_aimbval)
                self.Alt_Aimbot_Key.configure(state=alt_aimbval)
            else:
                alt_aimbval="disabled"
                self.alt_aimbone_select.configure(state=alt_aimbval)
                self.Alt_Aimbot_Key.configure(state=alt_aimbval)
            print(self.Aimbot_Enabled.get())

        def Trigger_On():
            triggerval = self.Triggerbot_enabled.get()
            if triggerval==1:
                triggerval="normal"
                self.triggerbot_key.configure(state=triggerval)
                self.triggerbot_key.configure(state=triggerval)
                self.Trigger_bone.configure(state=triggerval)
            else:
                triggerval="disabled"
                self.triggerbot_key.configure(state=triggerval)
                self.triggerbot_key.configure(state=triggerval)
                self.Trigger_bone.configure(state=triggerval)

        def Recoil_On():
            recoilval = self.Recoil_enabled.get()
            if recoilval==1:
                recoilval="normal"
                self.Recoil_sens.configure(state=recoilval)
                self.Recoil_choice.configure(state=recoilval)
                self.Recoil_sens_input.configure(state=recoilval)
            else:
                recoilval="disabled"
                self.Recoil_sens.configure(state=recoilval)
                self.Recoil_choice.configure(state=recoilval)
                self.Recoil_sens_input.configure(state=recoilval)

        # load images with light and dark mode image
        #image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"Assets")

        self.aim_image = customtkinter.CTkImage(light_image=Image.open(os.path.join("aimlogoLIGHT.png")),
                                                dark_image=Image.open(os.path.join("aimlogoDARK.png")), size=(50, 50))
        self.aim_misc_image = customtkinter.CTkImage(light_image=Image.open(os.path.join( "miscaimLIGHT.png")),
                                                dark_image=Image.open(os.path.join("miscaimDARK.png")), size=(50, 50))
        self.visuals_image = customtkinter.CTkImage(light_image=Image.open(os.path.join("visualsLIGHT.png")),
                                                dark_image=Image.open(os.path.join("visualsDARK.png")), size=(50, 50))
        self.gen_image = customtkinter.CTkImage(light_image=Image.open(os.path.join("generallogoLIGHT.png")),
                                                dark_image=Image.open(os.path.join("generallogoDARK.png")), size=(50, 50))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", compound="right",
        font=("Watchword Bold Demo", 14))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.navigation_frame_button = customtkinter.CTkButton(self.navigation_frame, text="panthium <3", command=discord, fg_color='gray17', hover_color='gray17', font=("Watchword Bold Demo", 15), text_color='gray99', width=1)
        self.navigation_frame_button.grid(row=0, column=0, padx=20, pady=20)

        self.Global_Move_Button1 = customtkinter.CTkSwitch(self.navigation_frame, text="", command=move_toggle)
        self.Global_Move_Button1.place(x=20, y=393)

        self.Key_Enter = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Key", show="♡", width=90)
        self.Key_Enter.place(x=20, y=423)

        self.Key_Button = customtkinter.CTkButton(self.navigation_frame, text="Enter", width = 30, command=keyenter)
        self.Key_Button.place(x=118, y=423)

        #create all the tabs
        self.aim_tab = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Aimbot",
        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        image=self.aim_image, anchor="w", command=self.aim_tab_event, font=("Watchword Bold Demo", 13))

        self.aim_tab.grid(row=1, column=0, sticky="ew")


        self.aim_misc_tab = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Aim Misc         ",
        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        image=self.aim_misc_image, anchor="w", command=self.aim_misc_tab_event, font=("Watchword Bold Demo", 13))

        self.aim_misc_tab.grid(row=2, column=0, sticky="ew")


        self.visuals_tab = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, width=190, border_spacing=10, text="Visuals",
        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        image=self.visuals_image, anchor="w", command=self.visuals_tab_event, font=("Watchword Bold Demo", 13))

        self.visuals_tab.grid(row=3, column=0)


        self.gen_tab = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, width=190, border_spacing=10, text="General",
        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        image=self.gen_image, anchor="w", command=self.gen_tab_event, font=("Watchword Bold Demo", 13))

        self.gen_tab.place(x=0, y=290)


        #add buttons below the tabs
        self.force_quit = customtkinter.CTkButton(self.navigation_frame, text = "Force Quit", command=force_quit, font=("Watchword Bold Demo", 14))
        self.force_quit.place(x=20, y=459)

        # create home frame
        self.aim_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.aim_frame.grid_columnconfigure(0, weight=1)


        #create all the buttons in the aimbot tab
        self.Aimbot_Enabled = customtkinter.CTkSwitch(self.aim_frame, text="Enable Aimbot", font=("Watchword Bold Demo", 14), command=Aim_On, state="disabled")
        self.Aimbot_Enabled.place(x=20, y=20)

        self.FOV_Slider = customtkinter.CTkSlider(self.aim_frame, from_=30, to=300, command=FOV_val, state="disabled")
        self.FOV_Slider.place(x=15, y=65)

        self.FOV_Title = customtkinter.CTkLabel(self.aim_frame, text = "FOV - 165 x 165px", font=("Watchword Bold Demo", 14), state="disabled")
        self.FOV_Title.place(x=225, y=58)
        
        self.Smoothing_Slider = customtkinter.CTkSlider(self.aim_frame, from_=1, to=100, command=Smooth_val, state="disabled")
        self.Smoothing_Slider.place(x=15, y=100)

        self.Smoothing_Title = customtkinter.CTkLabel(self.aim_frame, text = "Smoothing - 50%", font=("Watchword Bold Demo", 14,), state="disabled")
        self.Smoothing_Title.place(x=225, y=93)

        self.Aimbot_Key = customtkinter.CTkOptionMenu(self.aim_frame, values=["Left Mouse", "Right Mouse", "Mouse 4", "Mouse 5"], state="disabled", font=("Watchword Bold Demo", 12))
        self.Aimbot_Key.place(x=20, y=133)

        self.Threshhold_Slider = customtkinter.CTkSlider(self.aim_frame, from_=0, to=10, command=Threshhold_val, state="disabled")
        self.Threshhold_Slider.place(x=15, y=175)
        self.Threshhold_Slider.set(0)

        self.Threshhold_Title = customtkinter.CTkLabel(self.aim_frame, text = "Aim Threshhold - 0", font=("Watchword Bold Demo", 14), state="disabled")
        self.Threshhold_Title.place(x=225, y=167)

        self.Aimbone = customtkinter.CTkOptionMenu(self.aim_frame, values = ["Head", "Neck", "Body"], state="disabled", font=("Watchword Bold Demo", 12))
        self.Aimbone.place(x=20, y=205)

        self.alt_aimbone = customtkinter.CTkSwitch(self.aim_frame, text="Alternate Aimbone", font=("Watchword Bold Demo", 12), state="disabled", command=alt_aimbone_enable)
        self.alt_aimbone.place(x=20, y=245)

        self.alt_aimbone_select = customtkinter.CTkOptionMenu(self.aim_frame, values = ["Head", "Neck", "Body"], state="disabled", font=("Watchword Bold Demo", 12), width=100)
        self.alt_aimbone_select.place(x=20, y=280)

        self.Alt_Aimbot_Key = customtkinter.CTkOptionMenu(self.aim_frame, values=["Left Mouse", "Right Mouse", "Mouse 4", "Mouse 5"], state="disabled", font=("Watchword Bold Demo", 12), width=100)
        self.Alt_Aimbot_Key.place(x=130, y=280)

        self.core_count = customtkinter.CTkSlider(self.aim_frame, from_=1, to=psutil.cpu_count(logical=True), command=Core_count, state="disabled")
        self.core_count.place(x=15, y=325)

        self.core_count_title = customtkinter.CTkLabel(self.aim_frame, text = f"Active cores - {psutil.cpu_count(logical=True) - 2}", font=("Watchword Bold Demo", 14), state="disabled")
        self.core_count_title.place(x=225, y=318)

        self.core_count_warning = customtkinter.CTkLabel(self.aim_frame, text = f"", font=("Watchword Bold Demo", 10), state="disabled")
        self.core_count_warning.place(x=20, y=355)

        self.core_count_warning.configure(text =f"You currently have {psutil.cpu_count(logical=True)} cores on your PC, and we always      \nreccomend using 1 to 2 cores less than you have available\nto leave space for other programs, and retain FPS ingame")
        self.core_count.set(psutil.cpu_count(logical=True) - 2)


        #define the aim misc frame
        self.aim_misc_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #create all the buttons for the triggerbot
        self.Triggerbot_enabled = customtkinter.CTkSwitch(self.aim_misc_frame, text="Enable Triggerbot", font=("Watchword Bold Demo", 14), command=Trigger_On, state="disabled")
        self.Triggerbot_enabled.place(x=20, y=20)

        self.triggerbot_key = customtkinter.CTkOptionMenu(self.aim_misc_frame, values=["Left Mouse", "Right Mouse", "Mouse 4", "Mouse 5"], state="disabled", font=("Watchword Bold Demo", 12))
        self.triggerbot_key.place(x=20, y=57)

        self.Trigger_bone = customtkinter.CTkOptionMenu(self.aim_misc_frame, values=["Head", "Body", "Legs", "Any"], state="disabled", font=("Watchword Bold Demo", 12))
        self.Trigger_bone.place(x=20, y=92)
        self.Trigger_bone.set("Any")


        #create all the buttons for the recoil control
        self.Recoil_enabled = customtkinter.CTkSwitch(self.aim_misc_frame, text="Enable Recoil Control", font=("Watchword Bold Demo", 14), command=Recoil_On, state="disabled")
        self.Recoil_enabled.place(x=20, y=180)

        self.Recoil_sens = customtkinter.CTkEntry(self.aim_misc_frame, placeholder_text="Ingame Sensitivity", font=("Watchword Bold Demo", 12))
        self.Recoil_sens.place(x=20, y=220)

        self.Recoil_sens_input = customtkinter.CTkButton(self.aim_misc_frame, text="Enter", width=50, font=("Watchword Bold Demo", 12), state="disabled")
        self.Recoil_sens_input.place(x=170, y=220)

        self.Recoil_choice = customtkinter.CTkOptionMenu(self.aim_misc_frame, values=["Soldier 76", "Cassidy [Alt Fire]"], font=("Watchword Bold Demo", 12))
        self.Recoil_choice.place(x=20, y=260)

        self.Recoil_choice.configure(state="disabled")


        #define the visuals frame
        self.visuals_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #create all the butons inside the visuals frame

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.visuals_frame, values=["Dark", "Light"],command=self.change_appearance_mode_event, font=("Watchword Bold Demo", 12))
        self.appearance_mode_menu.place(x=20, y=20)



        #define the general frame
        self.general_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")


        #create all the buttons inside the general frame
        self.ConfigList = customtkinter.CTkOptionMenu(self.general_frame, values = [], width=200, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigList.place(x=20, y=20)

        self.ConfigInput = customtkinter.CTkEntry(self.general_frame, placeholder_text="Config name", width=160, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigInput.place(x=230, y=20)

        self.ConfigLoad = customtkinter.CTkButton(self.general_frame, text="Load", width=60, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigLoad.place(x=20, y=60)

        self.ConfigSave = customtkinter.CTkButton(self.general_frame, text="Save", width=60, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigSave.place(x=89, y=60)

        self.ConfigDelete = customtkinter.CTkButton(self.general_frame, text="Delete", width=60, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigDelete.place(x=158, y=60)

        self.ConfigCreate = customtkinter.CTkButton(self.general_frame, text="Create", width=160, font=("Watchword Bold Demo", 12), state="disabled")
        self.ConfigCreate.place(x=230, y=60)

        self.BhopToggle = customtkinter.CTkSwitch(self.general_frame, text="Bhop", font=("Watchword Bold Demo", 14), state="disabled")
        self.BhopToggle.place(x=20, y=100)

        self.DebugToggle = customtkinter.CTkSwitch(self.general_frame, text="Debug mode", font=("Watchword Bold Demo", 14), state="disabled")
        self.DebugToggle.place(x=20, y=135)

        #create apply buttons

        self.apply_aimbot = customtkinter.CTkButton(self.aim_frame, text="Apply", width = 75, font=("Watchword Bold Demo", 12), state="disabled", command=apply_aim)
        self.apply_aimbot.place(x=325, y=465)

        self.apply_misc = customtkinter.CTkButton(self.aim_misc_frame, text="Apply", width = 75, font=("Watchword Bold Demo", 12), state="disabled", command=apply_aim)
        self.apply_misc.place(x=325, y=465)

        self.apply_visual = customtkinter.CTkButton(self.visuals_frame, text="Apply", width = 75, font=("Watchword Bold Demo", 12), state="disabled", command=apply_aim)
        self.apply_visual.place(x=325, y=465)

        self.apply_gen = customtkinter.CTkButton(self.general_frame, text="Apply", width = 75, font=("Watchword Bold Demo", 12), state="disabled", command=apply_aim)
        self.apply_gen.place(x=325, y=465)

        self.select_frame_by_name("Aimbot")


        
    #create the function to change tabs
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.aim_tab.configure(fg_color=("gray75", "gray25") if name == "Aimbot" else "transparent")
        self.aim_misc_tab.configure(fg_color=("gray75", "gray25") if name == "Triggerbot         " else "transparent")
        self.visuals_tab.configure(fg_color=("gray75", "gray25") if name == "Visuals" else "transparent")
        self.gen_tab.configure(fg_color=("gray75", "gray25") if name == "General" else "transparent")

        # show selected frame
        if name == "Aimbot":
            self.aim_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.aim_frame.grid_forget()
        if name == "Triggerbot         ":
            self.aim_misc_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.aim_misc_frame.grid_forget()
        if name == "Visuals":
            self.visuals_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.visuals_frame.grid_forget()
        if name == "General":
            self.general_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.general_frame.grid_forget()
    
    def aim_tab_event(self):
        self.select_frame_by_name("Aimbot")

    def aim_misc_tab_event(self):
        self.select_frame_by_name("Triggerbot         ")

    def visuals_tab_event(self):
        self.select_frame_by_name("Visuals")

    def gen_tab_event(self):
        self.select_frame_by_name("General")

    def apply():
        print("apply")

    def change_appearance_mode_event(self, new_appearance_mode):
        if new_appearance_mode=='Dark':
            self.navigation_frame_button.configure(fg_color='gray17', hover_color='gray17', text_color='gray99')
        else:
            self.navigation_frame_button.configure(fg_color='gray85', hover_color='gray85', text_color='gray1')
        customtkinter.set_appearance_mode(new_appearance_mode)

    
# keycheck()

def main_func():
    while True:
        app = App()
        app.mainloop()



if __name__ == '__main__':

    multiprocessing.freeze_support()

    p1 = multiprocessing.Process(target=main_func)
    p1.start()
    print("running on core 1")
    p1.join()