#!/usr/bin/env python

import os
from xml.etree.ElementTree import ElementTree

import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk

theme_path = 'themes/Cyanbread'

nsify = lambda x: ''.join(['{http://schemas.android.com/apk/res/android}', x])

def res_to_file(res):
    # We're ignoring the potential security vulerability with os.path.exists();
    # just find the valid path(s)
    
    # Could just be xml
    maybe_file = os.path.join(theme_path, 'res', ''.join([res[1:], '.xml']))
    if os.path.exists(maybe_file):
        return maybe_file
        
    # Could also be a .png
    maybe_file = os.path.join(theme_path, 'res', ''.join([res[1:], '.png']))
    if os.path.exists(maybe_file):
        return maybe_file

    # Or a  .9.png
    maybe_file = os.path.join(theme_path, 'res', ''.join([res[1:], '.9.png']))
    if os.path.exists(maybe_file):
        return maybe_file
        
    # If it's a drawable, go hunting
    if res[1:10] == 'drawable/':
        for extra_path in ['-hdpi', '-mdpi', '-ldpi']:
            # Could also be a .png
            maybe_file = os.path.join(theme_path, 'res', ''.join([res[1:9], extra_path, res[9:], '.png']))
            if os.path.exists(maybe_file):
                return maybe_file

            # Or a  .9.png
            maybe_file = os.path.join(theme_path, 'res', ''.join([res[1:9], extra_path, res[9:], '.9.png']))
            if os.path.exists(maybe_file):
                return maybe_file
    
    # If not, this is probably not a file
    return None

class ThemeCreator:
    
    def on_window_delete_event(self, widget, event, data=None):
        return False

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
        
    def on_newtheme_activate(self, widget, data=None):
        print "clicked new"
        
    def on_opentheme_activate(self, widget, data=None):
        manifest_file = 'themes/Cyanbread/AndroidManifest.xml'
        manifest = ElementTree()
        manifest.parse(manifest_file)
        for prospect in manifest.iterfind('theme/meta-data'):
            if prospect.attrib[nsify('name')] == 'com.tmobile.theme.redirections':
                redirections_id = prospect.attrib[nsify('resource')]
                break
        
        redirections_file = res_to_file(redirections_id)
        redirections = ElementTree()
        redirections.parse(redirections_file)
        for redir in redirections.iterfind('package-redirections'):
            self.pkgs.append([redir.attrib[nsify('name')], redir.attrib[nsify('resource')]])
    
    def on_packagelist_cursor_changed(self, widget, data=None):
        (tree, cursor) = self.pkgview.get_selection().get_selected()
        resources_file = res_to_file(tree.get_value(cursor, 1))
        resources = ElementTree()
        resources.parse(resources_file)
        
        self.res.clear()
        for resource in resources.iterfind('item'):
            res_file = res_to_file(resource.text)
            if res_file is not None and res_file[-4:] == '.png':
                res_img = gtk.gdk.pixbuf_new_from_file(res_file)
            else:
                res_img = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 1, 1)
            self.res.append([
                resource.attrib['name'],
                resource.text,
                res_img,
                ])

    def on_savetheme_activate(self, widget, data=None):
        print "clicked save"
        
    def on_quit_activate(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        uifile = "ThemeCreator.glade"
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(uifile)
    
        self.wTree.connect_signals(self)

        self.pkgs = self.wTree.get_object("packages")
        self.res = self.wTree.get_object("resources")

        self.pkgview = self.wTree.get_object("packagelist")
        column = gtk.TreeViewColumn("Package", gtk.CellRendererText(), text=0)
        self.pkgview.append_column(column)
        
        self.resview = self.wTree.get_object("resourcelist")
        self.resview.set_text_column(0)
        self.resview.set_pixbuf_column(2)

        self.wTree.get_object("window").show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = ThemeCreator()
    hello.main()
