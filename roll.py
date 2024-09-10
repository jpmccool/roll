class DiceRoll :
    
    # Split a dice roll string into easily digested tokens
    # TODO - Ensure that rollstr is sanitized
    def tokenize (rollstr) :
        components = re.split("(?=[\+-])", rollstr)
        tokens = [ ]
        for token in components :
            #Assumes: [\+-]? (0|[1-9][0-9]*)? [dD] ([1-9][0-9]*)
            if (token == '') :
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
            else :
                # error
                pass
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
            if k == last_k and (sign == last_sign or k == 1) : # continue accumulating for this value of k, unless there is a change in sign or k is 1
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
    
    
    def __init__ (self, rollstr) :
        print("Creating DiceRoll object for: " + rollstr)
        return
