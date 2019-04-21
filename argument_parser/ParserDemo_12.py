import argparse

parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number", type=int)
parser.add_argument("-v", "--verbosity", help="increase output verbosity", type=int, default=0, choices=[0, 1, 2])
args = parser.parse_args()

answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)

