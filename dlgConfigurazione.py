## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import gi
import ast
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# from motore_backup import MotoreBackup


class Msg(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Messaggio", transient_for=parent, flags=0)
        # self.add_buttons(
        #    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        # )

        self.set_default_size(150, 100)
        self.__msg = ""
        self.label = Gtk.Label(label=self.__msg, margin=30)

        box = self.get_content_area()
        box.add(self.label)
        self.set_modal(True)
        # self.show_all()

    def set_msg(self, msg):
        self.label.set_text(msg)
        self.show_all()
    # self.run()


class DlgNuovo(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="Nuovo backups")
        # self.fconf = fconf
        # with open(self.fconf, "r") as data:
        #    self.bks = ast.literal_eval(data.read())
        #    data.close()
        self.set_default_size(400, 300)
        # self.set_border_width(10)

        self.parent = parent
        # print(self.parent.bks)
        grid = Gtk.Grid()

        lbl = Gtk.Label(label="Inserisci codice")
        lbl.set_property("margin", 10)
        self.txtCodice = Gtk.Entry()
        self.txtCodice.set_property("width-request", 100)
        self.txtCodice.set_property("margin", 10)
        # self.txtCodice.set_property("height-request",200)
        grid.attach(lbl, 0, 0, 1, 1)
        grid.attach(self.txtCodice, 1, 0, 1, 1)

        lbl = Gtk.Label(label="Inserisci Titolo")
        lbl.set_property("margin", 10)
        self.txtTitolo = Gtk.Entry()
        self.txtTitolo.set_property("width-request", 200)
        self.txtTitolo.set_property("margin", 10)
        grid.attach(lbl, 0, 1, 1, 1)
        grid.attach(self.txtTitolo, 1, 1, 1, 1)

        # *************** pulsantiera
        hbox = Gtk.Box(margin=10, spacing=6)
        # hbox.set_property("height-request", 200)

        button = Gtk.Button.new_with_mnemonic("Annulla")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_annulla_clicked)
        hbox.add(button)

        button = Gtk.Button.new_with_mnemonic("Salva")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_salva_clicked)
        hbox.add(button)
        grid.attach(hbox, 1, 2, 1, 1)

        self.add(grid)

    def pulisci(self, s):
        s = s.replace("à", "a")
        s = s.replace("è", "e")
        s = s.replace("é", "e")
        s = s.replace("ì", "i")
        s = s.replace("ò", "o")
        s = s.replace("ù", "u")
        s = s.replace("À", "a")
        s = s.replace("È", "e")
        s = s.replace("É", "e")
        s = s.replace("Ì", "i")
        s = s.replace("Ò", "o")
        s = s.replace("Ù", "o")
        return s

    def __esisteCodice(self, s):
        # print("esisteCodice")
        return s in self.parent.bks['bks']

    def __salvaNuovo(self, ch, titolo):
        # print("salvaNuovo")
        # self.bks['bks'] = ch
        self.parent.bks['bks'][ch] = {
                'attivo': True ,'titolo': titolo,
                'dirDA': {'remoto': False, 'da': '', 'mnt': ch+"DA"},
                'dirTO': {'remoto': False, 'to': '', 'mnt': ch+"TO"},
                'cron': {'minuto': '1', 'ora': '0', 'giorno': '1', 'mese': '1', 'settimana': [1, 2]}
            }
        self.parent.lst_chiavi.append(ch)
        os.system("mkdir -p "+self.parent.bks['bks'][ch]['dirDA']['mnt'])
        os.system("mkdir -p "+self.parent.bks['bks'][ch]['dirTO']['mnt'])
        with open(self.parent.fconf, "w") as data:
            data.write(str(self.parent.bks))
            data.close()
    def on_annulla_clicked(self, bt):
        # print("annulla")
        self.destroy()

    def on_salva_clicked(self, bt):
        # print("Salva")
        self.msg = Msg(self)
        if self.txtCodice.get_text().isalpha():
            ch = self.pulisci(self.txtCodice.get_text())
            if self.__esisteCodice(ch):
                self.msg.set_msg("Codice esistente")
            else:
                titolo = self.txtTitolo.get_text()
                if len(titolo) == 0:
                    self.msg.set_msg("Inserisci il titolo")
                else:
                    self.__salvaNuovo(ch, titolo)
                    self.destroy()
        else:
            self.msg.set_msg("NON puoi inserire nel codice caratteri diversi da quelli dell'alfabeto")


