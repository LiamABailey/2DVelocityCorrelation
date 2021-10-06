"""
Tests for inplanevelcorr.py
"""

import unittest
import velocitycorrelation2d.inplanevelcorr as vc


class TestVelocityCorr(unittest.TestCase):

    def test_velocity_corr(self):
        """
        Base test - checks
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
