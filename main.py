from typing import Tuple
import numpy as np
import scipy.optimize as so


def mlr(xy: Tuple[np.ndarray, np.ndarray], a: float, b: float, c: float) -> float:
    x, y = xy
    return x * a + y * b + c


def slr(x: np.ndarray, a: float, b: float) -> float:
    return x * a + b


if __name__ == "__main__":
    NUM = 65
    xx = np.linspace(0, 4, NUM)
    yy = np.linspace(0, 4, NUM)
    aa = 3
    bb = -0.5
    cc = 1

    zz = slr(xx, aa, bb) + (np.random.random(NUM) - 0.5)

    xx2, yy2 = np.meshgrid(np.linspace(0, 4, NUM), np.linspace(0, 4, NUM))
    zz2 = mlr((xx2, yy2), aa, bb, cc)

    raveled = np.array([xx2.ravel(), yy2.ravel()])
    opt_para, opt_cov = so.curve_fit(mlr, raveled, np.ravel(zz2))
    print(opt_para)
    print(opt_cov)


