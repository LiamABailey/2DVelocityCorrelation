"""
Module containing core methods for performing the measure of velocity correlation
 as a function of in-plane distance
"""


def velocity_corr(data, radius_size):
    """
    Following the spatial correlation algorithm in Dombrowski et al. (2004),
    calculate the spatial correlation (w/ additional metastatistics) for
    the radius_size. Observes at 8 orientations at a pi/4 step.

    Args
    ----
        data : np.ndarray
            The data of interest, formatted as (n,m,2), where
            [:,:,0] are the X velocities, and [:,:,1] are the Y velocities.

        radius_size : 0 < int < min(n,m)
            The size of the radius, in x/y grid coordinates

    Returns
    -------
        float : the correlation score

        int : the number of centers reviewed

        int : the number of centers w/ 8 eligible surrounding data points

        int : the number of centers w/ 4+ eligible surrounding data points

    """
