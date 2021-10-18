"""
Module containing public-facing elements to support the use of the package
"""
from itertools import product
import numpy as np
import pandas as pd

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
                    step_size,
                    px_unit_conversion = 1,
                    xcoord_fea = 'x [px]',
                     ycoord_fea = 'y [px]'):
    """
    Some scientific applications provide data where vector start points
    are a number of units (often pixels) separated from one another. Data
    must be rescaled such that observations are (potentially) next to one another.

    Adjust positions s.t. min = 0,
    max = (data_max - data_min)/(step_size * px_unit_conversion)

    Args
    ----
        in_df : pd.DataFrame
            The input data

        step_size : int > 0
            The rescaling factor describing the distance between observations
            (in 'pixels')

        px_unit_conversion: float > 0, default 1
            The measurement unit corresponding to the length/width of a
            single pixel

        ycoord_fea : str, default = 'y [px]'
            The x-coordinate column name

        xcoord_fea : str, default = 'x [px]'
            The x-coordinate column name

    Returns
    -------
        pd.DataFrame: The dataframe, with positions rescaled
    """
    TOL = 1e-5

    if step_size <= 0:
        raise ValueError("Step Size must be greater than zero")
    if type(step_size) != int:
        raise TypeError("Step size must be an integer")

    if px_unit_conversion <= 0:
        raise ValueError("Conversion factor must be greater than zero")

    new_df = in_df.copy()
    for c in [xcoord_fea, ycoord_fea]:
        new_df[c] = ((new_df[c] - np.min(new_df[c]))/(step_size * px_unit_conversion))

    # check for castability to integer
    if np.any(np.abs(new_df[[ycoord_fea, xcoord_fea]].values % 1) > TOL):
        raise ValueError("Cannot safely cast scaled values to integers. "
                        "Confirm that step size and px_unit_conversion are correct.")

    new_df[xcoord_fea] = new_df[xcoord_fea].values.astype(np.int64)
    new_df[ycoord_fea] = new_df[ycoord_fea].values.astype(np.int64)
    return new_df
