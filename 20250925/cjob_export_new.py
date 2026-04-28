import numpy as np

pattern_name_prefix = "20250116_HMIAII6_pdgrtatest_device"
exposure_name = "gates_fine"
export_job_name = "fgates_job.cjob"
local_mark_name = "prvn_pos5"
global_mark_name = "kmorey_pos20"
num_patterns = 9
dose = 650 #uC/cm^2
beam_current_name = "2na_200.beam_100"
global_marks = [[-1525,-1075], [-1525,1075], [1525,1075], [1525,-1075]]

string = f"""<?xml version="1.0" encoding="UTF-8"?>
<cjob version="v02_22" type="ebpg5200">
  <substrate substrate="mask">
    <mask size="10.5mmx10mm"/>
    <color rgb="200 200 200" substrate="mask"/>
    <position coord="0,0"/>
    <exposure workinglevel="high" height="none" ht="100kV" name="{exposure_name}">
      <position coord="0,0"/>
      <checks enabled="false"/>\n"""

#coord_array = np.linspace(-1350, 1350, 4, True)

coord_array = np.linspace(-900, 900, 3, True)

x, y = np.meshgrid(coord_array, coord_array)

xflat = x.flatten()
yflat = y.flatten()

mark1 = (xflat-50, yflat-50)
mark2 = (xflat-50, yflat+50)
mark3 = (xflat+50, yflat+50)
mark4 = (xflat+50, yflat-50)

for k in range(num_patterns):
    string+=f"""      <pattern name="{pattern_name_prefix}{k}.gpf">
        <position coord="0,0"/>
        <beam defocus="#0" name="{beam_current_name}" dose="{dose}"/>
        <marker enabled="true" name="{local_mark_name}">
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
string+=f"""      <pattern name="{pattern_name_prefix}{num_patterns}.gpf">
        <position coord="0,0"/>
        <beam defocus="#0" name="{beam_current_name}" dose="{dose}"/>
      </pattern>\n"""
string+= f"""<marker enabled="true" name="{global_mark_name}">
        <markerlist>
          <position coord="{global_marks[0][0]},{global_marks[0][1]}"/>
        </markerlist>
        <markerlist>
          <position coord="{global_marks[1][0]},{global_marks[1][1]}"/>
        </markerlist>
        <markerlist>
          <position coord="{global_marks[2][0]},{global_marks[2][1]}"/>
        </markerlist>
        <markerlist>
          <position coord="{global_marks[3][0]},{global_marks[3][1]}"/>
        </markerlist>
        <markerlist/>
        <markerlist/>
        <markerlist/>
        <markerlist/>
      </marker>
    </exposure>
  </substrate>
</cjob>"""

with open(export_job_name, "w") as f:
    f.write(string)