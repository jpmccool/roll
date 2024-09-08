class DiceRoll :
    
    # Split a dice roll string into easily digested tokens
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
            #print("token = ", token, sep = '')
            tokens.append(token)
        return tokens
    
    
    def __init__ (self, rollstr) :
        print("Creating DiceRoll object for: " + rollstr)
        return
