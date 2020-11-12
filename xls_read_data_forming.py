#Faster way by using Panda//
import numpy as np
import pandas as pd
io = "./wu/1184sta.xlsx"
df = pd.read_excel(io,header=0)
excel_header = df.columns.tolist()

p = np.array(df)
m = np.insert(p,0,values=excel_header,axis=0)

print(m)
[rows,cols]=m.shape #获取行列数
fisrt_cell = m[0,0] #（1，1）cell暂存

#[m[i,j] == 1 for i in range(rows) for j in range(cols) if m[i][0] == m[:,j][0] ] not working

for i in range(rows):#行数range
    for j in range(cols):#列数range
        if m[i][0] == m[:,j][0] :#行的数值=列的数值时，将该行变成'1'（从list转成的array本来就全是str）
            m[i,j]=1

#[m[i,j] == 0 for i in range(1,rows) for j in range(5,cols) if m[i,j]!= 1] not working

for i in range(1,rows):
    for j in range(5,cols):
        if m[i, j] != 1:
            m[i,j] = 0

m[0,0]=fisrt_cell #替换（1,1cell）
m = pd.DataFrame(m)#从array输出dataframe

print(m)
m.to_excel('./wu/output.xlsx',header=False,index=False)#不要表头不要索引
print('All Done')


'''
#slow way using xlrd//
import numpy as np
import xlrd
import pandas as pd

m=[]
data = xlrd.open_workbook("/Users/zireael19andre/Movies/TubeGet/1184sta.xlsx")
table = data.sheet_by_index(0)#按索引获取工作表，0就是工作表1
for i in range(table.nrows):#table.nrows表示总行数
    line=table.row_values(i)#读取每行数据，保存在line里面，line是list
    m.append(line)#将line加入到resArray中，resArray是二维list
m=np.array(m)#将resArray从二维list变成数组


[rows,cols]=m.shape
x=0
y=0
for i in range(rows):#行数range
    for j in range(cols):#列数range
        if m[i][x] == m[:,j][y] :#行的数值=列的数值时，将该行变成'1'（从list转成的array本来就全是str）
            m[i,j]='1'
for z in range(1,rows):#除去第一行（行头）
    for q in range(5,cols):#除去前5列（列头，不相关数据）
        if m[z, q] != '1':
            m[z,q] = 0
for b in range(1, rows):  # 除去第一行（行头）
    for c in range(5, cols):  # 除去前5列（列头，不相关数据）
        m[b,c]=int(m[b,c])
print(m)

data = pd.DataFrame(m)
writer = pd.ExcelWriter('/Users/zireael19andre/Movies/TubeGet/result.xlsx')		# 写入Excel文件
data.to_excel(writer, 'page_1', float_format='%.5f')		# ‘page_1’是写入excel的sheet名
writer.save()
writer.close()
print('All Done')
'''






