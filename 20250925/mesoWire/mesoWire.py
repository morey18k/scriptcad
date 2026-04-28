import klayout.db as db
import klayout.lib
import math
from mesoWire.mesa_dot import make_mesa_1, make_mesaf_1
from mesoWire.ohmics_dot import make_ohmics_1
from mesoWire.gates import  create_gatepads
from alignment import rectangle_insert
# Creating layout and top cells

def create_mesoWire(p, um):
    #layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                # "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")
    layout = db.Layout(True)
    top = layout.create_cell("TOP")

    other_align = layout.layer(db.LayerInfo(0, 0))
    mesaPos = layout.layer(db.LayerInfo(2, 0))
    mesaNeg = layout.layer(db.LayerInfo(10, 0))
    ohmics = layout.layer(db.LayerInfo(3, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    mesa_region  = make_mesa_1(um, p) 
    mesaf = make_mesaf_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 
    cgatesrgn = create_gatepads(um, p) 

    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(mesaNeg).insert(mesaf)
    top.shapes(cgates).insert(cgatesrgn)

    parameters_title = {
        "layer": layout.get_info(other_align),
        "text": f"{p.name}",
        "mag": 20
        }
    
    parameters_quote = {
        "layer": layout.get_info(other_align),
        "text": f"{p.quote}",
        "mag": 10
    }


    cellt = layout.create_cell("TEXT", "Basic", parameters_title)
    cellq = layout.create_cell("TEXT", "Basic", parameters_quote)

    top.insert(db.CellInstArray(cellt.cell_index(), db.Trans((p.namex+p.centerx)*um, (p.namey+p.centery)*um)))
    top.insert(db.CellInstArray(cellq.cell_index(), db.Trans((p.quotex+p.centerx)*um, (p.quotey+p.centery)*um)))

    

    return layout