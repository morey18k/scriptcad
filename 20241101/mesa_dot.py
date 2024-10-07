import klayout.db as db
import math
# Creating layout and top cells
layout = db.Layout(True)
layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/other_bar.gds")
top = layout.cell("TOP")
# Mesa Layer


mesaPos = layout.layer(2, 0)
layout.clear_layer(mesaPos)


um = 1e3
# trapezoid for connection between pad
# and hall bar


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

class params():
    dohmicsy = 200
    dohmicsx = 400
    padsize = 150
    cronSize = 5
    h_connector = 15

    wHallbar = 100
    lHallbar = 400
    w_connector = 35
    h_tcn = 0.85*dohmicsy
    w_dcn = 75


p = params()


region = create_cron_box(p.padsize, p.padsize, p.cronSize, um)

mesa_region = db.Region()


mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))
mesa_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, -0.5*p.dohmicsy*um))
mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, 0.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*p.dohmicsx*um, 1.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, -1.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, -0.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, 0.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*p.dohmicsx*um, 1.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0, 1.5*p.dohmicsy*um))

mesa_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0, -1.5*p.dohmicsy*um))



mesa_bar = db.Box(p.wHallbar*um, p.lHallbar*um)

rightend = p.dohmicsx*0.5-0.5*p.padsize
leftend = p.wHallbar*0.5
centerC = 0.5*(rightend+leftend)




connector = create_cron_box(rightend-leftend, p.h_connector, p.cronSize, um)

mesa_region += db.Region(mesa_bar).transformed(
                           db.ICplxTrans.new(1, 0, False, 0.0*um, 0.0*um))


mesa_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -centerC*um, 0.5*p.dohmicsy*um))

mesa_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, centerC*um, 0.5*p.dohmicsy*um))

mesa_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, centerC*um, -0.5*p.dohmicsy*um))

mesa_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -centerC*um, -0.5*p.dohmicsy*um))



topcn = create_cron_box(p.wHallbar, 1.5*p.dohmicsy-0.5*p.padsize-p.lHallbar*0.5, p.cronSize, um)



mesa_region += topcn.transformed(
                           db.ICplxTrans.new(1, 0, False, 0*um, 0.5*(1.5*p.dohmicsy-0.5*p.padsize+0.5*p.lHallbar)*um))

mesa_region += topcn.transformed(
                           db.ICplxTrans.new(1, 0, False, 0*um, -0.5*(1.5*p.dohmicsy-0.5*p.padsize+0.5*p.lHallbar)*um))





short_connector = create_cron_box(p.w_connector, p.h_connector, p.cronSize, um)


mesa_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*(p.w_connector+p.wHallbar)*um, p.h_tcn*um))

mesa_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*(p.w_connector+p.wHallbar)*um, p.h_tcn*um))
mesa_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*(p.w_connector+p.wHallbar)*um, -p.h_tcn*um))
mesa_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*(p.w_connector+p.wHallbar)*um, -p.h_tcn*um))

point1 = (p.w_connector+0.5*p.wHallbar, p.h_tcn)
point2 = (0.5*p.dohmicsx-0.5*p.padsize, 1.5*p.dohmicsy-0.5*p.padsize)
theta = (180/math.pi)*math.atan2(point2[1]-point1[1],point2[0]-point1[0])

centerx = 0.5*(point2[0]+point1[0])
centery = 0.5*(point2[1]+point1[1])

dcn = create_cron_box(p.w_dcn, p.h_connector, p.cronSize, um)

mesa_region += dcn.transformed(
                           db.ICplxTrans.new(1, theta, False, centerx*um, centery*um))

mesa_region += dcn.transformed(
                           db.ICplxTrans.new(1, 180-theta, False, -centerx*um, centery*um))

mesa_region += dcn.transformed(
                           db.ICplxTrans.new(1, 180-theta, False, centerx*um, -centery*um))

mesa_region += dcn.transformed(
                           db.ICplxTrans.new(1, theta, False, -centerx*um, -centery*um))


top.shapes(mesaPos).insert(mesa_region.merged())


layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/other_bar.gds")

    
