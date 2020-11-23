# File Share Size Analysis

A small script to create graphs showing folder size changes over time

## Requirements

* matplotlib (tested with 3.1.2 but should be compatible with most versions)
* Input data files that match the regular expression "First level_\d{2}-\d{2}-\d{4}.txt" (e.g "First level_*dd*-*mm*-*yyyy*.txt")
  * The contents of these files must be in the format G:\\\<sub-directory> [SIZE]
  
## Usage
1. Ensure the above requirements are met
2. Place the script in the same directories as the input files
3. Run the script and view the graphs that are outputted 