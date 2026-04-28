import klayout.db as db
import klayout.lib
import math
from hybridDot.mesa_dot import make_mesa_1, make_mesaf_1
from hybridDot.ohmics_dot import make_ohmics_1, make_island_1
from hybridDot.gates import create_finegates, create_gatepads

# Creating layout and top cells


def create_hybridDot(p, um):
    #layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                # "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")
    layout = db.Layout(True)
    top = layout.create_cell("TOP")

    align = layout.layer(db.LayerInfo(1, 0))
    
    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))

    
    mesaNeg = layout.layer(db.LayerInfo(10, 0))

    island = layout.layer(db.LayerInfo(61, 0))

    fgates = layout.layer(db.LayerInfo(4, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))

    align_rgn  = make_align_marks(p, um)
    mesa_region  = make_mesa_1(um, p) 
    ohmics_region  = make_ohmics_1(um, p) 
    island_region  = make_island_1(um, p) 

    qpcregion = create_finegates(um, p) 

    mesaf = make_mesaf_1(um, p) 

    cgatesrgn = create_gatepads(um, p) 

    
    top.shapes(align).insert(align_rgn)
    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaNeg).insert(mesaf)
    top.shapes(mesaPos).insert(mesa_region)
    top.shapes(island).insert(island_region)
    top.shapes(fgates).insert(qpcregion)
    top.shapes(cgates).insert(cgatesrgn)
    

    return layout

def make_align_marks(p, um):
    align_rgn =  db.Region()

    mark = db.Box(p.laSize*um, p.laSize*um)
    
    p.align1 = [(-200, 100),
                (200, 100),
                (200, -100),
                (-200, -100),
    ]
    
    p.align2 = [(-70, 70),
                (70, 70),
                (70, -70),
                (-70, -70),
    ]

    p.align3 = [(-380, 135),
                (380, 135),
                (380, -135),
                (-380, -135),
    ]

    p.align4 = [(-380, 65),
                (380, 65),
                (380, -65),
                (-380, -65),
    ]

    for pos in p.align1:
        align_rgn.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    for pos in p.align2:
        align_rgn.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))

    
    return align_rgn.transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
