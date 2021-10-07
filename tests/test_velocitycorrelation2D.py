"""
Tests for velocitycorrelation2D.py
"""

import unittest

import numpy as np

import velocitycorrelation2D as vc


class TestVelocityCorr(unittest.TestCase):

    def test_velocity_corr(self):
        """
        Base test - checks an arbitrary variation
        """


    def test_velocity_corr_negativeradius(self):
        """
        OOB condition - what happens when the radius is less than 0
        """
        radius = -1
        data = np.random_sample((10,10,2,))
        with self.asertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_zeroradius(self):
        """
        OOB condition - what happens when the radius is zero
        """
        radius = 0
        data = np.random_sample((10,10,2,))
        with self.asertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_extremeradius(self):
        """
        OOB condition - what happens when the radius >= min(m,n)
        """
        radius = 10
        data = np.random_sample((10,11,2,))
        with self.asertRaises(ValueError):
            vc.velocity_corr(data, radius)


    def test_velocity_corr_oneradius(self):
        """
        Boundary condition - what happens when the radius = 1
        """
        radius = 1
        data = np.random.sample((10,10,2,))
        _, n_reviewed, n_center_8, n_center_4 = vc.velocity_corr(data, radius)
        # all 100 points have neighbors 1 step away, so all will be reviewed
        self.assertEquals(n_reviewed, 100)
        # none of the points along the boundary will have 8 neighbors
        self.assertEquals(n_center_8, 64)
        # all but the 4 corners will have 4 or more neighbors
        self.assertEquals(n_center_4, 96)


    def test_velocity_corr_maximalradius(self):
        """
        Boundary condition - what happens whin the radius = min(m,n) -1
        """
        radius = 9
        data = np.random.sample((10,10,2))
        _, n_reviewed, n_center_8, n_center_4 = vc.velocity_corr(data,radius)
        # any points with a neighbor at a cardinal direction (+/-9,0) or (0,+/-9) will be reviewed
        # any points with a neighbor at (+/-6, +/-6)
        # this is the edges,
        self.assertEquals(n_reviewed, 72)
        # none of the edge points will have 8 neighbors
        self.assertEquals(n_center_8, 0)
        # none of the edge points will have 4 neighbors)
        self.assertEquals(n_center_4, 0)
        # note, in this case some points around each corner will be compared to
        # 3 other points, but none will be compared to 4


    def test_velocity_corr_wrongdatadim(self):
        """
        Data condition - process should check for 3 dimensions
        """
        radius = 1
        data = np.random_sample((2,))
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


    def test_velocity_corr_nearzero(self):
        """
        Test that the program returns the proper near-zero correlation
        """


    def test_velocity_corr_low(self):
        """
        Test that the program returns the proper low correlation
        """


    def test_velocity_corr_largeradius(self):
        """
        Test that the function works as expected when the radius is large
        relative to the data provided
        """
