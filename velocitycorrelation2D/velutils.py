"""
Module containing public-facing elements to support the use of the package
"""
from itertools import product

import numpy as np
import pandas as pd


def _gcd_fp(x, y, rtol = 1e-05, atol = 1e-10, rnd = -1):
    """
    Find the gcd to two floating point numbers, up to a tolerance,
    via a modified Euclid's algorithm

    Args
    ----
        x, y: float
            The floating point numbers

        rtol: float, default = 1e-05
            The relative tolerance

        atol: float, default = 1e07
            The absolute tolerance

        rnd: int, default = -1,
            The level of rounding applied to the output. provide a natural
            number to activate.

    Returns
    -------
        float : gcd(x,y)

    """
    # need the minimum to define tolerance
    m = min(abs(x), abs(y))
    while abs(y) > (rtol * m + atol):
        x, y = y, x % y
    if rnd > 0:
        x = round(x, rnd)
    return x


def find_conversion_factor(in_df, xcoord_fea='x [px]', ycoord_fea='y [px]'):
    """
    Identifies the conversion factor such that the distance between observations
    in the grid is +/-1 for the x and y coordinates. Requires the y scaling
    to be the same as the x scaling

    Args
    ----
        in_df : pd.DataFrame
            The input data

        xcoord_fea : str, default = 'x [px]'
            The x-coordinate column name. Can only contain non-negative integer
            values.

        ycoord_fea : str, default = 'y [px]'
            The y-coordinate column name. Can only contain non-negative integer
            values.

    Returns
    -------
        float : the conversion factor
    """

    coord_scales = {
        xcoord_fea: -1,
        ycoord_fea: -1
    }
    # find gcd for x-coord, y_coord
    for crd in coord_scales.keys():
        coord_vals = in_df[crd].values - in_df[crd].values.min()
        candidate_gcf = _gcd_fp(coord_vals[0], coord_vals[1], rnd = 12)
        # we can repeatedly apply the gcd finding method to find the
        # shared gcd
        for ix in range(2, len(coord_vals)):
            candidate_gcf = _gcd_fp(candidate_gcf, coord_vals[ix], rnd = 12)
        coord_scales[crd] = candidate_gcf
    # require scales to be equal for both parts of the coordinate system
    if coord_scales[xcoord_fea] != coord_scales[ycoord_fea]:
        raise ValueError(("X and Y coordinates must be on same scale"
            f", found {coord_scales[xcoord_fea]} and {coord_scales[ycoord_fea]}"))

    return coord_scales[xcoord_fea]


def square_input(in_df,xcoord_fea='x [px]',
                        ycoord_fea='y [px]',
                        xvel_fea='u [px/frame]',
                        yvel_fea='v [px/frame]'):
    """
    Given an input pandas data frame of the format:
        [xcoord_fea int,ycoord_fea int ,xvel_fea float,yvel_fea float]

    creates a 3D matrix of dimension <max(ycoord),max(xcoord),2>, where the
    first panel of the 3rd dimension is the X velocity, and the second panel
    is the Y velocity.

    Any matrix elements without corresponding data frame entries are NaN.

    Args
    ----
        in_df : pd.DataFrame
            The input data

        xcoord_fea : str, default = 'x [px]'
            The x-coordinate column name. Can only contain non-negative integer
            values.

        ycoord_fea : str, default = 'y [px]'
            The y-coordinate column name. Can only contain non-negative integer
            values.

        xvel_fea : str, default = 'u [px/frame]'
            The x-velocity column name

        yvel_fea : str, default = 'v [px/frame]'
            The y-velocity column name

    Returns
    -------
        np.ndarray : 3D matrix as desribed above. Size (n,m,2) with dtype
            np.float64

    """
    # from numpy dtype.kind, signed and unsigned integer codes
    ITYPES = ['i','u']
    if not set([xcoord_fea, ycoord_fea, xvel_fea, yvel_fea]) <= set(in_df.columns):
        raise ValueError("DataFrame provided must contain all four columns")
    if (in_df[xcoord_fea] < 0).any() or (in_df[ycoord_fea] < 0).any():
        raise ValueError("Coordinate column values must be non-negative")
    if in_df[xcoord_fea].dtype.kind not in ITYPES:
        raise ValueError("X-coordinate column must be an integer type")
    if in_df[ycoord_fea].dtype.kind not in ITYPES:
        raise ValueError("Y-coordinate column must be an integer type ")

    #replace any pd.NA with np.nan
    in_df = in_df.replace({pd.NA: np.nan})

    max_x = np.max(in_df[xcoord_fea])
    max_y = np.max(in_df[ycoord_fea])
    #expand the pandas dataframe
    exp_pos = pd.DataFrame(
        list(product(list(range(max_x+1)),list(range(max_y+1)))),
        columns = [xcoord_fea, ycoord_fea]
    )
    exp_in_df = exp_pos.merge(right = in_df, how = 'left', on = [xcoord_fea, ycoord_fea])
    x_vel = exp_in_df.sort_values([ycoord_fea, xcoord_fea]).drop(yvel_fea, axis=1)\
                .pivot(index = ycoord_fea, columns = xcoord_fea, values = xvel_fea)\
                .sort_index()
    y_vel = exp_in_df.sort_values([ycoord_fea, xcoord_fea]).drop(xvel_fea, axis=1)\
                .pivot(index = ycoord_fea, columns = xcoord_fea, values = yvel_fea)\
                .sort_index()

    #require columns in order
    try:
        assert list(x_vel.columns) == list(y_vel.columns)
        assert list(x_vel.index) == list(x_vel.index)
    except AssertionError as e:
        msg = ('Unable to coerce input to 3D array: X-velocity and Y-velocity '
                'not unstacked consistently')
        raise AssertionError(msg)

    return np.dstack([x_vel.values, y_vel.values])


def rescale_positions(in_df,
                    conversion_factor = 1,
                    xcoord_fea = 'x [px]',
                     ycoord_fea = 'y [px]'):
    """
    Some scientific applications provide data where vector start points
    are a number of units (often pixels) separated from one another. Data
    must be rescaled such that observations are (potentially) next to one another.

    Adjust positions s.t. min = 0,
    max = (data_max - data_min)/(step_size * conversion_factor)

    Args
    ----
        in_df : pd.DataFrame
            The input data

        conversion_factor: float > 0, default 1
            The conversion factor s.t. the grid basis is [1,1]

        ycoord_fea : str, default = 'y [px]'
            The x-coordinate column name

        xcoord_fea : str, default = 'x [px]'
            The x-coordinate column name

    Returns
    -------
        pd.DataFrame: The dataframe, with positions rescaled
    """
    TOL = 1e-5

    if conversion_factor <= 0:
        raise ValueError("Conversion factor must be greater than zero")

    new_df = in_df.copy()
    for c in [xcoord_fea, ycoord_fea]:
        new_df[c] = ((new_df[c] - np.min(new_df[c]))/( conversion_factor))

    # check for castability to integer
    if np.any(np.abs(new_df[[ycoord_fea, xcoord_fea]].values % 1) > TOL):
        raise ValueError("Cannot safely cast scaled values to integers. "
                        "Confirm that step size and conversion_factor are correct.")

    new_df[xcoord_fea] = new_df[xcoord_fea].values.astype(np.int64)
    new_df[ycoord_fea] = new_df[ycoord_fea].values.astype(np.int64)
    return new_df
