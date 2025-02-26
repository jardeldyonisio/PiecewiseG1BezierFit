# Piecewise G1 Bezier Fit Python

This project provides a Python implementation of the Piecewise G1 Bezier Fit algorithm, which is used for fitting piecewise G1 continuous Bezier curves.

## Overview

The Piecewise G1 Bezier Fit algorithm is designed to create smooth and continuous curves, which are useful in various applications such as computer graphics, path planning, and data interpolation.

## Documentation

For detailed documentation and examples, please refer to the original repository: [PiecewiseG1BezierFit on GitLab](https://gitlab.com/erehm/PiecewiseG1BezierFit).

## TODO

- This implementation includes three methods. The first method fits a unique Bézier curve, while the second and third methods fit a B-spline. However, there are issues with the `fmin` function in Python during the conversion process, so currently, only the first method is functional;
- Conda env.

## Related Work

The branch `single_bezier` is used in a Teach and Repeat project, which focuses on autonomous navigation by teaching a robot a path and having it repeat the path accurately. This branch demonstrates the practical application of the Piecewise G1 Bezier Fit algorithm in real-world scenarios.

You can find the project [in this repository](https://github.com/jardeldyonisio/teach_and_repeat).
