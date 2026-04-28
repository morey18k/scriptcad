import klayout.db as db
import klayout.lib
import math
from semiSens.mesa_dot import make_mesa_1, make_mesaf_1
from semiSens.ohmics_dot import make_ohmics_1, make_island_1
from semiSens.gates import create_finegates, create_finegates_med, create_gatepads, create_patches
# Creating layout and top cells


def create_semiSens(p, um):
    #layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                # "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")
    layout = db.Layout(True)
    top = layout.create_cell("TOP")

    other_align = layout.layer(db.LayerInfo(0, 0))

    align = layout.layer(db.LayerInfo(1, 0))
    
    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))


    mesaNeg = layout.layer(db.LayerInfo(10, 0))

    island = layout.layer(db.LayerInfo(61, 0))

    fgates = layout.layer(db.LayerInfo(4, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    patches = layout.layer(db.LayerInfo(6, 0))

    
    align_region  = make_align_marks(p, um) 
    mesa_region  = make_mesa_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 
    island_region  = make_island_1(um, p) 

    if p.island_sizeX <0.8:         
        qpcregion = create_finegates_med(um, p)
    else:
        qpcregion = create_finegates(um, p) 

    mesaf = make_mesaf_1(um, p) 

    cgatesrgn = create_gatepads(um, p) 

    patchesrgn = create_patches(um, p) 

    top.shapes(align).insert(align_region)

    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaNeg).insert(mesaf)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(island).insert(island_region)
    top.shapes(fgates).insert(qpcregion)
    top.shapes(cgates).insert(cgatesrgn)
    top.shapes(patches).insert(patchesrgn)

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

def make_align_marks(p, um):
    align_rgn =  db.Region()

    mark = db.Box(p.laSize*um, p.laSize*um)
    p.align1 = [(-230, 375),
                (85, 365),
                (85, -365),
                (-230, -375),
    ]

    p.align2 = [(-170, 130),
                (85, 280),
                (85, -280),
                (-170, -130),
    ]

    p.align3 = [(-75, 275),
                (85, 230),
                (85, -230),
                (-75, -275),
    ]

    p.align4 = [(-270, 130),
                (85, 25),
                (85, -25),
                (-270, -130),
    ]

    for pos in p.align1:
        align_rgn.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    for pos in p.align2:
        align_rgn.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    
    return align_rgn.transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

