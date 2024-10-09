import gdsfactory as gf
from functools import partial

if __name__ == "__main__":
    c = gf.Component()
    w = gf.components.array(partial(gf.c.straight, cross_section = "metal_routing_small", width = 1), columns=1, rows=10, spacing=(5, 5))
    left = c << w

    wleft = gf.components.array(partial(gf.c.straight, cross_section = "metal_routing_small", width = 1), columns=1, rows=5, spacing=(5, 5))
    lefter = c << wleft

    d = gf.components.array(partial(gf.c.straight, cross_section = "metal_routing", width = 1), columns=1, rows=10, spacing=(80, 80))
    right = c << d
    
    
    right.dmove((300, -320))

    lefter.dmove((-300, 0))

    obstacle = gf.components.rectangle(size=(300, 10))
    obstacle1 = c << obstacle
    obstacle2 = c << obstacle
    obstacle1.dymin = 70
    obstacle2.dxmin = 150

    ports1 = left.ports.filter(orientation=0)
    ports2 = right.ports.filter(orientation=180)

    routes = gf.routing.route_bundle(
        c,
        ports1,
        ports2,
        separation = 10,
        allow_width_mismatch = True,
        route_width = 1.0,
        cross_section = "metal_routing_small",
        waypoints = [(200, 20), (220, 20)]
    )
    c.show()