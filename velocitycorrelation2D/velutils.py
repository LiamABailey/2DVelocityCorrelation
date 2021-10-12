"""
Module containing public-facing elements to support the use of the package
"""


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

    new_df = in_df.copy()
    for c in [xcoord_fea, ycoord_fea]:
        new_df[c] = ((new_df[c] - np.min(new_df[c]))/(px_step_size * px_unit_conversion))

    # check for castability to integer
    if np.abs(new_df[[ycoord_fea, xcoord_fea]].values % 1) > TOL:
        raise ValueError("Cannot safely cast scaled values to integers. "
                        "Confirm that step size and px_unit_conversion are correct.")

    new_df[xcoord_fea] = new_df[xcoord_fea].values.astype(np.int64)
    new_df[ycoord_fea] = new_df[ycoord_fea].values.astype(np.int64)
    return new_df
