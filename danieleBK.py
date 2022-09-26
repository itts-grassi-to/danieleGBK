#!/usr/bin/env python3

# gtk-example.py
# (c) Aleksander Alekseev 2016
# http://eax.me/

import signal
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import Notify
from gmain import MainW

APPID = "GTK Test"
CURRDIR = os.path.dirname(os.path.abspath(__file__))
# could be PNG or SVG as well
#print(CURRDIR)
ICON = os.path.join(CURRDIR, 'danieleBK.png')
# ICON = os.path.join(CURRDIR, 'python3.xpm')
#print(ICON)
# Cross-platform tray icon implementation
# See:
# * http://ubuntuforums.org/showthread.php?t=1923373#post11902222
# * https://github.com/syncthing/syncthing-gtk/blob/master/syncthing_gtk/statusicon.py
class TrayIcon:

    def __init__(self, appid, icon, menu):
        self.menu = menu

        APPIND_SUPPORT = 1
        try:
            from gi.repository import AppIndicator3
        except:
            APPIND_SUPPORT = 0

        if APPIND_SUPPORT == 1:
            self.ind = AppIndicator3.Indicator.new(
                appid, icon,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:
            self.ind = Gtk.StatusIcon()
            self.ind.set_from_file(icon)
            self.ind.connect('popup-menu', self.onPopupMenu)

    def onPopupMenu(self, icon, button, time):
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, icon,
                        button, time)


class Handler:

    def __init__(self):
        self.window_is_hidden = True
        window.hide()

    # def onShowButtonClicked(self, button):
    #    msg = "Clicked: " + entry.get_text()
    #    dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO,
    #                               Gtk.ButtonsType.OK, msg)
    #    dialog.run()
    #    dialog.destroy()

    def onNotify(self, *args):
        Notify.Notification.new("Notification", "Hello!", ICON).show()

    def onVisuNascondi(self, *args):
        if self.window_is_hidden:
            window.show()
        else:
            window.hide()

        self.window_is_hidden = not self.window_is_hidden

    def onChiudi(self, *args):
        Notify.uninit()
        # Gtk.main_quit()
        window.fine()

# Handle pressing Ctr+C properly, ignored by default
signal.signal(signal.SIGINT, signal.SIG_DFL)

builder = Gtk.Builder()
builder.add_from_file('danieleBK.glade')
# builder.add(MainW)

# window = builder.get_object('window1')
# window.set_icon_from_file(ICON)
# window.show_all()
window = MainW()
window.set_icon_from_file(ICON)
window.connect("destroy", MainW.fine)
window.show_all()
# window.hide()
builder.connect_signals(Handler())

#entry = builder.get_object('entry1')
menu = builder.get_object('menuST')
icon = TrayIcon(APPID, ICON, menu)
Notify.init(APPID)

Gtk.main()
