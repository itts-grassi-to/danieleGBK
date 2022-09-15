import gi
import ast

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Msg(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Messaggio", transient_for=parent, flags=0)
        #self.add_buttons(
        #    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        #)

        self.set_default_size(150, 100)
        self.__msg=""
        self.label = Gtk.Label(label=self.__msg,margin=30)

        box = self.get_content_area()
        box.add(self.label)
        self.set_modal(True)
        #self.show_all()
    def set_msg(self,msg):
		   self.label.set_text(msg)
		   self.show_all()
		   #self.run()

class DlgNuovo(Gtk.Window):
	def __init__(self,fconf):
		super().__init__(title="Nuovo backups")
		self.fconf=fconf
		with open(self.fconf, "r") as data:
			self.bks = ast.literal_eval(data.read())
			data.close()
		
		#print(self.bks)
		self.set_default_size(400, 300)    
		#self.set_border_width(10)
		grid=Gtk.Grid()
		
		
		lbl=Gtk.Label(label="Inserisci codice")
		lbl.set_property("margin", 10)
		self.txtCodice=Gtk.Entry()
		self.txtCodice.set_property("width-request", 100)
		self.txtCodice.set_property("margin", 10)
		#self.txtCodice.set_property("height-request",200)
		grid.attach(lbl,0,0,1,1)
		grid.attach(self.txtCodice,1,0,1,1)
		
		lbl=Gtk.Label(label="Inserisci Titolo")
		lbl.set_property("margin", 10)
		self.txtTitolo=Gtk.Entry()
		self.txtTitolo.set_property("width-request", 200)
		self.txtTitolo.set_property("margin", 10)
		grid.attach(lbl,0,1,1,1)
		grid.attach(self.txtTitolo,1,1,1,1)
		
		#*************** pulsantiera
		hbox=Gtk.Box(margin=10,spacing=6)
		#hbox.set_property("height-request", 200)
		
		button = Gtk.Button.new_with_mnemonic("Annulla")
		button.set_property("width-request", 85)
		button.set_property("height-request",15)
		button.connect("clicked", self.on_annulla_clicked)
		hbox.add(button)

		button = Gtk.Button.new_with_mnemonic("Salva")
		button.set_property("width-request", 85)
		button.set_property("height-request",15)
		button.connect("clicked", self.on_salva_clicked)
		hbox.add(button)
		grid.attach(hbox,1,2,1,1)
		
		self.add(grid)
	def pulisci(self,s):
		s=s.replace("à","a")
		s=s.replace("è","e")
		s=s.replace("é","e")
		s=s.replace("ì","i")
		s=s.replace("ò","o")
		s=s.replace("ù","u")
		s=s.replace("À","a")
		s=s.replace("È","e")
		s=s.replace("É","e")
		s=s.replace("Ì","i")
		s=s.replace("Ò","o")
		s=s.replace("Ù","o")
		return s
	def __esisteCodice(self,s):
		#print("esisteCodice")
		return s in self.bks
	def __salvaNuovo(self,ch,titolo):
		#print("salvaNuovo")
		self.bks[ch]={'titolo':titolo}
		with open(self.fconf, "w") as data:
			data.write(str(self.bks))
			data.close()

	def on_annulla_clicked(self,bt):
		#print("annulla")
		self.destroy()
	def on_salva_clicked(self,bt):
		#print("Salva")
		self.msg=Msg(self)
		if self.txtCodice.get_text().isalpha():
			ch=self.pulisci(self.txtCodice.get_text())
			if self.__esisteCodice(ch):
				self.msg.set_msg("Codice esistente")
			else:	
				titolo=self.txtTitolo.get_text()
				if len(titolo)==0:
					self.msg.set_msg("Inserisci il titolo")
				else:
					self.__salvaNuovo(ch,titolo)
					self.destroy()
		else:
			self.msg.set_msg("NON puoi inserire nel codice caratteri diversi da quelli dell'alfabeto")
		
class DlgConf(Gtk.Window):
    def __init__(self,diz):
        super().__init__(title="Configurazione backups")
        print(diz)
        self.bk=diz
        self.set_default_size(500, 300)
        self.set_border_width(10)
        box = Gtk.Grid()
        self.nb=Gtk.Notebook()
        self.nb.set_property("width-request", 480)
        self.nb.set_property("height-request",260)
        #self.add(self.nb)
        box.attach(self.nb,0,0,1,1)
		
        self.__primaPagina()
        self.__secondaPagina()
        
        #self.add(self.__attachButton())
        box.attach(self.__attachButton(),0,1,1,1)
        #label = Gtk.Label(label="This is a dialog to display additional information")

        #box = self.get_content_area()
        #box.add(label)
        self.add(box)
        self.show_all()
#************************** ORIGINE ********************************        
    def __secondaPagina(self):
        #seconda pagina
        pg2=Gtk.Grid()
        pg2.set_border_width(10)
        pg2.set_property("width-request", 200)
        pg2.set_property("height-request",15)
        
        h=Gtk.Box(spacing=10)
        rdLocale = Gtk.RadioButton.new_with_label_from_widget(None, "Locale")
        rdLocale.connect("toggled", self.on_rd_toggled, "1")
        #pg2.attach(rdLocale,0,0,1,1)       
        #pg2.attach(Gtk.Entry(text="locale"),1,0,1,1)
        h.add(rdLocale)
        h.add(Gtk.Entry(text="locale"))
        button = Gtk.Button.new_with_mnemonic("Nuovo")
        button.set_property("width-request", 85)
        button.set_property("height-request",15)
        h.add(button)
        #button.connect("clicked", self.on_nuovo_clicked)
        #pg2.attach(button,2,0,1,1)
        pg2.attach(h,0,0,1,1)
        
        h=Gtk.Box(spacing=10)
        rdRemoto = Gtk.RadioButton.new_with_label_from_widget(rdLocale, "Remoto")
        rdRemoto.connect("toggled", self.on_rd_toggled, "2")
        #pg2.attach(rdRemoto,0,1,1,1)       
        #pg2.attach(Gtk.Label(label="Utente"),1,1,1,1)
        h.add(rdRemoto)
        self.utente=Gtk.Entry(text="")
        #pg2.attach(self.utente,2,1,1,1)
        h.add(self.utente)
        pg2.attach(h,0,1,1,1)
        self.nb.append_page(pg2,Gtk.Label(label="ORIGINE"))
    def on_rd_toggled(self,rd,name):
	    if rd.get_active():
		    state = "on"
	    else:
		    state = "off"
	    print("Button", name, "was turned", state)		
#******************************************************************
    def __primaPagina(self):
        #prima pagina
        self.generale=Gtk.Grid()
        self.generale.set_border_width(10)
        self.generale.attach(Gtk.Label(label=self.bk['titolo']),0,0,1,1)
        self.nb.append_page(self.generale,Gtk.Label(label="GENERALE"))
    def __attachButton(self):
	    hbox2=Gtk.Box(spacing=6)
	    button = Gtk.Button.new_with_mnemonic("Annulla")
	    button.set_property("width-request", 85)
	    button.set_property("height-request",15)
	    button.connect("clicked", self.on_annulla_clicked)
	    hbox2.add(button)
	    
	    button = Gtk.Button.new_with_mnemonic("Salva")
	    button.set_property("width-request", 85)
	    button.set_property("height-request",15)
	    button.connect("clicked", self.on_salva_clicked)
	    hbox2.add(button)	
	    return hbox2
    def on_annulla_clicked(self):
	    printf("Annulla")
    def on_salva_clicked(self):
        print("salva")	
	
def getImpostazioni(f):
		with open(f, "r") as data:
			d = ast.literal_eval(data.read())
			data.close()
			return d

win=DlgConf(getImpostazioni("./danieleBK.conf")['chDef'])
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
