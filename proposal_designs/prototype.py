import klayout.db as db
import numpy as np

def return_path(polygon, angle, length_path, threshold, pathwidth, um = 1e3):
    list_points = list(polygon.each_point_hull())
    counter = 0
    xsum = 0
    ysum = 0
    
    lowest_index = 0
    for k, point in enumerate(list_points):
        if threshold < 0:
            if point.y < list_points[lowest_index].y:
                lowest_index = k
        if threshold > 0:
            if point.y > list_points[lowest_index].y:
                lowest_index = k
    
    lower_index = lowest_index+1
    for k, point in enumerate(list_points):
        if k == lowest_index:
            continue
        if threshold < 0:
            if point.y < list_points[lower_index].y:
                lower_index = k
        if threshold > 0:
            if point.y > list_points[lower_index].y:
                lower_index = k
    """

    for point in list_points:
        if threshold < 0:
            if point.y<threshold:
                xsum +=point.x
                ysum +=point.y
                counter +=1
        if threshold > 0:
            if point.y>threshold:
                xsum +=point.x
                ysum +=point.y
                counter +=1
    """
    x0 = 0.5*(list_points[lowest_index].x + list_points[lower_index].x)
    y0 = 0.5*(list_points[lowest_index].y + list_points[lower_index].y)

    lc = length_path*np.cos(np.pi*angle/180)*um
    ls = length_path*np.sin(np.pi*angle/180)*um

    c = 4*np.cos(np.pi*angle/180)*um
    s = 4*np.sin(np.pi*angle/180)*um

    if threshold < 0:
        point1 = db.Point(x0-0.01*s, y0 + 0.01*c)
        point2 = db.Point(x0+0.1*ls, y0-0.1*lc)
        point3= db.Point(x0+ls, y0-lc)

    if threshold > 0:
        point1 = db.Point(x0-0.01*s, y0 - 0.01*c)
        point2 = db.Point(x0+0.1*ls, y0+0.1*lc)
        point3 = db.Point(x0+ls, y0+lc)
    return db.Path([point1, point2, point3], pathwidth*um)
        

def create_qpc(widthqpc, height_gate = 0.1, length_gate = 0.2, um = 1e3):
    rect = db.Box((length_gate-0.1)*um, height_gate*um)
    qpcregion = db.Region()
    qpcregion.insert(rect.transformed(db.ICplxTrans.new(1, 0, False, -0.5*widthqpc*um-0.5*length_gate*um+0.05*um, 0)))
    qpcregion.insert(rect.transformed(db.ICplxTrans.new(1, 0, False, 0.5*widthqpc*um+0.5*length_gate*um-0.05*um, 0)))
    qpcregion.round_corners(0.1*um, 0.1*um, 32)
    rect = db.Box((length_gate-0.05)*um, height_gate*um)
    qpcregion.insert(rect.transformed(db.ICplxTrans.new(1, 0, False, (-0.5*widthqpc-0.5*length_gate-0.025)*um, 0)))
    qpcregion.insert(rect.transformed(db.ICplxTrans.new(1, 0, False, (0.5*widthqpc+0.5*length_gate+0.025)*um, 0)))
    return qpcregion.merged()

def create_trench(um, p):
    sq3p2 = np.sqrt(3)/2
    trench_region = db.Region()
    trench1 = db.Region(db.Box(p.trenchwidth*um, 0.7*p.island_spacing*um))
    tregion = db.Region()
    tregion += trench1.transformed(db.ICplxTrans.new(1, -60, False, 0, 0)).moved(-sq3p2*p.tl1*um, -(1/2)*p.tl1*um)
    tregion += trench1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0)).moved(0, p.tl1*um)
    tregion += trench1.transformed(db.ICplxTrans.new(1, 60, False, 0, 0)).moved(sq3p2*p.tl1*um, -(1/2)*p.tl1*um)
    tregion += trench1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0)).moved(0, -p.tl1*um)

    tregion.merge()
    #trench_region += tregion.moved((1/2)*p.tl*um, (1/3)*sq3p2*p.tl*um)
    #trench_region += tregion.moved(-(1/2)*p.tl*um, (1/3)*sq3p2*p.tl*um)
    trench_region += tregion.moved(0*um, (-2/3)*sq3p2*p.tl*um)
    trench_region += tregion.moved(0*um, (-2/3)*sq3p2*p.tl*um).transformed(db.ICplxTrans.new(1, -120, False, 0, 0))
    trench_region += tregion.moved(0*um, (-2/3)*sq3p2*p.tl*um).transformed(db.ICplxTrans.new(1, 120, False, 0, 0))

    return trench_region.merged()

