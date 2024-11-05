import klayout.db as db
import math

# Creating layout and top cells
# trapezoid for connection between pad
# and hall bar

def create_cron_ohm(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um-width_cron*um, height_box*um-width_cron*um)
    regionEnd = (db.Region(rect))
    return regionEnd

def make_ohmics_1(um, p):
    region = create_cron_ohm(1.40*p.padsize, 0.75*p.padsize, p.cronSize, um)

    ohm_region = db.Region()


    ohm_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))
    ohm_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -0.9*p.dohmicsy*um))
    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 0.9*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -1.5*p.dohmicsy*um))
    

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -0.9*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 0.9*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, -0.3*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.75*p.dohmicsx*um, 0.3*p.dohmicsy*um))
    
    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, -0.3*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.75*p.dohmicsx*um, 0.3*p.dohmicsy*um))


    ycons = [-370, -270, -170, 0, 200, 370]
    yfs = [-350+700*k/5 for k in range(len(ycons))]
    pathlist = []
    for k in range(len(p.ypos)):
        point1 = db.Point(-(0.5*p.wHallbar+4)*um, (p.ypos[k]-1)*um)
        point2 = db.Point(-(0.5*p.wHallbar+10)*um, ycons[k]*um)
        point3 = db.Point(-(0.75*p.dohmicsx-0.70*p.padsize-50)*um, ycons[k]*um)
        point4 = db.Point(-(0.75*p.dohmicsx-0.70*p.padsize+2)*um, yfs[k]*um)
        pathlist.append(db.Path([point1, point2, point3, point4], width = 5*um))
        ohm_region.insert(pathlist[k].transformed(
                            db.ICplxTrans.new(1, 0, False, 0*um, 0*um)))
        ohm_region.insert(pathlist[k].transformed(
                            db.ICplxTrans.new(1, 180, True, 0*um, 0*um)))


    rightend = p.dohmicsx*0.5-0.5*p.padsize
    leftend = p.wHallbar*0.5
    centerC = 0.5*(rightend+leftend)




    connector = db.Box((rightend-leftend)*um, (p.h_connector+2*p.cronSize)*um)


    return ohm_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

def make_island_1(um, p):
    island_region = db.Region()
    island_box = db.Box(p.island_sizeX*um, p.island_sizeY*um)
    
    connector_width = 5
    connector_box = db.Box(connector_width*um, 3*um)
    inity = -390
    spacings = [0, 50, 100, 150, 200, 250]
    sum = 0
    p.ypos = []
    for k in range(len(spacings)):
        sum += spacings[k]
        p.ypos.append(inity + sum)
        island_region.insert(island_box.moved(0, p.ypos[k]*um))
        island_region.insert(connector_box.moved(-0.5*p.island_sizeX*um-0.4999*connector_width*um, p.ypos[k]*um))
        island_region.insert(connector_box.moved(0.5*p.island_sizeX*um+0.4999*connector_width*um, p.ypos[k]*um))


    island_region.round_corners(0.1*um, 0.1*um, 64)
    return island_region.transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
    
