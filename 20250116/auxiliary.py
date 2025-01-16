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
    ppady = 1500
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
