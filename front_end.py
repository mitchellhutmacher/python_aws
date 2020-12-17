import aws_rnw as rnw
import getpass
import os.path
import platform
import tkinter as tk
import webbrowser
from os import path
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


def design_window():
    def credentials_window(user, os):
        def savefile():
            str_to_save = "[default]\n"
            str_to_save += "aws_access_key_id=" + aki_var.get() + "\n"
            str_to_save += "aws_secret_access_key=" + sak_var.get() + "\n"
            if os == "Windows":
                file = open(r"C:\Users\{}\.aws\credentials".format(user), "w")
                file.write(str_to_save)
                file.close()
            else:
                file = open(r"/Users/{}/.aws/credentials".format(user), "w")
                file.write(str_to_save)
                file.close()
            return

        cred_win = tk.Tk()
        et = "In order to access AWS servers, you have to create a credentials"
        et += " file at the file address {}.  If you fill out the fields in "
        et += "this window, then the file will be created by this program.  "
        et += "Information on how to find the required information can be "
        et += "found at: "
        link = "https://docs.aws.amazon.com/cli/latest/"
        link += "userguide/cli-configure-files.html"
        explain = tk.Message(cred_win, text=et)
        explain.grid(row=0, column=0, sticky="w")
        link_txt = tk.Message(cred_win, text=link, fg="blue", cursor="hand2")
        link_txt.grid(row=0, column=1, sticky="s")
        link_txt.bind("<Button-1>", lambda e: webbrowser.open_new(link))

        access_key_id = tk.Label(cred_win, text="aws_access_key_id:")
        access_key_id.grid(row=1, column=0, sticky="e")

        aki_var = tk.StringVar()
        aki = ttk.Entry(cred_win, textvariable=aki_var)
        aki.grid(row=1, column=1)

        secret_access_key = tk.Label(cred_win, text="aws_secret_access_key:")
        secret_access_key.grid(row=2, column=0, sticky="e")

        sak_var = tk.StringVar()
        sak = ttk.Entry(cred_win, textvariable=sak_var)
        sak.grid(row=2, column=1)

        mk_file_btn = ttk.Button(cred_win, text="Save File",
                                 command=savefile)
        mk_file_btn.grid(row=3, column=1)
        return

    def check_credentials():
        os = platform.system()
        user = getpass.getuser()
        if os == "Windows":
            win_file = path.exists(r"C:\Users\{}\.aws\credentials".format(user))
            if win_file is False:
                credentials_window(user, os)
                return
            else:
                return
        else:
            mac_file = path.exists(r"/Users/{}/.aws/credentials".format(user))
            if mac_file is False:
                credentials_window(user, os)
                return
            else:
                return
        return

    def find_bucket_json():
        global file_list
        selections = buckets_sel.curselection()
        # print(selections)
        sel_bucket_list = []
        for choice in selections:
            sel_bucket_list.append(bucket_list[choice])
        files.set(value="")
        file_list = []
        if len(sel_bucket_list) > 0:
            file_list = rnw.get_json_from_bucket(sel_bucket_list)
            files.set(value=file_list)
        return

    def all_bucket_json():
        global file_list
        file_list = rnw.get_json_from_bucket(bucket_list)
        files.set(value=file_list)
        return

    def convert_sel():
        global file_list
        csv_str.set(value="")
        selections = file_sel.curselection()
        sel_file_list = []
        for choice in selections:
            sel_file_list.append(file_list[choice])
        if len(sel_file_list) > 0:
            dicts = rnw.make_json_list(sel_file_list)
            dicts = check_json_format(dicts)
            csv_str.set(value=rnw.make_csv(dicts))
        return

    def convert_all():
        global file_list
        csv_str.set(value="")
        if len(file_list) > 0:
            dicts = rnw.make_json_list(file_list)
            dicts = check_json_format(dicts)
            csv_str.set(value=rnw.make_csv(dicts))
        return

    def preview_csv():

        def prev_close():
            preview_window.destroy()
        preview_window = tk.Tk()
        xscrollbar = tk.Scrollbar(preview_window)
        yscrollbar = tk.Scrollbar(preview_window)
        csv = tk.Message(preview_window, text=csv_str.get())
        csv.grid(row=0, column=0, sticky="w")
        prev_close_btn = ttk.Button(preview_window, text="Close",
                                    command=prev_close)
        prev_close_btn.grid(row=1, column=0)

    def save_csv():
        file = tk.filedialog.asksaveasfile(mode="w", defaultextension=".csv")
        file.write(csv_str.get())
        file.close()
        return

    def close():
        root.destroy()

    root = tk.Tk()
    root.title("Client Feedback")
    my_font = ("calibri", 18)

    buckets_label = ttk.Label(root, text="Buckets", font=my_font)
    buckets_label.grid(row=1, column=0)

    yscrollbar = tk.Scrollbar(root)
    bucket_list = rnw.list_of_buckets()
    buckets = tk.StringVar(value=bucket_list)
    buckets_sel = tk.Listbox(root, selectmode="multiple",
                             yscrollcommand=yscrollbar.set,
                             listvariable=buckets)
    buckets_sel.grid(row=1, column=1, rowspan=2, columnspan=2)
    yscrollbar.config(command=buckets_sel.yview)

    buckets_btn = ttk.Button(root, text="Choose these buckets",
                             command=find_bucket_json)
    buckets_btn.grid(row=1, column=3)

    all_buckets_btn = ttk.Button(root, text="Choose all buckets",
                                 command=all_bucket_json)
    all_buckets_btn.grid(row=2,column=3)

    file_sel_label = ttk.Label(root, text="Files", font=my_font)
    file_sel_label.grid(row=3, column=0, rowspan=2)

    files = tk.StringVar()
    global file_list
    file_list = []
    file_sel = tk.Listbox(root, selectmode="multiple",
                             yscrollcommand=yscrollbar.set,
                             listvariable=files)
    file_sel.grid(row=3, column=1, columnspan=2, rowspan=2)
    yscrollbar.config(command=file_sel.yview)

    file_sel_btn = ttk.Button(root, text="Convert selected files",
                              command=convert_sel)
    file_sel_btn.grid(row=3, column=3)

    all_file_sel_btn = ttk.Button(root, text="Convert all files",
                                  command=convert_all)
    all_file_sel_btn.grid(row=4, column=3)

    csv_str = tk.StringVar(value="")

    preview_btn = ttk.Button(root, text="Preview CSV",
                             command=preview_csv)
    preview_btn.grid(row=5, column=0)

    save_btn = ttk.Button(root, text="Save CSV",
                          command=save_csv)
    save_btn.grid(row=5, column=1)

    close_btn = ttk.Button(root, text="Close",
                           command=close)
    close_btn.grid(row=99, column=99)
    check_credentials()
    root.mainloop()
    return


def check_json_format(dict_list):
    for dict in dict_list:
        try:
            dict["email"]
            dict["includeImportance"]
            dict["template"]
            dict["valueBlocks"]
        except KeyError:
            dict_list.remove(dict)
    return dict_list


if __name__ == "__main__":
    design_window()
