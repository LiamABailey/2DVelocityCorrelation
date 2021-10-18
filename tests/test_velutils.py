"""
Tests for velutils.py
"""
import numpy as np
from numpy.testing import assert_equal
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


    def test_rescale_positions_integers(self):
        """
        Confirm that the position columns are retuned as integer types
        """
        rescaled = u.rescale_positions(BASIC_FRAME, 3, 0.5)
        self.assertTrue(pd.api.types.is_integer_dtype(rescaled['x [px]']))
        self.assertTrue(pd.api.types.is_integer_dtype(rescaled['y [px]']))


class TestSquareInput(unittest.TestCase):

    def assertArrayEqual(self, a, b, msg = ""):
        try:
            assert_equal(a,b)
        except AssertionError as e:
            raise self.failureException(msg)


    def test_square_input(self):
        """
        basic test of square_input
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        expected_array = np.array([[[-0.1,-0.1],[0,2]],[[0.1,0.1],[0.2,0.3]]])
        self.assertArrayEqual(u.square_input(df), expected_array)


    def test_square_input_xcoord_col_ne(self):
        """
        test where provided xcoord_fea is not in the data frame
        """
        df = pd.DataFrame({
            'y [px]': [0,1,2],
            'u [px/frame]': [0.5,0.3,0.2],
            'v [px/frame]': [-0.2,.8, 0]
        })
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_ycoord_col_ne(self):
        """
        test where provided ycoord_fea is not in the data frame
        """
        df = pd.DataFrame({
            'x [px]': [1,2,3],
            'u [px/frame]': [0.5,0.3,0.2],
            'v [px/frame]': [-0.2,.8, 0]
        })
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_xvel_col_ne(self):
        """
        test where provided xvel_fea is not in the data frame
        """
        df = pd.DataFrame({
            'x [px]': [1,2,3],
            'y [px]': [0,1,2],
            'v [px/frame]': [-0.2,.8, 0]
        })
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_yvel_col_ne(self):
        """
        test where provided yvel_fea is not in the data frame
        """
        df = pd.DataFrame({
            'x [px]': [1,2,3],
            'y [px]': [0,1,2],
            'u [px/frame]': [0.5,0.3,0.2]
        })
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_extra_columns(self):
        """
        test where extra columns are provided (shouldn't impact result)
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        expected_array = np.array([[[-0.1,-0.1],[0,2]],[[0.1,0.1],[0.2,0.3]]])

        self.assertArrayEqual(u.square_input(df), expected_array)


    def test_square_input_vel_nas(self):
        """
        Test to confirm that NA velocity values are retained
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,pd.NA,0.2],
            'v [px/frame]': [-0.1,2.0,np.nan,0.3]}
        )
        expected_array = np.array([[[-0.1,-0.1],[0,2]],[[np.nan,np.nan],[0.2,0.3]]])

        self.assertArrayEqual(u.square_input(df), expected_array)


    def test_square_input_xcoord_nas(self):
        """
        Confirms that NAs in the x-coordinate column leads to a raised error
        """
        df = pd.DataFrame({
            'x [px]': [np.nan,1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_ycoord_nas(self):
        """
        Confirms that NAs in the y-coordinate column leads to a raised error
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,pd.NA,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)


    def test_square_input_xcoord_nonint(self):
        """
        Asserts error raised if x-coord column isn't integer-based
        """
        df = pd.DataFrame({
            'x [px]': [0,.1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)

    def test_square_input_ycoord_nonint(self):
        """
        Asserts error raised if y-coord column isn't integer-based
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,1,1.5],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)

    def test_square_input_xcoord_negative(self):
        """
        Asserts error raised if x-coord column contains negatives
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,-1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)

    def test_square_input_ycoord_negative(self):
        """
        Asserts error raised if y-coord contains negatives
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,-1,1],
            'u [px/frame]': [-0.1,0.0,0.1,0.2],
            'v [px/frame]': [-0.1,2.0,0.1,0.3]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)

    def test_square_input_fill_not_provided(self):
        """
        Checks for NAs in positions not provided in the dataframe.
        """
        df = pd.DataFrame({
            'x [px]': [0,1,0,1],
            'y [px]': [0,0,1,1],
            'u [px/frame]': [-0.1,0.0,0.1,np.nan],
            'v [px/frame]': [-0.1,2.0,0.1,np.nan]}
        )
        with self.assertRaises(ValueError):
            u.square_input(df)
