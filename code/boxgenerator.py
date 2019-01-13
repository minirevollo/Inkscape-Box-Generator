#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: mini@revollo.de
member of the erfindergarden

Inkscape Erweiterung - Box Generator
13.01.2019

Danke an neon22    https://github.com/Neon22/inkscape_extension_template
Nach seiner Anleitung konnte ich dieses Programm erstellen.

'''

import inkex       # Required
import simplestyle # will be needed here for styles support

__version__ = '0.2'

inkex.localize()

def points_to_svgd(p, close=True):
    """ convert list of points (x,y) pairs
        into a closed SVG path list
    """
    f = p[0]
    p = p[1:]
    svgd = 'M%.4f,%.4f' % f
    for x in p:
        svgd += 'L%.4f,%.4f' % x
    if close:
        svgd += 'z'
    return svgd



### Your main function subclasses the inkex.Effect class

class Box(inkex.Effect): 
    ###Erstellt die Box.
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
            
        # Define your list of parameters defined in the .inx file
        self.OptionParser.add_option("", "--breite",
                                     action="store", type="int",
                                     dest="breite", default = 30,
                                     help="Breite der Box")
        
        self.OptionParser.add_option("", "--hoehe",
                                     action="store", type="int",
                                     dest="hoehe", default = 50,
                                     help="Hoehe der Box")
        
        self.OptionParser.add_option("", "--tiefe",
                                     action="store", type="int", 
                                     dest="tiefe", default = 80,
                                     help="Tiefe der Box")

        self.OptionParser.add_option("", "--material",
                                     action="store", type="float",
                                     dest="material", default = 3.6,
                                     help="Materialstärke")
        
        self.OptionParser.add_option("", "--zahnbreite",
                                     action="store", type="int", 
                                     dest="zahnbreite", default = 7,
                                     help="Breite der Zähne")
        
        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
        self.front_punkte = []
        self.seite_punkte = []
        self.deckel_punkte = []
        
    
    def schreiben_x_y(self, x, y, liste):
        ###Schreibt die aktuellen Koordinaten in die Punkteliste
        
        if liste == 0:
            self.front_punkte.append((x, y))
        if liste == 1:
            self.seite_punkte.append((x, y))
        if liste == 2:
            self.deckel_punkte.append((x, y))
       

    def front_erstellen(self):
        
        ###Startpunkt wird gesetzt.
        liste = 0
        x = 0
        y = 0        
        self.schreiben_x_y(x, y, liste)
        #### 1. Seite.
        x = x + self.br
        self.schreiben_x_y(x, y, liste)
        for item in range(self.bzm):
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
        x = x + self.br
        self.schreiben_x_y(x, y, liste)    
        ### 2. Seite.
        y += self.hr 
        self.schreiben_x_y(x, y, liste)
        for item in range(self.hzm):
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y += self.hr
        self.schreiben_x_y(x, y, liste)
        ### 3. Seite.
        x -= self.br
        self.schreiben_x_y(x, y, liste)
        for item in range(self.bzm):
            x -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite /2
            self.schreiben_x_y(x, y, liste)
        x -= self.br
        self.schreiben_x_y(x, y, liste)
        ### 4. Seite.
        y -= self.hr
        self.schreiben_x_y(x, y, liste)
        for item in range(self.hzm):
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y -= self.hr
        self.schreiben_x_y(x, y, liste)
        
        
    def seite_erstellen(self):
            
        ###Startpunkt wird gesetzt.
        liste = 1
        x = self.breite + 5 + self.material
        y = 0
        self.schreiben_x_y(x, y, liste)
        #### 1. Seite.
        x = x + self.tr - self.material
        self.schreiben_x_y(x, y, liste)    
        for item in range(self.tzm):
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
        x = x + self.tr - self.material
        self.schreiben_x_y(x, y, liste)    
        ### 2. Seite.
        y += self.hr 
        self.schreiben_x_y(x, y, liste)
        for item in range(self.hzm):
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y += self.hr
        self.schreiben_x_y(x, y, liste)
        ### 3. Seite.
        x -= self.tr - self.material 
        self.schreiben_x_y(x, y, liste)
        for item in range(self.tzm):
            x -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite /2
            self.schreiben_x_y(x, y, liste)
        x -= self.tr - self.material
        self.schreiben_x_y(x, y, liste)
        ### 4. Seite.
        y -= self.hr
        self.schreiben_x_y(x, y, liste)
        for item in range(self.hzm):
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y -= self.hr
        self.schreiben_x_y(x, y, liste)
       
    def deckel_erstellen(self):
        
        ###Startpunkt wird gesetzt.
        liste = 2
        x = self.breite + 5 + self.tiefe + 5 + self.material
        y = self.material
        self.schreiben_x_y(x, y, liste)
        #### 1. Seite.
        x = x + self.tr - self.material
        self.schreiben_x_y(x, y, liste)    
        for item in range(self.tzm):
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x += (self.zahnbreite / 2)
            self.schreiben_x_y(x, y, liste)
        x = x + self.tr - self.material
        self.schreiben_x_y(x, y, liste)    
        ### 2. Seite.
        y += self.br - self.material
        self.schreiben_x_y(x, y, liste)
        for item in range(self.bzm):
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y += self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y += self.br - self.material
        self.schreiben_x_y(x, y, liste)
        ### 3. Seite.
        x -= self.tr - self.material
        self.schreiben_x_y(x, y, liste)
        for item in range(self.tzm):
            x -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            y += self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            y -= self.material
            self.schreiben_x_y(x, y, liste)
            x -= self.zahnbreite /2
            self.schreiben_x_y(x, y, liste)
        x -= self.tr - self.material
        self.schreiben_x_y(x, y, liste)
        ### 4. Seite.
        y -= self.br - self.material
        self.schreiben_x_y(x, y, liste)
        for item in range(self.bzm):
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
            x -= self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite
            self.schreiben_x_y(x, y, liste)
            x += self.material
            self.schreiben_x_y(x, y, liste)
            y -= self.zahnbreite / 2
            self.schreiben_x_y(x, y, liste)
        y -= self.br - self.material
        self.schreiben_x_y(x, y, liste)
       
    
    
    
### -------------------------------------------------------------------
### This is your main function and is called when the extension is run.
    
    def effect(self):
        ###Hauptprogramm
        
        # holt die Parameter aus Inkscape
        self.breite = self.options.breite
        self.hoehe = self.options.hoehe
        self.tiefe = self.options.tiefe
        self.material = self.options.material
        self.zahnbreite = self.options.zahnbreite
        
        self.puffer = self.material * 2 #um eine zu kleine Ecke zu vermeiden
        #Berechnung der Reste der Breite br zwischen Ecke und erstem Zahn
        self.bzm = int((self.breite - (2 * self.material) - self.puffer) / (self.zahnbreite * 2))
        self.br = (self.breite - (self.bzm * self.zahnbreite * 2)) / 2
        #Berechnung der Reste der Hoehe hr zwischen Ecke und erstem Zahn
        self.hzm = int((self.hoehe - (2 * self.material)  - self.puffer) / (self.zahnbreite * 2))
        self.hr = (self.hoehe - (self.hzm * self.zahnbreite * 2)) / 2 
        #Berechnung der Reste der Tiefe tr zwischen Ecke und erstem Zahn
        self.tzm = int((self.tiefe - (2 * self.material)  - self.puffer) / (self.zahnbreite * 2))
        self.tr = (self.tiefe - (self.tzm * self.zahnbreite * 2)) / 2
        
        self.front_erstellen()
        self.seite_erstellen()
        self.deckel_erstellen()
        
        path_stroke = '#101010'  # Farbe für die Box
        path_fill   = 'none'     # keine Füllung, nur eine Linie
        path_stroke_width  = '0.2' # can also be in form '0.6mm'
        
        # what page are we on
        page_id = self.options.active_tab # sometimes wrong the very first time

        # Die gesammelten x und y Koordinaten der Punkte werden in Pfade (d) umgewandelt.  
        
        front_pfad = points_to_svgd(self.front_punkte )
        seite_pfad = points_to_svgd(self.seite_punkte )
        deckel_pfad  = points_to_svgd(self.deckel_punkte )

        # Embed the path in a group to make animation easier:
        # Be sure to examine the internal structure by looking in the xml editor inside inkscape
        
        # Make a nice useful name
        g_attribs = { inkex.addNS('label','inkscape'): 'box-gruppe', 'id': "box",}
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        # Create SVG Path under this top level group
        # define style using basic dictionary
        front_attribute = {'id': "front", 'stroke': path_stroke, 'fill': path_fill, 'stroke-width': path_stroke_width, 'd': front_pfad}
        seite_attribute = {'id': "seite",'stroke': path_stroke, 'fill': path_fill, 'stroke-width': path_stroke_width, 'd': seite_pfad}
        deckel_attribute = {'id': "deckel",'stroke': path_stroke, 'fill': path_fill, 'stroke-width': path_stroke_width, 'd': deckel_pfad}
        # add path to scene                
        front = inkex.etree.SubElement(topgroup, inkex.addNS('path','svg'), front_attribute )
        seite = inkex.etree.SubElement(topgroup, inkex.addNS('path','svg'), seite_attribute )
        deckel = inkex.etree.SubElement(topgroup, inkex.addNS('path','svg'), deckel_attribute )

        # Make a nice useful name
        text_g_attribs = { inkex.addNS('label','inkscape'): 'box-gruppe', 'id': "Beschriftung",}
        # add the group to the document's current layer
        textgroup = inkex.etree.SubElement(self.current_layer, 'g', text_g_attribs )

        line_style = {'font-size': '5px', 'font-style':'normal', 'font-weight': 'normal',
                     'fill': '#ff0000', 'font-family': 'Consolas',
                     'text-anchor': 'middle', 'text-align': 'center'}
        front_line_attribs = {inkex.addNS('label','inkscape'): 'front-text',
                       'id': 'front text',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(int(self.breite / 2)),
                       'y': str(int(self.hoehe / 2)),
                       }
        seite_line_attribs = {inkex.addNS('label','inkscape'): 'seite-text',
                       'id': 'seite text',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(int(self.breite + self.tiefe / 2)),
                       'y': str(int(self.hoehe / 2)),
                       }
        deckel_line_attribs = {inkex.addNS('label','inkscape'): 'deckel-text',
                       'id': 'deckel text',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(int(self.breite + self.tiefe  * 1.5)),
                       'y': str(int(self.breite / 2)),
                       }
        front_line = inkex.etree.SubElement(textgroup, inkex.addNS('text','svg'), front_line_attribs)
        front_line.text = 'vorne/hinten'
        seite_line = inkex.etree.SubElement(textgroup, inkex.addNS('text','svg'), seite_line_attribs)
        seite_line.text = 'links/rechts'
        deckel_line = inkex.etree.SubElement(textgroup, inkex.addNS('text','svg'), deckel_line_attribs)
        deckel_line.text = 'oben/unten'



if __name__ == '__main__':
    box = Box()
    box.affect()

# Notes

