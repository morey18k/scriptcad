import klayout.db as db
import numpy as np
import klayout.lib
import math
from hallBar.hallBar import create_hallBar
from tlm.tlm import create_tlm
from hybridDot.hybridDot import create_hybridDot
from pdgDot.pdgDot import create_pdgDot

from semiconductorDot.semiconductorDot import create_semiconductorDot
from bowtie.bowtie import create_bowtie
from bowtieTrenchless.bowtieTrenchless import create_bowtieTrenchless

from bowtieNoMesa.bowtieNoMesa import create_bowtieNoMesa


from alignment import make_global_alignment, rectangle_insert

from auxiliary import create_aux1, create_aux2

chipsize = 3350

class params1():
    angle = 0
    centerx = 0
    centery = 0
    dohmicsy = 220
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 60
    lHallbar = 450
    w_connector = 35
    h_tcn = 0.85*dohmicsy
    w_dcn = 100
    connectorY = 0.6*dohmicsy

    has_topgate = False

    island_sizeX = 0.6
    island_sizeY = 1
    qpcwidth = 0.3
    dot_length = 2
    finegatewidth = 0.1
    coursegatewidth = 2
    gate_separation = 14
    vl1height = 0.3*dot_length

    device_height = (3*dohmicsy+padsize+2*cronSize)
    
    gatepadwidth = 0.7*padsize
    gatepadheight = device_height/3.7
    gatepadx = 0.95*dohmicsx
    gatepady = (1/3)*device_height


class params_bowtie(params1):
    dot_length = 10
    island_sizeY = 2
    island_sizeX = 1
    vl1height = 0.3*dot_length
    trenchsize = 0.3

class params_bowtieTrenchless(params_bowtie):
    island_sizeX = 2
    island_sizeY = 0.6

class params_pdGDot(params_bowtieTrenchless):
    dot_length = 2
    vl1height = 0.3*dot_length
    holeDot = False
    small_island = False

class params_pdGDot2(params_pdGDot):
    angle = 90
    holeDot = False

class params_pdGDot3(params_pdGDot):
    holeDot = True
    dot_length = 2.5
    vl1height = 0.3*dot_length
    island_sizeX = 1.2
    island_sizeY = 1.2

class params_pdGDot4(params_pdGDot):
    holeDot = True
    small_island = True
    dot_length = 1.6
    vl1height = 0.3*dot_length
    island_sizeX = 0.7
    island_sizeY = 0.7
    

class params_sconductor2(params1):
    dot_length = 1
    island_sizeX = 0.3
    vl1height = 0.3*dot_length

class params_gatedHallBar(params1):
    has_topgate = True

class params_bowtiepdg(params1):
    dot_length = 10
    island_sizeY = 1
    vl1height = 0.435*dot_length
    disable_mesa = True


class params2(params1):
    angle = 90

class params_sconductor1(params1):
    dot_length = 2
    vl1height = 0.375*dot_length


class params_tlm(params1):
    dohmicsy = 240
    dohmicsx = 400

    wHallbar = 20
    lHallbar = 800

    connector_widthX = wHallbar+2
    island_sizeX = 1
    island_sizeY = 1
    hastrench = False
    trenchsize = 0.3
    connectorSize = 0.2

class params_tlm2(params_tlm):
    hastrench = True
    trenchsize = 0.5
    island_sizeY = 2

class params_tlm3(params_tlm):
    angle = 90

class params_tlm4(params_tlm):
    hastrench = True
    angle = 90
    island_sizeY = 2
    trenchsize = 0.5

class params_tlm5(params_tlm):
    pass

class params_aux1():
    angle = 90
    centery = -1500
    centerx = 385
    has_trench = True
    has_island = True
    trenchsize = 0.3

class params_aux2(params_aux1):
    angle = 90
    centerx = 0
    has_trench = True
    has_island = False

class params_aux3(params_aux1):
    centerx = -385
    angle = 90
    has_trench = False
    has_island = False

class params_aux4(params_aux1):
    centery = 1500

class params_aux5(params_aux2):
    centery = 1500

class params_aux6(params_aux3):
    centery = 1500

um = 1e3

align = db.LayerInfo(1, 0)
mesaPos = db.LayerInfo(2, 0)
ohmics = db.LayerInfo(3, 0)
mesaNeg = db.LayerInfo(10, 0)
island = db.LayerInfo(61, 0)
fgates = db.LayerInfo(4, 0)
cgates = db.LayerInfo(5, 0)

gpads = db.LayerInfo(6,0)


mlayout = db.Layout(True)
top = mlayout.create_cell("TOP")

aux_layout = db.Layout(True)
aux_top = aux_layout.create_cell("TOP")

device_params = [params1(), params2(), params1(), params2(), params_sconductor1(), 
                 params_bowtie(), params_tlm(), params_bowtieTrenchless, 
                 params_pdGDot(), params_sconductor2(), params_tlm2(), 
                 params_gatedHallBar(), params_pdGDot2(), params_tlm3(),
                params_pdGDot3(), params_bowtiepdg()]

