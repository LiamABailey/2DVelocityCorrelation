"""
Tests for velutils.py
"""
import pandas as pd
import velocitycorrelation2d.velutils as u

class TestRescalePositions(unittest.TestCase):

    def test_rescale_positions(self):
        """
        basic test of rescaling
        """


    def test_rescale_step_size_oob(self):
        """
        Assert that error is raised if step size isn't greater than zero
        """


    def test_rescale_step_size_int(self):
        """
        Assert that step_size is an integer
        """


    def test_rescale_conversion_oob(self):
        """
        Assert that conversion factor is greater than zero
        """


    def test_rescale_invalid_conversion(self):
        """
        Assert that error is raised if rescaled positions are not
        safely casstable to integers
        """
