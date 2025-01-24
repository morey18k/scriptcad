import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from numpy.random import permutation
import klayout.db as db

class BondPlanInit():
    pad_x = []
    pad_y = []
    xcenter = []
    ycenter = []

def intersection_matrix(permute):
    out = np.zeros((48, 48))
    for k in range(len(permute)):
        for carrier_index in range(len(permute)):
            if carrier_index == k:
                out[k, carrier_index] = 0
                continue
            p1 = (bo.xcenter[k], bo.ycenter[k])
            p2 = (bo.pad_x[permute[k]], bo.pad_y[permute[k]])
            p3 = (bo.xcenter[carrier_index], bo.ycenter[carrier_index])
            p4 = (bo.pad_x[permute[carrier_index]], bo.pad_y[permute[carrier_index]])
            out[k, carrier_index] = (do_segments_intersect_once(p1, p2, p3, p4))
    return out

def distance(device_i, carrier_i, bo):
    return np.sqrt((bo.pad_x[device_i]-bo.xcenter[carrier_i])**2.0 + (bo.pad_y[device_i]-bo.ycenter[carrier_i])**2.0)

def do_segments_intersect_once(p1, p2, p3, p4):
    """
    Returns True if line segment p1->p2 intersects line segment p3->p4
    at exactly one point (i.e. a proper single crossing).
    Returns False otherwise.

    Each pX is a tuple of (x, y).
    """

    # Unpack points for readability
    (x1, y1), (x2, y2) = p1, p2
    (x3, y3), (x4, y4) = p3, p4

    # A small helper for orientation
    # orientation(a, b, c) returns:
    #    0 if a, b, c are collinear
    #    1 if the sequence a->b->c is clockwise
    #    2 if counterclockwise
    def orientation(a, b, c):
        (ax, ay), (bx, by), (cx, cy) = a, b, c
        val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
        if abs(val) < 1e-12:
            return 0  # collinear (within a small epsilon)
        return 1 if val > 0 else 2

    # A helper to check if point q lies on segment pr
    def on_segment(p, q, r):
        (px, py), (qx, qy), (rx, ry) = p, q, r
        return (min(px, rx) <= qx <= max(px, rx) and
                min(py, ry) <= qy <= max(py, ry))

    # Orientations needed for the general and special cases
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    # --- Check general intersection condition ---
    # Two segments p1->p2 and p3->p4 intersect if:
    #  1) The lines strictly intersect in orientation sense:
    #       o1 != o2 and o3 != o4
    #     which indicates a proper crossing
    #  2) Or special collinear overlap checks (but we do NOT want an overlap)
    intersect = False

    # Condition 1: properly intersect in orientation sense
    if o1 != o2 and o3 != o4:
        intersect = True
    else:
        # Condition 2: collinear but endpoints might lie on each other
        # For exactly one point intersection, we don't want
        # partial or entire overlap. But we do have to see if they share
        # exactly one endpoint. That can be "one intersection" or not,
        # depending on the problem statement.
        # Here we exclude all collinear overlaps from "exactly one point".
        
        # If collinear and p3 lies on p1->p2:
        if o1 == 0 and on_segment(p1, p3, p2): 
            intersect = True
        if o2 == 0 and on_segment(p1, p4, p2): 
            intersect = True
        if o3 == 0 and on_segment(p3, p1, p4): 
            intersect = True
        if o4 == 0 and on_segment(p3, p2, p4): 
            intersect = True

        # If we found a 'collinear' intersection, that could be
        # exactly at an endpoint or partially overlapping. We'll refine below.

    if not intersect:
        return False  # no intersection

    # --- Now refine: ensure it's exactly one point, not an overlap. ---
    # 1) If the segments are collinear and they share more than one point (overlap),
    #    that's not "one intersection".
    #    We can detect that if orientation(...) == 0 for everything
    #    and bounding boxes overlap for more than an endpoint.
    if (o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0):
        # All collinear
        # Check if bounding boxes overlap in more than an endpoint:
        # Project on x or y (we can check any dimension).
        # For x dimension:
        def proj_range(a, b):
            return (min(a[0], b[0]), max(a[0], b[0]))
        seg1 = proj_range(p1, p2)
        seg2 = proj_range(p3, p4)

        # If the intervals overlap in more than 0 length => not a single point
        overlap_min = max(seg1[0], seg2[0])
        overlap_max = min(seg1[1], seg2[1])
        if overlap_max > overlap_min:
            # There's an actual overlap region
            return False  # not a single intersection point
        else:
            # overlap_max == overlap_min => they share exactly an endpoint in X
            # but we must also confirm the same in Y dimension
            # Because collinearity might be vertical etc. We'll do the same for Y.
            seg1y = (min(p1[1], p2[1]), max(p1[1], p2[1]))
            seg2y = (min(p3[1], p4[1]), max(p3[1], p4[1]))
            overlap_min_y = max(seg1y[0], seg2y[0])
            overlap_max_y = min(seg1y[1], seg2y[1])
            # If they share exactly one point in Y as well,
            # then it is one intersection endpoint. Otherwise it's no intersection
            if overlap_max_y == overlap_min_y:
                # Exactly one common point
                return True
            else:
                return False

    # 2) If not collinear, we get exactly one intersection for standard crossing
    return True

