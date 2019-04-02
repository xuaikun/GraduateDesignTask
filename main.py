# encoding: utf-8
import os
import random
import itertools
import numpy as np
import HeatMap as HM
import TourFunction as TF
import matplotlib.pyplot as plt
import CliquePartitionAlgorithm as CP

# 打印测试信息的标志位
DebugFlag = False

result_path = "E:\\00000000000graduate-study\\GraduateDesignTask\\result"
# 使用备份数据的标志，False不使用，True使用
DataBackup = True
# 是否使用同一组障碍信息，False无备份障碍数据，True有障碍数据
ObstacleBackup = True
# 三种分布的标志，True为选择该分布，False表示不选择该分布
poissonFlag = False
normalFlag = False
uniformFlag = True 

# 电单车节点的个数
NodeNum = 10
# 电单车运动区域的大小单位m
EdgeLength = 500
# 障碍个数
ObstaclesNum = 20
# 障碍边长
ObstacleLength = 20

# 假设的,需要修改的，目前太大了
# Distance = (EdgeLength/10.0)*np.sqrt(2)
Distance = 121.3
# Normal_scale为正态分布的标准差【越小，产生的数据点越靠近对称轴】，最小值大概为1
# 标准差越大电单车节点越分散
Normal_scale = 70
# Normal_scale = 2
# 坐标刻度
CoordinateScale = 100
# 扩大到障碍外围至少+1m处
ObstacleExpand = 1

# 障碍坐标范围
ObstacleXDown = np.empty([1, ObstaclesNum], int)
ObstacleXUp   = np.empty([1, ObstaclesNum], int)
ObstacleYDown = np.empty([1, ObstaclesNum], int)
ObstacleYUp   = np.empty([1, ObstaclesNum], int)



# 判断路径是否存在
isExist = os.path.exists(result_path)
if not isExist:
    print "不存在该路径，创建对应路径"
    os.makedirs(result_path)
# 自主修改数据结果子的根目录
result_name = 'Node_' + str(int(NodeNum))
result_name = os.path.join(result_path, result_name)
isExist = os.path.exists(result_name)
if not isExist:
    print "不存在该路径，创建对应路径"
    os.makedirs(result_name)

# poisson
# normal
# uniform
# 自主修改数据结果子的子目录
poisson_path = 'poisson'
poisson_path = os.path.join(result_name, poisson_path)
isExist = os.path.exists(poisson_path)
if not isExist:
    print "不存在该路径，创建对应路径"
    os.makedirs(poisson_path)

normal_path = 'normal'
normal_path = os.path.join(result_name, normal_path)
isExist = os.path.exists(normal_path)
if not isExist:
    print "不存在该路径，创建对应路径"
    os.makedirs(normal_path)

uniform_path = 'uniform'
uniform_path = os.path.join(result_name, uniform_path)
isExist = os.path.exists(uniform_path)
if not isExist:
    print "不存在该路径，创建对应路径"
    os.makedirs(uniform_path)

Obstacle_information_data_txt = os.path.join(result_name, 'Obstacle_information_data.txt')
Node_poisson_information_data_txt = os.path.join(poisson_path, 'Node_poisson_information_data.txt')
Node_normal_information_data_txt = os.path.join(normal_path, 'Node_normal_information_data.txt')
Node_uniform_information_data_txt = os.path.join(uniform_path, 'Node_uniform_information_data.txt')

NodeAdjacencyMatrix_poisson_data_txt = os.path.join(poisson_path, 'NodeAdjacencyMatrix_data.txt')
NodeAdjacencyMatrix_normal_data_txt = os.path.join(normal_path, 'NodeAdjacencyMatrix_data.txt')
NodeAdjacencyMatrix_uniform_data_txt = os.path.join(uniform_path, 'NodeAdjacencyMatrix_data.txt')

