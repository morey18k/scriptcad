import klayout.db as db

def create_cron_box(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um, height_box*um)
    cronilation = db.Box(width_cron*um, width_cron*um)
    regionEnd = (db.Region(rect))

    vector = 10
    for k in range(int(width_box/vector)):

        cronCopy = cronilation.dup()
        cronCopy.move((-(width_box*0.5-width_cron)+k*vector)*um, -0.5*(height_box+width_cron)*um)
        regionEnd.insert(cronCopy)

        cronCopy = cronilation.dup()
        cronCopy.move((-(width_box*0.5-width_cron)+k*vector)*um, 0.5*(height_box+width_cron)*um)
        regionEnd.insert(cronCopy)
        
    for k in range(int(height_box/vector)):
        cronCopy = cronilation.dup()
        cronCopy.move(-0.5*(width_box+width_cron)*um, (-(height_box*0.5-width_cron)+k*vector)*um)
        regionEnd.insert(cronCopy)
        
        cronCopy = cronilation.dup()
        cronCopy.move(0.5*(width_box+width_cron)*um, (-(height_box*0.5-width_cron)+k*vector)*um)
        regionEnd.insert(cronCopy)

    return regionEnd

def create_aux1(p, um):
    layout = db.Layout(True)
    top = layout.create_cell("TOP")
    
    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))


    mesaNeg = layout.layer(db.LayerInfo(10, 0))

    island = layout.layer(db.LayerInfo(61, 0))

    fgates = layout.layer(db.LayerInfo(4, 0))

    cgates = layout.layer(db.LayerInfo(5, 0))
    
    mesa_region  = make_mesa(um, p) 
    ohmics_region  = make_ohmics(um, p) 
    island_region  = make_island(um, p) 

    #qpcregion = create_finegates(um, p) 
    
    mesaf = make_mesaf(um, p) 
    #cgatesrgn = create_gatepads(um, p) 
    top.shapes(ohmics).insert(ohmics_region)
    if p.has_trench:
        top.shapes(mesaNeg).insert(mesaf)
    top.shapes(mesaPos).insert(mesa_region)
    if p.has_island:
        top.shapes(island).insert(island_region)
    #top.shapes(fgates).insert(qpcregion)
    #top.shapes(cgates).insert(cgatesrgn)
    return layout

def create_aux2(um):
    layout = db.Layout(True)
    top = layout.create_cell("TOP")
    
    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))


    mesaNeg = layout.layer(db.LayerInfo(10, 0))

    island = layout.layer(db.LayerInfo(61, 0))
    
    mesa_region  = db.Region()
    ohmics_region = db.Region()
    pad1  = create_cron_box(150, 150, 5, um)
    pad2 = db.Box(161*um, 161*um)
    ppady = 2100
    ppadx = 1200
    for k in range(2):
        mesa_region.insert(pad1.moved((300*k-ppadx)*um,-ppady*um))
        ohmics_region.insert(pad2.moved((300*k-ppadx)*um,-ppady*um))
        mesa_region.insert(pad1.moved((300*k-ppadx)*um,ppady*um))
        ohmics_region.insert(pad2.moved((300*k-ppadx)*um,ppady*um))

        mesa_region.insert(pad1.moved((-300*k+ppadx)*um,-ppady*um))
        ohmics_region.insert(pad2.moved((-300*k+ppadx)*um,-ppady*um))
        mesa_region.insert(pad1.moved((-300*k+ppadx)*um,ppady*um))
        ohmics_region.insert(pad2.moved((-300*k+ppadx)*um,ppady*um))



    #qpcregion = create_finegates(um, p) 
    #cgatesrgn = create_gatepads(um, p) 
    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaPos).insert(mesa_region)
    #top.shapes(fgates).insert(qpcregion)
    #top.shapes(cgates).insert(cgatesrgn)
    return layout


