#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

class ThemeCreator:
    
    def on_window_delete_event(self, widget, event, data=None):
        return False

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
        
    def on_newtheme_activate(self, widget, data=None):
        print "clicked new"

    def __init__(self):
        uifile = "ThemeCreator.glade"
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(uifile)
    
        self.wTree.connect_signals(self)

        pkgs = self.wTree.get_object("packages")
        for x in ['One', 'Two']:
            pkgs.append([x])
        res = self.wTree.get_object("resources")
        for x in ['One', 'Two']:
            res.append([x])

        pkglist = self.wTree.get_object("packagelist")
        column = gtk.TreeViewColumn("Package", gtk.CellRendererText(), text=0)
        pkglist.append_column(column)
        
        reslist = self.wTree.get_object("resourcelist")
        reslist.set_text_column(0)

        self.wTree.get_object("window").show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = ThemeCreator()
    hello.main()
