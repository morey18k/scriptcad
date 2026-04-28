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
    
    qpc_instance = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= 0.4*p.wHallbar)

    finegates_region+= qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.45*p.lHallbar*um))
    finegates_region+= qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0*p.lHallbar*um))
    finegates_region+= qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.45*p.lHallbar*um))
    
    strip_gate = db.Box(1.1*p.wHallbar*um, p.finegatewidth*um)
    finegates_region+= strip_gate.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.35*p.lHallbar*um))
    finegates_region+= strip_gate.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.35*p.lHallbar*um))


    return finegates_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))


def create_gatepads(um, p):
    gatepads_rgn  = db.Region()
    topgate = db.Box((p.wHallbar+1)*um, (p.lHallbar+1)*um)
    connector = db.Path([db.Point(0*um, 0*um), db.Point(p.gatepadx*um, 0*um)], width = p.coursegatewidth*um)
    

    fanout1 = db.Path([db.Point(-0.6*p.gatepadx*um, (0.45*p.gatepady+0.5*p.gatepadheight+p.gate_separation)*um),
                db.Point(-(0.3*p.gatepadx-0.5*p.gatepadwidth-1.5*p.gate_separation)*um, (0.45*p.gatepady+0.5*p.gatepadheight+p.gate_separation)*um),                   
                db.Point(-(0.3*p.gatepadx-0.5*p.gatepadwidth-1.5*p.gate_separation)*um, 0.45*p.lHallbar*um),
                db.Point((-0.35*p.wHallbar)*um, 0.45*p.lHallbar*um)], width = p.coursegatewidth*um)
    
    fanout2 = db.Path([db.Point(p.gatepadx*um, p.gatepady*um),
                db.Point((p.gatepadx-0.5*p.gatepadwidth-1.5*p.gate_separation)*um, p.gatepady*um),                   
                db.Point((p.gatepadx-0.5*p.gatepadwidth-1.5*p.gate_separation)*um, (1.5*p.dohmicsy+0.5*p.padsize+1.5*p.gate_separation)*um),
                db.Point((0.5*(0.5*p.dohmicsx))*um, (1.5*p.dohmicsy+0.5*p.padsize+1.5*p.gate_separation)*um),
                db.Point((0.5*(0.5*p.dohmicsx))*um, (1.5*p.dohmicsy-0.5*p.padsize+0.5*p.gate_separation)*um),
                db.Point((0.3*p.gatepadx-0.5*p.gatepadwidth-1.5*p.gate_separation)*um, 0.45*p.lHallbar*um),
                db.Point((0.35*p.wHallbar)*um, 0.45*p.lHallbar*um)
], width = p.coursegatewidth*um)
    
    fanout3 = db.Path([db.Point(-0.6*p.gatepadx*um, 0*um),
                db.Point(-(0.35*p.wHallbar)*um, 0*um)
], width = p.coursegatewidth*um)
    
    fanout4 = db.Path([db.Point(p.gatepadx*um, 0*um),
                db.Point((0.35*p.wHallbar)*um, 0*um)
], width = p.coursegatewidth*um)
    
    fanout5 = db.Path([db.Point(-0.3*p.gatepadx*um, 0.35*p.lHallbar*um),
                db.Point(-(0.35*p.wHallbar)*um, 0.35*p.lHallbar*um)
], width = p.coursegatewidth*um)


    pad = db.Box(p.gatepadwidth*um, p.gatepadheight*um)

    gatepads_rgn.insert(fanout1)
    gatepads_rgn.insert(fanout2)
    gatepads_rgn.insert(fanout3)
    gatepads_rgn.insert(fanout4)
    gatepads_rgn.insert(fanout5)

    gatepads_rgn.insert(fanout1.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    gatepads_rgn.insert(fanout2.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    gatepads_rgn.insert(fanout5.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))


    gatepads_rgn.insert(pad.moved(p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, -p.gatepady*um))

    gatepads_rgn.insert(pad.transformed(db.ICplxTrans.new(0.92, 0, True, -0.28*p.gatepadx*um, 0.45*p.gatepady*um)))
    gatepads_rgn.insert(pad.transformed(db.ICplxTrans.new(0.92, 0, True, -0.28*p.gatepadx*um, -0.45*p.gatepady*um)))


    gatepads_rgn.insert(pad.moved(-0.65*p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(-0.65*p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(-0.65*p.gatepadx*um, -p.gatepady*um))

    return  (gatepads_rgn).merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))