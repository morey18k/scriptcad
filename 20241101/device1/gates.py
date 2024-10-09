import klayout.db as db

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
    qpc_instance = create_qpc(p.qpcwidth)

    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.5*p.dot_length*um))
    finegates_region += qpc_instance.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.5*p.dot_length*um))
    return finegates_region