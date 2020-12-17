import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--host')
parser.add_argument('-p', '--port', metavar="DESCRIPTIVE_PARAM")
parser.add_argument('-b', '--block', action='store_true')
args = parser.parse_args()
print(args)
print(args.port)

