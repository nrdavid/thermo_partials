# Thermodyanmic Partial Derivative Solver

This code allows one to express any thermodynamic partial derivative in terms of measureable materials quantities. This code works for 
the standard 4 free energies U, H, F G. This method utilizes the "method of Jacobians" outlined from Robert H. Swendsen's "An 
Introduction to Statistical Mechanics and Thermodynamics" (2019).

## Installation
You may build your environment from the provided `environment.yml`.
`conda env create -f environment.yml`

## Usage
To run use
`python thermo_partials.py --X S --Y T --Z P`
which should return
```
********** Jacobian Gymnastics **********

 o   \ o /  _ o         __|    \ /     |__        o _  \ o /   o
/|\    |     /\   ___\o   \o    |    o/    o/__   /\     |    /|\
/ \   / \   | \  /)  |    ( \  /o\  / )    |  (\  / |   / \   / \    @nrdavid
jacoby ( x = S, y = P ) called
jacoby ( x = T, y = P ) called
jacoby ( x = T, y = P ) returns 1
jacoby ( x = S, y = P ) returns c_p/T
jacoby ( x = T, y = P ) called
jacoby ( x = T, y = P ) returns 1
------Answer------
cₚ
──
T 
```
where each flag represents the following variables in the partial derivative:
$$\left(\frac{\partial X}{\partial Y} \right)_Z$$
