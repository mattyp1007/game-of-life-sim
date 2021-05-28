# game-of-life-sim

## Description
This Python program is based on the famous Conway's Game of Life:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

It takes an input of a text file containing a grid (any size) of O's (live cells) and .'s (dead cells). The game goes through 100 "generations" before outputting a file of the final generation.

## Instructions
To run this program, you must provide command line arguments for the input and output file names. I have provided examples in this repo, but you may create a custom input file as long as each row is of equal length and you include strictly O's (capital letter O) and .'s (full stop). To run the program, navigate to the folder and execute this in command line:

`python3 game-of-life-sim.py -i input.dat -o output.dat`

This program also supports multiprocessing, so in order to specify the number of processes you may provide an additional optional argument with `-t <number>`. The default is a single process, but an example of 8 processes would look like so:

`python3 game-of-life-sim.py -i input.dat -o output.dat -t 8`
