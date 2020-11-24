import argparse

from preprocessor import preprocessor

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '-c', '--csv',
        default=None,
        type=str,
        help='csv generated from autoface AI (default: None)')
    args = argparser.parse_args()

    churn = preprocessor()

    print("---------CSV being prepared...---------")
    # csv output from autoface.ai
    churn.csvCompiler(args.csv)
    print("---------CSV ready---------")

    print("---------Splitting frames into MicroX components---------")
    churn.microXMaker()
    print("---------Splitting of frames complete---------")

if __name__=="__main__":
    main()