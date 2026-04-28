import klayout.db as db
import numpy as np
import klayout.lib
import math
import gdspy
from hybridDot.hybridDot import create_hybridDot

from hallBar.hallBar import create_hallBar
from mesoWire.mesoWire import create_mesoWire
from tlm.tlm import create_tlm
from doubleDot.doubleDot import create_doubleDot
from qpchallBar.qpchallBar import create_qpchallBar
from pdgDot.pdgDot import create_pdgDot

from semiconductorDot.semiconductorDot import create_semiconductorDot
from bowtie.bowtie import create_bowtie
from bowtieTrenchless.bowtieTrenchless import create_bowtieTrenchless
from semiSens.semiSens import create_semiSens
from bowtieNoMesa.bowtieNoMesa import create_bowtieNoMesa


from alignment import make_global_alignment, make_global_alignment2, rectangle_insert

from auxiliary import create_aux1, create_aux2, create_aux3

chipsize = 4600
path = "/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/QDots-2/HMIAChipDesign/scriptcad/20250925/"

root = "20250925_HMIAII7_doubledots"

class params1():
    absolute = False
    angle = 0
    centerx = -200
    centery = -100
    dohmicsy = 250
    dohmicsx = 200
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 60
    lHallbar = 800
    w_connector = 50
    h_tcn = 0.85*dohmicsy
    w_dcn = 100
    connectorY = 0.6*dohmicsy
    num_gates = 20
    num_cols = num_gates//4

    has_topgate = False

    has_island = True

    island_sizeX = 1.0
    island_sizeY = 0.6
    qpcwidth = 0.3
    dot_length = 1.5
    finegatewidth = 0.1
    coursegatewidth = 2
    gate_separation = 14
    vl1height = 0.3*dot_length

    device_height = 5*dohmicsy
    
    gatepadwidth = 0.9*padsize
    gatepadheight = device_height/6
    gatepadx = 1*dohmicsx
    gatepady = (1/3)*device_height
    laSize = 5
    align1 = []
    align2 = []
    align3 = []
    align4 = []
    name = "Wuthering Heights"
    namex = -0.5*dohmicsx
    namey = 2.6*dohmicsy
    quotex = -0.5*dohmicsx
    quotey = 2.5*dohmicsy
    quote = "'Whatever our souls are made of, his and mine are the same.'"


class paramsSemiSens():
    absolute = False
    angle = 0
    centerx = -350
    centery = -300
    dohmicsy = 250
    dohmicsx = 200
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 100
    lHallbar = 800
    w_connector = 50
    h_tcn = 0.85*dohmicsy
    w_dcn = 100
    connectorY = 0.6*dohmicsy
    num_gates = 20
    num_cols = num_gates//4

    has_topgate = False
    has_island = True

    island_sizeX = 1.0
    island_sizeY = 0.6
    qpcwidth = 0.3
    dot_length = 1.5
    finegatewidth = 0.1
    coursegatewidth = 2
    gate_separation = 14
    vl1height = 0.3*dot_length

    device_height = 5*dohmicsy
    
    gatepadwidth = 0.9*padsize
    gatepadheight = device_height/7
    gatepadx = 0.95*dohmicsx
    gatepady = (1/3)*device_height
    laSize = 5
    align1 = []
    align2 = []
    align3 = []
    align4 = []
    name = "Jane Eyre"
    namex = -0.25*dohmicsx
    namey = 2.7*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 2.6*dohmicsy
    quote = "'Do you think that because I am poor, obscure, plain, and little, I am soulless and heartless? You think wrong!\\n\\n - I have as much soul as you, - and full as much heart!\n And if God had gifted me with some beauty and much wealth,\\n\\n I should have made it as hard for you to leave me, as it is now for me to leave you.'"

class paramsSemiSens_noisland(paramsSemiSens):
    has_island = True
    centerx = -425
    centery = 50
    dohmicsy = 250
    dohmicsx = 200
    island_sizeX = 0.6
    align1 = []
    align2 = []
    align3 = []
    align4 = []
    name = "Jane Eyre"
    namex = -0.25*dohmicsx
    namey = 2.7*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 2.6*dohmicsy
    quote = "'Do you think that because I am poor, obscure, plain, and little, I am soulless and heartless? You think wrong!\\n\\n - I have as much soul as you, - and full as much heart!\n And if God had gifted me with some beauty and much wealth,\\n\\n I should have made it as hard for you to leave me, as it is now for me to leave you.'"

    
class params_hallbar():
    absolute = False
    angle = 0
    centerx = -200
    centery = -320
    dohmicsy = 240
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 60
    lHallbar = 500
    w_connector = 35
    h_tcn = 0.85*dohmicsy
    w_dcn = 100
    connectorY = 0.6*dohmicsy

    has_topgate = True

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
    name = "Oliver Twist"
    namex = -0.25*dohmicsx
    namey = 2.0*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 1.9*dohmicsy
    quote = "'Please, sir, I want some more.'"


