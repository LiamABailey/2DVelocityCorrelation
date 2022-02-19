import argparse

import pandas as pd

from velocitycorrelation2D.velutils import rescale_positions, square_input, find_conversion_factor
from velocitycorrelation2D.correlation import velocity_corr


def process_file(path_to_input: str, path_to_output: str,
                data_start_row_ix: int=0, min_radius: int=1,
                max_radius: int=25, radius_step_size: int=25,
                px_conversion: int=1, px_step_size: int=1,
                x_pos_fea: str='x [m]', y_pos_fea: str='y [m]',
                x_vel_fea: str='u [m/s]', y_vel_fea: str='v [m/s]') -> None:
    """
    The main entrypoint into the process. Given the input file and arguments,
    constructs a csv with four columns: radius (in native px), correlation value,
    number of points with more than 0 comparison points, number of points 4 or more
    comparison points, number of points with all 8 comparison points

    Parameters
    ----------
        path_to_input: str
            The path to the input .csv file

        path_to_output: str
            The path to the output .csv file

        data_start_row_ix : int, default = 0
            The row containing column headers in the input data

        min_radius: int, default =  1
            The minimum radius of correlation calculation

        max_radius: int, default = 25
            The maximum radius of correlation calculation

        radius_step_size: int, default = 1
            The step size of radii to analyze. For instance, min =1, max = 10,
            step = 2 would result in the following observations:
                [1,3,5,7,9]

        x_pos_fea: str, default = 'x [m]'
            The name of the x-coordinate column

        y_pos_fea: str, default = 'y [m]'
            The name of the y-coordiname column

        x_vel_fea: str, default = 'u [m/s]'
            The name of the x-velocity column

        y_vel_fea: str, default = 'v [m/s]'
            The name of the y-velocity column


    Returns
    -------
        None

    """
    STEP_COL = 'RADIUS[step]'
    RADIUS_COL = 'RADIUS'
    CORR_COL = 'CORRELATION'
    GEQ1_OBS = 'N_CENTROIDS_1+_OBS'
    GEQ4_OBS = 'N_CENTROIDS_4+_OBS'
    EQ8_OBS = 'N_CENTROIDS_8_OBS'

    # read in the file
    raw_data = pd.read_csv(path_to_input, header = data_start_row_ix)
    print(f"Successfully ingested {path_to_input}")
    # check for column names
    required_cols = [x_pos_fea, y_pos_fea, x_vel_fea, y_vel_fea]
    if any([c not in raw_data.columns for c in required_cols]):
        raise ValueError(f"Input dataset doesn't contain the four columns {required_cols} at file row {data_start_row_ix}")
    # identify conversion factor
    conversion_factor = find_conversion_factor(raw_data, x_pos_fea, y_pos_fea)
    print(f"Discovered conversion factor of {conversion_factor}")
    # perform rescaling ops
    rescaled_data = rescale_positions(raw_data, conversion_factor = conversion_factor,
                                        xcoord_fea = x_pos_fea, ycoord_fea = y_pos_fea,
                                        tolerance = 5e-4)
    # square the data - convert from tabular to y*x*2
    squared_data = square_input(rescaled_data, xcoord_fea = x_pos_fea, ycoord_fea = y_pos_fea,
                                xvel_fea = x_vel_fea, yvel_fea = y_vel_fea)
    # perform the correlation_calulations
    #
    print("Ready to process")
    results = []
    for r in range(min_radius, max_radius + 1, radius_step_size):
        corr, n1p_obs, n4p_obs, n8_obs = velocity_corr(squared_data, r)
        results.append([r, r * conversion_factor, corr, n1p_obs, n4p_obs, n8_obs])

    result_frame = pd.DataFrame(results, columns = [STEP_COL, RADIUS_COL, CORR_COL, GEQ1_OBS, GEQ4_OBS, EQ8_OBS])
    result_frame.to_csv(path_to_output, index= False)
    print(f"Processing complete, output written to {path_to_output}")



def _construct_arg_parser() -> argparse.ArgumentParser:
    """
    Set up the arg parser to consume command-line inputs

    Parameters
    ----------
        None

    Returns
    -------
        argparse.ArgumentParser : The configured parser
    """
    help_description = """
    calc_spiral_corr.py: a utility for calculating spiraling velocity correlation.
    See below for input argument definitions.
    """
    help_epilog = """
    For additional detail, see `README.MD`
    """
    # definions of name, parameter combinations
    arg_definitions = (
        ("input", {
            "type" : str,
            "help" : "The fully specified path to the input file (.csv)"
        }),
        ("output",{
            "type" : str,
            "help" : "The fully speicified path to the output file (.csv)"
        }),
        ("--ds",{
            "type": int,
            "default": 0,
            "metavar": "data_start_row_ix",
            "help": "The row in the input .csv containing the column headers, indexed from zero. Default = 0"
        }),
        ("--rmin",{
            "type": int,
            "default": 1,
            "help": "The minimum radius size to observe. Default = 1"
        }),
        ("--rmax",{
            "type": int,
            "default": 25,
            "help": "The maximum radius size to observe. Default = 25"
        }),
        ("--rstep",{
            "type": int,
            "default": 1,
            "help": "The radius step size to compute. Default = 1"
        }),
        ("--xpfea",{
            "type": str,
            "default": "x [m]",
            "help": "The column name of the x-coordinate values. Default = 'x [m]'"
        }),
        ("--ypfea",{
            "type": str,
            "default": "y [m]",
            "help": "The column name of the y-coordinate values. Default = 'y [m]'"
        }),
        ("--xvfea",{
            "type": str,
            "default": "u [m/s]",
            "help": "The column name of the x-velocity values. Default = 'u [m/s]'"
        }),
        ("--yvfea",{
            "type": str,
            "default": "v [m/s]",
            "help": "The column name of the x-coordinate values. Default = 'v [m/s]'"
        })
    )
    parser = argparse.ArgumentParser(description = help_description,epilog = help_epilog)
    for arg_name, arg_params in arg_definitions:
        parser.add_argument(arg_name,**arg_params)
    return parser


if __name__ == '__main__':
    ps = _construct_arg_parser()
    _args = ps.parse_args()
    process_file(
        path_to_input = _args.input,
        path_to_output = _args.output,
        data_start_row_ix = _args.ds,
        min_radius = _args.rmin,
        max_radius = _args.rmax,
        radius_step_size = _args.rstep,
        x_pos_fea = _args.xpfea,
        y_pos_fea = _args.ypfea,
        x_vel_fea = _args.xvfea,
        y_vel_fea = _args.yvfea
    )