device_funcs = [create_hybridDot, create_hybridDot, create_hallBar, create_hallBar, 
                create_semiconductorDot, create_bowtie, create_tlm, create_bowtieTrenchless, 
                create_pdgDot, create_semiconductorDot, create_tlm, 
                create_hallBar, create_pdgDot, create_tlm,
                create_pdgDot, create_bowtieNoMesa]

device_params = [params_tlm(), params_tlm2(), params_tlm3(), params_tlm4(), params2(), 
                 params_gatedHallBar(), params_bowtie(), params_bowtieTrenchless, 
                 params1()]

device_funcs = [create_tlm, create_tlm, create_tlm, create_tlm, create_hallBar, create_hallBar, 
                create_bowtie, create_bowtieTrenchless, create_hybridDot]



#device_centers = [(0,0), (850, 0), (-850, 0), (0, -850), (0, 850), (850, 850), (-850, 850)]

coord_array = np.linspace(-900, 900, 3, True)
print(coord_array)
x, y = np.meshgrid(coord_array, coord_array)

device_centers = [(x.flatten()[k], y.flatten()[k]) for k in range(len(device_params))]
for k, p in enumerate(device_params):
    p.centerx = device_centers[k][0]
    p.centery = device_centers[k][1]

layers = [align, mesaPos, ohmics, mesaNeg, island, fgates, cgates]



device_layouts = [device_funcs[k](device_params[k], um) for k in range(len(device_params))]

align_layer = mlayout.layer(align)
ohmics_layer = mlayout.layer(ohmics)
fgates_layer = mlayout.layer(fgates)

top.shapes(align_layer).insert(make_global_alignment(um, top, chipsize, align_layer))


##local alignment
mesaPos_mrgn = db.Region()
for k, p in enumerate(device_params):
    amark = db.Box(5*um, 5*um)
    align_rgn = rectangle_insert(amark, 90*um, 90*um)
    align_rgn += rectangle_insert(amark, 90*um, 50*um)
    ohmics_rgn = rectangle_insert(amark, 50*um, 50*um)
    fgates_rgn = rectangle_insert(amark, 50*um, 90*um)
    
    boxSize = 30
    locx = 90
    locy = 50

    rgnlm = db.Region()
    rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(locx*um, locy*um))
    rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(-locx*um, locy*um))
    rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(locx*um, -locy*um))
    rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(-locx*um, -locy*um))

    mesaPos_mrgn += rgnlm.moved(p.centerx*um, p.centery*um)

    top.shapes(align_layer).insert(align_rgn.moved(p.centerx*um, p.centery*um))
    top.shapes(ohmics_layer).insert(ohmics_rgn.moved(p.centerx*um, p.centery*um))
    top.shapes(fgates_layer).insert(fgates_rgn.moved(p.centerx*um, p.centery*um))

mesa_boundary = db.Region() 
box1 = db.Box(3600*um, chipsize*um)
box2 = db.Box(chipsize*um, 1150*um)
mesa_boundary.insert(box1)
mesa_boundary.insert(box2)
mesa_boundary.merged()

aux_params = [params_aux1(), params_aux2(),params_aux3(),
              params_aux4(), params_aux5(), params_aux6()]
aux_layouts = [create_aux1(p, um) for p in aux_params]

aux_layouts += [create_aux2(um)]

r2 = db.Region()
for layerinfo in layers:
    r1 = db.Region()
    ar1 = db.Region()
    for layout in device_layouts:
        l = layout.layer(layerinfo)
        r1 += db.Region(layout.top_cell().begin_shapes_rec(l))
    for layout in aux_layouts:
        l = layout.layer(layerinfo)
        r1 += db.Region(layout.top_cell().begin_shapes_rec(l))
        ar1 += db.Region(layout.top_cell().begin_shapes_rec(l))
    master_layer = mlayout.layer(layerinfo)
    aux_layer = aux_layout.layer(layerinfo)
    if layerinfo == mesaPos:
        top.shapes(master_layer).insert(mesa_boundary-r1-mesaPos_mrgn)
    elif layerinfo == cgates:
        r2 = r1.dup()
        top.shapes(master_layer).insert(r1)
        aux_top.shapes(aux_layer).insert(ar1)
    else:
        top.shapes(master_layer).insert(r1)
        aux_top.shapes(aux_layer).insert(ar1)
    
gpads_layer = mlayout.layer(gpads)
r2.size(-25*um)
r2.size(25*um)
top.shapes(gpads_layer).insert(r2)



mlayout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20250116/20250116_HMIAII6_pdgrtatest.gds")

for k, layout in enumerate(device_layouts):
    layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             f"QDots-2/HMIAChipDesign/scriptcad/20250116/20250116_HMIAII6_pdgrtatest_device{k}.gds")
    
aux_layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             f"QDots-2/HMIAChipDesign/scriptcad/20250116/20250116_HMIAII6_pdgrtatest_device{len(device_layouts)}.gds")