class DlgConf(Gtk.Window):
    # def __init__(self, fconf, chDiz, th):
    def __init__(self, parent):
        # print(chDiz)
        self.fconf = parent.fconf
        self.chDiz = parent.lst_chiavi[parent.lstMain.get_selected_row().get_index()]
        self.parent=parent
        with open(self.fconf, "r") as data:
            self.bks = ast.literal_eval(data.read())
            data.close()
        self.bk = self.bks['bks'][self.chDiz]
        # print(self.bk)
        super().__init__(title="MODIFICA I PARAMETRI DI BACKUP DI " + self.bk['titolo'])
        self.set_default_size(800, 300)
        self.set_border_width(10)
        box = Gtk.Grid()
        self.nb = Gtk.Notebook()
        self.nb.set_property("width-request", 780)
        self.nb.set_property("height-request", 260)
        # self.add(self.nb)
        box.attach(self.nb, 0, 0, 1, 1)

        self.__prima_pagina()
        self.__seconda_pagina()
        self.__terzaPagina()
        # self.add(self.__attachButton())
        box.attach(self.__attach_button(), 0, 1, 1, 1)
        # label = Gtk.Label(label="This is a dialog to display additional information")

        # box = self.get_content_area()
        # box.add(label)
        self.add(box)
        self.show_all()

    # ************************** DESTINAZIONE ********************************
    def __terzaPagina(self):
        # seconda pagina
        pg2 = Gtk.Grid()
        pg2.set_border_width(5)
        pg2.set_property("width-request", 300)
        # pg2.set_property("height-request",150)
        larg1 = 90

        h = Gtk.Box(spacing=10)
        rdLocaleTO = Gtk.RadioButton.new_with_label_from_widget(None, "Locale")
        rdLocaleTO.set_property("width-request", larg1)
        rdLocaleTO.connect("toggled", self.on_rd_toggled_to, "loc")
        h.add(rdLocaleTO)

        self.txtLocPathTO = Gtk.Entry(text="", editable=False)
        self.txtLocPathTO.set_property("max-width-chars", 80)
        h.add(self.txtLocPathTO)

        self.btLocPathTO = Gtk.Button.new_with_mnemonic("----")
        self.btLocPathTO.set_property("width-request", 25)
        self.btLocPathTO.set_property("height-request", 15)
        self.btLocPathTO.connect("clicked", self.on_folder_clicked)
        h.add(self.btLocPathTO)
        pg2.attach(h, 0, 0, 1, 1)

        l = Gtk.HSeparator()
        l.set_property("height-request", 10)
        l.set_property("margin", 10)
        pg2.attach(l, 0, 1, 4, 1)

        h = Gtk.Box(spacing=10)
        self.rdRemotoTO = Gtk.RadioButton.new_with_label_from_widget(rdLocaleTO, "Remoto")
        self.rdRemotoTO.set_property("width-request", larg1)
        # rdRemoto.connect("toggled", self.on_rd_toggled, "2")
        h.add(self.rdRemotoTO)
        h.add(Gtk.Label(label="Host", width_request=50, xalign=1))
        self.txtHostTO = Gtk.Entry(text="")
        # pg2.attach(self.utente,2,1,1,1)
        h.add(self.txtHostTO)
        pg2.attach(h, 0, 2, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Utente", width_request=50, xalign=1))
        self.txtUtenteTO = Gtk.Entry(text="")
        h.add(self.txtUtenteTO)
        pg2.attach(h, 0, 3, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Path", width_request=50, xalign=1))
        self.txtRemPathTO = Gtk.Entry(text="", max_width_chars=80)
        h.add(self.txtRemPathTO)
        pg2.attach(h, 0, 4, 1, 1)

        self.nb.append_page(pg2, Gtk.Label(label="DESTINAZIONE"))

        self.__init_origine_to()

    def __init_origine_to(self):
        if self.bk['dirTO']['remoto']:
            self.rdRemotoTO.set_active(True)
            i = self.bk['dirTO']['to'].find("@")
            if i != -1:
                self.txtUtenteTO.set_text(self.bk['dirTO']['to'][:i])
                ii = self.bk['dirTO']['to'].find(":")
                if ii != -1:
                    self.txtHostTO.set_text(self.bk['dirTO']['to'][i + 1:ii])
                    self.txtRemPathTO.set_text(self.bk['dirTO']['to'][ii + 1:])
        else:
            self.txtLocPathTO.set_text(self.bk['dirTO']['to'])

    def on_rd_toggled_to(self, rd, name):
        if rd.get_active():
            self.btLocPathTO.set_sensitive(True)
            self.txtHostTO.set_editable(False)
            self.txtUtenteTO.set_editable(False)
            self.txtRemPathTO.set_editable(False)
        else:
            self.txtHostTO.set_editable(True)
            self.txtUtenteTO.set_editable(True)
            self.txtRemPathTO.set_editable(True)
            self.btLocPathTO.set_sensitive(False)

    # ************************** ORIGINE ********************************
    def __seconda_pagina(self):
        # seconda pagina
        pg2 = Gtk.Grid()
        pg2.set_border_width(5)
        pg2.set_property("width-request", 300)
        # pg2.set_property("height-request",150)
        larg1 = 90

        h = Gtk.Box(spacing=10)
        rdLocale = Gtk.RadioButton.new_with_label_from_widget(None, "Locale")
        rdLocale.set_property("width-request", larg1)
        rdLocale.connect("toggled", self.on_rd_toggled, "loc")
        h.pack_start(rdLocale, True, True, 0)
        # h.add(rdLocale)
        # pg2.attach(rdLocale,0,0,1,1)

        self.txtLocPathDA = Gtk.Entry(text="", editable=False)
        self.txtLocPathDA.set_property("max-width-chars", 80)
        h.pack_start(self.txtLocPathDA, True, True, 0)
        # h.add(locPath)
        # pg2.attach(locPath,1,0,2,1)
        self.btLocPath = Gtk.Button.new_with_mnemonic("---")
        self.btLocPath.set_property("width-request", 25)
        self.btLocPath.set_property("height-request", 15)
        self.btLocPath.connect("clicked", self.on_folder_clicked)
        h.pack_start(self.btLocPath, False, True, 0)
        # h.add(button)
        # pg2.attach(button,3,0,1,1)
        pg2.attach(h, 0, 0, 1, 1)

        l = Gtk.HSeparator()
        l.set_property("height-request", 10)
        l.set_property("margin", 10)
        pg2.attach(l, 0, 1, 4, 1)

        h = Gtk.Box(spacing=10)
        self.rdRemotoDA = Gtk.RadioButton.new_with_label_from_widget(rdLocale, "Remoto")
        self.rdRemotoDA.set_property("width-request", larg1)
        # rdRemotoDA.connect("toggled", self.on_rd_toggled, "2")
        h.add(self.rdRemotoDA)
        h.add(Gtk.Label(label="Host", width_request=50, xalign=1))
        self.txtHostDA = Gtk.Entry(text="")
        # pg2.attach(self.utente,2,1,1,1)
        h.add(self.txtHostDA)
        pg2.attach(h, 0, 2, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Utente", width_request=50, xalign=1))
        self.txtUtenteDA = Gtk.Entry(text="")
        h.add(self.txtUtenteDA)
        pg2.attach(h, 0, 3, 1, 1)

        h = Gtk.Box(spacing=10)
        h.add(Gtk.Label(label="", width_request=larg1))
        h.add(Gtk.Label(label="Path", width_request=50, xalign=1))
        self.txtRemPathDA = Gtk.Entry(text="", max_width_chars=80)
        # self.txtRemPathDA.set_property("max-width-chars", 35)
        h.add(self.txtRemPathDA)
        pg2.attach(h, 0, 4, 1, 1)

        self.nb.append_page(pg2, Gtk.Label(label="ORIGINE"))

        self.__init_origineDA()

    def __init_origineDA(self):
        if self.bk['dirDA']['remoto']:
            self.rdRemotoDA.set_active(True)
            i = self.bk['dirDA']['da'].find("@")
            if i != -1:
                self.txtUtenteDA.set_text(self.bk['dirDA']['da'][:i])
                ii = self.bk['dirDA']['da'].find(":")
                if ii != -1:
                    self.txtHostDA.set_text(self.bk['dirDA']['da'][i + 1:ii])
                    self.txtRemPathDA.set_text(self.bk['dirDA']['da'][ii + 1:])
        else:
            self.txtLocPathDA.set_text(self.bk['dirDA']['da'])
    def on_rd_toggled(self, rd, name):
        if rd.get_active():
            self.btLocPath.set_sensitive(True)
            self.txtHostDA.set_editable(False)
            self.txtUtenteDA.set_editable(False)
            self.txtRemPathDA.set_editable(False)
        else:
            self.btLocPath.set_sensitive(False)
            self.txtHostDA.set_editable(True)
            self.txtUtenteDA.set_editable(True)
            self.txtRemPathDA.set_editable(True)

    # *************************** GENERALE *****************************
    def __prima_pagina(self):
        # prima pagina

        self.generale = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)# Gtk.Grid(spacing=10)
        self.generale.set_border_width(15)
        # ************************** ore cron
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, width_request=20)
        lbl = Gtk.Label(label='ORA')
        vbox.pack_start(lbl, False, True, 0)
        self.txtCronOra = Gtk.Entry(text=self.bk['cron']['ora'], editable=True, max_length=2)
        self.txtCronOra.set_width_chars(2)
        vbox.pack_start(self.txtCronOra, False, True, 0)
        self.generale.add(vbox)
        # ************************** minuti cron
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, width_request=20)
        lbl = Gtk.Label(label='MIN')
        vbox.pack_start(lbl, False, True, 0)
        self.txtCronMinuto = Gtk.Entry(text=self.bk['cron']['minuto'], editable=True, max_length=2)
        self.txtCronMinuto.set_width_chars(2)
        vbox.pack_start(self.txtCronMinuto, False, True, 0)
        # self.generale.attach(vbox, 0, 0, 1, 1)
        self.generale.add(vbox)
        # ************************** giorno cron
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        lbl = Gtk.Label(label='GIO')
        vbox.pack_start(lbl, False, True, 0)
        self.txtCronGiorno = Gtk.Entry(text=self.bk['cron']['giorno'], editable=True, max_length=2)
        self.txtCronGiorno.set_width_chars(2)
        vbox.pack_start(self.txtCronGiorno, False, True, 0)
        self.generale.add(vbox)
        # ************************** mese cron
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        lbl = Gtk.Label(label='MESE')
        vbox.pack_start(lbl, False, True, 0)
        self.txtCronMese = Gtk.Entry(text=self.bk['cron']['mese'], editable=True, max_length=2)
        self.txtCronMese.set_width_chars(2)
        vbox.pack_start(self.txtCronMese, False, True, 0)
        self.generale.add(vbox)
        # ************************** settimana cron
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        lbl = Gtk.Label(label='SETTIMANA')
        vbox.pack_start(lbl, False, True, 0)
        self.txtCronSettimanaLun = Gtk.CheckButton(label='Lunedì')
        self.txtCronSettimanaLun.set_active(self.__is_active(1))
        vbox.pack_start(self.txtCronSettimanaLun, False, True, 0)
        self.txtCronSettimanaMar = Gtk.CheckButton(label='Martedì')
        self.txtCronSettimanaMar.set_active(self.__is_active(2))
        vbox.pack_start(self.txtCronSettimanaMar, False, True, 0)
        self.txtCronSettimanaMer = Gtk.CheckButton(label='Mercoledì')
        self.txtCronSettimanaMer.set_active(self.__is_active(3))
        vbox.pack_start(self.txtCronSettimanaMer, False, True, 0)
        self.txtCronSettimanaGio = Gtk.CheckButton(label='Giovedì')
        self.txtCronSettimanaGio.set_active(self.__is_active(4))
        vbox.pack_start(self.txtCronSettimanaGio, False, True, 0)
        self.txtCronSettimanaVen = Gtk.CheckButton(label='Venerdì')
        self.txtCronSettimanaVen.set_active(self.__is_active(5))
        vbox.pack_start(self.txtCronSettimanaVen, False, True, 0)
        self.txtCronSettimanaSab = Gtk.CheckButton(label='Sabato')
        self.txtCronSettimanaSab.set_active(self.__is_active(6))
        vbox.pack_start(self.txtCronSettimanaSab, False, True, 0)
        self.txtCronSettimanaDom = Gtk.CheckButton(label='Domenica')
        self.txtCronSettimanaDom.set_active(self.__is_active(7))
        vbox.pack_start(self.txtCronSettimanaDom, False, True, 0)
        self.generale.add(vbox)
        # ************************** separatore
        l = Gtk.VSeparator()
        l.set_property("width-request", 10)
        l.set_property("margin", 10)
        self.generale.add(l)
        # ************************** altro
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox_mail = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_mail.pack_start(Gtk.Label(label='MAIL FROM', width_request=10), False, False, 0)
        self.txtMailFrom=Gtk.Entry(text=self.bks['altro']['mailFROM'],  max_width_chars=40)
        hbox_mail.pack_start(self.txtMailFrom, False, False, 0)
        vbox.add(hbox_mail)

        hbox_mail = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_mail.pack_start(Gtk.Label(label='        MAIL TO', width_request=10), False, False, 0)
        self.txtMailTO=Gtk.Entry(text=self.bks['altro']['mailTO'],  max_width_chars=40)
        hbox_mail.pack_start(self.txtMailTO, False, False, 0)
        vbox.add(hbox_mail)

        self.generale.add(vbox)
        # ******************************************************************

        self.nb.append_page(self.generale, Gtk.Label(label="GENERALE"))
    def __is_active(self, giorno):

        if self.bk['cron']['settimana'] == '*':
            return True
        return giorno in self.bk['cron']['settimana']


    def __attach_button(self):
        hbox2 = Gtk.Box(spacing=6)
        button = Gtk.Button.new_with_mnemonic("Annulla")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_annulla_clicked)
        hbox2.add(button)

        button = Gtk.Button.new_with_mnemonic("Salva")
        button.set_property("width-request", 85)
        button.set_property("height-request", 15)
        button.connect("clicked", self.on_salva_clicked)
        hbox2.add(button)
        return hbox2

    def on_folder_clicked(self, widget):
        # print(widget.get_label())
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(300, 200)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if widget.get_label() == "---":
                # print("Select clicked")
                # print("Folder selected: " + dialog.get_filename())
                self.txtLocPathDA.set_text(dialog.get_filename())
            elif widget.get_label() == "----":
                self.txtLocPathTO.set_text(dialog.get_filename())
        # elif response == Gtk.ResponseType.CANCEL:
        #    print("Cancel clicked")

        dialog.destroy()

    def on_annulla_clicked(self, widg):
        # print("Annulla")
        self.destroy()

    def __salva_cron(self):
        self.bk['cron']['minuto'] = self.txtCronMinuto.get_text()
        self.bk['cron']['ora'] = self.txtCronOra.get_text()
        self.bk['cron']['giorno'] = self.txtCronGiorno.get_text()
        self.bk['cron']['mese'] = self.txtCronMese.get_text()
        self.bk['cron']['settimana'] = []
        if self.txtCronSettimanaDom.get_active():
            self.bk['cron']['settimana'].append(0)
        if self.txtCronSettimanaLun.get_active():
            self.bk['cron']['settimana'].append(1)
        if self.txtCronSettimanaMar.get_active():
            self.bk['cron']['settimana'].append(2)
        if self.txtCronSettimanaMer.get_active():
            self.bk['cron']['settimana'].append(3)
        if self.txtCronSettimanaGio.get_active():
            self.bk['cron']['settimana'].append(4)
        if self.txtCronSettimanaVen.get_active():
            self.bk['cron']['settimana'].append(5)
        if self.txtCronSettimanaSab.get_active():
            self.bk['cron']['settimana'].append(6)
    def __salva_altro(self):
        self.bks['altro']['mailFROM'] = self.txtMailFrom.get_text()
        self.bks['altro']['mailTO'] = self.txtMailTO.get_text()
    def __salva_origine(self):
        # print("salva origine")
        # print(self.bks)
        if self.rdRemotoDA.get_active():
            self.bk['dirDA']['remoto'] = True
            self.bk['dirDA']['da'] = \
                str(self.txtUtenteDA.get_text()) + "@" \
                + str(self.txtHostDA.get_text()) + ":" \
                + str(self.txtRemPathDA.get_text())
        else:
            self.bk['dirDA']['remoto'] = False
            self.bk['dirDA']['da'] = self.txtLocPathDA.get_text()
    def __salvaDestinatario(self):
        if self.rdRemotoTO.get_active():
            self.bk['dirTO']['remoto'] = True
            self.bk['dirTO']['to'] = \
                str(self.txtUtenteTO.get_text()) + "@" \
                + str(self.txtHostTO.get_text()) + ":" \
                + str(self.txtRemPathTO.get_text())
        else:
            self.bk['dirTO']['remoto'] = False
            self.bk['dirTO']['to'] = self.txtLocPathTO.get_text()

    def __salvaTutto(self):
        # print(self.chDiz)
        self.__salva_origine()
        self.__salvaDestinatario()
        self.__salva_cron()
        self.__salva_altro()

        with open(self.fconf, "w") as data:
            data.write(str(self.bks))
            data.close()
        # print(self.bks)
        self.parent.set_restart_impostazioni()
        msg = Msg(self)
        msg.set_msg("Salvato HO")

    def on_salva_clicked(self, widget):
        # print("salva")
        self.__salvaTutto()


def getImpostazioni(f):
    with open(f, "r") as data:
        d = ast.literal_eval(data.read())
        data.close()
        return d


# win = DlgConf(getImpostazioni("./danieleBK.conf")['chDef'])
#win = DlgConf("./danieleBK.conf", "chDef")
#win.connect("destroy", Gtk.main_quit)
#win.show_all()
#Gtk.main()
