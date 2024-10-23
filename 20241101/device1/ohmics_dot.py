import klayout.db as db
import math
# Creating layout and top cells
# trapezoid for connection between pad
# and hall bar

def create_cron_ohm(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um+2*width_cron*um, height_box*um+2*width_cron*um)
    regionEnd = (db.Region(rect))
    return regionEnd

def make_ohmics_1(um, p):
    region = create_cron_ohm(p.padsize, p.padsize, p.cronSize, um)

    ohm_region = db.Region()


    ohm_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))
    ohm_region += region.transformed(
                                db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -0.5*p.dohmicsy*um))
    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, 0.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, -0.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, 0.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, 1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0, 1.5*p.dohmicsy*um))

    ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0, -1.5*p.dohmicsy*um))




    rightend = p.dohmicsx*0.5-0.5*p.padsize
    leftend = p.wHallbar*0.5
    centerC = 0.5*(rightend+leftend)




    connector = db.Box((rightend-leftend)*um, (p.h_connector+2*p.cronSize)*um)



    ohm_region += connector.transformed(
                            db.ICplxTrans.new(1, 0, False, -centerC*um, 0.5*p.dohmicsy*um))

    ohm_region += connector.transformed(
                            db.ICplxTrans.new(1, 0, False, centerC*um, 0.5*p.dohmicsy*um))

    ohm_region += connector.transformed(
                            db.ICplxTrans.new(1, 0, False, centerC*um, -0.5*p.dohmicsy*um))

    ohm_region += connector.transformed(
                            db.ICplxTrans.new(1, 0, False, -centerC*um, -0.5*p.dohmicsy*um))



    topcn = db.Box((p.wHallbar+2*p.cronSize)*um, (1.5*p.dohmicsy-0.5*p.padsize-p.lHallbar*0.5)*um)



    ohm_region += topcn.transformed(
                            db.ICplxTrans.new(1, 0, False, 0*um, 0.5*(1.5*p.dohmicsy-0.5*p.padsize+0.5*p.lHallbar)*um))

    ohm_region += topcn.transformed(
                            db.ICplxTrans.new(1, 0, False, 0*um, -0.5*(1.5*p.dohmicsy-0.5*p.padsize+0.5*p.lHallbar)*um))





    short_connector = db.Box(p.w_connector*um, (p.h_connector+2.01*p.cronSize)*um)


    ohm_region += short_connector.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*(p.w_connector+p.wHallbar)*um, p.h_tcn*um))

    ohm_region += short_connector.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*(p.w_connector+p.wHallbar)*um, p.h_tcn*um))
    ohm_region += short_connector.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*(p.w_connector+p.wHallbar)*um, -p.h_tcn*um))
    ohm_region += short_connector.transformed(
                            db.ICplxTrans.new(1, 0, False, -0.5*(p.w_connector+p.wHallbar)*um, -p.h_tcn*um))

    point1 = (p.w_connector+0.5*p.wHallbar, p.h_tcn)
    point2 = (0.5*p.dohmicsx-0.5*p.padsize, 1.5*p.dohmicsy-0.5*p.padsize)
    theta = (180/math.pi)*math.atan2(point2[1]-point1[1],point2[0]-point1[0])

    centerx = 0.5*(point2[0]+point1[0])
    centery = 0.5*(point2[1]+point1[1])

    dcn = create_cron_ohm(p.w_dcn, p.h_connector, p.cronSize, um)

    ohm_region += dcn.transformed(
                            db.ICplxTrans.new(1, theta, False, centerx*um, centery*um))

    ohm_region += dcn.transformed(
                            db.ICplxTrans.new(1, 180-theta, False, -centerx*um, centery*um))

    ohm_region += dcn.transformed(
                            db.ICplxTrans.new(1, 180-theta, False, centerx*um, -centery*um))

    ohm_region += dcn.transformed(
                            db.ICplxTrans.new(1, theta, False, -centerx*um, -centery*um))
    

    amark = db.Box(5*um, 5*um)

    xpos = centerC
    ypos = 0.35*p.dohmicsy
    #ohm_region.insert(amark.transformed(db.ICplxTrans.new(1, 0, False, xpos*um,  -ypos*um)))
    #ohm_region.insert(amark.transformed(db.ICplxTrans.new(1, 0, False, xpos*um,   ypos*um)))
    #ohm_region.insert(amark.transformed(db.ICplxTrans.new(1, 0, False, -xpos*um,  ypos*um)))
    #ohm_region.insert(amark.transformed(db.ICplxTrans.new(1, 0, False, -xpos*um, -ypos*um)))

    return ohm_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

def make_island_1(um, p):
    island_region = db.Region()
    island_box = db.Box(p.island_sizeX*um, p.island_sizeY*um)
    island_region.insert(island_box)
    island_region.round_corners(0.1*um, 0.1*um, 64)
    return island_region.transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
    
