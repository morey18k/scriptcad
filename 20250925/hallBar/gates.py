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
    lgate= 1.5*p.island_sizeX
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
    topgate = db.Box((p.wHallbar+1)*um, (p.lHallbar+1)*um)
    connector = db.Path([db.Point(0*um, 0*um), db.Point(p.gatepadx*um, 0*um)], width = p.coursegatewidth*um)
    if p.has_topgate:
        gatepads_rgn.insert(topgate)
        gatepads_rgn.insert(connector)



    pad = db.Box(p.gatepadwidth*um, p.gatepadheight*um)

    
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(p.gatepadx*um, -p.gatepady*um))

    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, p.gatepady*um))
    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, 0))
    gatepads_rgn.insert(pad.moved(-p.gatepadx*um, -p.gatepady*um))


    return  (gatepads_rgn).merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))