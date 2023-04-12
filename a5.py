
# --- IMPORTS ---

from math import factorial
from itertools import permutations

# --- CONSTATNTS ---

# 3 digit code & hints, constant allows for adjustment size
N = 3

# --- DATA STRUCTURES --- 

class Lock:

    '''
    Lock Class
        self.code: cracked code digits in their respective indexes
        self.valid: dictionary containing digits as keys and their misplaced indexes as values
        self.invalid: list of invalid digits
        self.well_placed: array of well placed Hints
        self.misplaced: array of misplaced Hints
    '''
    def __init__(self, invalid, well_placed, misplaced):
        print("\nINPUTTED LOCK\n")
        self.code = ['', '', ''] # the code
        self.valid = {} # valid digit dictionary, key: valid digit, value: misplaced indexes
        self.invalid = [digit for hint in invalid for digit in hint] # flatten
        self.well_placed = well_placed
        self.misplaced = misplaced
        print(self)
        return

    def __str__(self):
        s = "--- LOCK ---\n"
        s += f"Code: {self.code}\n"
        s += f"Valid Digits: {self.valid}\n"
        s += f"Invalid Digits: {self.invalid}\n"
        s += f"Well Placed Digits: {self.well_placed}\n"
        s += f"Misplaced Digits: {self.misplaced}\n"
        s += "------------"
        return s

    def is_cracked(self):
        accum = 0
        for val in self.code:
            if val != '': accum += 1
        return accum == N

    def _gen_digit_index_dict(self, arr):
        dict_ = {}
        for hint in arr:
            for i in range(N):
                # dont need hint[i] != '' because _clean_invalid() has not yet been called, but keep to be safe
                if(hint[i] != ''):
                    if(hint[i] not in dict_):
                        dict_[hint[i]] = [i]
                    else:
                        dict_[hint[i]].append(i)
        return dict_

    def _find_invalid_well_placed(self):
        dict_ = self._gen_digit_index_dict(self.well_placed)
        for digit, indexes in dict_.items():
            # set() lets us get unique indexes
            if(2 <= len(indexes) and 2 <= len(set(indexes)) and digit not in self.invalid): # if 2 <= len of set, then a digit is in 2 or more indexes in well_placed, therefore invalid
                print(f"-> well placed digit: {digit} appears in 2 or more different indexes in well placed(s) hint -> {digit} is invalid")
                self.invalid.append(digit)
        return

    def _find_invalid_well_misplaced(self):
        well_placed_dict = self._gen_digit_index_dict(self.well_placed)
        misplaced_dict = self._gen_digit_index_dict(self.misplaced)
        for digit in well_placed_dict:
            if(digit in misplaced_dict): # digit in well_placed appears in misplaced
                set1 = set(well_placed_dict[digit])
                set2 = set(misplaced_dict[digit])
                if(0 < len(set1 & set2) and digit not in self.invalid): # if the intersection of 2 index sets is greater than 0, they share a common index, therefore invalid
                    print(f"-> digit: {digit} appears in the same location in a well placed hint and misplaced hint -> {digit} is invalid")
                    self.invalid.append(digit)
        return

    def _clean_invalid_from_hints(self):
        cleaned = False
        for hint in self.well_placed:
            for i in range(N):
                if(hint[i] in self.invalid):
                    cleaned = True
                    print(f"-> {hint[i]} is in invalid list -> remove {hint[i]} from well placed hint")
                    hint[i] = ''
        for hint in self.misplaced:
            for i in range(N):
                if(hint[i] in self.invalid):
                    cleaned = True
                    print(f"-> {hint[i]} is in invalid list -> remove {hint[i]} from misplaced hint")
                    hint[i] = ''
        return cleaned

    '''
    INITIAL CLEAN
        1) search well_placed hints for digits that appear in different indexes, these digits must be invalid
        2) search in well_placed and misplaced hints for digits that appear in the same index, these digits must be invalid
        3) clean hints from all invalid digits found, including any invalid digits given to us by input
    '''
    def initial_clean(self):
        print("\nPERFORMING INTIAL CLEAN ON HINTS...\n")
        self._find_invalid_well_placed()
        self._find_invalid_well_misplaced()
        # called last since prior functions add digits to self.invalid
        self._clean_invalid_from_hints()
        print(f"\n{self}")
        return

    def _remove_from_valid(self, digit):
        if(digit in self.valid):
            del self.valid[digit]
        return

    def _well_placed_length_matches_special(self):
        evaluated = False
        for hint in self.well_placed:
            if(len(hint) == hint.num_special):
                for i in range(N):
                    if(hint[i] != '' and hint[i] not in self.code):
                        evaluated = True
                        print(f"-> well placed digit: {hint[i]} found to be special -> must be in the code in location {i}")
                        self.code[i] = hint[i]
                        self._remove_from_valid(hint[i]) # remove from valid if necessary
        return evaluated

    def _add_to_valid(self, digit):
        self.valid[digit] = []
        for hint in self.misplaced:
            for i in range(N):
                if(hint[i] == digit and i not in self.valid[digit]):
                    self.valid[digit].append(i)
        return

    def _is_digit_in_well_placed(self, digit):
        for hint in self.well_placed:
            for i in range(N):
                if(hint[i] == digit):
                    return True, i
        return False, -1
    
    def _misplaced_length_matches_special(self):
        evaluated = False
        for hint in self.misplaced:
            if(len(hint) == hint.num_special):
                for i in range(N):
                    if(hint[i] != '' and hint[i] not in self.code and hint[i] not in self.valid):
                        evaluated = True
                        res, j = self._is_digit_in_well_placed(hint[i]) # check if digit is in well_placed
                        if(res == True):
                            self.code[j] = hint[i] # exists in well_placed -> add to code
                            print(f"-> misplaced digit: {hint[i]} found to be special and found in well placed -> must be in the code in location {j}")
                        else:
                            self._add_to_valid(hint[i]) # does not exist in well_placed -> add to valid
                            print(f"-> misplaced digit: {hint[i]} found to be special -> this digit is valid in the code in a unkown location...")
        return evaluated

    def _update_valid_misplaced_indexes(self):
        for indexes in self.valid.values():
            for i in range(N):
                if(self.code[i] != '' and i not in indexes):
                    indexes.append(i)
        return

    def _valid_index_found(self):
        for digit, indexes in self.valid.items():
            if(len(indexes) == N - 1):
                for i in range(N):
                    if(i not in indexes):
                        return True, digit, i
        return False, 0, -1

    def _valid_has_N_minus_1_misplaced_indexes(self):
        evaluated = False
        # must iterate here cuz we cannot delete dictionary keys in a loop in the func
        res, digit, i = self._valid_index_found()
        while(res):
            evaluated = True
            self._remove_from_valid(digit)
            self.code[i] = digit
            print(f"-> valid digit: {digit} only has 1 remaining location it can be in the code -> must be in the code in location {i}")
            res, digit, i = self._valid_index_found()
        return evaluated

    '''
    EVAL HINTS
        1) len(well_placed_hint) == num_special, add digit(s) to code
        2) len(misplaced_hint) == num_special, add digit(s) to valid, (or to code if digit appears in well_placed)
        3) update valid dictionary with indexes of code digits
        4) remove valid digits that appear in N-1 unique indexes and add to code
    '''
    def eval_hints(self):
        print("\nEVALUATING HINTS... TRYING TO CRACK THE CODE...\n")
        evaluated = self._well_placed_length_matches_special()
        evaluated = self._misplaced_length_matches_special() or evaluated # evaluated must be on this side, otherwise if it was true and on the other side the function would not execute
        self._update_valid_misplaced_indexes() # do not need to check evaluated, because is evaluted if code digit found, evaluated = True in another func
        evaluated = self._valid_has_N_minus_1_misplaced_indexes() or evaluated
        if(not evaluated):
            print("-> there was nothing to evaluate")
        else:
            print(f"\n{self}")
        return
    
    def _clean_well_placed(self):
        cleaned = False
        for hint in self.well_placed:
            for i in range(N):
                if(hint[i] != ''):
                    if(hint[i] in self.code): # remove digits in code or valid
                        cleaned = True
                        print(f"-> {hint[i]} is in code already -> remove {hint[i]} from well placed hint")
                        hint[i] = ''
                        hint.num_special -= 1
                    elif(hint[i] in self.valid):
                        cleaned = True
                        print(f"-> {hint[i]} is in valid list already -> remove {hint[i]} from well placed hint")
                        hint[i] = ''
                        hint.num_special -= 1
                    elif(self.code[i] != ''): # remove digits in indexes already allocated in code
                        cleaned = True
                        print(f"-> {hint[i]} occupies the same index as a cracked digit -> {hint[i]} is invalid")
                        self.invalid.append(hint[i])
                        hint[i] = ''
        return cleaned

    def _clean_code_and_valid_from_misplaced(self):
        cleaned = False
        for hint in self.misplaced:
            for i in range(N):
                if(hint[i] != ''):
                    if(hint[i] in self.code):
                        cleaned = True
                        print(f"-> {hint[i]} is in code already -> remove {hint[i]} from misplaced hint")
                        hint[i] = ''
                        hint.num_special -= 1
                    elif(hint[i] in self.valid):
                        cleaned = True
                        print(f"-> {hint[i]} is in valid list already -> remove {hint[i]} from misplaced hint")
                        hint[i] = ''
                        hint.num_special -= 1
        return cleaned
    
    def _find_invalid_misplaced(self):
        cleaned = False
        missing_indexes = []
        for i in range(N):
            if(self.code[i] == ''):
                missing_indexes.append(i)
        dict_ = self._gen_digit_index_dict(self.misplaced)
        for digit, indexes in dict_.items():
            invalid = True
            for i in missing_indexes:
                if(i not in indexes):
                    invalid = False
            if(invalid and digit not in self.invalid):
                cleaned = True
                print(f"-> misplaced digit: {digit} is misplaced in every remaining empty index in the code -> {digit} is invalid")
                self.invalid.append(digit)
        return cleaned

    def _clean_misplaced(self):
        cleaned = self._clean_code_and_valid_from_misplaced() 
        cleaned = cleaned or self._find_invalid_misplaced()
        return cleaned

    def _add_digits_to_invalid(self, hint):
        for digit in hint:
            if(digit != ''):
                self.invalid.append(digit)
        return

    def _drop_hints(self):
        cleaned = False
        i = 0
        while(i < len(self.well_placed)):
            if(len(self.well_placed[i]) == 0): # drop length 0 hints
                cleaned = True
                print("-> dropping length 0 well placed hint")
                self.well_placed.pop(i)
            elif(self.well_placed[i].num_special == 0): # num_special == 0, add remaining digits to invalid and drop hint
                cleaned = True
                print(f"-> num_special == 0 -> adding digits to invalid and dropping hint: {self.well_placed[i]}")
                self._add_digits_to_invalid(self.well_placed[i])
                self.well_placed.pop(i)
            else:
                i += 1
        i = 0
        while(i < len(self.misplaced)):
            if(len(self.misplaced[i]) == 0): # drop length 0 hints
                cleaned = True
                print("-> dropping length 0 misplaced hint")
                self.misplaced.pop(i)
            elif(self.misplaced[i].num_special == 0): # num_special == 0, add remaining digits to invalid and drop hint
                cleaned = True
                print(f"-> num_special == 0 -> adding digits to invalid and dropping hint: {self.misplaced[i]}")
                self._add_digits_to_invalid(self.misplaced[i])
                self.misplaced.pop(i)
            else:
                i += 1
        return cleaned
    
    '''
    ITERATIVE CLEANS
        1) clean all digits in self.code from hints & decrement num_special
        2) clean all digits in self.valid from hints & decrement num_special
        3) clean all digits in well_placed that share the same index as a digit in self.code from hints and add to self.invalid
        4) clean all digits in misplaced that appear in every remaining empty index in self.code and add to self.invalid
        5) add all remaining digits in hints with num_special == 0 to invalid
        6) drops all hints with length == 0
        7) clean hints from any new invalid digits found
    '''
    def iterative_clean(self):
        print("\nPERFORMING ITERATIVE CLEAN ON HINTS...\n")
        cleaned = self._clean_well_placed() # 1) 2) 3)
        cleaned = self._clean_misplaced() or cleaned # 1) 2) 4) 
        cleaned = self._drop_hints() or cleaned # 5) 6)
        cleaned = self._clean_invalid_from_hints() or cleaned # 7)
        if(not cleaned):
            print("-> there was nothing to clean")
        else:
            print(f"\n{self}")
        return cleaned

    def _apply_code(self, perms):
        if(self.code == ['', '', '']): return
        print(f"-> using the cracked code digits to narrow down the {len(perms)} possible codes...", end=" ")
        i = 0
        while(i < len(perms)):
            j = 0
            valid = True
            while(valid and j < N):
                if(self.code[j] != '' and self.code[j] != perms[i][j]):
                    valid = False
                j += 1
            if(not valid):
                perms.pop(i)
            else:
                i += 1
        print(f"{len(perms)} possbile codes remaining")
        return

    def _apply_invalid(self, perms):
        if(self.invalid == []): return
        print(f"-> using the invalid digits to narrow down the {len(perms)} possible codes...", end=" ")
        i = 0
        while(i < len(perms)):
            j = 0
            valid = True
            while(valid and j < N):
                if(perms[i][j] in self.invalid):
                    valid = False
                j += 1
            if(not valid):
                perms.pop(i)
            else:
                i += 1
        print(f"{len(perms)} possbile codes remaining")
        return
    
    def _apply_valid(self, perms):
        if(not self.valid): return
        print(f"-> using the valid digits to narrow down the {len(perms)} possible codes...", end=" ")
        i = 0
        while(i < len(perms)):
            valid = True
            for digit, indexes in self.valid.items():
                if(digit not in perms[i]): # each perm should have valid digit in it
                    valid = False
                    break
                for index in indexes:
                    if(perms[i][index] == digit): # iterate through indexes of valid digit to ensure its not in that index
                        valid = False
                        break
            if(not valid):
                perms.pop(i)
            else:
                i += 1
        print(f"{len(perms)} possbile codes remaining")
        return

    def _apply_well_placed(self, perms):
        if(self.well_placed == []): return
        print(f"-> using the well placed hints to narrow down the {len(perms)} possible codes...", end=" ")
        i = 0
        while(i < len(perms)):
            j = 0
            valid = True
            while(valid and j < len(self.well_placed)): # every perm must have num_special digit(s) from every hint from well_placed in the correct location
                num_special = self.well_placed[j].num_special
                valid = False
                for k in range(N):
                    if(self.well_placed[j][k] == perms[i][k]):
                        num_special -= 1 
                if(num_special == 0): # perm must have exactly num_special digits from each well placed hint in the correct location
                    valid = True
                j += 1
            if(not valid):
                perms.pop(i)
            else:
                i += 1
        print(f"{len(perms)} possbile codes remaining")
        return

    def _apply_misplaced(self, perms):
        if(self.misplaced == []): return
        print(f"-> using the misplaced hints to narrow down the {len(perms)} possible codes...", end=" ")
        i = 0
        while(i < len(perms)):
            j = 0
            valid = True
            # num_special digit(s) in misplaced must appear in every perm (we check location later)
            while(valid and j < len(self.misplaced)): 
                num_special = self.misplaced[j].num_special
                valid = False
                for k in range(N):
                    if(self.misplaced[j][k] in perms[i]):
                        num_special -= 1
                if(num_special == 0):
                    valid = True
                j += 1
            j = 0
            # a digit in misplaced cannot be in the same location in every perm
            while(valid and j < len(self.misplaced)):
                k = 0
                while(valid and k < N):
                    if(self.misplaced[j][k] == perms[i][k]):
                        valid = False
                    k += 1
                j += 1
            if(not valid):
                perms.pop(i)
            else:
                i += 1
        print(f"{len(perms)} possbile codes remaining")
        return

    '''
    GENERATE PERMUTATIONS
        - when there is insufficient information to crack the code we must generate 10P3 and apply
          our refined hints to get the smallest subset of possible codes possible
        1) generate permutations
        2) elim all perms that dont have cracked digits in the right location
        3) elim all perms that contain an invalid digit
        4) elim all perms that don't contain all valid digits or have them in the wrong location
        5) elim all perms that don't contain num_special well placed digit(s) in its correct location for each hint in well_placed
        6) elim all perms that don't contain num_special misplaced digit(s) or contain a misplaced digit in a misplaced location for each hint in misplaced
    '''
    def gen_perms(self):
        print("\nCOULD NOT FIND 1 SOLUTION... GENERATING ALL POSSIBLE SOLUTIONS...\n")
        print(f"-> generating all {int(factorial(10)/factorial(10-N))} (10P{N}) possible codes")
        perms = list(permutations([0,1,2,3,4,5,6,7,8,9], N))
        self._apply_code(perms)
        self._apply_invalid(perms)
        self._apply_valid(perms)
        self._apply_well_placed(perms)
        self._apply_misplaced(perms)
        print(f"\nTHE {len(perms)} POSSIBLE CODES ARE...\n")
        return perms

