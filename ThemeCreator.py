#!/usr/bin/env python

import os
from xml.etree.ElementTree import ElementTree

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
        
    def on_opentheme_activate(self, widget, data=None):
        schemify = lambda x: ''.join(['{http://schemas.android.com/apk/res/android}', x])
        manifest_file = 'themes/Cyanbread/AndroidManifest.xml'
        manifest = ElementTree()
        manifest.parse(manifest_file)
        for prospect in manifest.iterfind('theme/meta-data'):
            if prospect.attrib[schemify('name')] == 'com.tmobile.theme.redirections':
                redirections_id = prospect.attrib[schemify('resource')]
                break
        
        redirections_file = os.path.join('themes/Cyanbread/res', ''.join([redirections_id[1:], '.xml']))
        redirections = ElementTree()
        redirections.parse(redirections_file)
        for redir in redirections.iterfind('package-redirections'):
            self.pkgs.append([redir.attrib[schemify('name')]])

    def on_savetheme_activate(self, widget, data=None):
        print "clicked save"

    def __init__(self):
        uifile = "ThemeCreator.glade"
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(uifile)
    
        self.wTree.connect_signals(self)

        self.pkgs = self.wTree.get_object("packages")
        self.res = self.wTree.get_object("resources")

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
