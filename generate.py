import argparse
import numpy as np
from translate import Translator
import tqdm

def get_parserparam():
    while 1:
        parser=argparse.ArgumentParser(prog="tofel word reviewer",description="To generate word books")
        parser.add_argument("-r","--random",action="store_true",default=False,help="whether you want the word books to be randomized")
        parser.add_argument("-s","--start",type=int,default=1,choices=list(range(1,146)),help="which word do you want to start from, default=1")
        parser.add_argument("-e","--end",type=int,default=146,choices=list(range(1,146)),help="which word do you want to end with, default=146")
        parser.add_argument("-t","--total",type=int,required=True,help="how many words do you want")
        parser.add_argument("-tt","--TOTAL",type=int,required=True,help="how many WORD BOOKS do you want")
        args=parser.parse_args()
        if args.total>=args.end-args.start+1:
            print("没这么多词给你复习！重新输一遍！")
            continue
        if args.start>args.end:
            print("开头不能大于结尾懂不懂啊！重新输一遍！")
            continue
        else:
            return args.random,args.start,args.end,args.total,args.TOTAL

def convert(char):
    translator=Translator(from_lang="english",to_lang="chinese")
    return translator.translate(char)

def generator():
    israndom,start,end,total,TOTAL=get_parserparam()
    with open("collection.txt","r") as f:
        file1=[line.replace("\n","") for line in f if line !="\n"]
    f.close()
    pbar=tqdm.tqdm(range(TOTAL),desc="单词本")
    for idx in pbar:
        pbar.set_postfix({"正在处理的单词本":idx+1})
        with open(f"./word books/untranslated_{idx+1}.txt","w") as a:
            with open(f"./word books/translated_{idx+1}.txt","w") as b:
                file2=file1[start-1:end]
                if israndom:
                    file3=np.random.choice(file2,total,replace=False)
                else:
                    index1=list(range(len(file2)))
                    index2=np.random.choice(index1,total)
                    file3=[]
                    for j in range(len(index2)):
                        file3.append(file2[j])
                pbar2=tqdm.tqdm(range(len(file3)),desc=f"处理第{idx+1}/{TOTAL}个单词本")
                for count in (pbar2):
                    pbar2.set_postfix({"正在处理的词组":f"{count+1}/{len(file3)}"})
                    if file3[count].find(",")==-1:
                        temp=file3[count]
                        a.write(f"第{count+1}组词： {temp}\n")
                        try:
                            b.write(f"第{count+1}组词： {temp}:{convert(temp)}\n")
                        except Exception as e:
                            b.write(f"第{count + 1}组词： {temp}:翻译失败\n")
                    else:
                        temp=(file3[count].replace(",","")).split()
                        a.write(f"第{count+1}组词： ")
                        b.write(f"第{count+1}组词： ")
                        for j in range(len(temp)):
                            a.write(f"{temp[j]}; ")
                            try:
                                b.write(f"{temp[j]}:{convert(temp[j])}; ")
                            except Exception as e:
                                b.write(f"{temp[j]}:翻译失败; ")
                            if j==len(temp)-1:
                                a.write("\n")
                                b.write("\n")
            b.close()
        a.close()
    pass
if __name__=="__main__":
    generator()

