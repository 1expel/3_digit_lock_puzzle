# ASSUMPTIONS

- 1 solution - 2 numbers cannot be well placed in the same location
    - does not mean we can find this solution
- no duplicate numbers in code
- any number from 0-9 can be used in the code, even if it does not appear in hints

# PREFACE

- why I do not initally generate all permutations of digits given
    - generating permutations is slow
    - generating permutations and applying raw hints does not guarantee a solution - collective information from hints must be combined together to refine hints, making them more powerful
    - trying to combine hints to crack the code without permutations is efficient
- if the code cannot be cracked by the hints alone
    - 1) permutations will be generated
    - 2) the modified hints made in trying to crack the code will be used to narrow down the permutations to the smallest subset possible
        - unmodified hints will have a bigger subset of codes
- IF i did generate permutations at the beginning
    - i still would need to essentially try and crack the code from hints alone, as this ensures i am reducing hints / combining them in ever way possible
        - so in the worst case the code cannot be cracked, the permutations are narrowed down to the best subset possible

# IMPLEMETATION

## DATA STRUCTURES

### HINT CLASS

- Data
    - hint digits
    - number of special digits (e.g. 1 correct but wrong placed OR 2 correct and well placed)
    - does not store / know whether hint is well placed, or misplaced, Lock is used for that
- Notable Dunder Methods
    - __len()__ only counts digits and skips '' chars
    - __getitem__ and __setitem__ allow for ease of digit retrival and modification
    - __iter__ for looping
    - __str__ and __str__ for testing

### LOCK CLASS

- Data
    - self.code: stores the cracked code digits
    - self.valid: digit(s) known to be correct, but in an unknown location
    - self.invalid: digit(s) known to be incorrect
    - self.well_placed: array of well placed hints
    - self.misplaced: array of misplaced hints
- Methods
    - __str__ for ease of viewing the lock's state in between function calls
    - all initial clean methods
    - all hint evaluation methods
    - all iterative clean methods
    - all gen and clean perm methods

## CRACKING THE CODE

### INITIAL CLEAN

1) search well_placed hints for digits that appear in different indexes, these digits must be invalid
2) search in well_placed and misplaced hints for digits that appear in the same index, these digits must be invalid
3) clean hints from all invalid digits found, including any invalid digits given to us by input

### EVAL HINTS   

1) len(well_placed_hint) == num_special -> add digit(s) to code and remove digit(s) from valid (if necessary)
2) len(misplaced_hint) == num_special -> add digit(s) to code if digit is also in well_placed, else add digit(s) to valid
3) update valid dictionary with indexes of code digits
4) remove valid digits that appear in N-1 unique indexes and add to code
            
### ITERATIVE CLEANS

1) clean all digits in self.code from hints & decrement num_special
2) clean all digits in self.valid from hints & decrement num_special
3) clean all digits in well_placed that share the same index as a digit in self.code from hints and to self.invalid
4) clean all digits in misplaced that appear in every remaining empty index in self.code and add to self.invalid
5) add all remaining digits in hints with num_special == 0 to invalid
6) drops all hints with length == 0
7) clean hints from any new invalid digits found

### GENERATE PERMUTATIONS

- when there is insufficient information to crack the code we must generate 10P3 and apply our refined hints to get the smallest subset of possible codes possible
1) generate permutations
2) elim all perms that dont have cracked digits in the right location
3) elim all perms that contain an invalid digit
4) elim all perms that don't contain all valid digits or have them in the wrong location
5) elim all perms that don't contain num_special well placed digit(s) in its correct location for each hint in well_placed
6) elim all perms that don't contain num_special misplaced digit(s) or contain a misplaced digit in a misplaced location for each hint in misplaced

# THE PUZZLE INSTANCE I USED

see image.png

## OUTPUT1

- in output1.txt I used all the hints used in the image as input

## OUTPUT2

- in output2.txt I used all the hints as input, minus the first hint ([7, 8, 3], one number is correct and well placed)

## OUTPUT3

- in output3.txt I used all the hints as input, minus the last 2 hints ([4, 2, 8], nothing is correct AND [4, 8, 0], one number is correct but wrong placed)
