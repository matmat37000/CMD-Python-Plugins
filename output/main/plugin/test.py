import argparse

parser = argparse.ArgumentParser(
    description="A simple testing command."
)

# parser.add_argument("argument", help="Path to a file to process.")
parser.add_argument(
    "-a" , "--args", help="Argument testing", default="Merde"
)

args = parser.parse_args()
print(args.args)