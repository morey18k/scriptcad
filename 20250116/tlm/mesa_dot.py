import klayout.db as db
import math
# Creating layout and top cells
# Mesa Layer


# trapezoid for connection between pad
# and hall bar


def create_cron_box(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um, height_box*um)
    regionEnd = (db.Region(rect))
    return regionEnd



def make_mesa_1(um, p):
    region = create_cron_box(1.40*p.padsize, 0.75*p.padsize, p.cronSize, um)

    mesa_region = db.Region()


    mesa_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))
    mesa_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -0.9*p.dohmicsy*um))
    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 0.9*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))
    

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -0.9*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 0.9*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -0.3*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 0.3*p.dohmicsy*um))
    
    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -0.3*p.dohmicsy*um))

    mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 0.3*p.dohmicsy*um))


    mesa_bar = db.Box(p.wHallbar*um, p.lHallbar*um)

    rightend = p.dohmicsx*0.5-0.5*p.padsize
    leftend = p.wHallbar*0.5
    centerC = 0.5*(rightend+leftend)




    connector = create_cron_box(rightend-leftend, p.h_connector, p.cronSize, um)

    mesa_region += db.Region(mesa_bar).transformed(
                            db.ICplxTrans.new(1, 0, False, 0.0*um, 0.0*um))


    return (mesa_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um))))


def make_mesaf_1(um, p):

    fine_region = db.Region()

    trenchlength = 1.0*p.wHallbar

    region = db.Region()
   
    trench = db.Box((trenchlength+1)*um, p.trenchsize*um)
    region.insert(trench)

    trenchaddon = db.Box(p.trenchsize*um, (p.trenchsize+0.2)*um)
    region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False, -0.2*trenchlength*um, 0)))
    region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False,  0.2*trenchlength*um, 0)))

    for k in range(len(p.ypos)):
        fine_region+=region.moved(0, p.ypos[k]*um)
    return fine_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
