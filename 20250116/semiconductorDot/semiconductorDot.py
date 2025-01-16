import klayout.db as db
import klayout.lib
import math
from semiconductorDot.mesa_dot import make_mesa_1, make_mesaf_1
from semiconductorDot.ohmics_dot import make_ohmics_1, make_island_1
from semiconductorDot.gates import create_finegates, create_gatepads
from alignment import rectangle_insert
# Creating layout and top cells

def create_semiconductorDot(p, um):
    layout = db.Layout(True)
    top = layout.create_cell("TOP")

    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))


    fgates = layout.layer(db.LayerInfo(4, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    mesa_region  = make_mesa_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 

    qpcregion = create_finegates(um, p) 


    cgatesrgn = create_gatepads(um, p) 

    

    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(fgates).insert(qpcregion)
    top.shapes(cgates).insert(cgatesrgn)
    

    return layout