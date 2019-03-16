# encoding: utf-8
import itertools
import random
import matplotlib.pyplot as plt
import numpy as np
import HeatMap as HM

poissonFlag = True
normalFlag = True
uniformFlag = True
# 电单车节点的个数
NodeNum = 40000
# 电单车运动区域的大小单位m
EdgeLight = 500

if poissonFlag is True:
	# 充电节点按泊松分布
	x = np.zeros([1, NodeNum], dtype = np.float)
	y = np.zeros([1, NodeNum], dtype = np.float)
	# lam 是对称轴，算均值， size是要生成点的个数
	x1 = np.random.poisson(lam = EdgeLight/10.0, size = int(NodeNum/4.0))
	print "x1 =", x1
	print "type(x1) =", type(x1)
	y1 = np.random.poisson(lam = EdgeLight/10.0, size = int(NodeNum/4.0))
	print "y1 =", y1 

	x2 = np.random.poisson(lam = EdgeLight*2/5.0, size = int(NodeNum/4.0))
	print "x2 =", x2
	print "type(x2) =", type(x2)
	y2 = np.random.poisson(lam = EdgeLight*3/5.0, size = int(NodeNum/4.0))
	print "y2 =", y2 

	x3 = np.random.poisson(lam = EdgeLight*3/5.0, size = int(NodeNum/4.0))
	print "x3 =", x3
	print "type(x3) =", type(x3)
	y3 = np.random.poisson(lam = EdgeLight*3/5.0, size = int(NodeNum/4.0))
	print "y3 =", y3 

	x4 = np.random.poisson(lam = EdgeLight*3/5.0, size = int(NodeNum/4.0))
	print "x4 =", x4
	print "type(x4) =", type(x4)
	y4 = np.random.poisson(lam = EdgeLight*4/5.0, size = int(NodeNum/4.0))
	print "y4 =", y4 


	for i in range(0, len(x1)):
		x[0][i] = x1[i]
		y[0][i] = y1[i]
	i = 0
	for j in range(len(x1), len(x2) + len(x1)):
		x[0][j] = x2[i]
		y[0][j] = y2[i]
		i = i + 1
		if i == len(x2):
			break
	i = 0
	for k in range(len(x2) + len(x1), len(x2) + len(x1) + len(x3)):
		x[0][k] = x3[i]
		y[0][k] = y3[i]
		i = i + 1
		if i == len(x3):
			break
	i = 0
	for m in range(len(x2) + len(x1) + len(x3), len(x2) + len(x1) + len(x3)+ len(x4)):
		x[0][m] = x4[i]
		y[0][m] = y4[i]
		i = i + 1
		if i == len(x4):
			break

	plt.scatter(x,y)
	plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(x[0])):
		x_new.append(x[0][i])
		y_new.append(y[0][i])
	# 画节点分布的热力图
	HM.draw_heatmap(x_new, y_new)
if normalFlag is True:
	# 充电节点按正态分布或者高斯分布
	# loc 是均值【对称轴】
	# scale 为标准差【越小，产生的数据点越靠近对称轴】
	# size 是要生成点的个数
	# numpy.random.normal(loc=0.0, scale=1.0, size=None)

	x = np.zeros([1, NodeNum], dtype = np.float)
	y = np.zeros([1, NodeNum], dtype = np.float)
	# lam 是对称轴，算均值， size是要生成点的个数
	x1 = np.random.normal(EdgeLight/5.0, 1, size = int(NodeNum/4.0))
	print "x1 =", x1
	print "type(x1) =", type(x1)
	y1 = np.random.normal(EdgeLight/5.0, 1, size = int(NodeNum/4.0))
	print "y1 =", y1 

	x2 = np.random.normal(EdgeLight*2/5.0, 1, size = int(NodeNum/4.0))
	print "x2 =", x2
	print "type(x2) =", type(x2)
	y2 = np.random.normal(EdgeLight/5.0, 1, size = int(NodeNum/4.0))
	print "y2 =", y2 

	x3 = np.random.normal(EdgeLight*3/5.0, 1, size = int(NodeNum/4.0))
	print "x3 =", x3
	print "type(x3) =", type(x3)
	y3 = np.random.normal(EdgeLight*2/5.0, 1, size = int(NodeNum/4.0))
	print "y3 =", y3 

	x4 = np.random.normal(EdgeLight*4/5.0, 1, size = int(NodeNum/4.0))
	print "x4 =", x4
	print "type(x4) =", type(x4)
	y4 = np.random.normal(EdgeLight*3/5.0, 1, size = int(NodeNum/4.0))
	print "y4 =", y4 


	for i in range(0, len(x1)):
		x[0][i] = x1[i]
		y[0][i] = y1[i]
	i = 0
	for j in range(len(x1), len(x2) + len(x1)):
		x[0][j] = x2[i]
		y[0][j] = y2[i]
		i = i + 1
		if i == len(x2):
			break
	i = 0
	for k in range(len(x2) + len(x1), len(x2) + len(x1) + len(x3)):
		x[0][k] = x3[i]
		y[0][k] = y3[i]
		i = i + 1
		if i == len(x3):
			break
	i = 0
	for m in range(len(x2) + len(x1) + len(x3), len(x2) + len(x1) + len(x3)+ len(x4)):
		x[0][m] = x4[i]
		y[0][m] = y4[i]
		i = i + 1
		if i == len(x4):
			break

	plt.scatter(x,y)
	plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(x[0])):
		x_new.append(x[0][i])
		y_new.append(y[0][i])
	# 画节点分布的热力图
	HM.draw_heatmap(x_new, y_new)

if uniformFlag is True:
	# 节点按均匀分布
	# low为坐标下限
	# high为坐标上限
	# size为节点个数
	# numpy.random.uniform(low=0.0, high=1.0, size=None)
	x = np.random.uniform(1, EdgeLight, NodeNum)
	y = np.random.uniform(1, EdgeLight, NodeNum)
	plt.scatter(x,y)
	plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(x)):
		x_new.append(x[i])
		y_new.append(y[i])
	# 画节点分布的热力图
	HM.draw_heatmap(x_new, y_new)