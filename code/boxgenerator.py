#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Example of extensions template for inkscape

'''

import inkex       # Required
import simplestyle # will be needed here for styles support
import os          # here for alternative debug method only - so not usually required
# many other useful ones in extensions folder. E.g. simplepath, cubicsuperpath, ...

from math import cos, sin, radians

__version__ = '0.2'

inkex.localize()

### Your helper functions go here
def points_to_svgd(p, close=True):
    """ convert list of points (x,y) pairs
        into a closed SVG path list
    """
    print("hallo world")
    f = p[0]
    p = p[1:]
    svgd = 'M%.4f,%.4f' % f
    for x in p:
        svgd += 'L%.4f,%.4f' % x
    if close:
        svgd += 'z'
    return svgd

def points_to_bbox(p):
    """ from a list of points (x,y pairs)
        - return the lower-left xy and upper-right xy
    """
    llx = urx = p[0][0]
    lly = ury = p[0][1]
    for x in p[1:]:
        if   x[0] < llx: llx = x[0]
        elif x[0] > urx: urx = x[0]
        if   x[1] < lly: lly = x[1]
        elif x[1] > ury: ury = x[1]
    return (llx, lly, urx, ury)

def points_to_bbox_center(p):
    """ from a list of points (x,y pairs)
        - find midpoint of bounding box around all points
        - return (x,y)
    """
    bbox = points_to_bbox(p)
    return ((bbox[0]+bbox[2])/2.0, (bbox[1]+bbox[3])/2.0)




### Your main function subclasses the inkex.Effect class

class Box(inkex.Effect): # choose a better name
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
        # Two ways to get debug info:
        # OR just use inkex.debug(string) instead...
        try:
            self.tty = open("/dev/tty", 'w')
        except:
            self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
            # print >>self.tty, "gears-dev " + __version__
            
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
        
        
        
        
    def getUnittouu(self, param):
        " for 0.48 and 0.91 compatibility "
        try:
            return inkex.unittouu(param)
        except AttributeError:
            return self.unittouu(param)
    
    def add_text(self, node, text, position, text_height=12):
        """ Create and insert a single line of text into the svg under node.
        """
        line_style = {'font-size': '%dpx' % text_height, 'font-style':'normal', 'font-weight': 'normal',
                     'fill': '#F6921E', 'font-family': 'Bitstream Vera Sans,sans-serif',
                     'text-anchor': 'middle', 'text-align': 'center'}
        line_attribs = {inkex.addNS('label','inkscape'): 'Annotation',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(position[0]),
                       'y': str((position[1] + text_height) * 1.2)
                       }
        line = inkex.etree.SubElement(node, inkex.addNS('text','svg'), line_attribs)
        line.text = text

           
    def calc_unit_factor(self):
        """ return the scale factor for all dimension conversions.
            - The document units are always irrelevant as
              everything in inkscape is expected to be in 90dpi pixel units
        """
        # namedView = self.document.getroot().find(inkex.addNS('namedview', 'sodipodi'))
        # doc_units = self.getUnittouu(str(1.0) + namedView.get(inkex.addNS('document-units', 'inkscape')))
        unit_factor = self.getUnittouu(str(1.0) + self.options.units)
        return unit_factor
    
    def schreiben_x_y(self, x, y, liste):
        ###Schreibt die aktuellen Koordinaten in die Punkteliste
        
        liste.append((x,y))
         

    def front_erstellen(self):
        
        ###Startpunkt wird gesetzt.
        liste = self.front_punkte
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
        liste = self.front_punkte
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
        liste = self.front_punkte
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
        """ Calculate Gear factors from inputs.
            - Make list of radii, angles, and centers for each tooth and 
              iterate through them
            - Turn on other visual features e.g. cross, rack, annotations, etc
        """
        
        # gather incoming params and convert
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
        
        path_stroke = '#000000'  # take color from tab3
        path_fill   = 'none'     # no fill - just a line
        path_stroke_width  = 0.6 # can also be in form '0.6mm'
        
        # calculate unit factor for units defined in dialog. 
        #unit_factor = self.calc_unit_factor()
        # what page are we on
        page_id = self.options.active_tab # sometimes wrong the very first time

        # Do your thing - create some points or a path or whatever...  
        front_pfad = points_to_svgd(self.front_punkte )
        seite_pfad = points_to_svgd(self.seite_punkte )
        deckel_pfad  = points_to_svgd(self.deckel_punkte )

        #inkex.debug(path)
        #bbox_center = points_to_bbox_center( points )
        # example debug
        # print >>self.tty, bbox_center
        # or
        # inkex.debug("bbox center %s" % bbox_center)

        
        # Embed the path in a group to make animation easier:
        # Be sure to examine the internal structure by looking in the xml editor inside inkscape
        # This finds center of exisiting document page
        
       
        # Make a nice useful name
        g_attribs = { inkex.addNS('label','inkscape'): 'box-gruppe'}
        # add the group to the document's current layer
        topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        # Create SVG Path under this top level group
        # define style using basic dictionary
        pfad_attribute = { 'stroke': path_stroke, 'fill': path_fill, 'stroke-width': path_stroke_width }
        # add path to scene                
        front = inkex.etree.SubElement(topgroup, inkex.addNS('front_pfad','svg'), pfad_attribute )
        seite = inkex.etree.SubElement(topgroup, inkex.addNS('seite_pfad','svg'), pfad_attribute )
        deckel = inkex.etree.SubElement(topgroup, inkex.addNS('deckel_pfad','svg'), pfad_attribute )


if __name__ == '__main__':
    box = Box()
    box.affect()

# Notes

