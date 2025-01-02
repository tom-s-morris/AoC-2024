# AoC-2024
Advent of Code 2024

## Day 1: Historian Hysteria
Simple algorithm to compare two lists.

## Day 2: Red-Nosed Reports
Sequences which must be all increasing or decreasing. Part 2 allows removal of a single bad report; my approach uses deepcopy which is inefficient, the lists are short as it's week 1.

## Day 3: Mull It Over
Finding 'mul' instructions in a garbled stream of data using regular expressions.

## Day 4: Ceres Search
Simple wordsearch! Find words in the shape of 'X' for part 2.

## Day 5: Print Queue
Create a dependency graph to order a stream of page numbers.

## Day 6: Guard Gallivant
Path-finding in a square array.
More interesting is part 2: locating an extra wall to force the guard into an infinite loop.
I investigated the cycle length in part 3 and created a histogram of the results. The cycle lengh is a multiple of 4 as the guard must turn through a multiple of 360 degrees to return to his original location.

```
004 | ##########################################################################################################################################################################################################################################################################################################################################################################################################################################################
008 | ########################################################################################################
012 | ################################################################################
016 | #################################################################
020 | ################################
024 | #############################################
028 | #########################################################################
032 | ###########################################################
036 | ########################################################################
040 | ##################################################################################
044 | #################################################
048 | ####################################
052 | ################################################
056 | #####################################
060 | #############################################
064 | ###################################
068 | #######################
072 | ######################################
076 | ###########################################
080 | ###############################################
084 | #########################################
088 | ###################################
092 | #####################
096 | ##########################
100 | ####################
104 | ##############################
108 | ################
112 | ################
116 | ###################
120 | #####
124 | ##
128 | ##
```

## Day 7: Bridge Repair
Use the *itertools* library to find all numeric outputs using combinations of addition, multiplication and concatenation operators.

## Day 8: Resonant Collinearity
Another 2D problem based on nodes due to wave interference from pairs of antennas.

## Day 9: Disk Fragmenter
A simple disk defragmentation algorithm. The files must be contiguous for part 2 to improve file read performance.

## Day 10: Hoof It
Another 2D problem, based on topographic data (land height measured from 0 to 9). The land should be traversed from "sea level" to the highest point(s) on the map to make for a scenic hike.

## Day 11: Plutonian Pebbles
Follow a system of rules and count the pebbles after N steps.
Part 2 is more tricky as the compute time increases exponentially, so a trick must be found to simplify the calculation. I used a tree to cache the partial/recurring states.

## Day 13: Claw Contraption
A mathematical problem using linear algebra.

## Day 16: Reindeer Maze
A maze solver!

## Day 17: Chronospatial Computer
A fun task to implement a simple RISC-like computer.  
**TODO** Part 2 was not so fun, as the problem size is quite large (8^16) and requires some analysis to identify the pattern. I tried to reverse engineer the encoding algorithm without success!

## Day 19: Linen Layout
An interesting task to make up long sequences from short fragments.  
**TODO** Part 2 again requires some caching of the intermediate states.



