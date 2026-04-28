import klayout.db as db
import gdsfactory as gf
import sys
from doubleDot.mesa_dot import make_mesa_gatepads

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

def create_patches(um, p):
    patch_region = db.Region()
    patch_box = db.Box(0.5*p.island_sizeX*um, 0.4*p.island_sizeY*um)

    patch_box_big = db.Box(1.5*p.island_sizeX*um, 0.25*p.island_sizeY*um)    

    if p.has_island and p.island_sizeX >=0.8:
        patch_region.insert(patch_box.transformed(db.ICplxTrans.new(1, 0, False, 0.5*p.island_sizeX*um, 0.5*p.dot_length*um)))
        patch_region.insert(patch_box.transformed(db.ICplxTrans.new(1, 0, False, -0.5*p.island_sizeX*um, 0.5*p.dot_length*um)))
        patch_region.insert(patch_box.transformed(db.ICplxTrans.new(1, 0, False, -0.5*p.island_sizeX*um, -0.5*p.dot_length*um)))
        patch_region.insert(patch_box.transformed(db.ICplxTrans.new(1, 0, False, 0.5*p.island_sizeX*um, -0.5*p.dot_length*um)))
    elif p.has_island and p.island_sizeX <0.8:
        patch_region.insert(patch_box_big.transformed(db.ICplxTrans.new(1, 0, False, 0*p.island_sizeX*um, 0.5*p.dot_length*um)))
        patch_region.insert(patch_box_big.transformed(db.ICplxTrans.new(1, 0, False, 0*p.island_sizeX*um, -0.5*p.dot_length*um)))
    
    patch_region.round_corners(0.05*um, 0.05*um, 32)
    return patch_region.transformed(db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um))

