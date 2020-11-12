import numpy as np
import pandas as pd
from sklearn import linear_model

io = './wu/wu_new.csv'
df = pd.read_csv(io)
df_step1 = df.drop(columns=['teisu_step3','M_step3'])
header=np.array(df.columns)
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#print(header)


def loop1(self):
    x1 = df_step1.iloc[:, 1:1188]  # 等式右侧(第一步)[b0-c1183]
    x2 = df_step1.iloc[:, 1:1189]  # b0-c1184
    y = df_step1.iloc[:, 0]  # 等式左侧
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(x1, y)  # x=等式右边的项，y=log
    residual = clf.coef_  # 算出的所有系数
    c1184 = -sum(np.delete(residual, [0, 1, 2, 3]))  # c1184
    residual = np.append(residual, c1184)  # 全系数
    g = np.array(x2)
    [rows, cols] = g.shape  # 获取行列数
    for row in range(rows):
        g[row] = g[row] * residual
    # [g[row] == g[row] * residual for row in range(rows)]
    g = np.insert(g, 0, values=np.array(y), axis=1)
    for row in range(rows):
        g[row][0] = g[row][0] - sum(g[row][4:1189])
    m = pd.DataFrame(g)

    y = m.iloc[:, 0]
    step2 = df_step1.iloc[:, 1189:1222]
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(step2, y)  # x=等式左边的log项，y=b0位，初始为1
    residual_step2 = clf.coef_  # 算出step2的所有系数
    b2 = residual_step2[-1]

    aj = residual_step2[0:32]
    AJ = pd.DataFrame(aj)
    M = df[['teisu_step3', 'M_step3']]
    M = M.drop(M.index[32:])
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(M, AJ)  # x=等式右边的项，y=log
    residual_step3 = clf.coef_  # 算出的所有系数
    print(residual_step3)
    b1 = residual_step3[-1][-1]
    return b1,b2

def loop_more(b1,b2):
    rob = [b1, b2]
    rob_np = np.array(rob)
    x_l2 = df_step1.iloc[:, 2:4]
    y_l2 = df_step1.iloc[:, 0]
    g_l2 = np.array(x_l2)
    [rows, cols] = g_l2.shape  # 获取行列数
    for row in range(rows):
        g_l2[row] = g_l2[row] * rob_np
    g_l2 = np.insert(g_l2, 0, values=np.array(y_l2), axis=1)
    for row in range(rows):
        g_l2[row][0] = g_l2[row][0] - sum(g_l2[row][1:])
    y_l2_step1 = pd.DataFrame(g_l2).iloc[:, 0]
    tep_y1 = np.array(df_step1.iloc[:, 1])
    tep_y2 = df_step1.iloc[:, 4:1188]
    x_l2 = tep_y2
    x_l2.insert(loc=0, column='teisu(b0)', value=tep_y1)
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(x_l2, y_l2_step1)  # x=等式右边的项，y=log
    residual_l2 = clf.coef_  # 算出的所有系数
    c1184_l2 = -sum(np.delete(residual_l2, [0, 1]))  # c1184
    residual_l2 = np.append(residual_l2, c1184_l2)  # 全系数

    x2_l2 = df_step1.iloc[:, 4:1189]
    residual_l2 = np.delete(residual_l2, 0)
    g2_l2 = np.array(x2_l2).astype(np.float64)  # 是int64，需要转成float64，不然出来的结果就是0，（0。00几太小）
    [rows_l2, cols_l2] = g2_l2.shape  # 获取行列数
    for row in range(rows_l2):
        g2_l2[row] = g2_l2[row] * residual_l2
    g2_l2 = np.insert(g2_l2, 0, values=np.array(y_l2), axis=1)
    for row in range(rows):
        g2_l2[row][0] = g2_l2[row][0] - sum(g2_l2[row][1:])
    m_l2 = pd.DataFrame(g2_l2)
    y_l2_step2 = m_l2.iloc[:, 0]
    x_l2_step2 = df_step1.iloc[:, 1189:1222]
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(x_l2_step2, y_l2_step2)  # x=等式左边的log项，y=b0位，初始为1
    residual_l2_step2 = clf.coef_  # 算出step2的所有系数
    b2_l2 = residual_l2_step2[-1]

    aj = residual_l2_step2[0:32]
    AJ = pd.DataFrame(aj)
    M = df[['teisu_step3', 'M_step3']]
    M = M.drop(M.index[32:])
    clf = linear_model.LinearRegression(fit_intercept=False)  # 做回归分析，Bias 为0
    clf.fit(M, AJ)  # x=等式右边的项，y=log
    residual_l2_step3 = clf.coef_  # 算出的所有系数
    print(residual_l2_step3)
    b1_l2 = residual_l2_step3[-1][-1]
    # print(residual_l2,residual_l2_step2,residual_l2_step3)
    if output_modle == 1:
        return b1_l2, b2_l2
    if output_modle == 2:
        return residual_l2_step3.tolist(), b2_l2, residual_l2.tolist()

def flat(lists):
    res = []
    for i in lists:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res



p = []
compare_start = 0
count = 0
residual_finial = []
inp=int(input('Input your loop range:'))
for i in range(inp):
    if count == 0:
        p = list(loop1(1))
        count += 1
        print('Round:',count)
        compare_start=p[0]
        continue
    if count == 1:
        b1 = p[0]
        b2 = p[1]
        output_modle = 1
        compare_start = b1
        p = list(loop_more(b1, b2))
        count += 1
        print('Round:',count)
    if count >= 1:
        b1 = p[0]
        b2 = p[1]
        output_modle = 1
        if abs(1.0 - b1/compare_start) > 0.00001 and count == inp:
            compare_start = b1
            p = list(loop_more(b1,b2))
            print('B1 still unstable in this range, It ends up with', p[0], ',Plz try a bigger range.')
        elif abs(1.0 - b1/compare_start) > 0.00001:
            compare_start = b1
            p = list(loop_more(b1,b2))
            count += 1
            print('Round:',count)
        elif abs(1.0 - b1/compare_start) < 0.00001 and count > 1:
            compare_start = b1
            output_modle = 2
            residual_finial = list(loop_more(b1,b2))
            residual_finial = flat(residual_finial)
            print('Round:',count+1)
            print('B1_N:',residual_finial[1])
            print('B1_N-1:',compare_start)
            print('All residual result(b0-b2,b4-c1184[',len(residual_finial),']):','\n',residual_finial)
            break
print('\n\nAll Finished')
