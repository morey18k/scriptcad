import klayout.db as db
import numpy as np
import math
# Creating layout and top cells
# Mesa Layer


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



def make_mesa_ohmics(um, p):
    region = create_cron_box(p.padsize, p.padsize, p.cronSize, um)

    mesa_region = db.Region()

    
    offset = 0.5 if p.num_cols%2 == 0 else 0
    pad_centers_y = np.arange(-(p.num_cols//2)+offset, -(p.num_cols//2)+offset+p.num_cols)*p.dohmicsy
    pad_centers_y[1] -= 0.23*p.dohmicsy
    pad_centers_y[3] += 0.23*p.dohmicsy
    for k, center in enumerate(pad_centers_y):
        if k == 0 or k == len(pad_centers_y)-1:
            mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, p.dohmicsx*um, 0.975*center*um)))
            mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, 2*p.dohmicsx*um, center*um)))
        else:   
            mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, 1.05*p.dohmicsx*um, center*um)))
            mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, 2.1*p.dohmicsx*um, center*um)))

    mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, 0.3*p.dohmicsx*um, 1.95*p.dohmicsy*um)))
    mesa_region.insert(region.transformed(db.ICplxTrans.new(1, 0, False, 0.3*p.dohmicsx*um, -1.95*p.dohmicsy*um)))        
        

    probe_points = [((-0.5*p.wHallbar-0.5*p.w_connector)*um, -0.4*p.lHallbar*um)
                    , ((-0.5*p.wHallbar+0.5*p.w_connector)*um, (-0.5*p.lHallbar-0.5*p.h_connector)*um)
                    , ((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.4*p.lHallbar*um)
                    , ((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.24*p.lHallbar*um)
                    , ((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.08*p.lHallbar*um)]
    
    for points in probe_points:
        mesa_region.insert(db.Box((p.w_connector)*um, p.h_connector*um).transformed(db.ICplxTrans.new(1, 0, False, points[0], points[1])))
        mesa_region.insert(db.Box((p.w_connector)*um, p.h_connector*um).transformed(db.ICplxTrans.new(1, 0, False, points[0], -points[1])))
    wohmic_trace = 15

    ohmic_trace_1 = db.Path([((-0.5*p.wHallbar-p.w_connector+0.5*wohmic_trace)*um, -0.4*p.lHallbar*um), 
                             ((-0.5*p.wHallbar-p.w_connector+0.5*wohmic_trace)*um, -0.4*p.lHallbar*um),
                             ((-0.5*p.wHallbar-p.w_connector+0.5*wohmic_trace)*um, -0.75*p.lHallbar*um),
                             (1.8*p.dohmicsx*um, -0.75*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, -0.6*p.lHallbar*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_2 = db.Path([(0*um, (-0.5*p.lHallbar-0.5*p.h_connector)*um), 
                             (0.75*p.dohmicsx*um, (-0.5*p.lHallbar-0.5*p.h_connector)*um),
                             (0.75*p.dohmicsx*um, -0.6*p.lHallbar*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_3 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.4*p.lHallbar*um), 
                             ((0.75*p.dohmicsx)*um, -0.4*p.lHallbar*um),
                             ], width = 15*um)
    
    ohmic_trace_4 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.24*p.lHallbar*um), 
                             ((0.5*p.wHallbar+p.w_connector)*um, -0.24*p.lHallbar*um),
                             ((0.5*p.wHallbar+p.w_connector)*um, (-0.24*p.lHallbar)*um),
                             ((1.8*p.dohmicsx)*um, (-0.24*p.lHallbar)*um),
                             ((1.8*p.dohmicsx)*um, (-0.3*p.lHallbar)*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_5 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, -0.08*p.lHallbar*um), 
                             ((0.75*p.dohmicsx)*um, -0.08*p.lHallbar*um),
                             ], width = wohmic_trace*um)
    
    ohmic_trace_6 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, 0.08*p.lHallbar*um), 
                             ((0.5*p.wHallbar+p.w_connector)*um, 0.08*p.lHallbar*um),
                             ((0.5*p.wHallbar+p.w_connector)*um, 0.13*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, 0.13*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, 0*p.lHallbar*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_7 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, 0.24*p.lHallbar*um), 
                             ((0.5*p.wHallbar+p.w_connector)*um, 0.24*p.lHallbar*um),
                             ((0.5*p.wHallbar+p.w_connector)*um, 0.24*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, 0.24*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, 0.30*p.lHallbar*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_8 = db.Path([((0.5*p.wHallbar+0.5*p.w_connector)*um, 0.4*p.lHallbar*um), 
                             ((0.75*p.dohmicsx)*um, 0.4*p.lHallbar*um),
                             ], width = wohmic_trace*um)
    
    ohmic_trace_9 = db.Path([(0*um, (0.5*p.lHallbar+0.5*p.h_connector)*um), 
                             (0.75*p.dohmicsx*um, (+0.5*p.lHallbar+0.5*p.h_connector)*um),
                             (0.75*p.dohmicsx*um, 0.6*p.lHallbar*um)
                             ], width = wohmic_trace*um)
    
    ohmic_trace_10 = db.Path([((-0.5*p.wHallbar-1.0*p.w_connector+0.5*wohmic_trace)*um, 0.4*p.lHallbar*um), 
                             ((-0.5*p.wHallbar-1.0*p.w_connector+0.5*wohmic_trace)*um, 0.4*p.lHallbar*um),
                             ((-0.5*p.wHallbar-1.0*p.w_connector+0.5*wohmic_trace)*um, 0.75*p.lHallbar*um),
                             (1.8*p.dohmicsx*um, 0.75*p.lHallbar*um),
                             ((1.8*p.dohmicsx)*um, 0.6*p.lHallbar*um)
                             ], width = wohmic_trace*um)

    ohmic_trace_11 = db.Path([((2.0*p.dohmicsx)*um, -1*p.dohmicsy*um),
                                ((2.5*p.dohmicsx)*um, -1*p.dohmicsy*um),
                                ((2.5*p.dohmicsx)*um, -1.5*p.dohmicsy*um),
                                ((3.5*p.dohmicsx)*um, -1.5*p.dohmicsy*um),
                                ((3.5*p.dohmicsx)*um, -2.5*p.dohmicsy*um),
                                ], width = 15*um)

    ohmic_trace_12 = db.Path([((2.0*p.dohmicsx)*um, 1*p.dohmicsy*um),
                                ((2.5*p.dohmicsx)*um, 1*p.dohmicsy*um),
                                ((2.5*p.dohmicsx)*um, 1.5*p.dohmicsy*um),
                                ((3.5*p.dohmicsx)*um, 1.5*p.dohmicsy*um),
                                ((3.5*p.dohmicsx)*um, 2.5*p.dohmicsy*um),
                                ], width = 15*um)                      
    
    mesa_region.insert(ohmic_trace_1)
    mesa_region.insert(ohmic_trace_2)
    mesa_region.insert(ohmic_trace_3)
    mesa_region.insert(ohmic_trace_4)
    mesa_region.insert(ohmic_trace_5)
    mesa_region.insert(ohmic_trace_6)
    mesa_region.insert(ohmic_trace_7)
    mesa_region.insert(ohmic_trace_8)
    mesa_region.insert(ohmic_trace_9)
    mesa_region.insert(ohmic_trace_10)
    mesa_region.insert(ohmic_trace_11)
    mesa_region.insert(ohmic_trace_12)
    return mesa_region

def make_mesaf_1(um, p):

    trenchlength = p.island_sizeX*1.3

    region = db.Region()
    other = db.Polygon([((-0.5*p.wHallbar-1)*um, -0.25*p.dohmicsy*um), ((-0.5*p.wHallbar-1)*um, 0.25*p.dohmicsy*um), (-0.5*trenchlength*um, 0.03*p.dohmicsy*um), (-0.5*trenchlength*um, -0.03*p.dohmicsy*um)])
    
    #region.insert(other.transformed(db.ICplxTrans.new(1, 0, False, 0, 0)))
    #region.insert(other.transformed(db.ICplxTrans.new(1, 180, False, 0, 0)))
    
    trench = db.Box((trenchlength)*um, 0.12*um)

    if p.has_island:
        region.insert(trench.transformed(db.ICplxTrans.new(1, 0, False, 0, -0.5*p.dot_length*um)))
        region.insert(trench.transformed(db.ICplxTrans.new(1, 0, False, 0, 0.5*p.dot_length*um)))


    #trenchaddon = db.Box(0.12*um, 0.32*um)
    #region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False, -0.2*trenchlength*um, 0)))
    #region.insert(trenchaddon.transformed(db.ICplxTrans.new(1, 0, False,  0.2*trenchlength*um, 0)))

    return region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um)))

