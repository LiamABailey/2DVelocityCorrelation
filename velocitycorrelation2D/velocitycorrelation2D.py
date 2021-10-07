"""
Module containing core methods for performing the measure of velocity correlation
 as a function of in-plane distance
"""
import numpy as np

def _fz(v):
    """
    Applies Fisher's Z transform to the provided value

    See "Averaging Correlations: Expected Values and Bias in Combined Pearson
    rs and Fisher's z Transformations", Corey et al, for jusification for using
    the transform for averaging correlations

    Args
    ----
        v : float or np.ndarray of floats
            The correlation value

    Returns
    -------
        float : the transformed value (z-score)
    """
    return np.arctanh(v)

def _fz_inv(z):
    """
    Applies the inverse of Fisher's Z transform

    Args
    ----
        z : float or np.ndarray of floats
            The Z score to transform

    Returns
    -------
        float : the transformed value (fisher's r)
    """
    return np.tanh(z)


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