# Add Virtual Node
def AddVirtualNode(Coordinate, Coordinatex_New, Coordinatey_New, ObstacleCoordinate, ObstaclesNum, NodeList):
	# 在这里我已经获取了所有节点x坐标集合Coordinate[0]，y坐标集合Coordinate[1]，以及障碍区域的信息
	# 统计之前生成了多少个节点的坐标
	CoordinateLen = len(Coordinate[0])
	
	for l in range(0, CoordinateLen):
		Coordinatex_New.append(Coordinate[0][l])
		Coordinatey_New.append(Coordinate[1][l])
	for i in range(0, CoordinateLen):
		for j in range(i + 1, CoordinateLen):
			# 第一个节点的坐标
			Coordinate[0][i]	# x坐标
			Coordinate[1][i]	# y坐标

			# 第二个节点坐标
			Coordinate[0][j]	# x坐标
			Coordinate[1][j]	# y坐标
			# 添加x坐标序列
			polyfitx = []
			# 添加y坐标序列
			polyfity = []
			polyfitx.append(Coordinate[0][i])
			polyfitx.append(Coordinate[0][j])
			polyfity.append(Coordinate[1][i])
			polyfity.append(Coordinate[1][j])
			# x与y的函数关系
			fxy = np.polyfit(polyfitx, polyfity, 1)
			# y与x的函数关系
			fyx = np.polyfit(polyfity, polyfitx, 1)
			# x与y的函数方程
			pxy = np.poly1d(fxy)
			# y与x的函数方程
			pyx = np.poly1d(fyx)
			if DebugFlag is True:
				print "已经获得函数方程"
				print "pxy =", pxy
				print "pyx =", pyx
			# 准备对障碍区域一一测试
			# ObstacleCoordinate
			ObstacleXDown[0] = ObstacleCoordinate[0]
			# print "ObstacleXDown[0] =\n", ObstacleXDown[0]
			ObstacleXUp[0]   = ObstacleCoordinate[1]
			# print "ObstacleXUp[0] =\n", ObstacleXUp[0]
			ObstacleYDown[0] = ObstacleCoordinate[2]
			# print "ObstacleYDown[0] =\n", ObstacleYDown[0]
			ObstacleYUp[0]   = ObstacleCoordinate[3]
			# print "ObstacleYUp[0] =\n", ObstacleYUp[0]
			# 对于障碍区域依次循环检测，决定是否添加虚拟节点
			for k in range(0, ObstaclesNum):
				# 当前障碍的四个点的对应的横坐标和纵坐标
				# 左下角坐标
				ObstacleXDown[0][k]
				ObstacleYDown[0][k]
				# 左上角坐标
				ObstacleXDown[0][k]
				ObstacleYUp[0][k]
				# 右下角坐标
				ObstacleXUp[0][k]
				ObstacleYDown[0][k]
				# 右上角坐标
				ObstacleXUp[0][k]
				ObstacleYUp[0][k]
				# 对4条边进行操作
				# 保存交点的序列
				Intersectionx = []
				Intersectiony = []
				Nodei = Coordinate[0][i]	# i节点的x坐标
				Nodej = Coordinate[0][j]    # j节点的x坐标
				Maxx = Nodej
				Minx = Nodei 
				# 两个坐标的x坐标值把大小区分一下
				if Nodei > Nodej:
					Maxx = Nodei
					Minx = Nodej
				if (ObstacleXUp[0][k] < Minx) or (ObstacleXDown[0][k] > Maxx):
					print "no exists Obstacle at i and j"
				else:
					print "exists Obstacle at i and j"
					for m in range(0, 4):
						if m == 0:
							print "detect left"
							xleft = ObstacleXDown[0][k]
							# 测试结果取2位小数
							print "pxy(xleft) =", round(pxy(xleft), 2)
							virtualx = xleft
							virtualy = round(pxy(xleft), 2)
								
							if (virtualy < ObstacleYDown[0][k]) or (virtualy > ObstacleYUp[0][k]):
								print "no exists Intersection at left"
							else:
								print "exists Intersection at left"
								Intersectionx.append(virtualx)
								Intersectiony.append(virtualy)
								print "Intersection =", (virtualx, virtualy)
						
						elif m == 1:
							print "detect right"
							xright = ObstacleXUp[0][k]
							# 测试结果取2位小数
							print "pxy(xright) =", round(pxy(xright), 2)
							virtualx = xright
							virtualy = round(pxy(xright), 2)
								
							if(virtualy < ObstacleYDown[0][k]) or (virtualy > ObstacleYUp[0][k]):
								print "no exists Intersection at right"		
							else:
								print "exists Intersection at right"
								Intersectionx.append(virtualx)
								Intersectiony.append(virtualy)
								print "Intersection =", (virtualx, virtualy)
						
						elif m == 2:
							print "detect top"
							yUp = ObstacleYUp[0][k] 
							# 测试结果取2位小数
							print "pyx(yUp) =", round(pyx(yUp), 2)
							virtualy = yUp
							virtualx = round(pyx(yUp), 2)
							if (virtualx < ObstacleXDown[0][k]) or (virtualx > ObstacleXUp[0][k]):
								print "no exists Intersection at top"
							else:
								print "exists Intersection at top"
								Intersectionx.append(virtualx)
								Intersectiony.append(virtualy)
								print "Intersection =", (virtualx, virtualy)

						elif m == 3:
							print "detect down"
							ydown = ObstacleYDown[0][k]
							# 测试结果取2位小数
							print "pyx(ydown) =", round(pyx(ydown), 2)
							virtualy = ydown
							virtualx = round(pyx(ydown), 2)
							
							if (virtualx < ObstacleXDown[0][k]) or (virtualx > ObstacleXUp[0][k]):
								print "no exists Intersection at down"
							else:
								print "exists Intersection at down"
								Intersectionx.append(virtualx)
								Intersectiony.append(virtualy)
								print "Intersection =", (virtualx, virtualy)
					if len(Intersectionx) > 0:
						# 仅当出现交点才需要检查交点信息，并且最多有两个交点
						
						if DebugFlag is True:
							print "i =", i
							print "j =", j
							print "Intersectionx =", Intersectionx
							print "Intersectiony =", Intersectiony
						virtualx = (Intersectionx[0] + Intersectionx[len(Intersectionx) - 1])/2.0
						virtualy = (Intersectiony[0] + Intersectiony[len(Intersectiony) - 1])/2.0

						# 这里还得做个判断，产生的虚拟节点，应该只能存在于两个节点之间
						Maxx  	# 两个节点中x大的
						Minx 	# 两个节点中x小的
						# 第一个节点的坐标
						Coordinate[0][i]	# x坐标
						Coordinate[1][i]	# y坐标

						# 第二个节点坐标
						Coordinate[0][j]	# x坐标
						Coordinate[1][j]	# y坐标
						# virtualx不再两个节点之间的最大
						if (Minx < virtualx) and (virtualx < Maxx):
							# 虚拟节点到两个点的距离不能大于设定的Distance，因为它的存在变得无所谓了
							# 这样可以大大减少计算量
							# 好好想想这里需要使用的是什么距离，需要用A_Star算法解决吗？
							if (np.sqrt(np.power((virtualx - Coordinate[0][i]), 2) + np.power((virtualy - Coordinate[1][i]), 2)) < Distance
								) and (np.sqrt(np.power((virtualx - Coordinate[0][j]), 2) + np.power((virtualy - Coordinate[1][j]), 2)) < Distance):
								if DebugFlag is True:
									print "New node's Coordinate =", (virtualx, virtualy)
									print "NodeList =", NodeList 
								NodeList.append(NodeList[len(NodeList) - 1] + 1)
								if DebugFlag is True:
									print "NodeList =", NodeList
									print "Coordinate[0] =\n", Coordinate[0]
									print "Coordinate[1] =\n", Coordinate[1]
								Coordinatex_New.append(round(virtualx, 2))
								Coordinatey_New.append(round(virtualy, 2))
								if DebugFlag is True:
									print "Coordinatex_New =\n", Coordinatex_New
									print "Coordinatey_New =\n", Coordinatey_New
	

