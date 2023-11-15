import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

from rayoptics.environment import *

use_material = False

description = '\
Source Modern Lens Design, Smith 1992 \
page 51 \
F/4.5 25.2deg TRIPLET US 1,987,878/1935 Schneider \
'

EFL =   98.56   # Effective focal length
BFL =   81.43   # Back focal length
NA =    -0.1127 # Numerical aperture
GIH =   46.33   # Image height
HFOV=   25.17   # Half field in degrees
PTZ =   -2.831  # Petzval radius as fraction of EFL
VL =    23.43   # Vertex length from first to last surface
OD =    np.inf   # Object distance

radius = [26.160,
          1201.700,
        -83.460,
          25.670,
          0,
          302.610,
          -54.790
          ]

thickness = [4.916,
             3.988,
             1.038,
             4.000,
             6.925,
             2.567,
             81.433]

material = ['LAK12',
            'air',
            'SF2',
            'air',
            'air',
            'LAK22',
            'air']

index = [1.678,
         1,
         1.648,
         1,
         1,
         1.651,
         1
         ]

Vno = [55.2,
       0,
       33.8,
       0,
       0,
       55.9,
       0]

sa = [11.7,
      11.7,
      10.2,
      10.2,
      9.2,
      10.3,
      10.3]

apertureIndex = 4

class Lens:
    def __init__(self):
        self.description = description
        self.radius = radius
        self.thickness = thickness
        self.pos = ([0.] + thickness)[:-1]
        self.material = material
        self.index = index
        self.Vno = Vno
        self.sa = sa
        self.apertureIndex = apertureIndex
        self.apertureDiameter = self.sa[apertureIndex]*2
        self.objectDistance = OD
        self.diagonal = GIH*2
        self.hfov = HFOV

    def __str__(self):
        pass

    def __repr__(self):
        pass


if __name__ == "__main__":
    lens = Lens()

    opm = OpticalModel()

    sm = opm['seq_model']
    osp = opm['optical_spec']
    pm = opm['parax_model']
    em = opm['ele_model']
    pt = opm['part_tree']
    ar = opm['analysis_results']

    osp['pupil'] = PupilSpec(osp, key=['object', 'pupil'], value=lens.apertureDiameter)
    osp['wvls'] = WvlSpec([('F', 0.5), (587.5618, 1.0), ('C', 0.5)], ref_wl=1)
    osp['fov'] = FieldSpec(osp, key=['object', 'angle'], value=lens.hfov, flds=[0., 0.707, 1.], is_relative=True)

    opm.radius_mode = True

    sm.gaps[0].thi=1e10

    if use_material:
        for i, (rad, thi, mat) in enumerate(zip(lens.radius, lens.thickness, lens.material)):
            if mat == 'air':
                sm.add_surface([rad, thi])
            else:
                sm.add_surface([rad, thi, mat, 'Schott'])
            if i == lens.apertureIndex:
                sm.set_stop()
    else:
        for i, (rad, thi, ind) in enumerate(zip(lens.radius, lens.thickness, lens.index)):
            sm.add_surface([rad, thi, ind])
            if i == lens.apertureIndex:
                sm.set_stop()


    opm.update_model()
    isdark = False
    layout_plt = plt.figure(FigureClass=InteractiveLayout, opt_model=opm, is_dark=isdark)
    layout_plt.plot()
    layout_plt.show()

    abr_plt = plt.figure(FigureClass=RayFanFigure, opt_model=opm, data_type='Ray', scale_type=Fit.All_Same, is_dark=isdark)
    abr_plt.plot()
    abr_plt.show()

    pm.first_order_data()



