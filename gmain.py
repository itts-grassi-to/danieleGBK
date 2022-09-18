## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import gi
import ast
from motore_backup import *
from dlgConfigurazione import *

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainW(Gtk.Window):
    def __init__(self):
        super().__init__(title="DANIELE BACKUP")
        self.set_default_size(500, 300)
        self.set_border_width(20)
        self.fconf = "./danieleBK.conf"
        self.bks = self.__get_impostazioni(self.fconf)['bks']
        # print(self.bks)
        self.lst_lbl = []
        self.lst_chiavi = []
        # contenitore a griglia
        # grid=Gtk.Grid(column_homogeneous=True,padding=10)
        grid = Gtk.Grid()
        grid.set_border_width(10)

        # oggetti
        self.lstMain = self.__attach_lista()
        grid.add(self.lstMain)
        grid.attach(self.__attach_button(), 0, 1, 1, 1)

        self.add(grid)

        self.th = MotoreBackup(self.fconf)

    def __attach_button(self):
        hbox2 = Gtk.Box(spacing=6)
        button = Gtk.Button.new_with_mnemonic("Nuovo")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_nuovo_clicked)
        hbox2.add(button)

        button = Gtk.Button.new_with_mnemonic("Modifica")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_modifica_clicked)
        hbox2.add(button)
        return hbox2

    def __attach_lista(self):
        lst = Gtk.ListBox()
        lst.set_property("width-request", 300)
        lst.set_property("margin", 10)
        lst.set_property("height-request", 200)
        for chiave in self.bks:
            # print(self.bks[chiave])
            lbl = Gtk.Label(xalign=Gtk.Justification.LEFT)
            lbl.set_markup("<big><b>" + self.bks[chiave]["titolo"] + "</b></big>")

            lst.add(lbl)
            self.lst_lbl.append(lbl)
            self.lst_chiavi.append(chiave)
        return lst

    def __get_impostazioni(self, f):
        with open(f, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
            return d

    def on_nuovo_clicked(self, bt):
        # print("NUOVO")

        w = DlgNuovo(self.fconf)
        w.connect("destroy", Gtk.main_quit)
        w.set_modal(True)
        w.show_all()
        Gtk.main()
        print("fine nuovo")

    def on_modifica_clicked(self, bt):
        # lbl = Gtk.Label(label="T")
        row = self.lstMain.get_selected_row()
        # print(self.lst_lbl[row.get_index()].get_text())
        print(self.lst_chiavi[row.get_index()])
        w = DlgConf(self.fconf, self.lst_chiavi[row.get_index()])
        w.connect("destroy", Gtk.main_quit)
        w.set_modal(True)
        w.show_all()
        Gtk.main()


    def fine(self):
        print("hofinito")
        self.th.thFine=True
        Gtk.main_quit()


win = MainW()

win.connect("destroy", MainW.fine)
win.show_all()
Gtk.main()
