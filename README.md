# CAAF - Cellular Automaton Model of Atrial Fibrillation
Python implementation of the cellular automaton model of atrial fibrillation
(CAAF) developed during my PhD. The model is described in the following paper:

[Simple Model for Identifying Critical Regions in Atrial Fibrillation](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.114.028104)

K Christensen, KA Manani, NS Peters, PRL 2016

[![An episode of atrial fibrillation in the model](https://img.youtube.com/vi/a-uq-mvUqCM/0.jpg)](https://www.youtube.com/watch?v=a-uq-mvUqCM)



# Installation
Install directly from the sourcecode:

    python setup.py install

# Requirements
CAAF requires the following to run:
* [ffmpeg](https://www.ffmpeg.org/download.html)
* numpy
* matplotlib
* numba


# Quick start
A simulation can be run conveniently form the command line. A default set of model parameters are set in main.py, the model can be run from
the same file. Use the 'num_iters' parameter in the command line to set the number of iterations
the model should run for. Set the 'plot' parameter to 1 to record the simulation in the figures subdirectory.

    python main.py --num_iters 100 --plot 1

# Usage
The model has been implemented as a class called Heart. Heart objects contain
the structure of the CA lattice, methods to create the lattice and run the simulations,
and stores the results of running a simulation.

    from CAAF import model
    heart = model.Heart()
    heart.update_grid(n_iters=100)
    print(heart.num_active_cells)