def create_finegates(um, p):
    finegates_region = db.Region()

    sq3p2 = np.sqrt(3)/2
    qpc1 = create_qpc(0.3, length_gate= p.island_spacing*0.5, um = um)

    qpc2 = create_qpc(0.3, length_gate= 0.2, um = um)

    finegates_region += qpc1.transformed(db.ICplxTrans.new(1, 90, False, 0*um, (2/3)*sq3p2*p.qlength*um))
    finegates_region += qpc1.transformed(db.ICplxTrans.new(1, -30, False, (1/2)*p.qlength*um, -(1/3)*sq3p2*p.qlength*um))
    finegates_region += qpc1.transformed(db.ICplxTrans.new(1, 30, False, -(1/2)*p.qlength*um, -(1/3)*sq3p2*p.qlength*um))
    
    qpcleft = qpc2.transformed(db.ICplxTrans.new(1, -20, False, -0.4*um, -(2/3)*sq3p2*p.lead_length*um))
    qpcright = qpc2.transformed(db.ICplxTrans.new(1, 20, False, 0.4*um, -(2/3)*sq3p2*p.lead_length*um))

    finegates_region += qpcleft
    finegates_region += qpcright
    finegates_region += qpcleft.transformed(db.ICplxTrans.new(1, -120, False, 0, 0))
    finegates_region += qpcright.transformed(db.ICplxTrans.new(1, -120, False, 0, 0))

    finegates_region += qpcleft.transformed(db.ICplxTrans.new(1, 120, False, 0, 0))
    finegates_region += qpcright.transformed(db.ICplxTrans.new(1, 120, False, 0, 0))


    qpc3 = create_qpc(0.3, length_gate= 0.65, um = um).rounded_corners(0.1*um, 0.1*um, 64)


    finegates_region += qpc3.moved(0*um, -p.island_spacing*um).transformed(db.ICplxTrans.new(1, -60, False, 0*um, 0*um))
    finegates_region += qpc3.moved(0*um, -p.island_spacing*um).transformed(db.ICplxTrans.new(1, 60, False, 0*um, 0*um))
    finegates_region += qpc3.moved(0*um, -p.island_spacing*um).transformed(db.ICplxTrans.new(1, 180, False, 0*um, 0*um))


    lboxgate = db.Polygon(db.Box(0.1*um, p.long_gatelength*um))
    lfanout = 20

    polygon1 = lboxgate.moved(-0.4*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, -60, False, 0*um, 0*um))
    finegates_region+= polygon1
    path1 = return_path(polygon1, -72, lfanout, -1, 0.1, um)
    finegates_region+= path1

    polygon2 = lboxgate.moved(0.4*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, -60, False, 0*um, 0*um))
    finegates_region+= polygon2
    path2 = return_path(polygon2, -36, lfanout, -1, 0.1, um)
    finegates_region+= path2
    
    polygon3 = lboxgate.moved(0*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, -60, False, 0*um, 0*um))
    finegates_region+= polygon3
    path3 = return_path(polygon3, -54, lfanout, -1, 0.1, um)
    finegates_region+= path3


    polygon4= lboxgate.moved(1.05*p.island_length*um, -0.97*(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, -60, False, 0*um, 0*um))
    finegates_region+= polygon4
    path4 = return_path(polygon4, -18, lfanout, -1, 0.1, um)
    finegates_region+= path4

    polygon5 = lboxgate.moved(-1.05*p.island_length*um, -0.97*(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, 60, False, 0*um, 0*um))
    finegates_region+= polygon5
    path5 = return_path(polygon5, 18, lfanout, -1, 0.1, um)
    finegates_region+= path5

    box_gate = db.Box(0.1*um, p.long_gatelength*um)
    
    mboxgate  = db.Polygon(box_gate).moved(-0.3*um, -0.5*p.long_gatelength*um)
    polygon6 = mboxgate.transformed(db.ICplxTrans.new(1, 20, False, 0.4*um, -(2/3)*sq3p2*p.lead_length*um))
    finegates_region+= polygon6
    path6 = return_path(polygon6, 0, lfanout, -1, 0.1, um)
    finegates_region+= path6

    mboxgate  = db.Polygon(box_gate).moved(0.3*um, -0.5*p.long_gatelength*um)
    polygon7 = mboxgate.transformed(db.ICplxTrans.new(1, -20, False, -0.4*um, -(2/3)*sq3p2*p.lead_length*um))
    finegates_region+= polygon7
    path7 = return_path(polygon7, 0, lfanout, -1, 0.1, um)
    finegates_region+= path7

    polygon8 = lboxgate.moved(-0.4*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, 60, False, 0*um, 0*um))
    finegates_region+= polygon8
    path8 = return_path(polygon8, 36, lfanout, -1, 0.1, um)
    finegates_region+= path8

    polygon9 = lboxgate.moved(0.4*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, 60, False, 0*um, 0*um))
    finegates_region+= polygon9
    path9 = return_path(polygon9, 72, lfanout, -1, 0.1, um)
    finegates_region+= path9

    polygon10 = lboxgate.moved(0*um, -(p.island_spacing+p.long_gatelength*0.5)*um).transformed(db.ICplxTrans.new(1, 60, False, 0*um, 0*um))
    finegates_region+= polygon10
    path10 = return_path(polygon10, 54, lfanout, -1, 0.1, um)
    finegates_region+= path10

    polygon11 = polygon4.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon11
    path11 = return_path(polygon11, -36, lfanout, 1, 0.1, um)
    finegates_region+= path11

    polygon12 = polygon5.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon12
    path12 = return_path(polygon12, -90, lfanout, -1, 0.1, um)
    finegates_region+= path12

    polygon13 = polygon6.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon13
    path13 = return_path(polygon13, -72, lfanout, 1, 0.1, um)
    finegates_region+= path13

    polygon14 = polygon7.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon14
    path14 = return_path(polygon14, -54, lfanout, 1, 0.1, um)
    finegates_region+= path14

    polygon15 = polygon1.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon15
    path15 = return_path(polygon15, 18, lfanout, 1, 0.1, um)
    finegates_region+= path15

    polygon16 = polygon2.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon16
    path16 = return_path(polygon16, -18, lfanout, 1, 0.1, um)
    finegates_region+= path16
    
    polygon17 =  polygon3.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um))
    finegates_region+= polygon17
    path17 = return_path(polygon17, 0, lfanout, 1, 0.1, um)
    finegates_region+= path17


    polygon18 = polygon4.transformed(db.ICplxTrans.new(1, 120, False, 0*um, 0*um))
    finegates_region+= polygon18
    path18 = return_path(polygon18, 90, lfanout, -1, 0.1, um)
    finegates_region+= path18

    polygon19 = polygon5.transformed(db.ICplxTrans.new(1, 120, False, 0*um, 0*um))
    finegates_region+= polygon19
    path19 = return_path(polygon19, 36, lfanout, 1, 0.1, um)
    finegates_region+= path19

    polygon20 = polygon6.transformed(db.ICplxTrans.new(1, 120, False, 0*um, 0*um))
    finegates_region+= polygon20
    path20 = return_path(polygon20, 54, lfanout, 1, 0.1, um)
    finegates_region+= path20

    polygon21 = polygon7.transformed(db.ICplxTrans.new(1, 120, False, 0*um, 0*um))
    finegates_region+= polygon21
    path21 = return_path(polygon21, 72, lfanout, 1, 0.1, um)
    finegates_region+= path21


    return finegates_region.merged()
    

