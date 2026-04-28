import klayout.db as db
import math
from semiSens.mesa_dot import make_mesa_ohmics
# Creating layout and top cells
# trapezoid for connection between pad
# and hall bar

def create_cron_ohm(width_box, height_box, width_cron, um = 1e3):
    rect = db.Box(width_box*um+2*width_cron*um, height_box*um+2*width_cron*um)
    regionEnd = (db.Region(rect))
    return regionEnd

def make_ohmics_1(um, p):
    
    ohm_region = db.Region()
    ohm_region += make_mesa_ohmics(um, p).size(1*um)
    return ohm_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

def make_island_1(um, p):
    island_region = db.Region()
    island_box = db.Box(p.island_sizeX*um, p.island_sizeY*um)
    if p.has_island:
        island_region.insert(island_box.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.5*p.dot_length*um)))
        island_region.insert(island_box.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.5*p.dot_length*um)))
    island_region.round_corners(0.1*um, 0.1*um, 64)

    mark = db.Box(p.laSize*um, p.laSize*um)
    for pos in p.align3:
        island_region.insert(mark.transformed(db.ICplxTrans.new(1, 0, False, pos[0]*um, pos[1]*um)))
    
    
    return island_region.transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))
    
