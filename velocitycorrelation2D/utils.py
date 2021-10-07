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
            The x-coordinate column name

        ycoord_fea : str, default = 'y [px]'
            The y-coordinate column name

        xvel_fea : str, default = 'u [px/frame]'
            The x-velocity column name

        yvel_fea : str, default = 'v [px/frame]'
            The y-velocity column name

    Returns
    -------
        np.ndarray : 3D matrix as desribed above. Size (n,m,2) with dtype
            np.float64

    """
