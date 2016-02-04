#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Reader.py
#
#  Copyright 2016 ras <riisras@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Aprogram; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
# !/usr/bin/python
import Tkinter as tk
import sqlite3
import tkFont
import ttk
from tkFileDialog import askdirectory

from Methods import *


class GUI(object):

    def __init__(self, master):
        self.master = master
        fontHead = tkFont.Font(family="Arial", size=10, weight=tkFont.BOLD)
        fontBold = tkFont.Font(family="Arial", size=8, weight=tkFont.BOLD)
        fontReg = tkFont.Font(family="Arial", size=8)
        frameN = tk.Frame(master)
        frameN.grid(row=0, padx=5, pady=5)
        frameXBH = tk.Frame(frameN)
        frameXBH.grid(row=0, columnspan=5, padx=5)
        tk.Canvas(frameXBH, borderwidth=0, relief="flat", height=1, width=20, background="#cccccc").grid(row=0)
        tk.Label(frameXBH, text="Forensics Reader", font=fontBold, width=15).grid(row=0, column=1)
        tk.Canvas(frameXBH, borderwidth=0, relief="flat", height=1, width=800, background="#cccccc").grid(row=0,column=2,sticky="WE")
        tk.Label(frameN, text="Directory containing exported files:", font=fontReg).grid(row=1, sticky="W")
        global xbPath
        xbPath = tk.Entry(frameN, text="hhe", width=30, font=fontReg)
        xbPath.grid(row=1, column=1, sticky="W")
        xbBrowse = tk.Button(frameN, text="Browse for folder", font=fontReg, command=lambda: self.get_dir(xbPath))
        xbBrowse.grid(row=1, column=2, sticky="W")
        xbRel = tk.Checkbutton(frameN, text="Save case for later", font=fontReg)
        xbRel.grid(row=1, column=4, sticky="W")
        tk.Canvas(frameN, borderwidth=1, relief="groove", width=800, height=0).grid(row=2, columnspan=5, pady=10)
        btnStart = tk.Button(frameN, text="Start", width=10, command=lambda: self._grid(frameXBH))
        btnStart.grid(row=3, column=3, sticky="E")
        btnCancel = tk.Button(frameN, text="Cancel", width=10, command=lambda: self.cancel_btn())
        btnCancel.grid(row=3, column=4, sticky="W")



    def cancel_btn(self):
        raise SystemExit

    def get_dir(self, xbPath):
        xbPath.delete(0, "end")
        xbPath.insert(1, askdirectory(mustexist=1, title="Please select folder containing exported files").replace("/", "\\"))

    def StartExam(self):  # Order:(db, cursor, hive, TableName, regPath, Key, Category):

        ReadAllReg(db, cursor, xbPath.get() + "\\NTUSER.DAT", "Info", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths", "Typed Urls")  # Typed Paths

        ReadSingleReg(db, cursor, xbPath.get() + "\\SYSTEM", "Info", "Select", "Current", "CurrentControlSet")  # CurrentControlSet

    def _grid(self, master):
        self.StartExam()
        self.create_window(master)

    def create_window(self, master):
        cursor.execute('''SELECT * FROM %s''' % "Info")
        all_rows = cursor.fetchall()
        fo = open("Info.txt", "wb")
        for row in all_rows:
            print('{0} : {1}, {2}, {3}'.format(row[0], row[1], row[2], row[3]))
            fo.writelines('{0} : {1}, {2}, {3}\r\n'.format(row[0], row[1], row[2], row[3]))
        root = tk.Toplevel()
        tree = ttk.Treeview(root)
        tree["columns"] = ("one", "two", "three")
        tree.column("one", width=100)
        tree.column("two", width=100)
        tree.column("three", width=100)
        tree.heading("one", text="coulmn A")
        tree.heading("two", text="column B")
        tree.heading("two", text="column C")
        tree.insert("", 0, text="Line 1", values=("1A", "1b"))
        id2 = tree.insert("", 1, "dir2", text="Dir 2")
        tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))
        ##alternatively:
        tree.insert("", 3, "dir3", text="Dir 3")
        tree.insert("dir3", 3, text=" sub dir 3", values=("3A", " 3B"))
        tree.insert("", 3, "dir4", text="Dir 4")
        tree.insert("dir4", 3, text=" sub dir 4", values=("3A", " 3B"))
        tree.insert("dir4", 3, text=" sub dir 4", values=("33", " 333"))
        tree.pack()
        fo.close()
        root.mainloop()


db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute('''CREATE TABLE Info(Id INTEGER PRIMARY KEY, Name TEXT, Value TEXT,Category TEXT)''')


"""
# print "Mounted Devices:"
    # result2 = ReadAllReg(dirname + r"\SYSTEM", "MountedDevices", db)
    # print "Current controlset: %s" % forensicating.control_set_check(path + r'\SYSTEM')
    # print os_settings(path + r'\SYSTEM', dirname + r'\SOFTWARE')

"""

def main():
    db.commit()
    db.close()



if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)
    app = GUI(root)
    root.mainloop()
