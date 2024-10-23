import gdsfactory as gf
from functools import partial
import klayout.db as db

if __name__ == "__main__":
    c = gf.Component()    
    w1 = gf.c.straight(length = 2, cross_section = "metal_routing", layer = 'M3')
    top = c << w1
    middle = c << w1
    bottom = c << w1
    top.dmove((0, 10))
    bottom.dmove((0, -10))
    
    rtop = c << w1
    rmiddle = c << w1
    rbottom = c << w1
    rtop.dmove((200, 200))
    rmiddle.dmove((200, 0))
    rbottom.dmove((200, -200))

    ports1 = top.ports.filter(orientation=0) + middle.ports.filter(orientation=0) + bottom.ports.filter(orientation=0)
    ports2 = rtop.ports.filter(orientation=180) + rmiddle.ports.filter(orientation=180) + rbottom.ports.filter(orientation=180)

    routes = gf.routing.route_bundle(
        c,
        ports1,
        ports2,
        separation = 10,
        allow_width_mismatch = True,
        route_width = 1.0,
        cross_section = "metal_routing",
        waypoints = [(100, 5), (120, 5)]
    )
    
    rgn = db.Region(c.get_polygons()[23])

    layout = db.Layout(True)
    layout.read("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
                "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")

    top = layout.cell("TOP")
    um = 1e3

    cgates = layout.layer(5, 0)

    top.shapes(cgates).insert(rgn)
    layout.write("/Users/karnamorey/Google Drive/Shared drives/GGG GDrive/"
             "QDots-2/HMIAChipDesign/scriptcad/20241101/other_bar.gds")


   