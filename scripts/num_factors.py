#!/usr/bin/env python
from argparse import ArgumentParser
from collections import Counter

def factorize(n):
    if n < 2:
        return []
    factors = []
    p = 2

    while True:
        if n == 1:
            return factors
        r = n % p
        if r == 0:
            factors.append(p)
            n = n / p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            p += 2
        else:
            p += 1

def serial(maxnum):
    tot_unique = Counter()
    for i in xrange(2,maxnum+1):
        tot_unique.update([task(i)])
    return tot_unique

def task(n):
    return len(set(factorize(n)))


def multiprocess_parallel(maxnum):
    from multiprocessing import Pool,cpu_count
    pool = Pool(processes=cpu_count())
    result = pool.map_async(task,(xrange(2,maxnum+1)))
    
    return Counter(result.get())

def ipython_parallel(maxnum):
    from IPython.parallel import Client
    cli = Client()
    dview = cli[:]
    
    @dview.parallel(block=True)
    def par_factorize(n):
        if n < 2:
            return 0
        factors = []
        p = 2
    
        while True:
            if n == 1:
                return len(set(factors))
            r = n % p
            if r == 0:
                factors.append(p)
                n = n / p
            elif p * p >= n:
                factors.append(n)
                return len(set(factors))
            elif p > 2:
                p += 2
            else:
                p += 1
        
    c = Counter(par_factorize.map(range(2,maxnum+1)))
    return c
    
       
if __name__=="__main__":
    parser = ArgumentParser(description="Find unique factors from 2 to given number")
    
    common_parser = ArgumentParser(add_help=False)
    common_parser.add_argument("-n",default=500000,type=int, help="Maximum number to factorize")

    subparsers = parser.add_subparsers()
    
    parser_serial = subparsers.add_parser("s",parents=[common_parser])
    parser_serial.set_defaults(func=serial)
    
    parser_multi = subparsers.add_parser("m",parents=[common_parser])
    parser_multi.set_defaults(func=multiprocess_parallel)
    
    parser_ipy = subparsers.add_parser("i",parents=[common_parser])
    parser_ipy.set_defaults(func=ipython_parallel)

    args = parser.parse_args()
    
    tot_unique = args.func(args.n)
    print tot_unique
