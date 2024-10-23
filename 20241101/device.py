import klayout.db as db
import klayout.lib
import math
from hallBar.hallBar import create_hallBar
from hybridDot.hybridDot import create_hybridDot
from semiconductorDot.semiconductorDot import create_semiconductorDot
from bowtie.bowtie import create_bowtie
from alignment import make_global_alignment, rectangle_insert

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


class params2():
    angle = 90
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

class params3():
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
    dot_length = 10
    finegatewidth = 0.1
    coursegatewidth = 2
    gate_separation = 14

    device_height = (3*dohmicsy+padsize+2*cronSize)
    
    gatepadwidth = 0.6*padsize
    gatepadheight = device_height/3.2
    gatepadx = 0.9*dohmicsx
    gatepady = (1/3)*device_height


um = 1e3

align = db.LayerInfo(1, 0)
mesaPos = db.LayerInfo(2, 0)
ohmics = db.LayerInfo(3, 0)
mesaNeg = db.LayerInfo(10, 0)
island = db.LayerInfo(61, 0)
fgates = db.LayerInfo(4, 0)
cgates = db.LayerInfo(5, 0)



mlayout = db.Layout(True)
top = mlayout.create_cell("TOP")

device_params = [params1(), params2(), params1(), params2(), params1(), params3()]
device_funcs = [create_hybridDot, create_hybridDot, create_hallBar, create_hallBar, create_semiconductorDot, create_bowtie]
device_centers = [(0,0), (850, 0), (-850, 0), (0, -850), (0, 850), (850, 850)]

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
for k, p in enumerate(device_params):
    amark = db.Box(5*um, 5*um)
    align_rgn = rectangle_insert(amark, 60*um, 80*um)
    align_rgn += rectangle_insert(amark, 80*um, 60*um)
    ohmics_rgn = rectangle_insert(amark, 60*um, 60*um)
    fgates_rgn = rectangle_insert(amark, 80*um, 80*um)

    top.shapes(align_layer).insert(align_rgn.moved(p.centerx*um, p.centery*um))
    top.shapes(ohmics_layer).insert(ohmics_rgn.moved(p.centerx*um, p.centery*um))
    top.shapes(fgates_layer).insert(fgates_rgn.moved(p.centerx*um, p.centery*um))

mesa_boundary = db.Region() 
box1 = db.Box(4300*um, 5000*um)
box2 = db.Box(5000*um, 2000*um)
mesa_boundary.insert(box1)
mesa_boundary.insert(box2)
mesa_boundary.merged()

for layerinfo in layers:
    r1 = db.Region()
    for layout in device_layouts:
        l = layout.layer(layerinfo)
        r1 += db.Region(layout.top_cell().begin_shapes_rec(l))
    master_layer = mlayout.layer(layerinfo)
    if layerinfo == mesaPos:
        top.shapes(master_layer).insert(mesa_boundary-r1)
    else:
        top.shapes(master_layer).insert(r1)


mlayout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/device.gds")

for k, layout in enumerate(device_layouts):
    layout.write(f"/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/device{k}.gds")