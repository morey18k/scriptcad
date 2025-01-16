import klayout.db as db
import klayout.lib
import math
from hallBar.mesa_dot import make_mesa_1
from hallBar.ohmics_dot import make_ohmics_1
from hallBar.gates import  create_gatepads
from alignment import rectangle_insert
# Creating layout and top cells

def create_hallBar(p, um):
    #layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                # "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")
    layout = db.Layout(True)
    top = layout.create_cell("TOP")

    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    mesa_region  = make_mesa_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 
    cgatesrgn = create_gatepads(um, p) 

    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(cgates).insert(cgatesrgn)

    return layout