def create_aux3(um):
    layout = db.Layout(True)
    top = layout.create_cell("TOP")
    
    mesaPos = layout.layer(db.LayerInfo(2, 0))

    ohmics = layout.layer(db.LayerInfo(3, 0))
    mesaNeg = layout.layer(db.LayerInfo(10, 0))
    island = layout.layer(db.LayerInfo(61, 0))
    
    mesa_region  = db.Region()
    ohmics_region = db.Region()
    pad3  = create_cron_box(100, 400, 5, um)
    pad1  = create_cron_box(200, 200, 5, um)
    pad2 = db.Box(161*um, 161*um)

    rpadregion = db.Region()
    rpadregion.insert(pad1.moved(-1750*um,2075*um))
    rpadregion.insert(pad3.moved(-1800*um,1700*um))
    rpadregion.insert(pad1.moved(-1450*um,2075*um))

    rpadregion.insert(pad1.moved(1750*um,2075*um))
    rpadregion.insert(pad1.moved(1850*um,1800*um))
    rpadregion.insert(pad1.moved(1450*um,2075*um))

    

    rpadregion.insert(pad1.moved(-1750*um,-2075*um))
    rpadregion.insert(pad3.moved(-1900*um,-1700*um))
    rpadregion.insert(pad1.moved(-1450*um,-2075*um))

    rpadregion.insert(pad1.moved(1750*um,-2075*um))
    rpadregion.insert(pad3.moved(1900*um,-1700*um))
    rpadregion.insert(pad1.moved(1450*um,-2075*um))

    trace_width= 15

    path1 = db.Path([db.Point(350*um, 320*um),
                    db.Point(350*um, 350*um),
                     db.Point(-1720*um, 350*um),
                     db.Point(-1720*um, -570*um),
                     db.Point(-1810*um, -570*um),
                      db.Point(-1810*um, -2050*um)], width = trace_width*um)

    path2 = db.Path([db.Point(1600*um, 320*um),
                    db.Point(1600*um, 400*um),
                     db.Point(-1770*um, 400*um),
                     db.Point(-1770*um, -500*um),
                     db.Point(-1870*um, -500*um),
                      db.Point(-1870*um, -1800*um)], width = trace_width*um)
    
    path3 = db.Path([db.Point(-700*um, -700*um),
                    db.Point(-700*um, -600*um),
                    db.Point(-1550*um, -600*um),
                    db.Point(-1550*um, -640*um),
                    db.Point(-1730*um, -640*um),
                    db.Point(-1730*um, -1940*um),
                     db.Point(-1540*um, -1940*um),
                      db.Point(-1540*um, -2050*um)], width = trace_width*um)

    path4 = db.Path([db.Point(-700*um, -1920*um),
                     db.Point(-700*um, -2240*um),
                     db.Point(1700*um, -2240*um),
                     db.Point(1700*um, -2050*um),
                    ], width = trace_width*um)
    
    path5 = db.Path([db.Point(350*um, -900*um),
                     db.Point(350*um, -1000*um),
                     db.Point(790*um, -1000*um),
                     db.Point(790*um, -1950*um),
                     db.Point(1350*um, -1950*um),
                     db.Point(1350*um, -2000*um),
                    ], width = trace_width*um)

    path6 = db.Path([db.Point(1600*um, -900*um),
                     db.Point(1600*um, -1040*um),
                     db.Point(1900*um, -1040*um),
                     db.Point(1900*um, -1600*um),
                    ], width = trace_width*um)
    
    path7 = db.Path([db.Point(-650*um, 650*um),
                     db.Point(-650*um, 575*um),
                     db.Point(-1725*um, 575*um),
                     db.Point(-1750*um, 575*um),
                     db.Point(-1750*um, 1400*um),
                     db.Point(-1700*um, 1400*um),
                      db.Point(-1700*um, 1900*um),
                      db.Point(-1500*um, 1900*um),
                      db.Point(-1500*um, 2000*um),
    ], width = trace_width*um)

    path8 = db.Path([db.Point(400*um, 650*um),
                        db.Point(400*um, 525*um),
                        db.Point(-1800*um, 525*um),
                        db.Point(-1800*um, 1650*um),
    ], width = trace_width*um)

    path9 = db.Path([db.Point(1475*um, 650*um),
                        db.Point(1475*um, 475*um),
                        db.Point(-1875*um, 475*um),
                        db.Point(-1875*um, 475*um),
                        db.Point(-1875*um, 1400*um),
                        db.Point(-1950*um, 1400*um),
                        db.Point(-1950*um, 2050*um),
                        db.Point(-1800*um, 2050*um),
    ], width = trace_width*um)

    path10 = db.Path([db.Point(-650*um, 1850*um),
                      db.Point(-650*um, 1985*um),
                      db.Point(-650*um, 1985*um),
                      db.Point(1400*um, 1985*um),
    ], width = trace_width*um)

    path11 = db.Path([db.Point(400*um, 1850*um),
                      db.Point(400*um, 1935*um),
                      db.Point(1675*um, 1935*um),
                      db.Point(1675*um, 2000*um),
    ], width = trace_width*um)

    path12 = db.Path([db.Point(1475*um, 1867.5*um),
                      db.Point(1800*um, 1867.5*um),
    ], width = trace_width*um)

    

    
    rpadregion.insert(path1)
    rpadregion.insert(path2)
    rpadregion.insert(path3)
    rpadregion.insert(path4)
    rpadregion.insert(path5)
    rpadregion.insert(path6)
    rpadregion.insert(path7)
    rpadregion.insert(path8)
    rpadregion.insert(path9)
    rpadregion.insert(path10)
    rpadregion.insert(path11)
    rpadregion.insert(path12)

    mesa_region+= rpadregion

    ohmics_region+= rpadregion.size(1*um)
    #qpcregion = create_finegates(um, p) 
    #cgatesrgn = create_gatepads(um, p) 
    top.shapes(ohmics).insert(ohmics_region)
    top.shapes(mesaPos).insert(mesa_region)
    #top.shapes(fgates).insert(qpcregion)
    #top.shapes(cgates).insert(cgatesrgn)
    return layout


def make_mesa(um, p):
    pad1 = create_cron_box(130, 130, 5, um)
    region = db.Region()
    region.insert(pad1.moved(0, 100*um))
    region.insert(pad1.moved(0, -100*um))
    box = db.Box(10*um, 100*um)
    region.insert(box)
    return region.merged().transformed(db.ICplxTrans.new(1, p.angle, False, p.centerx*um, p.centery*um))

def make_mesaf(um, p):
    trenchlength = 10
    region = db.Region()
    trench = db.Box((trenchlength+1)*um, p.trenchsize*um)
    region.insert(trench)

    trenchaddon = db.Box(p.trenchsize*um, (p.trenchsize+0.2)*um)
    region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False, -0.2*trenchlength*um, 0)))
    region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False,  0.2*trenchlength*um, 0)))
    return region.merged().transformed(db.ICplxTrans.new(1, p.angle, False, p.centerx*um, p.centery*um))



def make_island(um, p):
    region = db.Region()
    island = db.Box(2*um, 2*um)
    region.insert(island)
    region.round_corners(0.1*um, 0.1*um, 64)
    return region.merged().transformed(db.ICplxTrans.new(1, p.angle, False, p.centerx*um, p.centery*um))

def make_ohmics(um, p):
    region = db.Region()
    pad1 = db.Box(141*um, 141*um)
    region.insert(pad1.moved(0, 100*um))
    region.insert(pad1.moved(0, -100*um))
    return region.merged().transformed(db.ICplxTrans.new(1, p.angle, False, p.centerx*um, p.centery*um))