def create_finegates(um, p):
    finegates_region = db.Region()
    lgate= 1.3*p.island_sizeX
    qpc_instance = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= lgate)

    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 1*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -1*p.dot_length*um))
    
    vlr = db.Region()

    vl1height = p.vl1height
    vertical_line1 = db.Box(p.finegatewidth*um, vl1height*um)
    vlr.insert(vertical_line1)
    vlr.round_corners(0.1*um, 0.1*um, 32)

    lgate_extent = 0.1*p.dot_length
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, lgate_extent*um)))

    vlr.merge()

    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-lgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-lgate_extent)*um))
    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))

    rgate_extent = 0.6*p.dot_length
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.5-0.1*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.5-0.1*p.dot_length)*um))

    
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.6*rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.3*rgate_extent*um)))


    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.5-rgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.5-rgate_extent)*um))

    plunger_region = db.Region()

    plunger = db.Box(2.3*p.dot_length*um, p.finegatewidth*um)
    plunger_region.insert(plunger)
    plunger_region.round_corners(0.1*um, 0.1*um, 32)
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.85*p.dot_length+2.5*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.85*p.dot_length+2.5*p.finegatewidth)*um, 0.5*p.dot_length*um))

    alt_plunger_region = db.Region()
    alt_plunger = db.Box(4*p.dot_length*um, p.finegatewidth*um)
    alt_plunger_region.insert(alt_plunger)
    alt_plunger_region.round_corners(0.1*um, 0.1*um, 32)
    if p.has_island:
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(p.dot_length+2.5*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(p.dot_length+2.5*p.finegatewidth)*um, 0.5*p.dot_length*um))


    dualplungers = create_qpc(2*lgate+p.qpcwidth-2*p.finegatewidth, height_gate = p.finegatewidth, length_gate= 0.5*p.gate_separation-0.5*(2*lgate+p.qpcwidth-2*p.finegatewidth))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0*p.dot_length*um))
    l_cs = 3*p.finegatewidth
    cs_qpc = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= l_cs)
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, 0, False, (p.dot_length+p.finegatewidth+p.qpcwidth)*um, -0.5*p.dot_length*um))
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, 0, False, (p.dot_length+p.finegatewidth+p.qpcwidth)*um, 0.5*p.dot_length*um))

    #finegates_region += dualplungers


    fanout = db.Region()

    path1 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 2*p.gate_separation*um)], width = p.finegatewidth*um)

    path0 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 4*p.gate_separation*um)], width = p.finegatewidth*um)

    finegates_region.insert(path0)
    finegates_region.insert(path0.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, True, 0, 0)))

    path2 = db.Path([db.Point(-(3*p.dot_length+2*p.finegatewidth)*um, (0.5*p.dot_length)*um), db.Point(-1*p.gate_separation*um, 1*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path2)
    finegates_region.insert(path2.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    path3 =db.Path([db.Point(-(p.dot_length-p.finegatewidth)*um, 0*um), db.Point(-1*p.gate_separation*um, 0*um)], width = p.finegatewidth*um)
    finegates_region.insert(path3)
    finegates_region.insert(path3.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))

    path4 = db.Path([db.Point((p.dot_length+2*l_cs+p.qpcwidth-0.75*p.finegatewidth)*um, (0.5*p.dot_length)*um), db.Point(3*p.dot_length*um, (1.75*p.dot_length)*um),db.Point(0.5*p.gate_separation*um, 0.5*p.gate_separation*um), db.Point(1.0*p.gate_separation*um, 1.5*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path4)
    finegates_region.insert(path4.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    finegates_region.round_corners(0.1*um, 0.1*um, 32)
    
     
    mark = db.Box(p.laSize*um, p.laSize*um)
    for pos in p.align4:
        finegates_region.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    
    return finegates_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))


def create_gatepads(um, p):
    gatepads_rgn  = db.Region()
    
    pad = db.Box(p.gatepadwidth*um, p.gatepadheight*um)


    gate_trace_1 = db.Path([((-0.5*p.wHallbar)*um, 0.1*p.lHallbar*um),
                ((-0.6*p.dohmicsx)*um, 0.1*p.lHallbar*um),
                ((-0.6*p.dohmicsx)*um, 0.3*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, 0.3*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, 0.47*p.lHallbar*um),
                ((-0.9*p.dohmicsx)*um, 0.47*p.lHallbar*um),
                ((-0.9*p.dohmicsx)*um, 0.6*p.lHallbar*um),
                ], width = p.coursegatewidth*um)
    

    gate_trace_2 = db.Path([((-0.5*p.wHallbar)*um, 0.05*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, 0.05*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, 0.25*p.lHallbar*um),
                ((-1*p.dohmicsx)*um, 0.25*p.lHallbar*um)
                ], width = p.coursegatewidth*um)
    
    gate_trace_3 = db.Path([((-0.5*p.wHallbar)*um, 0*p.lHallbar*um),
                ((-1*p.dohmicsx)*um, 0*p.lHallbar*um)
                ], width = p.coursegatewidth*um)
    
    gate_trace_4 = db.Path([((-0.5*p.wHallbar)*um, -0.05*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, -0.05*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, -0.25*p.lHallbar*um),
                ((-1*p.dohmicsx)*um, -0.25*p.lHallbar*um)
                ], width = p.coursegatewidth*um)
    
    gate_trace_5 = db.Path([((-0.5*p.wHallbar)*um, -0.1*p.lHallbar*um),
                ((-0.6*p.dohmicsx)*um, -0.1*p.lHallbar*um),
                ((-0.6*p.dohmicsx)*um, -0.3*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, -0.3*p.lHallbar*um),
                ((-0.68*p.dohmicsx)*um, -0.47*p.lHallbar*um),
                ((-0.9*p.dohmicsx)*um, -0.47*p.lHallbar*um),
                ((-0.9*p.dohmicsx)*um, -0.6*p.lHallbar*um),
                ], width = p.coursegatewidth*um)

    gate_trace_6 = db.Path([((+0.5*p.wHallbar)*um, -0.28*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, -0.28*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, -0.20*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um, -0.20*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um, -0.5*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2*p.dohmicsx)*um, -0.5*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2*p.dohmicsx)*um, -0.55*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2.5*p.dohmicsx)*um, -0.55*p.lHallbar*um)
    ], width = p.coursegatewidth*um)

    gate_trace_7 = db.Path([((+0.5*p.wHallbar)*um, -0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+0.5*p.w_connector)*um, -0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+0.5*p.w_connector)*um, -0.13*p.lHallbar*um),
                ((+0.5*p.wHallbar+p.w_connector+p.dohmicsx)*um,  -0.13*p.lHallbar*um),
                ((+0.5*p.wHallbar+p.w_connector+p.dohmicsx)*um, -0.14*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2*p.dohmicsx)*um, -0.14*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2*p.dohmicsx)*um, -0.20*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2.5*p.dohmicsx)*um, -0.20*p.lHallbar*um)
    ], width = p.coursegatewidth*um)


    gate_trace_8 = db.Path([((+0.5*p.wHallbar)*um, 0*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, 0*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, 0.11*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um,  0.11*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um, -0.12*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2.5*p.dohmicsx)*um, -0.12*p.lHallbar*um)
    ], width = p.coursegatewidth*um)

    gate_trace_9 = db.Path([((+0.5*p.wHallbar)*um, 0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+p.w_connector)*um, 0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+p.w_connector)*um, 0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+p.dohmicsx)*um,  0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+p.dohmicsx)*um, 0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2*p.dohmicsx)*um, 0.16*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2*p.dohmicsx)*um, 0.25*p.lHallbar*um),
                ((+0.5*p.wHallbar+2*p.w_connector+2.5*p.dohmicsx)*um, 0.25*p.lHallbar*um)
    ], width = p.coursegatewidth*um)


    gate_trace_10 = db.Path([((+0.5*p.wHallbar)*um, 0.28*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, 0.28*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector)*um, 0.20*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um, 0.20*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+p.dohmicsx)*um, 0.5*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2*p.dohmicsx)*um, 0.5*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2*p.dohmicsx)*um, 0.55*p.lHallbar*um),
                ((+0.5*p.wHallbar+1.5*p.w_connector+2.5*p.dohmicsx)*um, 0.55*p.lHallbar*um)
    ], width = p.coursegatewidth*um)

    fanout1 = db.Path([db.Point(list(gate_trace_1.each_point())[0].x-1*um, list(gate_trace_1.each_point())[0].y), db.Point(-0.5*p.gate_separation*um, 2*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout2 = db.Path([db.Point(list(gate_trace_2.each_point())[0].x-1*um, list(gate_trace_2.each_point())[0].y), db.Point(-1*p.gate_separation*um, 1*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout3 = db.Path([db.Point(list(gate_trace_3.each_point())[0].x-1*um, list(gate_trace_3.each_point())[0].y), db.Point(-1*p.gate_separation*um, 0*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout4 = db.Path([db.Point(list(gate_trace_4.each_point())[0].x-1*um, list(gate_trace_4.each_point())[0].y), db.Point(-1*p.gate_separation*um, -1*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout5 = db.Path([db.Point(list(gate_trace_5.each_point())[0].x-1*um, list(gate_trace_5.each_point())[0].y), db.Point(-0.5*p.gate_separation*um, -2*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout6 = db.Path([db.Point(list(gate_trace_6.each_point())[0].x+1*um, list(gate_trace_6.each_point())[0].y), db.Point(0.5*p.gate_separation*um, list(gate_trace_6.each_point())[0].y), db.Point(0.5*p.gate_separation*um, -4*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout7 = db.Path([db.Point(list(gate_trace_7.each_point())[0].x+1*um, list(gate_trace_7.each_point())[0].y), db.Point(1.5*p.gate_separation*um, list(gate_trace_7.each_point())[0].y),db.Point(1.0*p.gate_separation*um, -1.5*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout8 = db.Path([db.Point(list(gate_trace_8.each_point())[0].x+1*um, list(gate_trace_8.each_point())[0].y), db.Point(1*p.gate_separation*um, 0*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout9 = db.Path([db.Point(list(gate_trace_9.each_point())[0].x+1*um, list(gate_trace_9.each_point())[0].y), db.Point(1.5*p.gate_separation*um, list(gate_trace_9.each_point())[0].y), db.Point(1.0*p.gate_separation*um, 1.5*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)
    fanout10 = db.Path([db.Point(list(gate_trace_10.each_point())[0].x+1*um, list(gate_trace_10.each_point())[0].y),db.Point(0.5*p.gate_separation*um, list(gate_trace_10.each_point())[0].y), db.Point(0.5*p.gate_separation*um, 4*p.gate_separation*um)], width = 0.5*p.coursegatewidth*um)


    gatepads_rgn.insert(fanout1)
    gatepads_rgn.insert(fanout2)
    gatepads_rgn.insert(fanout3)
    gatepads_rgn.insert(fanout4)
    gatepads_rgn.insert(fanout5)

    gatepads_rgn.insert(fanout6)
    gatepads_rgn.insert(fanout7)
    gatepads_rgn.insert(fanout8)
    gatepads_rgn.insert(fanout9)
    gatepads_rgn.insert(fanout10)


    patch = db.Region(db.Box(1*um, 2*um))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 15, False, list(fanout1.each_point())[-1].x, list(fanout1.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 20, False, list(fanout2.each_point())[-1].x, list(fanout2.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 90, False, list(fanout3.each_point())[-1].x, list(fanout3.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, -20, False, list(fanout4.each_point())[-1].x, list(fanout4.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, -15, False, list(fanout5.each_point())[-1].x, list(fanout5.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 5, False, list(fanout6.each_point())[-1].x, list(fanout6.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 25, False, list(fanout7.each_point())[-1].x, list(fanout7.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 90, False, list(fanout8.each_point())[-1].x, list(fanout8.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 0, False, list(fanout9.each_point())[-1].x, list(fanout9.each_point())[-1].y)))
    gatepads_rgn.insert(patch.transformed(db.ICplxTrans(1, 0, False, list(fanout10.each_point())[-1].x, list(fanout10.each_point())[-1].y)))

    gatepads_rgn.insert(gate_trace_1)
    gatepads_rgn.insert(gate_trace_2)
    gatepads_rgn.insert(gate_trace_3)
    gatepads_rgn.insert(gate_trace_4)
    gatepads_rgn.insert(gate_trace_5)
    gatepads_rgn.insert(gate_trace_6)
    gatepads_rgn.insert(gate_trace_7)
    gatepads_rgn.insert(gate_trace_8)
    gatepads_rgn.insert(gate_trace_9)
    gatepads_rgn.insert(gate_trace_10)

    gatepads_rgn += make_mesa_gatepads(um, p).size(-1*um)

    gatepads_rgn.round_corners(0.4*um, 0.4*um, 32)

    return  gatepads_rgn.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

def create_finegates_ambitious(um, p):
    finegates_region = db.Region()
    lgate= 1.2*p.island_sizeX
    qpc_instance = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= lgate)

    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 1*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -1*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0*p.dot_length*um))

    vlr = db.Region()

    vl1height = p.vl1height
    vertical_line1 = db.Box(p.finegatewidth*um, vl1height*um)
    vlr.insert(vertical_line1)
    vlr.round_corners(0.1*um, 0.1*um, 32)

    lgate_extent = 0.1*p.dot_length
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, lgate_extent*um)))

    vlr.merge()

    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -0.05*p.dot_length*um))#-(0.5*p.dot_length-vl1height*0.5-lgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, 0.05*p.dot_length*um))#(0.5*p.dot_length-vl1height*0.5-lgate_extent)*um))
    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))

    rgate_extent = 0.3*p.dot_length
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.1)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.1)*um))

    
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.6*rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.3*rgate_extent*um)))


    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.5-rgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.5-rgate_extent)*um))

    plunger_region = db.Region()

    plunger = db.Box(2.3*p.dot_length*um, p.finegatewidth*um)
    plunger_region.insert(plunger)
    plunger_region.round_corners(0.1*um, 0.1*um, 32)
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.8*p.dot_length+2.5*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.8*p.dot_length+2.5*p.finegatewidth)*um, 0.5*p.dot_length*um))

    alt_plunger_region = db.Region()
    alt_plunger = db.Box(4*p.dot_length*um, p.finegatewidth*um)
    alt_plunger_region.insert(alt_plunger)
    alt_plunger_region.round_corners(0.1*um, 0.1*um, 32)
    if p.has_island:
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.3*p.dot_length+2.5*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.3*p.dot_length+2.5*p.finegatewidth)*um, 0.5*p.dot_length*um))


    dualplungers = create_qpc(2*lgate+p.qpcwidth-2*p.finegatewidth, height_gate = p.finegatewidth, length_gate= 0.5*p.gate_separation-0.5*(2*lgate+p.qpcwidth-2*p.finegatewidth))


    l_cs = 3*p.finegatewidth
    cs_qpc = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= l_cs)
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, -20, False, (p.dot_length+p.qpcwidth)*um, -1*p.dot_length*um))
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, 20, False, (p.dot_length+p.qpcwidth)*um, 1*p.dot_length*um))

    connector = db.Box(l_cs*um, p.finegatewidth*um)
    finegates_region += connector.transformed(db.ICplxTrans.new(1, 0, False, (0.50*p.dot_length+1.6*p.finegatewidth)*um, -0.815*p.dot_length*um))
    finegates_region += connector.transformed(db.ICplxTrans.new(1, 0, False, (0.50*p.dot_length+1.6*p.finegatewidth)*um, 0.815*p.dot_length*um))

    #finegates_region += dualplungers


    fanout = db.Region()

    path1 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 2*p.gate_separation*um)], width = p.finegatewidth*um)

    path0 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 4*p.gate_separation*um)], width = p.finegatewidth*um)

    finegates_region.insert(path0)
    finegates_region.insert(path0.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, True, 0, 0)))

    path2 = db.Path([db.Point(-(3*p.dot_length+2*p.finegatewidth)*um, (0.5*p.dot_length)*um), db.Point(-1*p.gate_separation*um, 1*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path2)
    finegates_region.insert(path2.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    path3 =db.Path([db.Point(-(p.dot_length-3*p.finegatewidth)*um, 0*um), db.Point(-1*p.gate_separation*um, 0*um)], width = p.finegatewidth*um)
    finegates_region.insert(path3)
    finegates_region.insert(path3.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))

    path4 = db.Path([db.Point((p.dot_length+2*l_cs+p.qpcwidth-2.0*p.finegatewidth)*um, (1.175*p.dot_length)*um), db.Point(3*p.dot_length*um, (1.75*p.dot_length)*um),db.Point(0.5*p.gate_separation*um, 0.5*p.gate_separation*um), db.Point(1.0*p.gate_separation*um, 1.5*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path4)
    finegates_region.insert(path4.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    finegates_region.round_corners(0.1*um, 0.1*um, 32)
    
     
    mark = db.Box(p.laSize*um, p.laSize*um)
    for pos in p.align4:
        finegates_region.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    
    return finegates_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))


def create_finegates_medium(um, p):
    finegates_region = db.Region()
    lgate= 1.3*p.island_sizeX
    qpc_instance = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= lgate)

    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 1*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -1*p.dot_length*um))
    
    vlr = db.Region()

    vl1height = p.vl1height
    vertical_line1 = db.Box(p.finegatewidth*um, vl1height*um)
    vlr.insert(vertical_line1)
    vlr.round_corners(0.1*um, 0.1*um, 32)

    lgate_extent = 0.1*p.dot_length
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, lgate_extent*um)))

    vlr.merge()

    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(0.46*p.dot_length-vl1height*0.5-lgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.46*p.dot_length-vl1height*0.5-lgate_extent)*um))
    #finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (0.5*p.dot_length-vl1height*0.5-0.05*p.dot_length)*um))

    rgate_extent = 0.6*p.dot_length
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.5+0.04*p.dot_length)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, -(0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.5+0.04*p.dot_length)*um))

    
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.76*rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.6*rgate_extent*um)))
    vlr.insert(vertical_line1.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.3*rgate_extent*um)))


    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 180, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, -(1*p.dot_length-vl1height*0.5-rgate_extent)*um))
    finegates_region += vlr.transformed(db.ICplxTrans.new(1, 0, False, (0.5*p.qpcwidth-0.5*p.finegatewidth+lgate)*um, (1*p.dot_length-vl1height*0.5-rgate_extent)*um))

    plunger_region = db.Region()

    plunger = db.Box(2.3*p.dot_length*um, p.finegatewidth*um)
    plunger_region.insert(plunger)
    plunger_region.round_corners(0.1*um, 0.1*um, 32)
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.85*p.dot_length+2.5*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
    finegates_region += plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(1.85*p.dot_length+2.5*p.finegatewidth)*um, 0.5*p.dot_length*um))

    alt_plunger_region = db.Region()
    alt_plunger = db.Box(4*p.dot_length*um, p.finegatewidth*um)
    alt_plunger_region.insert(alt_plunger)
    alt_plunger_region.round_corners(0.1*um, 0.1*um, 32)
    if p.has_island:
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(p.dot_length+3.75*p.finegatewidth)*um, -(0.5*p.dot_length*um)))
        finegates_region += alt_plunger_region.transformed(db.ICplxTrans.new(1, 0, False, -(p.dot_length+3.75*p.finegatewidth)*um, 0.5*p.dot_length*um))


    dualplungers = create_qpc(2*lgate+p.qpcwidth-2*p.finegatewidth, height_gate = p.finegatewidth, length_gate= 0.5*p.gate_separation-0.5*(2*lgate+p.qpcwidth-2*p.finegatewidth))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0*p.dot_length*um))
    l_cs = 3*p.finegatewidth
    cs_qpc = create_qpc(p.qpcwidth, height_gate = p.finegatewidth, length_gate= l_cs)
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, -10, False, (p.dot_length+p.finegatewidth+p.qpcwidth)*um, -0.67*p.dot_length*um))
    finegates_region += cs_qpc.transformed(db.ICplxTrans.new(1, 10, False, (p.dot_length+p.finegatewidth+p.qpcwidth)*um, 0.67*p.dot_length*um))
    
    connector = db.Box(l_cs*um, p.finegatewidth*um)
    finegates_region += connector.transformed(db.ICplxTrans.new(1, 0, False, (0.50*p.dot_length+4.3*p.finegatewidth)*um, -0.6*p.dot_length*um))
    finegates_region += connector.transformed(db.ICplxTrans.new(1, 0, False, (0.50*p.dot_length+4.3*p.finegatewidth)*um, 0.6*p.dot_length*um))
    #finegates_region += dualplungers


    fanout = db.Region()

    path1 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 2*p.gate_separation*um)], width = p.finegatewidth*um)

    path0 = db.Path([db.Point((lgate+0.5*p.qpcwidth-p.finegatewidth)*um, (1*p.dot_length-0.5*p.finegatewidth)*um), db.Point(0.5*p.gate_separation*um, 4*p.gate_separation*um)], width = p.finegatewidth*um)

    finegates_region.insert(path0)
    finegates_region.insert(path0.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    finegates_region.insert(path1.transformed(db.ICplxTrans.new(1, 180, True, 0, 0)))

    path2 = db.Path([db.Point(-(3*p.dot_length+3*p.finegatewidth)*um, (0.5*p.dot_length)*um), db.Point(-1*p.gate_separation*um, 1*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path2)
    finegates_region.insert(path2.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    path3 =db.Path([db.Point(-(p.dot_length-2*p.finegatewidth)*um, 0*um), db.Point(-1*p.gate_separation*um, 0*um)], width = p.finegatewidth*um)
    finegates_region.insert(path3)
    finegates_region.insert(path3.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))

    path4 = db.Path([db.Point((p.dot_length+2*l_cs+p.qpcwidth-0.75*p.finegatewidth)*um, (0.73*p.dot_length)*um), db.Point(3*p.dot_length*um, (1.75*p.dot_length)*um),db.Point(0.5*p.gate_separation*um, 0.5*p.gate_separation*um), db.Point(1.0*p.gate_separation*um, 1.5*p.gate_separation*um)], width = p.finegatewidth*um)
    finegates_region.insert(path4)
    finegates_region.insert(path4.transformed(db.ICplxTrans.new(1, 0, True, 0, 0)))

    finegates_region.round_corners(0.1*um, 0.1*um, 32)
    
     
    mark = db.Box(p.laSize*um, p.laSize*um)
    for pos in p.align4:
        finegates_region.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    
    return finegates_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
