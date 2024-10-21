import klayout.db as db
import math
from device1.mesa_dot import make_mesa_1, make_mesaf_1
from device1.ohmics_dot import make_ohmics_1, make_island_1
from device1.gates import create_finegates, create_gatepads
# Creating layout and top cells

class params1():
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

layout = db.Layout(True)
layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")

top = layout.cell("TOP")
um = 1e3

mesaPos = layout.layer(2, 0)
layout.clear_layer(mesaPos)

ohmics = layout.layer(3, 0)
layout.clear_layer(ohmics)


mesaNeg = layout.layer(10, 0)

island = layout.layer(61, 0)
layout.clear_layer(island)

layout.clear_layer(mesaNeg)

fgates = layout.layer(4, 0)
layout.clear_layer(fgates)

cgates = layout.layer(5, 0)
layout.clear_layer(cgates)


mesa_region  = make_mesa_1(um, p1)
ohmics_region  = make_ohmics_1(um, p1)
island_region  = make_island_1(um, p1)

qpcregion = create_finegates(um, p1)

mesaf = make_mesaf_1(um, p1)

cgatesrgn = create_gatepads(um, p1)

mesa_boundary = db.Region(db.Box(4300*um, 5000*um))

top.shapes(ohmics).insert(ohmics_region)
top.shapes(mesaNeg).insert(mesaf)
top.shapes(mesaPos).insert(mesa_boundary-mesa_region)
top.shapes(island).insert(island_region)
top.shapes(fgates).insert(qpcregion)
top.shapes(cgates).insert(cgatesrgn)

layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")