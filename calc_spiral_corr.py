import argparse

from velocitycorrelation2D import rescale_positions, square_input, velocity_corr


def process_file() -> None:
    """
    The main entrypoint into the process

    Parameters
    ----------


    Returns
    -------
        None

    """
    pass





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
            "help": "The row in the input .csv containing the column headers. Default = 0"
        }),
        ("--rmin",{
            "type": int,
            "default": 1,
            "help": "The minimum radius size (in px_grid_spacing/px) to observe. Default = 1"
        }),
        ("--rmax",{
            "type": int,
            "default": 25,
            "help": "The maximum radius size (in px_grid_spacing/px) to observe. Default = 25"
        }),
        ("--rstep",{
            "type": int,
            "default": 1,
            "help": "The radius step size (in px_grid_spacing/px) to compute. Default = 1"
        }),
        ("--pxconv",{
            "type": float,
            "help": "The conversion factor between um to px for x/y coordinate features. If not provided, no conversion applied."
        }),
        ("--pxstep",{
            "type": int,
            "default": 1,
            "metavar": "px_grid_spacing",
            "help": "The grid spacing between each observation, in px. Default = 1"
        }),
        ("--xpfea",{
            "type": str,
            "default": "x [px]",
            "help": "The column name of the x-coordinate values. Default = 'x [px]'"
        }),
        ("--ypfea",{
            "type": str,
            "default": "y [px]",
            "help": "The column name of the y-coordinate values. Default = 'y [px]'"
        }),
        ("--xvfea",{
            "type": str,
            "default": "u [px/frame]",
            "help": "The column name of the x-velocity values. Default = 'u [px/frame]'"
        }),
        ("--yvfea",{
            "type": str,
            "default": "v [px/frame]",
            "help": "The column name of the x-coordinate values. Default = 'v [px/frame]'"
        })
    )
    parser = argparse.ArgumentParser(description = help_description,epilog = help_epilog)
    for arg_name, arg_params in arg_definitions:
        parser.add_argument(arg_name,**arg_params)
    return parser


if __name__ == '__main__':
    ps = _construct_arg_parser()
    print(ps.parse_args())