def make_mesa_gatepads(um, p):
    mesa_region = db.Region()
    offset = 0.5 if p.num_cols%2 == 0 else 0
    gate_pad = db.Box(p.gatepadwidth*um, p.gatepadheight*um)
    pad_centers_y = np.arange(-(p.num_cols//2)+offset, -(p.num_cols//2)+offset+p.num_cols)*p.dohmicsy
    for center in pad_centers_y:
        mesa_region.insert(gate_pad.transformed(db.ICplxTrans.new(1, 0, False, 4*p.dohmicsx*um, center*um)))
        mesa_region.insert(gate_pad.transformed(db.ICplxTrans.new(1, 0, False, 3*p.dohmicsx*um, center*um)))
        mesa_region.insert(gate_pad.transformed(db.ICplxTrans.new(1, 0, False, -1*p.dohmicsx*um, center*um)))

    return mesa_region

def make_mesa_1(um, p):
    mesa_region = make_mesa_ohmics(um, p)
    hallbar = db.Box(p.wHallbar*um, p.lHallbar*um)
    mesa_region.insert(hallbar)
    mesa_region += make_mesa_gatepads(um, p)
    shield = db.Box((p.laSize+20)*um, (p.laSize+20)*um)
    for k in range(4):
        mesa_region.insert(shield.transformed(db.ICplxTrans.new(1, 0, False, p.align2[k][0]*um, p.align2[k][1]*um)))

    return (mesa_region.merged().transformed((db.ICplxTrans(1, p.angle, False, p.centerx*um, p.centery*um))))