# deleteVirtualNode
def DeleteVirtualNode(CliqueResult):
	len(CliqueResult) # 节点群集合
	DeleteNullCluste = []
	for i in range(0, len(CliqueResult)):
		# 获取其中一个节点群集合,将标号大于NodeNum - 1的节点从节点群中删掉
		CliqueR_list = CliqueResult[i]
		delete_list = []
		for j in range(0, len(CliqueR_list)):
			if CliqueR_list[j] >= NodeNum:
				# 统计需要删除的节点
				delete_list.append(CliqueR_list[j])
		# 循环删除delete_list中的节点
		for j in range(0, len(delete_list)):
			CliqueR_list.remove(delete_list[j])
		if len(CliqueR_list) == 0:
			# 如果当前的电单车节点集群中不存在节点，
			# 意味着它为空节点集群，需要删掉
			DeleteNullCluste.append(CliqueR_list)
	# 删掉空的节点集群
	for j in range(0, len(DeleteNullCluste)):
		CliqueResult.remove(DeleteNullCluste[j])
	return

# add Xcoordinate and Ycoordinate
def AddXandYCoordinate(Coordinate, Coordinate_new, NodeNum):
	NodeXCoordinate = np.empty([1, NodeNum], float)
	NodeYCoordinate = np.empty([1, NodeNum], float)
	NodeXCoordinate[0] = Coordinate_new[0]
	NodeYCoordinate[0] = Coordinate_new[1]
	Coordinate.append(Coordinate_new[0])
	Coordinate.append(Coordinate_new[1])
	Coordinate.append(NodeXCoordinate)
	Coordinate.append(NodeYCoordinate)
	return Coordinate
