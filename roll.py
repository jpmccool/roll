import re
from operator import itemgetter
import random

class DiceRoll :
    
    # Split a dice roll string into easily digested tokens
    # TODO - Ensure that rollstr is sanitized
    def tokenize (rollstr) :
        components = re.split("(?=[\+-])", rollstr)
        tokens = [ ]
        for token in components :
            #Assumes: [\+-]? (0|[1-9][0-9]*)? [dD] ([1-9][0-9]*)
            if token == '' :
                continue
            if token.startswith('+') :
                nk = re.split("[dD]", token[1:])
                sign = 1
            elif token.startswith('-') : 
                nk = re.split("[dD]", token[1:])
                sign = -1
            else :
                nk = re.split("[dD]", token)
                sign = 1
            if len(nk) == 1 :
                token = (sign * int(nk[0]), 1)
            elif len(nk) == 2 :
                token = (sign * int(nk[0]) if len(nk[0]) > 0 else sign, int(nk[1]))
            tokens.append(token)
        return tokens
        
    # Sort a list of tokens by descending k, then by descending m, and condense into as few rolls as possible
    def sort_tokens (tokens) :
        # Sort tokens by descending k, then by descending m, and condense redundant terms
        tokens.sort(key=itemgetter(1, 0), reverse=True)
        rolls = [ ]
        last_sign = 0
        curr_n = 0
        last_k = 0
        mod = 0
        for token in tokens :
            n = token[0]
            k = token[1]
            if n == 0 :
                continue
            sign = 1 if n > 0 else -1
            if (k == last_k) and (sign == last_sign or k == 1) : # continue accumulating for this value of k, unless there is a change in sign or k is 1
                curr_n += n
            else :# k != last_k or (sign != last_sign and k > 1)
                if curr_n != 0 :
                    rolls.append((curr_n, last_k))
                curr_n = n
                last_k = k
            last_sign = sign
        if curr_n != 0 :
            rolls.append((curr_n, last_k))
        return rolls
    
    # Update a dice roll's propability distribution (p) by adding another (k)-side die 
    def convolve (p, k) :
        plen = len(p)
        dist = [ ]
        dist.append(p[0])
        for i in range(1, plen + k - 1) :
            sum = dist[i - 1]
            if (i < plen) : sum += p[i]
            if (i >= k)   : sum -= p[i-k]
            dist.append(sum)
        return dist
    
    # Calculate statistics for the current dice roll, i.e. probability distribution
    def calculate_stats (self) :
        for roll in self.rolls :
            n = roll[0]
            k = roll[1]
            if n > 0 :
                self.low_val += n
            elif n < 0 :
                self.low_val += n * k
            else :
                continue # since this contributes no dice - this should be redundant
            self.size += abs(n) * (k - 1)
            self.total *= k**abs(n)
            if k > 1 :
                for x in range(abs(n)) :
                    self.probs = DiceRoll.convolve(self.probs, k)
        # Expectation value
        # TODO: There is an easier way to do this (by adding individual dice expectations)
        val = self.low_val
        for p in self.probs :
            self.expected += val * p;
            val += 1
        self.expected /= self.total
    
    # Find a canonical form for the dice roll string
    def canonicalize (self) :
        for roll in self.rolls :
            n = roll[0]
            k = roll[1]
            if k == 1:
                self.canonical_rollstr += ("+" if n > 0 else "") + str(n);
            elif len(self.canonical_rollstr) > 0 :
                self.canonical_rollstr += ("+" if n > 0 else "") + str(n) + "d" + str(k);
            else :
                self.canonical_rollstr += str(n) + "d" + str(k)
    
    # Rolls all the dice and returns the total (including modifiers)
    # Also stores the dice rolls and total for retrieval
    def roll (self) :
        self.dice_rolls = [ ]
        self.roll_total = 0
        for roll in self.rolls :
            n = roll[0]
            k = roll[1]
            if k == 1 :
                self.roll_total += n
                self.dice_rolls.append((n,))
            else :
                ndk = [ ]
                for die in range(abs(n)) :
                    num = random.randrange(1, k + 1)
                    if (n < 0) :
                        num *= -1
                    self.roll_total += num
                    ndk.append(num)
                self.dice_rolls.append(tuple(ndk))
        return self.roll_total
    
    # Find the probability of having rolled the most recent total
    # Returns the probability as a fraction, not a percentage
    def prob_of (self, total = None) :
        if total is None :
            p = self.probs[self.roll_total - self.low_val]
        else :
            if (total >= self.low_val) and (total < self.low_val + self.size) :
                p = self.probs[total - self.low_val]
            else :
                p = 0.00
        return p / self.total
    
    
    # TODO: Add method to return the probability distribution as a list of (value, probability) tuples
    #       - with option to return tuples as (value, probability-as-integer) ?
    
    # TODO: Add method to retrieve statistics in a well documented format
    #       - expected value (mean), max probability, value range/size, probability distribution (off by default), variance/stddev
    
    # TODO: Add ability to modify this roll with additional rolls and mods
    # def modify (roll, rollstr) :
    
    
    # Display
    original_rollstr = ""
    canonical_rollstr = ""
    
    # Rolls to make
    rolls = [ ]
    
    # Stats
    low_val = 0
    size = 1
    total = 1
    probs = [ 1 ]
    expected = 0
    
    # Most recent dice roll results
    dice_rolls = [ ]
    roll_total = 0
    
    
    def __init__ (self, rollstr) :
        print("Creating DiceRoll object for: " + rollstr)
        self.original_rollstr = rollstr
        self.rolls = DiceRoll.sort_tokens(DiceRoll.tokenize(rollstr))
        self.calculate_stats()
        self.canonicalize();
        return
    
    def __str__ (self) :
        return self.canonical_rollstr
    


roll = DiceRoll("-d4-d6+5d6-0d20+2-3d6-8+d4")
print(roll)

roll = DiceRoll("5d6-4d6+1d4-1d4-6")
result = roll.roll()
print("Roll:", roll)
print("Total:", result)
print(f"Probability: {roll.prob_of() :.2%}")
