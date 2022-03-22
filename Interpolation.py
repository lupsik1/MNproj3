import numpy as np


def lagrange_interpolation_polynomial_value(x, y, xp):
    # dla wektorów x oraz y zwraca interpolowoaną wartość yp dla zadanego xp
    # x = array, y = array, xp = int/float/double etc.
    m = len(x)
    n = m - 1

    yp = 0
    for i in range(n + 1):
        p = 1
        for j in range(n + 1):
            if j != i:
                p *= (xp - x[j]) / (x[i] - x[j])
        yp += y[i] * p
    return yp


def interpolate_using_lagrange(x, y, n):
    interpolated_values = []
    x_int = np.linspace(0, x[len(x) - 1], num=n)  # x-values for the interpolated result
    for i in range(n):
        interpolated_values.append(lagrange_interpolation_polynomial_value(x, y, x_int[i]))

    return interpolated_values


def interpolate_using_splines(x, y, n):
    y_int = []  # x-values for the interpolated result
    x_int = []
    x = np.array(x)
    y = np.array(y)
    org_range = len(x)
    # sx = three x values for the subgrange, sy = three y values for the subrange
    for i in range(0, org_range, 3):
        sx = x[i:i + 3]
        sy = y[i:i + 3]
        coeffs = get_spline_coefficients(sx, sy)

        int_sx = np.linspace(sx[0], sx[2], 2*n)
        for j in range(n):
            val = get_value_from_coeffs(coeffs, sx, int_sx[j])
            y_int.append(val)
            x_int.append(int_sx[j])
        for j in range(n, 2 * n):
            val = get_value_from_coeffs(coeffs, sx, int_sx[j], first_subrange=False)
            y_int.append(val)
            x_int.append(int_sx[j])

    return x_int,y_int


def get_spline_coefficients(x, y):
    # len(x) and len(y) must be equal 3, failing to meet this requirement means i probably eff'd up
    # returns coefficients a0...d0, a1...d1
    if len(x) != 3 or len(y) != 3:
        print("Incorrect input data")
        return

    # define matrix parameters
    h = x[1] - x[0]  # assuming h is const between variables (hint: it should be)

    # generate the coeff.(?) matrix
    a = np.matrix([[1, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, 0, 0, 0],
                   [1, h, h ** 2, h ** 3, 0, 0, 0, 0],
                   [0, 0, 0, 0, 1, h, h ** 2, h ** 3],
                   [0, 1, 2 * h, 3 * h ** 2, 0, -1, 0, 0],
                   [0, 0, 2, 6 * h, 0, 0, -2, 0],
                   [0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 2, 6 * h]])

    # value vector
    b = np.atleast_2d(np.matrix([y[0], y[1], y[1], y[2], 0, 0, 0, 0])).transpose()

    x = np.array(np.linalg.solve(a, b))
    return x


def get_value_from_coeffs(coeffs, x, xp, first_subrange=True):
    a0, b0, c0, d0, a1, b1, c1, d1 = coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4], coeffs[5], coeffs[6], \
                                     coeffs[7]

    fx = 0
    if first_subrange:
        return float(a0 + b0 * (xp - x[0]) + c0 * ((xp - x[0]) ** 2) + d0 * ((xp - x[0]) ** 3))
    else:
        return float(a1 + b1 * (xp - x[1]) + c1 * ((xp - x[1]) ** 2) + d1 * ((xp - x[1]) ** 3))
