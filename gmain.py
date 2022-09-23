## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import gi
import ast

from dlgConfigurazione import DlgNuovo, DlgConf
from motore_backup import MotoreBackup

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainW(Gtk.Window, MotoreBackup):


    def __init__(self):
        Gtk.Window.__init__(self, title="DANIELE BACKUP")
        MotoreBackup.__init__(self)
        self.set_default_size(500, 300)
        self.set_border_width(20)
        # self.fconf = "./danieleBK.conf"
        self.bks = self.__get_impostazioni(self.fconf)
        # print(self.bks)
        # self.lst_lbl = []
        self.lst_chiavi = []

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.lstMain = self.__get_lista()
        box_outer.pack_start(self.lstMain, True, True, 0)

        box_outer.pack_start(self.__attach_button(), True, True, 0)
        self.add(box_outer)
        # self.th = MotoreBackup(self.fconf)
    def __get_lista(self):
        lst = self.__attach_list()
        self.__attach_rows(lst)
        return lst
    def __attach_list(self):
        listbox = Gtk.ListBox()
        # listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listbox.set_property("height-request", 200)
        listbox.set_property("margin", 10)
        return listbox
    def __attach_rows(self,lst):
        print("Backup: " + str(self.bks['bks']))
        for chiave in self.bks['bks']:
            lst.add(self.__attach_row(chiave))
    def __attach_row(self, ch):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        bk = self.bks['bks'][ch]
        label = Gtk.Label(label=bk['titolo'], xalign=0)
        label.set_property("width-request", 450)
        hbox.pack_start(label, False, True, 0)

        check = Gtk.CheckButton(label=ch)
        check.set_active(bk['attivo'])
        check.connect("toggled", self.__on_toggled_ck)
        hbox.pack_start(check, False, True, 0)

        self.lst_chiavi.append(ch)
        # hbox.pack_start(check, False, True, 0)

        return row

    def __on_toggled_ck(self, ck):
        ch = ck.get_label()
        self.bks['bks'][ch]['attivo'] = ck.get_active()
        with open(self.fconf, "w") as data:
            data.write(str(self.bks))
            data.close()
        self.set_restart_impostazioni()
    def fgmain_old(self):
        # contenitore a griglia

        grid = Gtk.Grid()
        grid.set_border_width(10)

        # oggetti
        self.lstMain = self.__attach_lista()
        grid.add(self.lstMain)
        grid.attach(self.__attach_button(), 0, 1, 1, 1)

        self.add(grid)

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

    def __attach_lista_old(self):
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

        w = DlgNuovo(self)
        w.connect("destroy", Gtk.main_quit)
        w.set_modal(True)
        w.show_all()
        Gtk.main()
        self.lstMain.add(self.__attach_row(self.lst_chiavi.pop()))
        self.show_all()
        print("fine nuovo")
        # self.bks = self.__get_impostazioni(self.fconf)
        # self.lstMain.add(self.__attach_lista())

    def on_modifica_clicked(self, bt):
        w = DlgConf(self)
        w.connect("destroy", Gtk.main_quit)
        w.set_modal(True)
        w.show_all()
        Gtk.main()


    def fine(self):
        print("hofinito")
        self.thFine=True
        Gtk.main_quit()

win = MainW()

win.connect("destroy", MainW.fine)
win.show_all()
Gtk.main()
