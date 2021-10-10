"""
Module containing core methods for performing the measure of velocity correlation
 as a function of in-plane distance
"""
import numpy as np

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

        int : the number of centers reviewed (One or more data points eligible
            at radius_size distance)

        int : the number of centers w/ 4+ eligible surrounding data points

        int : the number of centers w/ 8 eligible surrounding data points

    """
    if not _validate_data_format(data):
        raise TypeError("Data is not in the proper [n,m,2] shape")

    if radius_size < 1:
        raise ValueError("Radius must be 1 or greater")
    elif radius_size >= np.min(data.shape[:-1]):
        raise ValueError("Radius must be less than min(n,m)")

    #track the number of samples per centroids
    point_samples = np.zeros_like(data[:,:,0])

    # calculate <v^2)_x via einstein's noation to create the
    # dot product of the x and y vectors at each point
    vxx = np.nanmean(np.einsum('ijk,ijk->ij',data,data))
    # calculate <v>_x^2 - average, then dot
    d = np.nanmean(data, axis = (0,1))
    vx2 = np.dot(d,d)

    # pre-compute the location of observed points relative to the centroids
    UNITX = np.array([np.cos(x) for x in np.arange(0,2*np.pi,np.pi/4)])
    UNITY = np.array([np.sin(x) for x in np.arange(0,2*np.pi,np.pi/4)])
    xrad = np.round(UNITX * radius_size).astype(np.int64)
    yrad = np.round(UNITY * radius_size).astype(np.int64)

    # we collect the correlation score for each orientation
    rcorr = []

    for (x_or, y_or) in zip(xrad, yrad):
        # pad the data with NaNs to handle OOB
        y_ora, x_ora = np.abs(y_or), np.abs(x_or)
        data_p = np.pad(data, tuple((v,)*2 for v in (y_ora, x_ora, 0)), constant_values = np.nan)
        # we 'shift' the data over by the x and y lengths of the radius of obseravation
        _data_r_x = np.roll(data_p, x_or, axis = 1)
        ys, xs = _data_r_x.shape[:2]
        # remove padding as we roll in the y dimension
        data_r = np.roll(_data_r_x, y_or, axis = 0)[y_ora:ys-y_ora, x_ora:xs-x_ora,:]
        # take v(x + r) * v(x)
        vxr = np.einsum('ijk,ijk->ij',data,data_r)
        # record where a comparison was made
        point_samples[np.where(~np.isnan(vxr))] += 1
        # calculate the corelation score and append
        rcorr.append((np.nanmean(vxr) - vx2)/(vxx - vx2))

    return np.nanmean(rcorr),\
        len(np.where(point_samples > 0)[0]),\
        len(np.where(point_samples >= 4)[0]),\
        len(np.where(point_samples == 8)[0]),


def _validate_data_format(data):
    """
    Raises an error if the matrix provided is not of shape [n,m,2]

    Args
    ----
        data : np.ndarray
            The data of interest, formatted as (n,m,2)

    Returns
    -------
        bool : True if format is valid, False otherwise
    """
    return (data.ndim == 3 and data.shape[2] == 2)
