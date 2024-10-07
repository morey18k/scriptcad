import klayout.db as db
import math
# Creating layout and top cells
layout = db.Layout(True)
layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/other_bar.gds")
top = layout.cell("TOP")
# Mesa Layer


ohmics = layout.layer(3, 0)
layout.clear_layer(ohmics)


um = 1e3
# trapezoid for connection between pad
# and hall bar


def create_cron_ohm(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um+2*width_cron*um, height_box*um+2*width_cron*um)
    regionEnd = (db.Region(rect))
    return regionEnd

dohmicsy = 200

dohmicsx = 400


padsize = 150

region = create_cron_ohm(padsize, padsize, 5.5, um)

ohm_region = db.Region()


ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*dohmicsx*um, -1.5*dohmicsy*um))
ohm_region += region.transformed(
                            db.ICplxTrans.new(1, 0, False, 0.5*dohmicsx*um, -1.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*dohmicsx*um, -0.5*dohmicsy*um))
ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*dohmicsx*um, 0.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*dohmicsx*um, 1.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*dohmicsx*um, -1.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*dohmicsx*um, -0.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*dohmicsx*um, 0.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*dohmicsx*um, 1.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0, 1.5*dohmicsy*um))

ohm_region += region.transformed(
                           db.ICplxTrans.new(1, 0, False, 0, -1.5*dohmicsy*um))


wHallbar = 100
lHallbar = 400

rightend = dohmicsx*0.5-0.5*padsize
leftend = wHallbar*0.5
centerC = 0.5*(rightend+leftend)


h_connector = 15

connector = db.Box((rightend-leftend)*um, h_connector*um+10*um)



ohm_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -centerC*um, 0.5*dohmicsy*um))

ohm_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, centerC*um, 0.5*dohmicsy*um))

ohm_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, centerC*um, -0.5*dohmicsy*um))

ohm_region += connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -centerC*um, -0.5*dohmicsy*um))



topcn = create_cron_ohm(wHallbar, 1.5*dohmicsy-0.5*padsize-lHallbar*0.5, 5, um)



ohm_region += topcn.transformed(
                           db.ICplxTrans.new(1, 0, False, 0*um, 0.5*(1.5*dohmicsy-0.5*padsize+0.5*lHallbar)*um))

ohm_region += topcn.transformed(
                           db.ICplxTrans.new(1, 0, False, 0*um, -0.5*(1.5*dohmicsy-0.5*padsize+0.5*lHallbar)*um))



w_connector = 35

short_connector = create_cron_ohm(w_connector, h_connector, 5, um)

h_tcn = 0.85*dohmicsy
ohm_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*(w_connector+wHallbar)*um, h_tcn*um))

ohm_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*(w_connector+wHallbar)*um, h_tcn*um))
ohm_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, 0.5*(w_connector+wHallbar)*um, -h_tcn*um))
ohm_region += short_connector.transformed(
                           db.ICplxTrans.new(1, 0, False, -0.5*(w_connector+wHallbar)*um, -h_tcn*um))

point1 = (w_connector+0.5*wHallbar, h_tcn)
point2 = (0.5*dohmicsx-0.5*padsize, 1.5*dohmicsy-0.5*padsize)
theta = (180/math.pi)*math.atan2(point2[1]-point1[1],point2[0]-point1[0])

centerx = 0.5*(point2[0]+point1[0])
centery = 0.5*(point2[1]+point1[1])

w_dcn = 75

dcn = create_cron_ohm(w_dcn, h_connector, 5, um)

ohm_region += dcn.transformed(
                           db.ICplxTrans.new(1, theta, False, centerx*um, centery*um))

ohm_region += dcn.transformed(
                           db.ICplxTrans.new(1, 180-theta, False, -centerx*um, centery*um))

ohm_region += dcn.transformed(
                           db.ICplxTrans.new(1, 180-theta, False, centerx*um, -centery*um))

ohm_region += dcn.transformed(
                           db.ICplxTrans.new(1, theta, False, -centerx*um, -centery*um))


top.shapes(ohmics).insert(ohm_region.merged())


layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/other_bar.gds")

    