class params_qpchallbar(params_hallbar):
    absolute = False
    centerx = 0
    centery = -200
    angle = 90

    dohmicsx = params_hallbar.dohmicsx
    dohmicsy = params_hallbar.dohmicsy

    name = "A Study in Scarlet"
    namex = -1*dohmicsx
    namey = 2.0*dohmicsy
    quotex = -1*dohmicsx
    quotey = 1.9*dohmicsy
    quote = "'From a drop of water, a logician could infer the possibility of an Atlantic or a Niagara without having seen or heard of one or the other.\\n\\n So all life is a great chain, the nature of which is known whenever we are shown a single link of it.'"

class params_mesowire():
    absolute = False
    angle = 0
    centerx = -800
    centery = -300
    dohmicsy = 220
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 20
    lHallbar = 450

    wWire = 0.8
    lWire = 400

    w_connector = 35
    h_tcn = 0.93*dohmicsy
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
    name = "David Copperfield"
    namex = -0.25*dohmicsx
    namey = 2.1*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 2.0*dohmicsy
    quote = "'Whether I shall turn out to be the hero of my own life, or whether that station \\n\\nwill be held by anybody else, these pages must show.'"

class params_m2(params_mesowire):
    absolute = True
    wWire = 0.6
    lWire = 400
    centerx = 1750
    centery = 0
    dohmicsy = 220
    dohmicsx = 400
    name = "David Copperfield, with M2 wires"
    namex = -0.25*dohmicsx
    namey = 2.1*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 2.0*dohmicsy
    quote = "'Whether I shall turn out to be the hero of my own life, or"

class params_m3(params_mesowire):
    absolute = True
    wWire = 0.5
    lWire = 400
    name = "David Copperfield, with M2 wires"
    centerx = -2100
    centery = 0
    dohmicsy = 220
    dohmicsx = 400
    namex = -0.25*dohmicsx
    namey = 2.1*dohmicsy
    quotex = -0.25*dohmicsx
    quotey = 2.0*dohmicsy
    quote = "'Whether I shall turn out to be the hero of my own life, or"


class params_diff(params1):
    absolute = False
    centerx = -300
    centery = -300
    dohmicsx = 200
    dohmicsy = 250
    has_island = False
    name = "Wuthering Heights"
    namex = -0.5*dohmicsx
    namey = 2.6*dohmicsy
    quotex = -0.5*dohmicsx
    quotey = 2.5*dohmicsy
    quote = "'Whatever our souls are made of, his and mine are the same.'"


class params_ambitious(params1):
    absolute = False
    centerx = -300
    centery = 75
    dohmicsx = 200
    dohmicsy = 250

    island_sizeX = 0.3
    island_sizeY = 0.5
    dot_length = 0.8
    vl1height = 0.5*dot_length

    has_island = True
    name = "Wuthering Heights"
    namex = -0.5*dohmicsx
    namey = 2.6*dohmicsy
    quotex = -0.5*dohmicsx
    quotey = 2.5*dohmicsy
    quote = "'Whatever our souls are made of, his and mine are the same.'"

class params_medium(params1):
    absolute = False
    centerx = -150
    centery = 50
    dohmicsx = 200
    dohmicsy = 250
    has_island = True

    island_sizeX = 0.6
    island_sizeY = 0.6
    dot_length = 1.1
    vl1height = 0.4*dot_length

    name = "Wuthering Heights"
    namex = -0.5*dohmicsx
    namey = 2.6*dohmicsy
    quotex = -0.5*dohmicsx
    quotey = 2.5*dohmicsy
    quote = "'Whatever our souls are made of, his and mine are the same.'"

class paramsqdot():
    absolute = True
    angle = 0
    centerx = 1300
    centery = -1500
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
    laSize = 5
    align1 = []
    align2 = []
    align3 = []
    align4 = []

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



class params_tlm(paramsqdot):
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
    centery = -2100
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
    centery = 2100

class params_aux5(params_aux2):
    centery = 2100

class params_aux6(params_aux3):
    centery = 2100

um = 1e3

align = db.LayerInfo(1, 0)

alignPt = db.LayerInfo(0, 0)

mesaPos = db.LayerInfo(2, 0)
ohmics = db.LayerInfo(3, 0)
mesaNeg = db.LayerInfo(10, 0)
island = db.LayerInfo(61, 0)
fgates = db.LayerInfo(4, 0)
cgates = db.LayerInfo(5, 0)
patches = db.LayerInfo(6, 0)


gpads = db.LayerInfo(7,0)


mlayout = db.Layout(True)
top = mlayout.create_cell("TOP")

aux_layout = db.Layout(True)
aux_top = aux_layout.create_cell("TOP")


