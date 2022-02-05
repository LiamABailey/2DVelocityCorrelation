# 2DVelocityCorrelation

Implementation of the velocity correlation algorithm used in 'Self-concentration and Large-Scale Coherence in Bacterial Dynamics', Dombrowski et al; 'Cytoplasmic streaming in Drosophilia oocytes with kinesin activity and correlates with the microtubule cytoskeleton architecture', Ganguly et al.

Core function `square_input` is available in `velocitycorrelation2D`, other functions to format the data can be found in `velocitycorrelation2D.velutils`

`import velocitycorrelation2D as vd`  
`from velocitycorrelaction2D import velutils`


## Velocity Correlation as a Function of In-Plane Distance

Domrowski et al. proposes the following algorithm to compute velocity correlation over a collection of velocity vectors:
<p align="center">
  <img src = "READMEAssets\correlation_eq.png" alt="I(r_{||}) = \frac{\langle v(x_{||}+r_{||})\cdot v(x_{||})\rangle_x - \langle v \rangle^{2}_x}{\langle v^2\rangle_x - \langle v \rangle^{2}_x}"/>
</p>

Where:
 - x_|| is the point (x,y)
 - r_|| is the in-plane distance
 - v(x_||) is the velocity at point (x,y)

This correlation is averaged across an unspecified number of orientations - this implementation reviews 8 orientations, each separated by 45°, to measure the correlation of velocities across a given distance r_||.

## Processing via the command line using `calc_spiral_corr.py`

A script, `calc_spiral_corr.py` , has been written to support the calculation of the radius measure against tabular data. This process takes a single .csv as input (describing velocity in one frame), and returns a single .csv as output (describing the correlation across the desired radii). It supports a variety of inputs to configure the process, allowing for control over the measurement radii, and variations in file structure. Results are returned with respect to the radius size, where a radius unit of 1 is equal to the minimum distance between any two points in the X or Y coordinate spaces. Note that scales in the X and Y coordinate spaces are required to be equal, and that the program automatically attempts to identify these scales.


The help text (which can be recovered by the -h flag, is shown below).

    usage: calc_spiral_corr.py [-h] [--ds data_start_row_ix] [--rmin RMIN] [--rmax RMAX] [--rstep RSTEP]
                               [--xpfea XPFEA] [--ypfea YPFEA] [--xvfea XVFEA] [--yvfea YVFEA]
                               input output

    calc_spiral_corr.py: a utility for calculating spiraling velocity correlation. See below for input argument definitions.

    positional arguments:
      input                 The fully specified path to the input file (.csv)
      output                The fully speicified path to the output file (.csv)

    optional arguments:
      -h, --help            show this help message and exit
      --ds data_start_row_ix
                            The row in the input .csv containing the column headers, indexed from zero. Default = 0
      --rmin RMIN           The minimum radius size (where a single unit is the minimum distance between any two points in the X or Y coordinate space) to observe. Default = 1
      --rmax RMAX           The maximum radius size (where a single unit is the minimum distance between any two points in the X or Y coordinate space) to observe. Default = 25
      --rstep RSTEP         The radius step size (where a single unit is the minimum distance between any two points in the X or Y coordinate space) to compute. Default = 1
      --xpfea XPFEA         The column name of the x-coordinate values. Default = 'x [m]'
      --ypfea YPFEA         The column name of the y-coordinate values. Default = 'y [m]'
      --xvfea XVFEA         The column name of the x-velocity values. Default = 'u [m/s]'
      --yvfea YVFEA         The column name of the x-coordinate values. Default = 'v [m/s]'


Sample command: <br/>

    python calc_spiral_corr.py C:\Users\Liam\Documents\Projects\2020\radial_correlation_measure\data\px_basis\PIVlab_0001.txt C:\Users\Liam\Desktop\test_output.csv --ds 2 --rmin 1 --rmax 50 --pxstep 5

## Using the provided package
The function `velocity_corr()` expects square data (s.t. all observation points are evenly spaced, and the y-velocity unit is the same as the x-velocity unit) as an `n*m*2` matrix, where `n` is the size of the y-dimension, `m` is the size of the x-dimension. The last dimension is depth-2, where the first layer is the x-velocity component, and the second layer is the y-velocity component.

As data is not always readily available in the above format, a number of functions, importable via `velocitycorrelation2D.utils` have been created to import and shape data:

- `find_conversion_factor()`:
  - Used to detect the conversion factor to convert from the floating-point positional measurements to the integer grid space, where each point's immediate neighbors are [-1,0,1] away in the x/y coordinate spaces
- `rescale_positions()`
  - Some scientific applications provide data where vector start points separated from one another by more than one pixel (such that division by a number *x* would place all observation points 1 pixel away from neighbors in the x/y coordinate space). This function (applied to the tabular data) rescales the positions s.t. they are one pixel away, and sets the minimum coordinate to (0,0).
- `square_input()`
  - Given the input dataframe with rows of [x-coord, y-coord, x-vel, y-vel], coverts from tabular format into the desired `n*m*2` matrix

**Note** If using both functions, `rescale_positions()` must be used first - `square_input()` returns a data format not accepted by `rescale_positions()`

## Requirements
    pandas>=1.1.*
    numpy>=1.1.*


## References

Ganguly, S., Williams, L., Palacios, I. and Goldstein, R., 2012. Cytoplasmic streaming in Drosophila oocytes varies with kinesin activity and correlates with the microtubule cytoskeleton architecture. Proceedings of the National Academy of Sciences, 109(38), pp.15109-15114.

Dombrowski, C., Cisneros, L., Chatkaew, S., Goldstein, R. and Kessler, J., 2004. Self-Concentration and Large-Scale Coherence in Bacterial Dynamics.