# 检查节点坐标是否出现异常
def CheckCoordinate(x, y, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand):
	ObstacleXDown[0] = ObstacleCoordinate[0]
	print "ObstacleXDown[0] =\n", ObstacleXDown[0]
	ObstacleXUp[0]   = ObstacleCoordinate[1]
	print "ObstacleXUp[0] =\n", ObstacleXUp[0]
	ObstacleYDown[0] = ObstacleCoordinate[2]
	print "ObstacleYDown[0] =\n", ObstacleYDown[0]
	ObstacleYUp[0]   = ObstacleCoordinate[3]
	print "ObstacleYUp[0] =\n", ObstacleYUp[0]
	# 判断节点群中是否有传感器节点被部署到障碍上了
	# 电单车节点随机放
    # 如果x或者y越界了，则需要重新生成该节点的坐标一部分或者全部，该坐标一定不可以越界
	
    # j为终止条件，即判断是否比较到最后一个障碍区域
	# 要判断当前生成节点是否存在某一个障碍里面，所以要与每一个障碍区域进行比较
        
	i = 0
	for i in range(0, len(x)):
		# print "i =", i
		# print "hello "
		if (x[i]<=0 or x[i]>= EdgeLength): 
			x[i] = round(random.uniform(1, EdgeLength), 2)

		if (y[i]<=0 or y[i]>= EdgeLength): 
			y[i] = round(random.uniform(1, EdgeLength), 2)
		j = 0
		# print "j =", j
		# print "ObstaclesNum =", ObstaclesNum
		while(j != ObstaclesNum):
			# j_temp 为一个中间转换值
			j_temp = j
			# 存在障碍的表示，初始化时假设变动后后的坐标处于障碍里面 EqualFlag = True表示生成的节点在障碍区域内
			EqualFlag = True
			ObstacleXDownBackup = ObstacleXDown[0][j_temp].copy()
			ObstacleXUpBackup = ObstacleXUp[0][j_temp].copy()
			ObstacleYDownBackup = ObstacleYDown[0][j_temp].copy()
			ObstacleYUpBackup = ObstacleYUp[0][j_temp].copy()
			ObstacleXDownBackup = ObstacleXDownBackup -ObstacleExpand
			ObstacleXUpBackup = ObstacleXUpBackup + ObstacleExpand
			ObstacleYDownBackup = ObstacleYDownBackup - ObstacleExpand
			ObstacleYUpBackup = ObstacleYUpBackup + ObstacleExpand
			# print "x[", i, "] =", x[i]
			# print "y[", i, "] =", y[i]
			# 电单车坐标的设置，扩大到障碍外围至少+1m处
			if((x[i] > (ObstacleXDownBackup)) and (x[i] < (ObstacleXUpBackup))) and(
			    (y[i] > (ObstacleYDownBackup)) and (y[i] < (ObstacleYUpBackup))):
				# 表示有电单车在障碍区域里面了，不符合,更新当前电单车坐标并与障碍区域意义比较
				# 中间值j_temp每次加1
				j_temp = j_temp + 1
				if EqualFlag is True:
					# print "change Coordinate before"
					# print "x[", i, "] =", x[i]
					# print "y[", i, "] =", y[i]
					x[i] = round(random.uniform(1, EdgeLength), 2)
					y[i] = round(random.uniform(1, EdgeLength), 2)
					# print "after"
					# print "x[", i, "] =", x[i]
					# print "y[", i, "] =", y[i]
					j_temp = 0
					j = 0
				EqualFlag  = False
				# 表示已经比较到最后一个障碍区域
				if j_temp >= ObstaclesNum:
					j = j_temp 
					# 退出while（）
					break
			else:
				# 表示坐标不在障碍区域内，进入比较下一个坐标
				j = j + 1
				# 当前坐标已经比较到看最后一个障碍区域
				if j >= ObstaclesNum:
					# 退出while
					break
	result = []
	result.append(x)
	result.append(y)
	return result

# 合并节点坐标
def MergeCoordinate(NodeXCoordinate, NodeYCoordinate, x1, y1, x2, y2, x3, y3, x4, y4):
	for i in range(0, len(x1)):
		NodeXCoordinate[0][i] = x1[i]
		NodeYCoordinate[0][i] = y1[i]
	i = 0
	for j in range(len(x1), len(x2) + len(x1)):
		NodeXCoordinate[0][j] = x2[i]
		NodeYCoordinate[0][j] = y2[i]
		i = i + 1
		if i == len(x2):
			break
	i = 0
	for k in range(len(x2) + len(x1), len(x2) + len(x1) + len(x3)):
		NodeXCoordinate[0][k] = x3[i]
		NodeYCoordinate[0][k] = y3[i]
		i = i + 1
		if i == len(x3):
			break
	i = 0
	for m in range(len(x2) + len(x1) + len(x3), len(x2) + len(x1) + len(x3)+ len(x4)):
		NodeXCoordinate[0][m] = x4[i]
		NodeYCoordinate[0][m] = y4[i]
		i = i + 1
		if i == len(x4):
			break
	result = []
	result.append(NodeXCoordinate)
	result.append(NodeYCoordinate)
	return result

