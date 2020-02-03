import argparse
import os.path as path

# ARGUMENT PARSER
def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='Path to the input file.')
    parser.add_argument('--links_per_hit', '-l', type=int, required=True,
                        help='Number of links in a hit.')
    parser.add_argument('--output', '-o', type=str, required=True,
                        help='Path to the output directory.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Prints EVERYTHING to the console.')
    args = parser.parse_args()
    return args

def main(args):
    links = [link.rstrip("\n") for link in open(args.input).readlines() if link]

    # split into chunks
    n = args.links_per_hit
    hits = [links[i * n:(i + 1) * n] for i in range((len(links) + n - 1) // n )] 

    for i, hit in enumerate(hits):
        file_name = path.join(args.output, f"batch{i+1}.txt")
        open(file_name, "w").write("\n".join(hit))


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
