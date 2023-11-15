import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

from rayoptics.environment import *

use_material = False

from p66_fraunhofer_objective_lens import *


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
        self.objectDistance = (lambda: np.inf if OD == 'infinite' else OD)()
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