def create_islands(um, p):
    sq3p2 = np.sqrt(3)/2
    island_rgn = db.Region()
    
    point1 = db.Point(0*um, -(2/3)*sq3p2*p.island_length*um)
    point2 = db.Point(-0.5*p.island_length*um, (1/3)*sq3p2*p.island_length*um)
    point3 = db.Point(0.5*p.island_length*um, (1/3)*sq3p2*p.island_length*um)

    triangle = db.Polygon([point1, point2, point3])

    square = db.Polygon(db.Box(p.island_length*um, p.island_length*um)).moved(0*um, (-(2/3)*sq3p2*p.island_spacing-0.1)*um)
    #island_rgn.insert(triangle.moved(0*um, -(2/3)*sq3p2*p.island_spacing*um))
    #island_rgn.insert(triangle.moved(0.5*p.island_spacing*um, (1/3)*sq3p2*p.island_spacing*um))
    #island_rgn.insert(triangle.moved(-0.5*p.island_spacing*um, (1/3)*sq3p2*p.island_spacing*um))
    #island_rgn.round_corners(0, 0.1*um, 64)

    island_rgn.insert(square)
    island_rgn.insert(square.transformed(db.ICplxTrans.new(1, 120, False, 0*um, 0*um)))
    island_rgn.insert(square.transformed(db.ICplxTrans.new(1, -120, False, 0*um, 0*um)))

    island_rgn.round_corners(p.island_length/2*um, p.island_length/2*um, 128)

    return island_rgn

class p():
    island_spacing = 2
    island_length  = 1.1
    qlength = 1*island_spacing
    trenchwidth = 0.12
    tl = 1.0*island_spacing
    tl1 = 0.29*island_spacing
    lead_length = 2*qlength
    short_gatelength = 0.4
    long_gatelength = 1.0



um = 1e3

mesaNeg = db.LayerInfo(10, 0)
island = db.LayerInfo(61, 0)
fgates = db.LayerInfo(4, 0)

layout = db.Layout(True)
top = layout.create_cell("TOP")

fgate_layer = layout.layer(fgates)
mesaNeg_layer = layout.layer(mesaNeg)
island_layer = layout.layer(island)


island_rgn = create_islands(um, p)
fregion = create_finegates(um, p)
trench_region = create_trench(um, p)

top.shapes(island_layer).insert(island_rgn)
top.shapes(fgate_layer).insert(fregion)
top.shapes(mesaNeg_layer).insert(trench_region)

layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
    "QDots-2/HMIAChipDesign/scriptcad/proposal_designs/prototype.gds")


