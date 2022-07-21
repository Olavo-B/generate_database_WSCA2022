from operator import mul
import src.read_file as read_file
import pandas as pd

def main():
    json_path = read_file.read_file('/home/olavo/foo/misc/results_2007_1-hop','misc/grn_benchmarks-main',1,1)
    df = pd.read_csv(json_path)
    print(df)

    # json_path = read_file.read_file('/home/olavo/foo/misc/results','misc/grn_benchmarks-main',2,2)
    # df = pd.read_csv(json_path)
    # print(df)

if __name__ == '__main__':
    main()