rect_centers = [
    ("path263", (446.145705, 365.142885)),
    ("path265", (446.145705, 153.404605)),
    ("path267", (446.145705, 47.262023)),
    ("path272", (22.4250145, 381.043275)),
    ("path274", (22.4250145, 273.58234)),
    ("path276", (22.4250145, 63.162413)),
    ("path281", (402.16524, 408.40265)),
    ("path283", (294.7043, 408.40265)),
    ("path285", (172.66524, 408.40265)),
    ("path286", (154.84688, 408.40265)),
    ("path287", (225.0, 408.40265)),
    ("path289", (84.2843895, 408.40265)),
    ("path303", (65.0851695, 20.742495)),
    ("path305", (172.544145, 20.742495)),
    ("path307", (294.58516, 20.742495)),
    ("path308", (312.405475, 20.742495)),
    ("path309", (330.223835, 20.742495)),
    ("path310", (242.2668, 20.742495)),
    ("path343", (382.964065, 20.742495)),
    ("path345", (446.145705, 382.90265)),
    ("path346", (446.145705, 347.322575)),
    ("path347", (446.145705, 293.504215)),
    ("path348", (446.145705, 275.443665)),
    ("path349", (446.145705, 135.642885)),
    ("path350", (446.145705, 117.824025)),
    ("path351", (446.145705, 223.543275)),
    ("path352", (446.145705, 205.781555)),
    ("path353", (446.145705, 65.023743)),
    ("path354", (22.4250145, 363.222965)),
    ("path355", (22.4250145, 345.404605)),
    ("path356", (22.4250145, 291.58234)),
    ("path357", (22.4250145, 151.543275)),
    ("path358", (22.4250145, 133.72296)),
    ("path359", (22.4250145, 115.90265)),
    ("path360", (22.4250145, 221.681945)),
    ("path361", (22.4250145, 203.86359)),
    ("path362", (22.4250145, 45.344053)),
    ("path363", (384.344925, 408.40265)),
    ("path364", (366.526565, 408.40265)),
    ("path365", (312.7043, 408.40265)),
    ("path366", (137.024615, 408.40265)),
    ("path367", (242.803915, 408.40265)),
    ("path368", (66.466026, 408.40265)),
    ("path369", (82.905479, 20.742495)),
    ("path370", (100.725787, 20.742495)),
    ("path371", (154.544145, 20.742495)),
    ("path372", (224.444535, 20.742495)),
    ("path373", (400.786335, 20.742495))]

rect_sizes = [
    ("path263",  (20.75781,  11.63671)),
    ("path265",  (20.75781,  11.51953)),
    ("path267",  (20.75781,  11.64063)),
    ("path272",  (20.761719, 11.52343)),
    ("path274",  (20.761719, 11.64062)),
    ("path276",  (20.761719, 11.51953)),
    ("path281",  (11.52344,  20.88282)),
    ("path283",  (11.64062,  20.88282)),
    ("path285",  (11.64062,  20.88282)),
    ("path286",  (11.51954,  20.88282)),
    ("path287",  (11.64062,  20.88282)),
    ("path289",  (11.51953,  20.88282)),
    ("path303",  (11.519529, 20.757806)),
    ("path305",  (11.64063,  20.757806)),
    ("path307",  (11.63672,  20.757806)),
    ("path308",  (11.51953,  20.757806)),
    ("path309",  (11.64063,  20.757806)),
    ("path310",  (11.64062,  20.757806)),
    ("path343",  (11.51953,  20.757806)),
    ("path345",  (20.75781,  11.64062)),
    ("path346",  (20.75781,  11.51953)),
    ("path347",  (20.75781,  11.64063)),
    ("path348",  (20.75781,  11.51953)),
    ("path349",  (20.75781,  11.51953)),
    ("path350",  (20.75781,  11.64063)),
    ("path351",  (20.75781,  11.64063)),
    ("path352",  (20.75781,  11.64063)),
    ("path353",  (20.75781,  11.64063)),
    ("path354",  (20.761719, 11.64063)),
    ("path355",  (20.761719, 11.51953)),
    ("path356",  (20.761719, 11.64062)),
    ("path357",  (20.761719, 11.64063)),
    ("path358",  (20.761719, 11.52344)),
    ("path359",  (20.761719, 11.64062)),
    ("path360",  (20.761719, 11.51953)),
    ("path361",  (20.761719, 11.64062)),
    ("path362",  (20.761719, 11.64063)),
    ("path363",  (11.64063,  20.88282)),
    ("path364",  (11.51953,  20.88282)),
    ("path365",  (11.64062,  20.88282)),
    ("path366",  (11.64063,  20.88282)),
    ("path367",  (11.51953,  20.88282)),
    ("path368",  (11.640616, 20.88282)),
    ("path369",  (11.63671,  20.757806)),
    ("path370",  (11.519526, 20.757806)),
    ("path371",  (11.64063,  20.757806)),
    ("path372",  (11.51953,  20.757806)),
    ("path373",  (11.64063,  20.757806))]