class Hint:

    # length: how many digits are there not including placeholders
    # num_special: how many special digits there are (correct & well placed or misplaced)
    # digits: array of 3 digits
    def __init__(self, digits, num_special = 1):
        self.digits = digits
        self.num_special = num_special
        return

    def __len__(self):
        accum = 0
        for val in self.digits:
            if val != '': accum += 1
        return accum

    # gets ith index in Hint.digits
    # use: Hint[i]
    def __getitem__(self, i):
        return self.digits[i]

    # sets ith index in Hint.digits with val
    # use: Hint[i] = val
    def __setitem__(self, i, val):
        self.digits[i] = val
        return
    
    def __iter__(self):
        for digit in self.digits:
            yield digit
        return

    def __str__(self):
        return f"Hint(len: {len(self)}, special: {self.num_special}, digits: {self.digits})"

    # allows for Hint objects to be printed while inside an array or dict
    # https://stackoverflow.com/questions/46406165/str-method-not-working-when-objects-are-inside-a-list-or-dict
    __repr__ = __str__

# --- DRIVER CODE --- 

def solve(lock):
    lock.initial_clean()
    cracked = False
    cleaned = True
    while(not cracked and cleaned):
        lock.eval_hints()
        cracked = lock.is_cracked()
        cleaned = lock.iterative_clean()
    if(cracked):
        print(f"\nTHE CODE HAS BEEN CRACKED... THE CODE IS: {lock.code}\n")
    else:
        print(f"-> {lock.gen_perms()}\n")
    return

# --- INPUT --- 

'''
# A4 
lock = Lock(
        [[4, 3, 8]], # this does not really need to be a 2d array but whatever
        [Hint([7, 8, 2])], 
        [Hint([7, 1, 6]), Hint([2, 0, 7], 2), Hint([4, 8, 0])]
    )
'''

'''
# A5 a)
lock = Lock(
        [[4, 2, 8]], 
        [Hint([7, 8, 3])], 
        [Hint([7, 1, 6]), Hint([3, 0, 7], 2), Hint([4, 8, 0])]
    )
'''

'''
# A5 b)
lock = Lock(
        [[4, 2, 8]], 
        [], 
        [Hint([7, 1, 6]), Hint([3, 0, 7], 2), Hint([4, 8, 0])]
    )
'''


# A5 c) 
lock = Lock(
        [], 
        [Hint([7, 8, 3])], 
        [Hint([7, 1, 6]), Hint([3, 0, 7], 2)]
    )


'''
# my test
lock = Lock(
        [], 
        [Hint([7, 8, 3], 2), Hint([2, 9, 4])], 
        []
    )
'''

solve(lock)

