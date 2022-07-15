import os

def pipeline():
    os.system("python generate.py -r -s 1 -e 100 -t 10 -tt 5")

if __name__=="__main__":
    pipeline()