order = [12, 43, 44, 45, 13, 46, 17, 14, 15, 16, 18, 47, 2,
         27, 24, 23, 1, 26, 25, 22, 21, 20, 0, 19, 6,37, 38, 39,
         7, 41, 10, 8, 9, 40, 11, 42, 3, 28, 29, 30, 4, 34, 35, 
         31, 32, 33, 5, 36]

order = np.roll(order, 10)

bo = BondPlanInit()

bigrectsize = np.array([340.59167, 317.31366])
bigrectcenter = np.array([235.427007, 213.822003])

bo.xcenter = 6800*(np.array([element[1][0] for element in rect_centers])[order]-bigrectcenter[0])/bigrectsize[0]
bo.ycenter = 6300*(np.array([element[1][1] for element in rect_centers])[order]-bigrectcenter[1])/bigrectsize[1]


width = (6800/bigrectsize[0])*np.array([element[1][0] for element in rect_sizes])[order]
height = (6300/bigrectsize[1])*np.array([element[1][1] for element in rect_sizes])[order]

anchorx = bo.xcenter - 0.5*width
anchory = bo.ycenter - 0.5*height

fig, ax = plt.subplots()



bigrectanchor = -0.5*bigrectsize

rect = patches.Rectangle((-3400, -3150), 6800, 6300, linewidth=0.5, edgecolor='k', facecolor='none')
ax.add_patch(rect)



ax.set_xlim(-4500, 4500)
ax.set_ylim(-4500, 4500)
plt.axis('equal')

ly = db.Layout()
ly.read("bonding.gds")

shapes = ly.top_cell().shapes(ly.layer(db.LayerInfo(0, 0)))

factor = 1e3
bo.pad_x = np.array([shape.bbox().center().x/factor for shape in shapes.each()])
bo.pad_y = np.array([shape.bbox().center().y/factor for shape in shapes.each()])

for k in range(48):
    rect = patches.Rectangle((anchorx[k], anchory[k]), width[k], height[k], linewidth=1, edgecolor='r', facecolor='none')
    ax.text(anchorx[k], anchory[k], k)
    ax.add_patch(rect)

    ax.text(bo.pad_x[k], bo.pad_y[k], k)

distance_matrix = np.array([[distance(i, j, bo) for i in range(48)] for j in range(48)])

bonds = []
nmax = 4
for k in range(nmax):
    pad_min_index = np.argmin(distance_matrix[k])
    
    distance_matrix[k, :] = np.inf
    distance_matrix[:, pad_min_index] = np.inf

    intersections = []
    for carrier_index in range(len(bonds)):
        p1 = (bo.xcenter[k], bo.ycenter[k])
        p2 = (bo.pad_x[pad_min_index], bo.pad_y[pad_min_index])
        p3 = (bo.xcenter[carrier_index], bo.ycenter[carrier_index])
        p4 = (bo.pad_x[bonds[carrier_index]], bo.pad_y[bonds[carrier_index]])

        intersections.append(do_segments_intersect_once(p1, p2, p3, p4))
    
    temp = 0
    intersect_array_0 = np.array(intersections)

    old_sum = 100
    print(np.sum(intersect_array_0), end = " ")
    while np.sum(intersect_array_0) >= 1:
        if np.sum(intersect_array_0)==old_sum:
            break
        conflict_bond = np.argmax(intersect_array_0)
        temp = pad_min_index
        pad_min_index = bonds[conflict_bond]
        bonds[conflict_bond] = temp
    
        intersections_new = []
        for carrier_index in range(len(bonds)):
            p1 = (bo.xcenter[k], bo.ycenter[k])
            p2 = (bo.pad_x[pad_min_index], bo.pad_y[pad_min_index])
            p3 = (bo.xcenter[carrier_index], bo.ycenter[carrier_index])
            p4 = (bo.pad_x[bonds[carrier_index]], bo.pad_y[bonds[carrier_index]])

        intersections_new.append(do_segments_intersect_once(p1, p2, p3, p4))
        old_sum = np.sum(intersect_array_0)
        intersect_array_0 = np.array(intersections_new)
        print(np.sum(intersect_array_0), end = " ")
    print("")
    #print(intersections_new)
    bonds.append(pad_min_index)

num_sim = 1000
crossings = np.full(num_sim, 500000)
pvals = np.empty((num_sim, 48), dtype = int)
for j in range(num_sim):
    pvals[j]  = permutation(48)
    crossings[j] = np.sum(intersection_matrix(pvals[j]))

#print(pvals)
print(np.amin(crossings))

imatrix = intersection_matrix(bonds)
print(imatrix, np.sum(imatrix))



for k in range(nmax):
    plt.plot([bo.xcenter[k], bo.pad_x[bonds[k]]], [bo.ycenter[k], bo.pad_y[bonds[k]]], color = 'k', linewidth = 0.2)

plt.show()

