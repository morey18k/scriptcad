import klayout.db as db
import gdsfactory as gf

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



def create_finegates(um, p):
    finegates_region = db.Region()
    lgate= 0.6*p.island_sizeX
    if p.holeDot:
        lgate = 0.8*p.island_sizeX
        if p.small_island:
            lgate = 1.0*p.island_sizeX


    qpc_instance = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= lgate)

    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.5*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.5*p.dot_length*um))
    
    vlr = db.Region()

    vl1height = p.vl1height
    vertical_line1 = db.Box(p.finegatewidth*um, vl1height*um)
    vlr.insert(vertical_line1)
    vlr.round_corners(0.1*um, 0.1*um, 32)
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.05*p.dot_length*um)))

    vlr.merge()

    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))

    dualplungers = create_qpc(2*lgate+p.qpcwidth-2*p.finegatewidth, height_gate = p.finegatewidth, length_gate= 0.5*p.gate_separation-0.5*(2*lgate+p.qpcwidth-2*p.finegatewidth))

    finegates_region += dualplungers


    fanout = db.Region()

    path1 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (0.5*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 0.5*p.gate_separation*um)], width = p.finegatewidth*um)

    finegates_region.insert(path1)
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, True, 0, 0)))
    return finegates_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))


def create_gatepads(um, p):
    gatepads_rgn  = db.Region()
    
    pad = db.Box(p.gatepadwidth*um, p.gatepadheight*um)

    
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, -p.gatepady*um))

    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, -p.gatepady*um))

    
    #gatepads_rgn.insert(pad.moved(0.9*p.dohmicsx*um, -1.0*p.dohmicsy*um))
    cgate_rgn = db.Region()
    path1 = db.Path([db.Point((0.5*p.gate_separation-1)*um, (0.5*p.gate_separation-1)*um), db.Point((p.gate_separation)*um, (p.gate_separation)*um)], width = 0.5*p.coursegatewidth*um)
    cgate_rgn.insert(path1)
    cgate_rgn.insert(path1.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    cgate_rgn.insert(path1.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    cgate_rgn.insert(path1.transformed(db.ICplxTrans.new(1, 180, True, 0, 0)))

    path2 = db.Path([db.Point((0.5*p.gate_separation-1)*um, 0*um), db.Point((p.gate_separation)*um, 0*um)], width = 0.5*p.coursegatewidth*um)
    cgate_rgn.insert(path2)
    cgate_rgn.insert(path2.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))

    c = gf.Component()    
    lgth = 1
    w1 = gf.c.straight(length = lgth, cross_section = "metal_routing", layer = 'M3')
    rtop = c << w1
    rmiddle = c << w1
    rbottom = c << w1
    rtop.dmove((p.gate_separation-1, p.gate_separation))
    rmiddle.dmove((p.gate_separation-1, 0))
    rbottom.dmove((p.gate_separation-1, -p.gate_separation))
    
    rpadtop = c << w1
    rpadmiddle = c << w1
    rpadbottom = c << w1
    rpadtop.dmove((p.gatepadx-0.5*p.gatepadwidth, p.gatepady))
    rpadmiddle.dmove((p.gatepadx-0.5*p.gatepadwidth, 0))
    rpadbottom.dmove((p.gatepadx-0.5*p.gatepadwidth, -p.gatepady))

    portsr1 = rtop.ports.filter(orientation=0) + rmiddle.ports.filter(orientation=0) + rbottom.ports.filter(orientation=0)
    portsr2 = rpadtop.ports.filter(orientation=180) + rpadmiddle.ports.filter(orientation=180) + rpadbottom.ports.filter(orientation=180)

    routes = gf.routing.route_bundle(
        c,
        portsr1,
        portsr2,
        separation = p.gate_separation,
        allow_width_mismatch = True,
        route_width = 1.0,
        cross_section = "metal_routing",
        waypoints = [(p.gatepadx*0.5, p.gate_separation*0.5), (p.gatepadx*0.6, p.gate_separation*0.5)]
    )


    ltop = c << w1
    lmiddle = c << w1
    lbottom = c << w1
    ltop.dmove((-p.gate_separation+1-lgth, p.gate_separation))
    lmiddle.dmove((-p.gate_separation+1-lgth, 0))
    lbottom.dmove((-p.gate_separation+1-lgth, -p.gate_separation))
    
    lpadtop = c << w1
    lpadmiddle = c << w1
    lpadbottom = c << w1
    lpadtop.dmove((-p.gatepadx+0.5*p.gatepadwidth, p.gatepady))
    lpadmiddle.dmove((-p.gatepadx+0.5*p.gatepadwidth, 0))
    lpadbottom.dmove((-p.gatepadx+0.5*p.gatepadwidth, -p.gatepady))

    portsl1 = ltop.ports.filter(orientation=180) + lmiddle.ports.filter(orientation=180) + lbottom.ports.filter(orientation=180)
    portsl2 = lpadtop.ports.filter(orientation=0) + lpadmiddle.ports.filter(orientation=0) + lpadbottom.ports.filter(orientation=0)

    routes = gf.routing.route_bundle(
        c,
        portsl1,
        portsl2,
        separation = p.gate_separation,
        allow_width_mismatch = True,
        route_width = 1.0,
        cross_section = "metal_routing",
        waypoints = [(-p.gatepadx*0.5, -p.gate_separation*0.5), (-p.gatepadx*0.6, -p.gate_separation*0.5)]
    )
    
    fanout = db.Region(c.get_polygons()[23])

    return  (gatepads_rgn+ cgate_rgn + fanout).merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))