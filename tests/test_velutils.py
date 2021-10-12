"""
Tests for velutils.py
"""
import pandas as pd
from pandas.testing import assert_frame_equal
import unittest

import velocitycorrelation2D.velutils as u


BASIC_FRAME = pd.DataFrame({
                            'x [px]': [2,3.5,5,6.5],
                            'y [px]': [1,1,2.5,2.5]
                            })

BASIC_RESULT_FRAME = pd.DataFrame({
                            'x [px]': [0,1,2,3],
                            'y [px]': [0,0,1,1]
                            })

class TestRescalePositions(unittest.TestCase):

    def assertFrameEqual(self, a, b, msg = ""):
        try:
            assert_frame_equal(a,b)
        except AssertionError as e:
            raise self.failureException(msg)

    def test_rescale_positions(self):
        """
        basic test of rescaling
        """
        rescaled = u.rescale_positions(BASIC_FRAME, 3, 0.5)
        self.assertFrameEqual(rescaled, BASIC_RESULT_FRAME)


    def test_rescale_step_size_oob(self):
        """
        Assert that error is raised if step size isn't greater than zero
        """
        step_size = 0
        with self.assertRaises(ValueError):
            u.rescale_positions(BASIC_FRAME, step_size, 0.5)

    def test_rescale_step_size_int(self):
        """
        Assert that step_size is an integer
        """
        step_size = 1.3
        with self.assertRaises(TypeError):
            u.rescale_positions(BASIC_FRAME, step_size, 0.5)


    def test_rescale_conversion_oob(self):
        """
        Assert that conversion factor is greater than zero
        """
        px_unit_conversion = -0.2
        with self.assertRaises(ValueError):
            u.rescale_positions(BASIC_FRAME, 3, px_unit_conversion)

    def test_rescale_invalid_conversion(self):
        """
        Assert that error is raised if rescaled positions are not
        safely casstable to integers
        """
        with self.assertRaises(ValueError):
            rescaled = u.rescale_positions(BASIC_FRAME, 1, 1)
