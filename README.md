# 2DVelocityCorrelation

Implementation of the velocity correlation algorithm used in 'Self-concentration and Large-Scale Coherence in Bacterial Dynamics', Dombrowski et al; 'Cytoplasmic streaming in Drosophilia oocytes with kinesin activity and correlates with the microtubule cytoskeleton architecture', Ganguly et al.

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

## Using the provided implementation
The function expects square data (s.t. all observation points are evenly spaced, and the y-velocity unit is the same as the x-velocity unit) as an `n*m*2` matrix, where `n` is the size of the y-dimension, `m` is the size of the x-dimension. The last dimension is depth-2, where the first layer is the x-velocity component, and the second layer is the y-velocity component.

As data is not always readily available in the above format, a number of functions, importable via `velocitycorrelation2D.utils` have been created to import and shape data:

TODO:
- Write import & shaping utilities
- test import & data shaping utilities
- documet core function output in readme


## References (WIP)

- Ganguly et al
- Dombrowski et al
- Alexander
