import argparse
from sympy import *
import sys
import inspect
import functools

def dump_args(func):
    """
    Decorator to print function call details.

    This includes parameters names and effective values.
    """

    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(map("{0[0]} = {0[1]!r}".format, func_args.items()))
        #print(f"{func.__module__}.{func.__qualname__} ( {func_args_str} )")
        print(f"{func.__qualname__} ( {func_args_str} ) called")
        return func(*args, **kwargs)

    return wrapper

def monitor_results(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        #print('function call ' + func.__name__ + '()')
        retval = func(*func_args,**func_kwargs)
        func_args = inspect.signature(func).bind(*func_args, **func_kwargs).arguments
        func_args_str = ", ".join(map("{0[0]} = {0[1]!r}".format, func_args.items()))
        # print('function call ' + func.__name__ + '()')
        print(func.__name__ + f' ( {func_args_str} ) returns ' + repr(retval))
        return retval
    return wrapper

@dump_args
@monitor_results
def jacoby(x, y):
    P, S, T, V, F, G, H, U, beta, k_t, c_v, c_p = symbols('P S T V F G H U beta k_t c_v c_p')
    if x == T and y == S:
        return jacoby(P, V)
    elif x == V and y == P:
        return beta*V*jacoby(T, P)
    elif x == V and y == T:
        return k_t*V*jacoby(T, P)
    elif x == S and y == P:
        return c_p*jacoby(T, P)/T
    elif x == S and y == V:
        return c_v*jacoby(T, V)/T
    elif x == y:
        return 0
    elif x == T and y == P:
        return 1
    elif x == U:
        return jacoby(S, y)*T + jacoby(y, V)*P
    elif x == H:
        return jacoby(S, y)*T + jacoby(P, y)*V
    elif x == F:
        return jacoby(y, T)*S + jacoby(y, V)*P
    elif x == G:
        return jacoby(y, T)*S + jacoby(P, y)*V
    else:
        return -1*jacoby(y, x)

def tracefunc(frame, event, arg, indent=[0]):
    if frame.f_code.co_name == 'jacoby':
        if event == "call":
            indent[0] += 2
            print("-" * indent[0] + "> call function", frame.f_code.co_name)
            print()
        elif event == "return":
            print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
            indent[0] -= 2
        return tracefunc


def main():
    thermo_vars = [args.X, args.Y, args.Z]
    measurables = ['P', 'S', 'T', 'V', 'F', 'G', 'H', 'U']
    if args.X == args.Y or args.X == args.Z or args.Y == args.Z:
        raise ValueError("No two variables may be equal!")
    for var in thermo_vars:
        if var not in measurables:
            raise ValueError(f'{var} is not a main thermodynamic variable! \n Please choose from {measurables}')
    x, y, z = symbols(f'{args.X} {args.Y} {args.Z}')
    P, S, T, V, F, G, H, U = symbols('P S T V F G H U')
    result = simplify(jacoby(x, z)/jacoby(y, z))
    #result = jacoby(x, z)/jacoby(y, z)
    print('------Answer------')
    pprint(result)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Thermodynamic Partial Derivative Solver")
    parser.add_argument("--X", type=str, required=True, help="Numerator var")
    parser.add_argument("--Y", type=str, required=True, help="Denominator var")
    parser.add_argument("--Z", type=str, required=True, help="Constant var")
    args = parser.parse_args()
    #sys.setprofile(tracefunc)
    print("********** Jacobian Gymnastics **********")
    print(r"""
 o   \ o /  _ o         __|    \ /     |__        o _  \ o /   o
/|\    |     /\   ___\o   \o    |    o/    o/__   /\     |    /|\
/ \   / \   | \  /)  |    ( \  /o\  / )    |  (\  / |   / \   / \    @nrdavid""")
    main()