import klayout.db as db

def make_global_alignment(um, top, chipsize, alayer):
    layout = top.layout()
    amark = db.Box(20*um, 20*um)
    global_rgn = db.Region()
    markxoff = 150
    numxoff = 250


    for k in range(15):
        global_rgn.insert(amark.moved(-(chipsize/2-markxoff)*um, ((chipsize/2-100)-100*k)*um))
        global_rgn.insert(amark.moved((chipsize/2-markxoff)*um, ((chipsize/2-100)-100*k)*um))

        global_rgn.insert(amark.moved(-(chipsize/2-markxoff)*um, -((chipsize/2-100)-100*k)*um))
        global_rgn.insert(amark.moved((chipsize/2-markxoff)*um, -((chipsize/2-100)-100*k)*um))

        parameters1 = {
        "layer": layout.get_info(alayer),
        "text": f"{k}",
        "mag": 20
        }

        cell = layout.create_cell("TEXT", "Basic", parameters1)


        top.insert(db.CellInstArray(cell.cell_index(), db.Trans(((chipsize/2)-numxoff)*um, (chipsize/2-100-7-100*k)*um)))
        top.insert(db.CellInstArray(cell.cell_index(), db.Trans(-((chipsize/2)-numxoff)*um, (chipsize/2-100-7-100*k)*um)))

        top.insert(db.CellInstArray(cell.cell_index(), db.Trans(((chipsize/2)-numxoff)*um, -(chipsize/2-100+7-100*k)*um)))
        top.insert(db.CellInstArray(cell.cell_index(), db.Trans(-((chipsize/2)-numxoff)*um, -(chipsize/2-100+7-100*k)*um)))
    return global_rgn


def rectangle_insert(shape, x, y):
    region = db.Region()
    region.insert(shape.moved(x, y))
    region.insert(shape.moved(-x, y))
    region.insert(shape.moved(-x, -y))
    region.insert(shape.moved(x, -y))
    return region