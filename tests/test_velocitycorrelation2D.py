"""
Tests for correlation.py
"""

import unittest

import numpy as np

import velocitycorrelation2D.correlation as vc


class TestVelocityCorr(unittest.TestCase):

    def test_velocity_corr_negativeradius(self):
        """
        OOB condition - what happens when the radius is less than 0
        """
        radius = -1
        data = np.random.sample((10,10,2,))
        with self.assertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_zeroradius(self):
        """
        OOB condition - what happens when the radius is zero
        """
        radius = 0
        data = np.random.sample((10,10,2,))
        with self.assertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_extremeradius(self):
        """
        OOB condition - what happens when the radius >= min(m,n)
        """
        radius = 10
        data = np.random.sample((10,11,2,))
        with self.assertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_oneradius(self):
        """
        Boundary condition - what happens when the radius = 1
        """
        radius = 1
        data = np.random.sample((10,10,2,))
        _, n_reviewed, n_center_4, n_center_8 = vc.velocity_corr(data, radius)
        # all 100 points have neighbors 1 step away, so all will be reviewed
        self.assertEqual(n_reviewed, 100)
        # none of the points along the boundary will have 8 neighbors
        self.assertEqual(n_center_4, 96)
        # all but the 4 corners will have 4 or more neighbors
        self.assertEqual(n_center_8, 64)


    def test_velocity_corr_maximalradius(self):
        """
        Boundary condition - what happens when the radius = min(m,n) -1
        """
        radius = 9
        data = np.random.sample((10,10,2))
        _, n_reviewed, n_center_4, n_center_8 = vc.velocity_corr(data,radius)
        # any points with a neighbor at a cardinal direction (+/-9,0) or (0,+/-9) will be reviewed
        # any points with a neighbor at (+/-6, +/-6)
        # this is the edges,
        self.assertEqual(n_reviewed, 72)
        # none of the edge points will have 8 neighbors
        self.assertEqual(n_center_4, 0)
        # none of the edge points will have 4 neighbors)
        self.assertEqual(n_center_8, 0)
        # note, in this case some points around each corner will be compared to
        # 3 other points, but none will be compared to 4


    def test_velocity_corr_wrongdatadim(self):
        """
        Data condition - process should check for 3 dimensions
        """
        radius = 1
        data = np.random.sample((2,))
        with self.assertRaises(TypeError):
            vc.velocity_corr(data, radius)



    def test_velocity_corr_wrongdepth(self):
        """
        Data condition - third dimension should be length 2
        """
        radius = 1
        data = np.random.sample((5,5,1,))
        with self.assertRaises(TypeError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_high(self):
        """
        Test that the program returns the proper high correlation
        """
        radius = 1
        data = _create_unit_spiral_array(5)
        corr, _, _, _ = vc.velocity_corr(data, radius)
        self.assertGreater(corr, 0.9)


    def test_velocity_corr_nearzero(self):
        """
        Test that the program returns the proper near-zero correlation
        """
        radius = 7
        np.random.seed(123)
        data = _create_unit_spiral_array(8,2)

        corr, _, _, _ = vc.velocity_corr(data, radius)
        self.assertTrue(-0.1 < corr < 0.1, msg = f"Correlation {corr} is not between -0.1 and 0.1")


    def test_velocity_corr_low(self):
        """
        Test that the program returns the proper low correlation
        """
        radius = 9
        t = np.ones((10,10))
        x = np.triu(t)
        y = -1 * np.tril(t)
        z = x + y
        data = np.zeros((10,10,2))
        data[:,:,0] = z
        data[:,:,1] = z
        corr, _, _, _, = vc.velocity_corr(data, radius)
        self.assertLess(corr, -0.5)


def _create_unit_spiral_array(radius, noise = 0 ):
    """
    Creates a collection of velocity vectors that form a spiral centered around
    the middle of the matrix, where the final array shape is [(2*radius + 1), (2*radius + 1),2]

    Args
    ----
        radius : int > 0

        noise : float >= 0; default 0
            The standard deviation of the normal distribution applied for randomness

    Returns
    -------
        np.array : The matrix containing spiral motion
    """
    dia = radius * 2 + 1
    pos= np.zeros((dia, dia, 2))
    pos[:,:,0] = np.broadcast_to(np.array(range(-radius, radius+1)), (dia,dia))
    pos[:,:,1] = -1 * np.repeat(np.array([range(-radius, radius+1)]).T, dia, axis = 1)
    spr = np.zeros_like(pos)
    spr[:,:,0] = np.cos(np.arctan2(pos[:,:,1],pos[:,:,0]) - (np.pi/2))
    spr[:,:,1] = np.sin(np.arctan2(pos[:,:,1],pos[:,:,0]) - (np.pi/2))
    if noise != 0:
        spr[:,:,0] += np.random.normal(0, scale = noise,size = spr.shape[:-1])
        spr[:,:,1] += np.random.normal(0, scale = noise,size = spr.shape[:-1])
    spr[radius,radius] = [0,0]
    return spr
