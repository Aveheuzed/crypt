from boolstring import to_bool,to_bytes

def group(seq,n,complete=None):
    assert n, "can't make groups of zero items !"
    i = n
    while i<=len(seq) :
        yield seq[i-n:i]
        i += n
    last = seq[i-n:]
    if len(last):
        if complete is None:
            yield last
        else :
            yield (last + complete*(n-len(last)))

def encode(text,key):
    text = to_bool(text)
    end = list()
    for t in group(text,sum(key)//len(key)):
        for k in key :
            k %= len(t)
            t0,t1 = t[:k],t[k:]
            new = [x^y for x,y in zip(t0,t1)]
            if len(t0)<len(t1):
                t = t1+new
            else :
                t = new+t0
        end += t
    return to_bytes(end)

def decode(text,key):
    text = to_bool(text)
    end = list()
    for t in group(text,sum(key)//len(key)):
        for k in reversed(key) :
            k %= len(t)
            t0,t1 = t[:len(t)-k],t[len(t)-k:]
            new = [x^y for x,y in zip(t0,t1)]
            if len(t0)<=len(t1):
                t = t1+new
            else :
                t = new+t0
        end += t
    return to_bytes(end)
