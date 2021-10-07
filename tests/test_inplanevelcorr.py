"""
Tests for inplanevelcorr.py
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


    def test_velocity_corr_zeroradius(self):
        """
        OOB condition - what happens when the radius is zero
        """


    def test_velocity_corr_extremeradius(self):
        """
        OOB condition - what happens when the radius >= min(m,n)
        """


    def test_velocity_corr_oneradius(self):
        """
        Boundary condition - what happens when the radius = 1
        """


    def test_velocity_corr_maximalradius(self):
        """
        Boundary condition - what happens whin the radius = min(m,n) -1
        """


    def test_velocity_corr_wrongdatadim(self):
        """
        Data condition - process should check for 3 dimensions
        """


    def test_velocity_corr_wrongdepth(self):
        """
        Data condition - third dimension should be length 2
        """


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

    def test__fz(self):
        """
        Base test of the fisher's Z transformation
        """

    def test__fz_neg1(self):
        """
        Base test of the fisher's Z transformation where the value to transform
        is -1
        """

    def test__fz_0(self):
        """
        Base test of the fisher's Z transformation where the value to transform
        is 0
        """

    def test__fz_1(self):
        """
        Base test of the fisher's Z transformation where the value to transform
        is 1
        """

    def test__fz_inv(self):
        """
        Base test of the fisher's Z inverse transformation
        """
        self.assertAlmostEqual(vc._fz_inv(1), (np.e**2 - 1)/(1 + np.e**2))


    def test__fz_inv_neginf(self):
        """
        Base test of the fisher's Z inverse transformation where the value to
        transform is -infinity
        """
        self.assertEqual(vc._fz_inv(-np.inf), -1)


    def test__fz_inv_0(self):
        """
        Base test of the fisher's Z inverse transformation where the value to
        transform is 0
        """
        self.assertEqual(vc._fz_inv(0), 0)


    def test__fz_inv_inf(self):
        """
        Base test of the fisher's Z inverse transformation where the value to
        transform is infinity
        """
        self.assertEqual(vc._fz_inv(np.inf), 1)
