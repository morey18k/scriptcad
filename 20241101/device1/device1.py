import klayout.db as db
import klayout.lib
import math
from device1.mesa_dot import make_mesa_1, make_mesaf_1
from device1.ohmics_dot import make_ohmics_1, make_island_1
from device1.gates import create_finegates, create_gatepads
from alignment import rectangle_insert
# Creating layout and top cells

chipsize = 5000 

class params1():
    angle = 0
    centerx = 0
    centery = 0
    dohmicsy = 220
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 100
    lHallbar = 450
    w_connector = 35
    h_tcn = 0.85*dohmicsy
    w_dcn = 90

    island_sizeX = 0.6
    island_sizeY = 1
    qpcwidth = 0.3
    dot_length = 2
    finegatewidth = 0.1
    coursegatewidth = 2
    gate_separation = 14

    device_height = (3*dohmicsy+padsize+2*cronSize)
    
    gatepadwidth = 0.6*padsize
    gatepadheight = device_height/3.2
    gatepadx = 0.9*dohmicsx
    gatepady = (1/3)*device_height



p1 =  params1()

def create_device_1(p, um):
    #layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                # "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")
    layout = db.Layout(True)
    top = layout.create_cell("TOP")
    um = 1e3



    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))


    mesaNeg = layout.layer(db.LayerInfo(10, 0))

    island = layout.layer(db.LayerInfo(61, 0))

    fgates = layout.layer(db.LayerInfo(4, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    mesa_region  = make_mesa_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 
    island_region  = make_island_1(um, p) 

    qpcregion = create_finegates(um, p) 

    mesaf = make_mesaf_1(um, p) 

    cgatesrgn = create_gatepads(um, p) 

    

    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaNeg).insert(mesaf)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(island).insert(island_region)
    top.shapes(fgates).insert(qpcregion)
    top.shapes(cgates).insert(cgatesrgn)
    

    return layout