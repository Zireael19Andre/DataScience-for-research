import numpy as np
import pandas as pd
io = './Bera/Var-Homo.xlsx'
df = pd.read_excel(io,sheet_name='Data') #选定数据表
df = df.drop(columns=['Unnamed: 0','Unnamed: 1'])#去除前两列无用数据
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(df,'\n','\n','\n','\n')
gt = pd.DataFrame(df,columns=[input('Input Your Column Name:')]) #输入操作对象列
inp = np.arange(float(input('Start Range:')),float(input('End Range:')),0.001,float).tolist() #指定区间指定刻度产生基准值
p = np.array(gt) #变成Numpy Array
p = np.append(p,values=0)
p = np.delete(p,0)#删除第一行


count_all_1 = 0  #count_all - 1 到分隔为止所有数个数
count_flase_1 =0  #count_all-count_flase 非nan数个数
count_all_2 = 0
count_flase_2 = 0
nan_set=[]#nan计数
for k in p.tolist():
    count_all_1+= 1
    if str(k) in 'nan': #in语句的左右两边都需要为String
        count_flase_1 += 1 #非number计数
        nan_set.append(k)
        if len(nan_set)== 2:
            a = p.tolist()[0:count_all_1-1]
            b = p.tolist()[count_all_1-1:-1]
            [b.pop(0) for pp in range(3)]
            c = count_all_1 - count_flase_1 #无损建筑实际计数值
            break
for l in b:
    count_all_2 += 1
    if str(l) in 'nan':
        count_flase_2 += 1
d = count_all_2 - count_flase_2 #受损建筑实际计数

z = []
y = []
res = {}
for i in range(len(inp)):#对基准值列表的分割基准值进行遍历
    p[-1] = inp[i]#添加至行尾（array）
    p.tolist()
    x = 0
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for j in p:#对列表遍历
        if p[x]!=p[x]:#跳过nan值
            x = x +1
            continue
        if len(z) == c and len(y) == d: #当结束一轮后，统计结果置零
            z=[]
            y=[]
        if float(p[x]) - float(p[-1]) > 0:#该值大于基准值（尾值）
            if len(z) < c:#当还在该轮（完好建筑）中时
                z.append('NB')#统计完好建筑
                x += 1
                TN += 1
            elif len(z) == c:#该轮的完好建筑遍历结束后
                y.append('NB')#统计破损建筑
                x +=1
                FN += 1
        elif float(p[x]) - float(p[-1]) <0:
            if len(z)<c:
                z.append('B')
                x += 1
                FP += 1
            elif len(z) == c:
                y.append('B')
                x += 1
                TP += 1
        try:
            recall = TP/(TP+FN)
        except:
            recall =0
        try:
            precision = TP / (TP + FP)
        except:
            precision = 0
        Acc = (TP+TN)/(c+d)
        pyes = (TP+FP)*(TP+FN)/pow((c+d),2)
        pno = (TN+FN)*(TN+FP)/pow((c+d),2)
        pe = pyes + pno
        k = (Acc-pe)/(1-pe)
        res[inp[i]]=k
print('\n','Loop Result:','\n',res,'\n')
print(' (Reference Value , Maximum Kappa Value):','\n',max(res.items(),key=lambda x:x[1])) #key=lambda 元素: 元素[字段索引]


