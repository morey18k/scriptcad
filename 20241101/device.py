import klayout.db as db
import math
from device1.mesa_dot import make_mesa_1, make_mesaf_1
from device1.ohmics_dot import make_ohmics_1, make_island_1
# Creating layout and top cells

class params1():
    dohmicsy = 200
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 100
    lHallbar = 400
    w_connector = 35
    h_tcn = 0.85*dohmicsy
    w_dcn = 75

    island_sizeX = 0.6
    island_sizeY = 1

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

mesa_region  = make_mesa_1(um, p1)
ohmics_region  = make_ohmics_1(um, p1)
island_region  = make_island_1(um, p1)


mesaf = make_mesaf_1(um, p1)

top.shapes(ohmics).insert(ohmics_region)
top.shapes(mesaNeg).insert(mesaf)
top.shapes(mesaPos).insert(mesa_region)
top.shapes(island).insert(island_region)

layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")