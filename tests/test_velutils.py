"""
Tests for velutils.py
"""
import os
import unittest

import numpy as np
from numpy.testing import assert_equal
import pandas as pd
from pandas.testing import assert_frame_equal

import velocitycorrelation2D.velutils as u


BASIC_FRAME = pd.DataFrame({
                            'x [px]': [2,3.5,5,6.5],
                            'y [px]': [1,1,2.5,2.5]
                            })
BASIC_RESULT_FRAME = pd.DataFrame({
                            'x [px]': [0,1,2,3],
                            'y [px]': [0,0,1,1]
                            })

class TestGCDFP(unittest.TestCase):

    def test_gcd_fp_int(self):
        """
        Tests of gcd_fp on integers
        """
        cases = [(3,2,1), (4,2,2), (19, 23, 1), (30,36,6)]
        for case in cases:
            with self.subTest(x = case[0], y = case[1]):
                self.assertEqual(u._gcd_fp(case[0], case[1]), case[2])

    def test_gcd_fp_mixed(self):
        """
        Tests of gcd_fp where one input is an integer, and
        the other is a float
        """
        cases = [(0.5, 1, 0.5), (1.0,2,1), (3, 1.9, 0.1), (0.8,2,0.4)]
        for case in cases:
            with self.subTest(x = case[0], y = case[1]):
                self.assertEqual(u._gcd_fp(case[0], case[1], rnd = 10), case[2])


    def test_gcd_fp_float_lt1_large(self):
        """
        Tests of gcd_fp where both values are near, but less than, 1
        """
        cases = [(.98, .96, .02), (0.99, 0.9, 0.09), (0.88, 0.96, 0.08), (0.99999, 0.88888, 0.11111)]
        for case in cases:
            with self.subTest(x = case[0], y = case[1]):
                self.assertEqual(u._gcd_fp(case[0], case[1], rnd = 10), case[2])

    def test_gcd_fp_float_gt0_small(self):
        """
        Tests where the values are near, but greater than, 0
        """
        cases = [(.03, .02, .01 ), (0.0000000075, 0.000000005, 0.0000000025),
                (7.370357806e-05, 7.54096794e-05, 3.4122e-07)]
        for case in cases:
            with self.subTest(x = case[0], y = case[1]):
                self.assertAlmostEqual(u._gcd_fp(case[0], case[1], rnd = 12), case[2], delta = min([case[0],case[1]]) * 0.0001)

    def test_gcd_fp_float_mixed(self):
        """
        Cases where the values provided vary widely
        """
        cases = [(100, 0.0000001, 0.0000001), (0.99999999945, 0.22222221, 0.11111105),
                (0.63, 0.0004, 0.0004)]
        for case in cases:
            with self.subTest(x = case[0], y = case[1]):
                self.assertAlmostEqual(u._gcd_fp(case[0], case[1], rnd = 12), case[2], delta = min([case[0],case[1]]) * 0.0001)


class TestFindConversionFactor(unittest.TestCase):

    def setUp(self):
        self.xcol = 'x [m]'
        self.ycol = 'y [m]'
        self.folder_path = os.path.join(os.path.dirname(__file__), "test_assets", "find_conversion_factor")
        self.file_extension = '.csv'

    def testFindConversionFactorSimple(self):
        """
        Basic tests of FindConversionFactor, where there are few records
        """
        # test assets are indexed 1...n
        n_tests = 1
        test_fnames = [f"basic_{i}{self.file_extension}" for i in range(1, n_tests+1)]
        test_results = pd.read_csv(os.path.join(self.folder_path, "basic_results.csv"))
        for i in range(1, n_tests+1):
            with self.subTest(i = i):
                test_data = pd.read_csv(os.path.join(self.folder_path, test_fnames[i-1]))
                expected = test_results.loc[test_results.test_ix == i, 'expected_value'].values[0]
                result = u.find_conversion_factor(test_data, xcoord_fea = self.xcol, ycoord_fea = self.ycol)
                self.assertEqual(expected, result)


    def testFindConversionFactorNoCommonXYFactor(self):
        """
        Validate error when x-coordinate and y-coordinate errors are
        not the same
        """
        pass


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
        rescaled = u.rescale_positions(BASIC_FRAME, 1.5)
        self.assertFrameEqual(rescaled, BASIC_RESULT_FRAME)


    def test_rescale_conversion_oob(self):
        """
        Assert that conversion factor is greater than zero
        """
        unit_conversion = -0.2
        with self.assertRaises(ValueError):
            u.rescale_positions(BASIC_FRAME, unit_conversion)

    def test_rescale_invalid_conversion(self):
        """
        Assert that error is raised if rescaled positions are not
        safely casstable to integers
        """
        with self.assertRaises(ValueError):
            rescaled = u.rescale_positions(BASIC_FRAME, 1)


    def test_rescale_positions_integers(self):
        """
        Confirm that the position columns are retuned as integer types
        """
        rescaled = u.rescale_positions(BASIC_FRAME, 1.5)
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
            'x [px]': [0,1,0],
            'y [px]': [0,0,1],
            'u [px/frame]': [-0.1,0.0,0.1],
            'v [px/frame]': [-0.1,2.0,0.1]}
        )
        expected_array = np.array([[[-0.1,-0.1],[0,2]],[[0.1,0.1],[np.nan,np.nan]]])
        result = u.square_input(df)
