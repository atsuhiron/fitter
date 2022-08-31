from typing import Tuple

import numpy as np
import scipy.optimize as so

from functions.gaussian import Gauss
import function_list
import utils.sample_generator as sample_gen
from fit import Fit
from grapihx.cui.cui_gfx import CuiGfx


def mlr(xy: Tuple[np.ndarray, np.ndarray], a: float, b: float, c: float) -> float:
    x, y = xy
    return x * a + y * b + c


def slr(x: np.ndarray, a: float, b: float) -> float:
    return x * a + b


if __name__ == "__main__":
    # NUM = 65
    # xx = np.linspace(0, 4, NUM)
    # yy = np.linspace(0, 4, NUM)
    # aa = 3
    # bb = -0.5
    # cc = 1
    #
    # zz = slr(xx, aa, bb) + (np.random.random(NUM) - 0.5)
    # xx2, yy2 = np.meshgrid(np.linspace(0, 4, NUM), np.linspace(0, 4, NUM))
    # zz2 = mlr((xx2, yy2), aa, bb, cc)
    # raveled = np.array([xx2.ravel(), yy2.ravel()])
    # opt_para, opt_cov = so.curve_fit(mlr, raveled, np.ravel(zz2), p0=[1.0, 1.0, 1.0])
    # print(opt_para)
    # print(opt_cov)
    #
    xm, ym, sample_data = sample_gen.gen_2d_gaussian()
    fl = function_list.FunctionList()
    fl.add_func(Gauss)
    fitter = Fit(sample_data, fl, (xm, ym))
    # init_param = [1.0, 1.0, 0.0, 1.0, 1.0, 0.2]
    # raveled_mesh = tuple(np.array([xm.ravel(), ym.ravel()]))
    # opt_para, opt_cov = so.curve_fit(fl.f, raveled_mesh, sample_data.ravel(), init_param, bounds=fl.get_bounds())
    # print(opt_para)
    # print(opt_cov)

    cui = CuiGfx(fitter, sample_data)
    cui.start()