device_params = [params1(), params_hallbar(), params_mesowire(), params_qpchallbar(), paramsSemiSens(), params_diff(), params_medium(), params_ambitious(), paramsSemiSens_noisland(), paramsqdot(), params_m2(), params_m3()]

device_funcs = [create_doubleDot, create_hallBar, create_mesoWire, create_qpchallBar, create_semiSens, create_doubleDot, create_doubleDot, create_doubleDot, create_semiSens, create_hybridDot, create_mesoWire, create_mesoWire]



#device_centers = [(0,0), (850, 0), (-850, 0), (0, -850), (0, 850), (850, 850), (-850, 850)]

coord_array = np.linspace(-1200, 1200, 3, True)
print(coord_array)
x, y = np.meshgrid(coord_array, coord_array)

device_centers = [(x.flatten()[k], y.flatten()[k]) for k in range(len(x.flatten()))]
for k, p in enumerate(device_params):
    if p.absolute:
        p.centerx = p.centerx
        p.centery = p.centery
    else:
        p.centerx = p.centerx + device_centers[k][0]
        p.centery = p.centery + device_centers[k][1]

layers = [alignPt, align, mesaPos, ohmics, mesaNeg, island, fgates, cgates, patches, gpads]



device_layouts = [device_funcs[k](device_params[k], um) for k in range(len(device_params))]

align_layer = mlayout.layer(align)
alignPt_layer = mlayout.layer(alignPt)
ohmics_layer = mlayout.layer(ohmics)
fgates_layer = mlayout.layer(fgates)
cgates_layer = mlayout.layer(cgates)
patches_layer = mlayout.layer(patches)
gpads_layer = mlayout.layer(gpads)


top.shapes(align_layer).insert(make_global_alignment(um, top, chipsize, align_layer))
top.shapes(alignPt_layer).insert(make_global_alignment2(um, top, chipsize, alignPt_layer))

##local alignment
mesaPos_mrgn = db.Region()
#  for k, p in enumerate(device_params):
#     amark = db.Box(5*um, 5*um)
#     align_rgn = rectangle_insert(amark, 90*um, 90*um)
#     align_rgn += rectangle_insert(amark, 90*um, 50*um)
#     ohmics_rgn = rectangle_insert(amark, 50*um, 50*um)
#     fgates_rgn = rectangle_insert(amark, 50*um, 90*um)
    
#     boxSize = 30
#     locx = 90
#     locy = 50

#     rgnlm = db.Region()
#     rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(locx*um, locy*um))
#     rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(-locx*um, locy*um))
#     rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(locx*um, -locy*um))
#     rgnlm.insert(db.Box(boxSize*um, boxSize*um).moved(-locx*um, -locy*um))

#     mesaPos_mrgn += rgnlm.moved(p.centerx*um, p.centery*um)

#     top.shapes(align_layer).insert(align_rgn.moved(p.centerx*um, p.centery*um))
#     top.shapes(ohmics_layer).insert(ohmics_rgn.moved(p.centerx*um, p.centery*um))
#     top.shapes(fgates_layer).insert(fgates_rgn.moved(p.centerx*um, p.centery*um))

mesa_boundary = db.Region() 
box1 = db.Box(4000*um, (chipsize)*um)
box2 = db.Box(chipsize*um, 1200*um)
mesa_boundary.insert(box1)
mesa_boundary.insert(box2)
mesa_boundary.merged()

aux_params = [params_aux1(), params_aux2(),params_aux3(),
              params_aux4(), params_aux5(), params_aux6()]
aux_layouts = [create_aux1(p, um) for p in aux_params]

aux_layouts += [create_aux2(um)]
aux_layouts += [create_aux3(um)]

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
        top.shapes(master_layer).insert((mesa_boundary-r1-mesaPos_mrgn).merged())
    elif layerinfo == cgates:
        r2 = r1.dup()
        top.shapes(master_layer).insert(r1.merged())
        aux_top.shapes(aux_layer).insert(ar1.merged())
    else:
        top.shapes(master_layer).insert(r1.merged())
        aux_top.shapes(aux_layer).insert(ar1.merged())
    
gpads_layer = mlayout.layer(gpads)
r2.size(-25*um)
r2.size(25*um)
top.shapes(gpads_layer).insert(r2)



mlayout.write(path+root + ".gds")

for k, layout in enumerate(device_layouts):
    layout.write(path + root+ f"device{k}.gds")
    
render_gds = gdspy.GdsLibrary(infile=path+root+".gds")
all_cells = render_gds.top_level()
cell = all_cells[0]
for iter_cell in all_cells:
    if iter_cell.name == 'TOP':
        cell = iter_cell
        break
cell.write_svg(path+root+ ".svg", background = None)

aux_layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             f"QDots-2/HMIAChipDesign/scriptcad/20250925/20250925_HMIAII7_doubledots_device{len(device_layouts)}.gds")