# 泊松分布
def Poisson(NodeNum, EdgeLength, ObstacleCoordinate):
	print "Poisson"
	NodeSum = 0
	# 先前的一个集群点中节点的额个数为int(NodeNum/4.0)
	NodePart = int(NodeNum/4.0)
	# 先前3部分节点的总和
	NodeSum = 3*NodePart
	# 剩余节点
	LastNode = NodeNum - NodeSum
	# 充电节点按泊松分布
	NodeXCoordinate = np.empty([1, NodeNum], float)
	NodeYCoordinate = np.empty([1, NodeNum], float)
	# lam 是对称轴，算均值， size是要生成点的个数
	x1 = np.random.poisson(lam = EdgeLength/5.0, size = NodePart)
	y1 = np.random.poisson(lam = EdgeLength/9.0, size = NodePart) 
	# 判断节点群中是否有传感器节点被部署到障碍上了
	result = CheckCoordinate(x1, y1, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x1 = result[0]
	y1 = result[1]

	x2 = np.random.poisson(lam = EdgeLength*2/5.0, size = NodePart)
	y2 = np.random.poisson(lam = EdgeLength*3/5.0, size = NodePart)

	# 判断节点群中是否有传感器节点被部署到障碍上了
	result = CheckCoordinate(x2, y2, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x2 = result[0]
	y2 = result[1]

	x3 = np.random.poisson(lam = EdgeLength*3/5.0, size = NodePart)
	y3 = np.random.poisson(lam = EdgeLength*3/5.0, size = NodePart)

	# 判断节点群中是否有传感器节点被部署到障碍上了
	result = CheckCoordinate(x3, y3, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x3 = result[0]
	y3 = result[1]

	x4 = np.random.poisson(lam = EdgeLength*3/5.0, size = LastNode)
	y4 = np.random.poisson(lam = EdgeLength/5.0, size = LastNode)

	# 判断节点群中是否有传感器节点被部署到障碍上了
	result = CheckCoordinate(x4, y4, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x4 = result[0]
	y4 = result[1]
	
	result = MergeCoordinate(NodeXCoordinate, NodeYCoordinate, x1, y1, x2, y2, x3, y3, x4, y4)
	NodeXCoordinate = result[0]
	NodeYCoordinate = result[1]

	# plt.scatter(NodeXCoordinate, NodeYCoordinate)
	# plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(NodeXCoordinate[0])):
		x_new.append(NodeXCoordinate[0][i])
		y_new.append(NodeYCoordinate[0][i])
	# 画节点分布的热力图
	HM.draw_heatmap(x_new, y_new)
	result = []
	result.append(x_new)
	result.append(y_new)
	result.append(NodeXCoordinate)
	result.append(NodeYCoordinate)
	return result

# 高斯分布
def Normal(NodeNum, EdgeLength, ObstacleCoordinate):
	print "Normal"
	# 充电节点按正态分布或者高斯分布
	# loc 是均值【对称轴】Normal_scale
	# scale 为标准差【越小，产生的数据点越靠近对称轴】
	# size 是要生成点的个数
	# numpy.random.normal(loc=0.0, scale=1.0, size=None)

	NodeXCoordinate = np.empty([1, NodeNum], float)
	NodeYCoordinate = np.empty([1, NodeNum], float)
	# 先前的一个集群点中节点的额个数为int(NodeNum/4.0)
	NodePart = int(NodeNum/4.0)
	# 先前3部分节点的总和
	NodeSum = 3*NodePart
	# 剩余节点
	LastNode = NodeNum - NodeSum
	# lam 是对称轴，算均值， size是要生成点的个数
	x1 = np.random.normal(EdgeLength/5.0, Normal_scale, size = NodePart)
	y1 = np.random.normal(EdgeLength/5.0, Normal_scale, size = NodePart)
	# 判断节点群中是否有传感器节点被部署到障碍上了
	result = CheckCoordinate(x1, y1, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x1 = result[0]
	y1 = result[1]
	
	x2 = np.random.normal(EdgeLength*2/5.0, Normal_scale, size = NodePart)
	y2 = np.random.normal(EdgeLength/5.0, Normal_scale, size = NodePart)

	result = CheckCoordinate(x2, y2, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x2 = result[0]
	y2 = result[1]

	x3 = np.random.normal(EdgeLength*3/5.0, Normal_scale, size = NodePart)
	y3 = np.random.normal(EdgeLength*2/5.0, Normal_scale, size = NodePart)

	result = CheckCoordinate(x3, y3, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x3 = result[0]
	y3 = result[1]

	x4 = np.random.normal(EdgeLength*4/5.0, Normal_scale, size = LastNode)
	y4 = np.random.normal(EdgeLength*3/5.0, Normal_scale, size = LastNode)

	result = CheckCoordinate(x4, y4, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x4 = result[0]
	y4 = result[1]

	result = MergeCoordinate(NodeXCoordinate, NodeYCoordinate, x1, y1, x2, y2, x3, y3, x4, y4)
	NodeXCoordinate = result[0]
	NodeYCoordinate = result[1]

	# plt.scatter(NodeXCoordinate, NodeYCoordinate)
	# plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(NodeXCoordinate[0])):
		x_new.append(NodeXCoordinate[0][i])
		y_new.append(NodeYCoordinate[0][i])
	# 画节点分布的热力图
	# HM.draw_heatmap(x_new, y_new)
	result = []
	result.append(x_new)
	result.append(y_new)
	result.append(NodeXCoordinate)
	result.append(NodeYCoordinate)
	return result

# 均匀分布
def Uniform(NodeNum_new, EdgeLength, ObstacleCoordinate):
	print "Uniform"
	# 障碍坐标区域，
	ObstacleXDown[0] = ObstacleCoordinate[0]
	ObstacleXUp[0]   = ObstacleCoordinate[1]
	ObstacleYDown[0] = ObstacleCoordinate[2]
	ObstacleYUp[0]   = ObstacleCoordinate[3]
	# 节点按均匀分布
	# low为坐标下限
	# high为坐标上限
	# size为节点个数
	# numpy.random.uniform(low=0.0, high=1.0, size=None)
	# 随机在二维空间中生成NodeNum辆电单车的坐标
    # 将生成的电单车坐标分别保存到x,y列表中# 保证电单车不在障碍区域内
	# 初始化电单车在二维空间中的坐标
	NodeXCoordinate = np.empty([1, NodeNum], float)
	NodeYCoordinate = np.empty([1, NodeNum], float)
	# low 是最小值，high为最大值， size是要生成点的个数
	# numpy.random.uniform(low=0.0, high=1.0, size=None)
	x = np.random.uniform(1, EdgeLength, size = NodeNum)
	y = np.random.uniform(1, EdgeLength, size = NodeNum)
	# 判断节点坐标是否越界
	result = CheckCoordinate(x, y, EdgeLength, ObstacleCoordinate, ObstaclesNum, ObstacleExpand)
	x = result[0]
	y = result[1]
	
	for i in range(0, len(x)):
		NodeXCoordinate[0][i] = x[i]
		NodeYCoordinate[0][i] = y[i]

	# plt.scatter(NodeXCoordinate, NodeYCoordinate)
	# plt.show()
	x_new = []
	y_new = []

	for i in range(0, len(NodeXCoordinate[0])):
		x_new.append(NodeXCoordinate[0][i])
		y_new.append(NodeYCoordinate[0][i])
	# 画节点分布的热力图
	# HM.draw_heatmap(x_new, y_new)
	
	result = []
	result.append(x_new)
	result.append(y_new)
	result.append(NodeXCoordinate)
	result.append(NodeYCoordinate)
	return result

# 构建邻接矩阵
def AdjacencyMatrix(NodeNum, Coordinate, Road_information, N_distance, ObstacleCoordinate, ObstaclesNum):
	# 提取坐标
	CoordinateX = Coordinate[2]
	CoordinateY = Coordinate[3]
	NodeList = []
	for i in range(0, NodeNum):
		NodeList.append(i)
	print "NodeList =\n", NodeList
	# 节点之间的实际路径，节点之间的距离，空间的长度，节点x坐标序列，节点y坐标序列，节点序号，剩余节点序号，障碍，障碍数量
	# 在障碍空间中计算节点之间的距离
	print "Statistic the Distance:"
	N_distance_Road_result = TF.CreateDistanceNewMatrix(Road_information, N_distance, EdgeLength, CoordinateX, CoordinateY, NodeList, NodeList, ObstacleCoordinate, ObstaclesNum)
	# 节点的距离
	N_distance = N_distance_Road_result[0]
	print "Distance =", Distance
	print "N_distance =\n", N_distance
	# 节点运动的实际路径
	Road_information = N_distance_Road_result[1]

	NodeAdjacencyMatrix = np.zeros([NodeNum, NodeNum], dtype = np.int)
	for i in range(0, NodeNum):
		for j in range(i, NodeNum):
			# 对角线的地方邻接矩阵的值为0
			if i == j:
				NodeAdjacencyMatrix[i][j] = 0
			# 不属于对角线的地方，按照距离来确定是否赋值1或0
			else:
				# 用欧几里得距离判断，这样就没现实场景的效果了
				# if np.sqrt(np.power((CoordinateX[i] - CoordinateX[j]),2) + np.power((CoordinateY[i] - CoordinateY[j]), 2)) < Distance:
				# 用A*算法求得的实际距离，小于该距离的，对应在邻接矩阵中的值为1
				if N_distance[i][j] < Distance:
					NodeAdjacencyMatrix[i][j] = 1
					NodeAdjacencyMatrix[j][i] = NodeAdjacencyMatrix[i][j]  
				# 两辆电单车的距离过大，表示不能用同一个充电桩进行充电
				else:
					NodeAdjacencyMatrix[i][j] = 0
					NodeAdjacencyMatrix[j][i] = NodeAdjacencyMatrix[i][j]
	return NodeAdjacencyMatrix

# 初始化数据
def Init(ObstaclesNum, EdgeLength, ObstacleLength):
	# 设置平面中的障碍
	# 返回障碍区域即：障碍的坐标
	if ObstacleBackup is False:
		ObstacleCoordinate = TF.SetObstacles(ObstaclesNum, EdgeLength, ObstacleLength)
		# 以整形保存
		np.savetxt(Obstacle_information_data_txt, ObstacleCoordinate, fmt='%d')
	if ObstacleBackup is True:
		ObstacleCoordinate = np.loadtxt(Obstacle_information_data_txt, dtype = np.int)
	# 电单车节点坐标序列初始化
	Coordinate = 1
	# 泊松分布
	if poissonFlag is True:
		Coordinate = Poisson(NodeNum, EdgeLength, ObstacleCoordinate)
		# 保存节点相关数据
		data = []
		data.append(Coordinate[0])
		data.append(Coordinate[1])
		np.savetxt(Node_poisson_information_data_txt, data, fmt='%0.2f')
	# 高斯分布
	if normalFlag is True:
		Coordinate = Normal(NodeNum, EdgeLength, ObstacleCoordinate)
		# 保存节点相关数据
		data = []
		data.append(Coordinate[0])
		data.append(Coordinate[1])
		np.savetxt(Node_normal_information_data_txt, data, fmt='%0.2f')
	# 均匀分布
	if uniformFlag is True:
		Coordinate = Uniform(NodeNum, EdgeLength, ObstacleCoordinate)
		# 保存节点相关数据
		data = []
		data.append(Coordinate[0])
		data.append(Coordinate[1])
		np.savetxt(Node_uniform_information_data_txt, data, fmt='%0.2f')
	result = []
	result.append(ObstacleCoordinate)
	result.append(Coordinate)
	return result

# 使用备份数据
def UseDataBackup(poissonFlag, normalFlag, uniformFlag, NodeNum):
	ObstacleCoordinate = np.loadtxt(Obstacle_information_data_txt, dtype = np.int)
	Coordinate = []
	# 泊松分布
	if poissonFlag is True:
		print "poisson"
		Coordinate_new = np.loadtxt(Node_poisson_information_data_txt)
		# 初始化电单车在二维空间中的坐标
		Coordinate = AddXandYCoordinate(Coordinate, Coordinate_new, NodeNum)
		
	# 高斯分布
	if normalFlag is True:
		print "normal"
		Coordinate_new = np.loadtxt(Node_normal_information_data_txt)
		# 初始化电单车在二维空间中的坐标
		Coordinate = AddXandYCoordinate(Coordinate, Coordinate_new, NodeNum)
		
	# 均匀分布
	if uniformFlag is True:
		print "uniform"
		Coordinate_new = np.loadtxt(Node_uniform_information_data_txt)
		# 初始化电单车在二维空间中的坐标
		Coordinate = AddXandYCoordinate(Coordinate, Coordinate_new, NodeNum)
	result = []
	result.append(ObstacleCoordinate)
	result.append(Coordinate)
	return result

# 保存邻接矩阵
def SaveNodeAdjacencyMatrix(distributeFlag,  NodeAdjacencyMatrix):
	# 保存邻接矩阵的数据
	if distributeFlag == 'poisson':
		np.savetxt(NodeAdjacencyMatrix_poisson_data_txt, NodeAdjacencyMatrix, fmt='%d')
	if distributeFlag == 'normal':
		np.savetxt(NodeAdjacencyMatrix_normal_data_txt, NodeAdjacencyMatrix, fmt='%d')
	if distributeFlag == 'uniform':
		np.savetxt(NodeAdjacencyMatrix_uniform_data_txt, NodeAdjacencyMatrix, fmt='%d')
	return
# 确定本次为什么分布
def SuredistributeFlag(poissonFlag, normalFlag, uniformFlag):
	distributeFlag = 'origin'
	# 泊松分布
	if poissonFlag is True:
		distributeFlag = 'poisson'
	# 高斯分布
	if normalFlag is True:
		distributeFlag = 'normal'
	# 均匀分布
	if uniformFlag is True:
		distributeFlag = 'uniform'
	return distributeFlag

# 主函数
def main():
	NodeList = []
	for i in range(0, NodeNum):
		NodeList.append(i)
	# 重新生成数据
	if DataBackup is False:
		result = Init(ObstaclesNum, EdgeLength, ObstacleLength)
		ObstacleCoordinate = result[0]
		Coordinate = result[1]
	# 使用备份数据
	if DataBackup is True:
		result = UseDataBackup(poissonFlag, normalFlag, uniformFlag, NodeNum)
		ObstacleCoordinate = result[0]
		Coordinate = result[1]
	# 确定本次为什么分布
	distributeFlag = SuredistributeFlag(poissonFlag, normalFlag, uniformFlag)
	
	Coordinatex_New = []
	Coordinatey_New = []
	# 添加虚拟节点
	AddVirtualNode(Coordinate, Coordinatex_New, Coordinatey_New, ObstacleCoordinate, ObstaclesNum, NodeList)

	# 将节点和障碍显示在平面二维平面中
	# TF.AllNodeShow(Coordinate[0], Coordinate[1], ObstacleCoordinate, ObstaclesNum, CoordinateScale, EdgeLength, result_name, distributeFlag)
	TF.AllNodeShow(Coordinatex_New, Coordinatey_New, ObstacleCoordinate, ObstaclesNum, CoordinateScale, EdgeLength, result_name, distributeFlag)
	
	# 重新组合Coordinate
	Coordinate_new = []
	Coordinate_new.append(Coordinatex_New)
	Coordinate_new.append(Coordinatey_New)
	NodeNum_new = len(NodeList)
	Coordinate = []
	Coordinate = AddXandYCoordinate(Coordinate, Coordinate_new, NodeNum_new)
	
	# np,show()
	# 根据距离大小生成节点之间的邻接矩阵
	# 创建距离矩阵的一下数组的初始化
	# 初始化邻接矩阵
	# NodeNum_new = NodeNum
	N_distance = np.zeros([NodeNum_new, NodeNum_new], dtype = np.float)
	# 两个节点之间的路径信息,用list来保存,即：从起点到终点过程中记录走过的位置
	Road_information = np.empty([NodeNum_new, NodeNum_new], list)
	NodeAdjacencyMatrix = AdjacencyMatrix(NodeNum_new, Coordinate, Road_information, N_distance, ObstacleCoordinate, ObstaclesNum)
	# 保存邻接矩阵数据
	SaveNodeAdjacencyMatrix(distributeFlag, NodeAdjacencyMatrix)
	# 使用团划分算法 NodeAdjacencyMatrix 表示生成的邻接矩阵
	CliqueResult = CP.CliquePartition(NodeAdjacencyMatrix)
	# CliqueResult[0] 为Delete_Edge方法的结果
	# CliqueResult[1] 为Delete_Degree方法的结果
	
	# 在最后的结果中，应该虚拟节点进行删除
	# 节点集合中，最大的节点的标号为NodeNum - 1
	DeleteVirtualNode(CliqueResult[0])

	print "CliqueResult[0] =\n", CliqueResult[0]
	# 将结果呈现在图形中
	TF.ChildrenTourConstruction(Coordinate[2], Coordinate[3], ObstacleCoordinate, ObstaclesNum, CliqueResult[0], NodeNum, distributeFlag, result_name, EdgeLength)
	D1 = np.sqrt(np.power((Coordinate[0][0] - Coordinate[0][5]), 2) + np.power((Coordinate[1][0] - Coordinate[1][5]), 2))
	D2 = np.sqrt(np.power((Coordinate[0][8] - Coordinate[0][9]), 2) + np.power((Coordinate[1][8] - Coordinate[1][9]), 2))
	# 欧几里得距离的测试
	print "distance[0][5] =", D1
	print "distance[8][9] =", D2
	# A*算法测试距离
	print "N_distance[0][5] =", N_distance[0][5]
	print "N_distance[8][9] =", N_distance[8][9]

# 程序开始
if __name__ == "__main__":
	main()
	
