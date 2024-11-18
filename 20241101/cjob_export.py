import numpy as np

string = """<?xml version="1.0" encoding="UTF-8"?>
<cjob version="v02_22" type="ebpg5200">
  <color num="1" pattern="20241101_HMIAII4_pdgdottest_device0.gpf" rgb="255 0 0"/>
  <color num="1" pattern="20241101_HMIAII4_pdgdottest_device1.gpf" rgb="0 255 0"/>
  <substrate substrate="mask">
    <mask size="4.5mmx4mm"/>
    <color rgb="200 200 200" substrate="mask"/>
    <position coord="0,0"/>
    <exposure workinglevel="high" height="none" ht="100kV" name="mesa_fine">
      <position coord="0,0"/>
      <checks enabled="false"/>\n"""

coord_array = np.linspace(-1350, 1350, 4, True)

x, y = np.meshgrid(coord_array, coord_array)

xflat = x.flatten()
yflat = y.flatten()

mark1 = (xflat-50, yflat-90)
mark2 = (xflat-50, yflat+90)
mark3 = (xflat+50, yflat+90)
mark4 = (xflat+50, yflat-90)

for k in range(16):
    string+=f"""      <pattern name="20241101_HMIAII4_pdgdottest_device{k}.gpf">
        <position coord="0,0"/>
        <beam defocus="#0" name="2na_200.beam_100" dose="650"/>
        <marker enabled="true" name="prvn_pos5">
          <markerlist>
            <position coord="{mark1[0][k]},{mark1[1][k]}"/>
          </markerlist>
          <markerlist>
            <position coord="{mark2[0][k]},{mark2[1][k]}"/>
          </markerlist>
          <markerlist>
            <position coord="{mark3[0][k]},{mark3[1][k]}"/>
          </markerlist>
          <markerlist>
            <position coord="{mark4[0][k]},{mark4[1][k]}"/>
          </markerlist>
        </marker>
      </pattern>\n"""
string+=f"""      <pattern name="20241101_HMIAII4_pdgdottest_device16.gpf">
        <position coord="0,0"/>
        <beam defocus="#0" name="2na_200.beam_100" dose="650"/>
      </pattern>\n"""
string+= """<marker enabled="true" name="kmorey_pos20">
        <markerlist>
          <position coord="-1850,-1700"/>
        </markerlist>
        <markerlist>
          <position coord="-1850,1700"/>
        </markerlist>
        <markerlist>
          <position coord="1850,1700"/>
        </markerlist>
        <markerlist>
          <position coord="1850,-1700"/>
        </markerlist>
        <markerlist/>
        <markerlist/>
        <markerlist/>
        <markerlist/>
      </marker>
    </exposure>
  </substrate>
</cjob>"""

with open("new_inas_mesafine.cjob", "w") as f:
    f.write(string)