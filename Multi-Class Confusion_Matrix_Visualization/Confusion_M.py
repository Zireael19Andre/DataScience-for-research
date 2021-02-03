import matplotlib.pyplot as plt
from tongji import Detect_Acc,Severe_Acc,L1_True,L2_True,L3_True,L4_True,All,All_s,ture,ture_s
from plotcm import plot_confusion_matrix
import numpy as np
names = ('Level_1',
         'Level_2',
         'Level_3',
         'Level_4')
plt.figure(figsize=(5,5))
cm = np.array([L1_True,
               L2_True,
               L3_True,
               L4_True,]
              ).astype(int)
plot_confusion_matrix(cm, names)
plt.show()

n = len(cm)
truesum=[]

print('\nRecognition_Res:')
print('Total of',sum(All),'Buildings,of which',sum(ture),'buildings were detected. Overall Acc.:%.2f%%' % (Detect_Acc*100))
print('Total of',sum(All_s),'Severe Damaged Buildings,of which',sum(ture_s),'buildings were detected. Overall Acc.:%.2f%%' % (Severe_Acc*100))
print('\nClassification_Res:')
for i in range(len(cm[0])):
    rowsum, colsum = sum(cm[i]), sum(cm[r][i] for r in range(n))
    truesum.append(cm[i][i])
    Precision = cm[i][i]/float(colsum)
    Recall = cm[i][i]/float(rowsum)
    try:
        #print('Level',i+1,'Precision: %s' % (cm[i][i]/float(colsum)), 'Recall: %s' % (cm[i][i]/float(rowsum)),'F1-Score:%s' % () )
        print('Level', i + 1, 'Precision: %.2f%%' % (Precision*100), 'Recall: %.2f%%' % (Recall*100),'F1-Score:%.2f' % ((2*Precision*Recall/(Precision+Recall))))
    except ZeroDivisionError:
        print('Precision: %s' % 0, 'Recall: %s' %0, 'F1-Score: %s' % 'Null')
print('Overall Acc.: %.2f%%' % ((sum(truesum)/np.sum(cm))*100))