# -*- coding: utf-8 -*-
# 此py文件主要存放功能函数
import os
import time
import random
import numpy as np
import A_Star_Algorithm as A
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
DebugFlag = True
kedu = 100

# 画圆圈
def DepictCircle(NodeCoordinateList, list_new, x_new_temp, y_new_temp, r, CSL_string):
    # 重新赋值节点坐标数组
    x_new = np.empty([1, len(list_new)], float)
    y_new = np.empty([1, len(list_new)], float)
    
    for i in range(0, len(list_new)):
        x_new[0][i] = x_new_temp[0][list_new[i]]
        y_new[0][i] = y_new_temp[0][list_new[i]]
        # 圆的基本信息
        # 1.圆半径
        # r = 60.65
        # 2.圆心坐标
        a = x_new[0][i]
        b = y_new[0][i]
        theta = np.arange(0, 2*np.pi, 0.01)
        # theta = np.arange(0, 2*np.pi, 0.1)
        x = a + r * np.cos(theta)
        y = b + r * np.sin(theta)

        CoordinateList_temp = []
        CoordinateList_temp.append(x)
        CoordinateList_temp.append(y)
        # 按顺序将节点圆周上的坐标进行保存
        NodeCoordinateList[0][list_new[i]] = CoordinateList_temp
        # 绘图
        plt.plot(x, y, CSL_string)
    return NodeCoordinateList 

# 设置障碍
'''
函数功能：在平面内设置障碍
函数输入：障碍数量，平面的边长，障碍区域边长
函数输出：障碍范围（横坐标下限，横坐标上限，纵坐标下限，纵坐标上限）
'''
def SetObstacles(ObstaclesNum, EdgeLength, ObstacleLength):    
    # 随机生成障碍区域
    ObstacleCoordinate = []
    # 障碍坐标范围
    ObstacleXDown = np.empty([1, ObstaclesNum], int)
    ObstacleXUp   = np.empty([1, ObstaclesNum], int)
    ObstacleYDown = np.empty([1, ObstaclesNum], int)
    ObstacleYUp   = np.empty([1, ObstaclesNum], int)
    for i in range(0, ObstaclesNum):
        ObstacleXDown[0][i] = (random.randint(1, EdgeLength))
        ObstacleYDown[0][i] = (random.randint(1, EdgeLength))
    # 保证障碍在要操作的二维区域内
    for i in range(0, ObstaclesNum):
        if ObstacleXDown[0][i] < EdgeLength - ObstacleLength:
            ObstacleXUp[0][i] = ObstacleXDown[0][i] + ObstacleLength
        else:
            x_temp = ObstacleXDown[0][i]
            ObstacleXUp[0][i] = x_temp
            ObstacleXDown[0][i] = x_temp - ObstacleLength
        if ObstacleYDown[0][i] < EdgeLength - ObstacleLength:
            ObstacleYUp[0][i] = ObstacleYDown[0][i] + ObstacleLength
        else:
            y_temp = ObstacleYDown[0][i]
            ObstacleYUp[0][i] = y_temp
            ObstacleYDown[0][i] = y_temp - ObstacleLength
    ObstacleCoordinate.append(ObstacleXDown[0])
    ObstacleCoordinate.append(ObstacleXUp[0])
    ObstacleCoordinate.append(ObstacleYDown[0])
    ObstacleCoordinate.append(ObstacleYUp[0])
    return ObstacleCoordinate

'''
函数功能：将服务站和节点以及障碍区域显示到图片中
函数输入：所有点横坐标集合和纵坐标集合，障碍范围集合，障碍数量，坐标刻度，服务站标签，二维空间边长，保存的路径
函数输出：None
'''
def AllNodeShow(x, y, obstacle_coordinate_new, obstacles_Num, kedu, edge_n, childern_result_name, distributeFlag):
    x_list = x
    y_list = y
    # 调整生成的图片的大小 # 设置figure_size尺寸
    plt.rcParams['figure.figsize'] = (10.0, 10.0) 
    #创建图并命名
    plt.figure('Scatter fig')
    plt.title('S & Node')
    ax = plt.gca()
    # 画网格
    plt.grid()
    # 障碍坐标区域使用绿色表示
    # 障碍横坐标x的范围
    x_down_list = obstacle_coordinate_new[0]
    x_up_list  = obstacle_coordinate_new[1]

    # 障碍纵坐标y的范围
    y_down_list = obstacle_coordinate_new[2]
    y_up_list = obstacle_coordinate_new[3]
    for j in range(0, obstacles_Num):
        x_down_value= x_down_list[j]
        x_up_value= x_up_list[j]
        y_down_value= y_down_list[j]
        y_up_value= y_up_list[j]
        # 障碍填充绿色
        plt.fill_between(range(x_down_value, x_up_value+1), y_down_value , y_up_value, facecolor='green')
    # 障碍图例显示
    ax.scatter((x_down_list[1]+x_up_list[1])/2, (
             y_down_list[1]+y_up_list[1])/2, color = 'green',label = 'Obstacle', marker = 's')
    # 图片坐标刻度设置 
    ax.xaxis.set_major_locator(MultipleLocator(kedu))
    ax.yaxis.set_major_locator(MultipleLocator(kedu))
    #设置x轴、y轴名称
    ax.set_xlabel('X(m)')
    ax.set_ylabel('Y(m)')
    
    # 每个节点用红圈圈表示出来
    ax.scatter(x_list, y_list,color = 'r',label = 'Node', marker = 'o')
    # ax.scatter(x_obstacle_list, y_obstacle_list,color = 'g', marker = '8')
    # S点为红色正方形，并且大一点
    # ax.scatter(x_list[0], y_list[0], s = 100, color = 'k',label = 'S', marker = 's')
    # 给S点标号
    # ax.text(x_list[0], y_list[0], S_Flag, fontsize=20)
    for i in range(0, len(y_list)):
        ax.text(x_list[i], y_list[i], i, fontsize = 10)
    # 图例位置
    ax.legend(loc='upper right', edgecolor='black')
    # 保存生成的图片 
    origin_path = distributeFlag + '0origin.png'  
    
    All_path = os.path.join(childern_result_name, origin_path)

    print "All_path =\n", All_path
    plt.savefig(All_path)
    
    plt.xlim([0 - 1,edge_n + 1]) #设置绘图X边界                                                                                                   
    plt.ylim([0 - 1,edge_n + 1]) #设置绘图Y边界
    plt.show()
    return

'''
函数功能：# 创建新邻接矩阵，对于过程中创建的邻接矩阵
函数输入：起点到终点所经过所有的路径的记录，邻接矩阵，二维空间的边长，所有节点的横坐标集合，所有节点纵坐标集合，所有节点的标号，未操作节点的标号，障碍集合，障碍个数
函数输出：一个列表，包含：各节点之间形成的邻接矩阵，两两节点之间的路径信息
'''
def CreateDistanceNewMatrix(Road_information_temp, N_distance_temp, EdgeLength, N_x_x, N_y_y, N_i_new, N_i_change, obstacle_coordinate_new, obstacle_num_new):
    # i和j表示第n个节点
    n = len(N_i_new)
    m = len(N_i_change)
    for i in range(0, m):
        for j in range(0, n):
            if N_i_change[i] == j:
                # 自己到自己的距离为0
                N_distance_temp[N_i_change[i]][j] = 0.0
                Road_information_temp[N_i_change[i]][j] = [[j, j],[j, j]]
            else:
                # i到j的距离，i<j,因为为无向图，可以使用N_distance[j][i]= N_distance[i][j] 将对称的位置赋相同的值
                # 将当前两个点的坐标提取出来
               
                x1 = N_x_x[0][N_i_new[N_i_change[i]]]
                y1 = N_y_y[0][N_i_new[N_i_change[i]]]
                
                first_coordinate = []
                first_coordinate.append(x1)
                first_coordinate.append(y1)
                x2 = N_x_x[0][N_i_new[j]]
                y2 = N_y_y[0][N_i_new[j]]
                
                second_coordinate = []
                second_coordinate.append(x2)
                second_coordinate.append(y2)
                # print "第一个坐标：", first_coordinate
                # print "第二个坐标：", second_coordinate
                result = A.a_star_algorithm(EdgeLength, first_coordinate, second_coordinate, obstacle_coordinate_new, obstacle_num_new, False)
                # print "构造回路的result = ", result
                # 电单车i到电单车j（或电单车j到电单车i）的实际距离
                # 距离取两位小数，就好
                N_distance_temp[N_i_change[i]][j] = round(result[3],2)
                N_distance_temp[j][N_i_change[i]] = round((N_distance_temp[N_i_change[i]][j]), 2)
                
                # result[5] 表示当前两个点的运动路径
                # 把路径保存到列表数组中不错
                Road_information_temp[N_i_change[i]][j] = result[5]
                Road_information_temp[j][N_i_change[i]] = Road_information_temp[N_i_change[i]][j]
                # print "Road_information =\n", Road_information
    result_new = []
    result_new.append(N_distance_temp)
    result_new.append(Road_information_temp)         
    return result_new

# 将子回路首尾连接起来
def ChildrenTourConstruction(x_new_temp, y_new_temp, obstacle_coordinate_new, ObstaclesNum, R_result, N, mechanism, result_name, EdgeLength, r, NodeCoordinateList):
    # 主要用于画图中进行操作，线条的颜色
    # LineColor =['b', 'g', 'r', 'c', 'm', 'y', 'k']
    LineColor =['b']
    # LineColor =['b']
    # 线条的风格
    LineStyle = ['-', '--', '-.', ':']
    # 线条的标志
    LineLogo = ['.', 'o', 'v', '^', '>', '<', '1', '2', '3', '4', 's', 'p', '*']

    if DebugFlag is True:
        print "模拟轨迹##########\n"
    Style_num = 0
    Color_num = 0
    result = R_result
    # 充电回路的名字
    MC_Num = 0
    # 图例显示的标志
    plt.figure('Scatter fig')
    plt.title('S & Node')
    ax = plt.gca()
    Sposition = result[0]

    x_new_temp[0][0] = x_new_temp[0][Sposition[0]]
    y_new_temp[0][0] = y_new_temp[0][Sposition[0]]
    
    # 电单车节点坐标重新赋值
    x_new = x_new_temp
    y_new = y_new_temp
    x_new_label = []
    y_new_label = []
    # 每个节点用红圈圈表示出来
    for k in range(0, N):
        x_new_label.append(x_new[0][k])
        y_new_label.append(y_new[0][k])

    ax.scatter(x_new_label, y_new_label,color = 'r',label = 'Node', marker = 'o')
    # 给每个节点标号MC_Num,N表示所有的节点都要标号
    
    for k in range(0, N):
        ax.text(x_new[0][k], y_new[0][k], k, fontsize = 10)
    legend_flag = True
    
    R_list = result
    
    z = len(R_list)
    SNode = []
    for p in range(0, z):
        # 提取每一个团的第一个节点
        R_temp = R_list[p]
        SNode.append(R_temp[0])
    XCoordinate_list = []
    YCoordinate_list = []
    # 将每个团的第一个节点提取出来充当暂时的充电桩
    for p in range(0, len(SNode)):
        XCoordinate_list.append(x_new[0][SNode[p]] + 10)
        YCoordinate_list.append(y_new[0][SNode[p]] + 10)
    
    # 打印检查产生的充电子回路有多少条，每条子回路由那些节点组成
    for p in range(0, z):
        R_value = R_list[p]
        goal = R_value
        # S点为黑色正方形，并且大一点
        # S_Flag = 'S' + '&' + str(goal[0])
        # if p == 0:
        # ax.text(x_new[0][goal[0]]+ 10, y_new[0][goal[0]]+ 10, S_Flag, fontsize=20)
        
        # 用于图例显示MC（）
        # 表示存在回路才需要连线
        if  len(R_value) == 1:
            list_new = R_value
            x = []
            y = []
            for j in range(0, len(list_new)):
                x.append(x_new[0][list_new[j]])
                y.append(y_new[0][list_new[j]])
            #分别存放所有点的横坐标和纵坐标，一一对应
            x_list = x
            y_list = y

            CSL_string = LineColor[Color_num]
            CSL_string = CSL_string + LineStyle[Style_num]
            if Color_num < (len(LineColor) - 1):
                Color_num = Color_num + 1 
            if Color_num == (len(LineColor) - 1):
                if Style_num < (len(LineStyle) - 1):
                    Style_num = Style_num + 1
                    Color_num = 0
                else:
                    CSL_string = LineColor[random.randint(0, len(LineColor)-1)]
                    CSL_string = CSL_string + LineStyle[random.randint(0, len(LineStyle)-1)]
            
            # 进行画圆
            NodeCoordinateList = DepictCircle(NodeCoordinateList, list_new, x_new_temp, y_new_temp, r, CSL_string)
            # 每个节点的圆周上的点集坐标序列
            # print "NodeCoordinateList =\n", NodeCoordinateList 
            print "len(NodeCoordinateList) =", len(NodeCoordinateList)

            # CSL_string = CSL_string + my_logo[random.randint(0, len(my_logo)-1)]
            # 计算当前是第几个回路
            MC_Num_temp = MC_Num 
            label_value = 'Clique' + str(MC_Num_temp)
            x_temp = x_list[0]
            y_temp = y_list[0]
            plt.plot(x_temp, y_temp, CSL_string, label = label_value, linewidth=1)
            MC_Num = MC_Num + 1
            
        if  len(R_value) != 1:
            list_new = R_value
            x = []
            y = []
            for j in range(0, len(list_new)):
                x.append(x_new[0][list_new[j]])
                y.append(y_new[0][list_new[j]])
            #分别存放所有点的横坐标和纵坐标，一一对应
            x_list = x
            y_list = y
            # 障碍坐标区域使用绿色表示
            # 障碍横坐标x的范围
            if legend_flag is True:
                x_down_list = obstacle_coordinate_new[0]
                x_up_list  = obstacle_coordinate_new[1]
            
                # 障碍纵坐标y的范围
                y_down_list = obstacle_coordinate_new[2]
                y_up_list = obstacle_coordinate_new[3]
                for j in range(0, ObstaclesNum):
                    x_down_value= x_down_list[j]
                    x_up_value= x_up_list[j]
                    y_down_value= y_down_list[j]
                    y_up_value= y_up_list[j]
                    # 给障碍填充绿色
                    plt.fill_between(range(x_down_value, x_up_value+1), y_down_value , y_up_value, facecolor='green')
                # 障碍图例显示
                ax.scatter((x_down_list[1]+x_up_list[1])/2, (
                         y_down_list[1]+y_up_list[1])/2, color = 'green',label = 'Obstacle', marker = 's')
                # 图片坐标刻度设置
                
                ax.xaxis.set_major_locator(MultipleLocator(kedu))
                ax.yaxis.set_major_locator(MultipleLocator(kedu))
                
                #设置x轴、y轴名称
                ax.set_xlabel('X(m)')
                ax.set_ylabel('Y(m)')
                legend_flag = False
            # 将节点连接构成回路
            # 获取当前回路节点个数
            q = len(x_list) - 1
            # 设置回路线条、格式、颜色等等
            
            CSL_string = LineColor[Color_num]
            CSL_string = CSL_string + LineStyle[Style_num]
            if Color_num < (len(LineColor) - 1):
                Color_num = Color_num + 1 
            if Color_num == (len(LineColor) - 1):
                if Style_num < (len(LineStyle) - 1):
                    Style_num = Style_num + 1
                    Color_num = 0
                else:
                    CSL_string = LineColor[random.randint(0, len(LineColor)-1)]
                    CSL_string = CSL_string + LineStyle[random.randint(0, len(LineStyle)-1)]
            
            # 进行画圆
            NodeCoordinateList = DepictCircle(NodeCoordinateList, list_new, x_new_temp, y_new_temp, r, CSL_string)
            # 每个节点的圆周上的点集坐标序列
            # print "NodeCoordinateList =\n", NodeCoordinateList 
            print "len(NodeCoordinateList) =", len(NodeCoordinateList)

            # CSL_string = CSL_string + my_logo[random.randint(0, len(my_logo)-1)]
            # 计算当前是第几个回路
            MC_Num_temp = MC_Num 
            label_value = 'Clique' + str(MC_Num_temp)
            for i in range(0, q):
                # 前后连接
                x_temp = [x_list[i], x_list[i+1]]
                y_temp = [y_list[i], y_list[i+1]]
                # label 表示线的颜色
                plt.plot(x_temp, y_temp, CSL_string, linewidth=1)
                if i == q - 1:
                    x_temp = [x_list[i + 1], x_list[0]]
                    y_temp = [y_list[i + 1], y_list[0]]
                    plt.plot(x_temp, y_temp, CSL_string, label = label_value, linewidth=1)
            MC_Num = MC_Num + 1
    # 充电桩的位置
    ax.scatter(XCoordinate_list, YCoordinate_list, s = 100, color = 'k',label = 'S', marker = 's')
    plt.grid()
    plt.legend(loc='upper right', edgecolor='black')
    ax.legend(loc='upper right', edgecolor='black')
    # 保存生成的图片
    
    Graph_Name = mechanism + '_Final.png'
    # print "Graph_Name =", Graph_Name
    origin_path = result_name
    # print "origin_path =", origin_path  
    All_path = os.path.join(origin_path, Graph_Name)
    # print "All_path =", All_path
    plt.savefig(All_path)
    plt.xlim([0 - 1, EdgeLength + 1]) #设置绘图X边界                                                                                                   
    plt.ylim([0 - 1, EdgeLength + 1]) #设置绘图Y边界
    plt.show()
    # 返回每个点集坐标序列
    return NodeCoordinateList

# 将子回路首尾连接起来
def ChildrenTourConstruction_new(x_new_temp, y_new_temp, obstacle_coordinate_new, ObstaclesNum, R_result, N, mechanism, result_name, EdgeLength, r, SCPCoordinate, NodeCoordinateList):
    # 主要用于画图中进行操作，线条的颜色
    # LineColor =['b', 'g', 'r', 'c', 'm', 'y', 'k']
    LineColor =['b']
    # 线条的风格
    LineStyle = ['-', '--', '-.', ':']
    # 线条的标志
    LineLogo = ['.', 'o', 'v', '^', '>', '<', '1', '2', '3', '4', 's', 'p', '*']

    if DebugFlag is True:
        print "模拟轨迹##########\n"
    Style_num = 0
    Color_num = 0
    result = R_result
    # 充电回路的名字
    MC_Num = 0
    # 图例显示的标志
    plt.figure('Scatter fig')
    plt.title('S & Node')
    ax = plt.gca()
    print "result =", result 
    print "x_new_temp =\n", x_new_temp
    print "y_new_temp =\n", y_new_temp
    Sposition = result[0]

    x_new_temp[0][0] = x_new_temp[0][Sposition[0]]
    y_new_temp[0][0] = y_new_temp[0][Sposition[0]]
    
    # 电单车节点坐标重新赋值
    x_new = x_new_temp
    y_new = y_new_temp
    x_new_label = []
    y_new_label = []
    # 每个节点用红圈圈表示出来
    for k in range(0, N):
        x_new_label.append(x_new[0][k])
        y_new_label.append(y_new[0][k])
    ax.scatter(x_new_label, y_new_label,color = 'r',label = 'Node', marker = 'o')
    # 给每个节点标号MC_Num,N表示所有的节点都要标号
    
    for k in range(0, N):
        ax.text(x_new[0][k], y_new[0][k], k, fontsize = 10)
    legend_flag = True
    
    R_list = result
    
    z = len(R_list)
    SNode = []
    for p in range(0, z):
        # 提取每一个团的第一个节点
        R_temp = R_list[p]
        SNode.append(R_temp[0])
    XCoordinate_list = []
    YCoordinate_list = []
    
    # 将每个团的第一个节点提取出来充当暂时的充电桩
    for p in range(0, len(SNode)):
        XCoordinate_list.append(x_new[0][SNode[p]] + 10)
        YCoordinate_list.append(y_new[0][SNode[p]] + 10)

    # 打印检查产生的充电子回路有多少条，每条子回路由那些节点组成
    for p in range(0, z):
        R_value = R_list[p]
        goal = R_value
        # S点为黑色正方形，并且大一点
        # S_Flag = 'S' + '&' + str(goal[0])
        # if p == 0:
        # ax.text(x_new[0][goal[0]]+ 10, y_new[0][goal[0]]+ 10, S_Flag, fontsize=20)
        
        # 用于图例显示MC（）
        # 表示存在回路才需要连线
        if  len(R_value) == 1:
            list_new = R_value
            x = []
            y = []
            for j in range(0, len(list_new)):
                x.append(x_new[0][list_new[j]])
                y.append(y_new[0][list_new[j]])
            #分别存放所有点的横坐标和纵坐标，一一对应
            x_list = x
            y_list = y

            CSL_string = LineColor[Color_num]
            CSL_string = CSL_string + LineStyle[Style_num]
            if Color_num < (len(LineColor) - 1):
                Color_num = Color_num + 1 
            if Color_num == (len(LineColor) - 1):
                if Style_num < (len(LineStyle) - 1):
                    Style_num = Style_num + 1
                    Color_num = 0
                else:
                    CSL_string = LineColor[random.randint(0, len(LineColor)-1)]
                    CSL_string = CSL_string + LineStyle[random.randint(0, len(LineStyle)-1)]
            # 进行画圆
            NodeCoordinateList = DepictCircle(NodeCoordinateList, list_new, x_new_temp, y_new_temp, r, CSL_string)
            # 每个节点的圆周上的点集坐标序列
            # print "NodeCoordinateList =\n", NodeCoordinateList 
            # print "len(NodeCoordinateList) =", len(NodeCoordinateList) 
            # CSL_string = CSL_string + my_logo[random.randint(0, len(my_logo)-1)]
            # 计算当前是第几个回路
            MC_Num_temp = MC_Num 
            label_value = 'Clique' + str(MC_Num_temp)
            x_temp = x_list[0]
            y_temp = y_list[0]
            plt.plot(x_temp, y_temp, CSL_string, label = label_value, linewidth=1)
            MC_Num = MC_Num + 1
            
        if  len(R_value) != 1:
            list_new = R_value
            x = []
            y = []
            for j in range(0, len(list_new)):
                x.append(x_new[0][list_new[j]])
                y.append(y_new[0][list_new[j]])
            #分别存放所有点的横坐标和纵坐标，一一对应
            x_list = x
            y_list = y
            # 障碍坐标区域使用绿色表示
            # 障碍横坐标x的范围
            if legend_flag is True:
                x_down_list = obstacle_coordinate_new[0]
                x_up_list  = obstacle_coordinate_new[1]
            
                # 障碍纵坐标y的范围
                y_down_list = obstacle_coordinate_new[2]
                y_up_list = obstacle_coordinate_new[3]
                for j in range(0, ObstaclesNum):
                    x_down_value= x_down_list[j]
                    x_up_value= x_up_list[j]
                    y_down_value= y_down_list[j]
                    y_up_value= y_up_list[j]
                    # 给障碍填充绿色
                    plt.fill_between(range(x_down_value, x_up_value+1), y_down_value , y_up_value, facecolor='green')
                # 障碍图例显示
                ax.scatter((x_down_list[1]+x_up_list[1])/2, (
                         y_down_list[1]+y_up_list[1])/2, color = 'green',label = 'Obstacle', marker = 's')
                # 图片坐标刻度设置
                
                ax.xaxis.set_major_locator(MultipleLocator(kedu))
                ax.yaxis.set_major_locator(MultipleLocator(kedu))
                
                #设置x轴、y轴名称
                ax.set_xlabel('X(m)')
                ax.set_ylabel('Y(m)')
                legend_flag = False
            # 将节点连接构成回路
            # 获取当前回路节点个数
            q = len(x_list) - 1
            # 设置回路线条、格式、颜色等等
            
            CSL_string = LineColor[Color_num]
            CSL_string = CSL_string + LineStyle[Style_num]
            if Color_num < (len(LineColor) - 1):
                Color_num = Color_num + 1 
            if Color_num == (len(LineColor) - 1):
                if Style_num < (len(LineStyle) - 1):
                    Style_num = Style_num + 1
                    Color_num = 0
                else:
                    CSL_string = LineColor[random.randint(0, len(LineColor)-1)]
                    CSL_string = CSL_string + LineStyle[random.randint(0, len(LineStyle)-1)]
            # 进行画圆
            NodeCoordinateList = DepictCircle(NodeCoordinateList, list_new, x_new_temp, y_new_temp, r, CSL_string)
            # 每个节点的圆周上的点集坐标序列
            # print "NodeCoordinateList =\n", NodeCoordinateList 
            # print "len(NodeCoordinateList) =", len(NodeCoordinateList) 
            # CSL_string = CSL_string + my_logo[random.randint(0, len(my_logo)-1)]
            # 计算当前是第几个回路
            MC_Num_temp = MC_Num 
            label_value = 'Clique' + str(MC_Num_temp)
            for i in range(0, q):
                # 前后连接
                x_temp = [x_list[i], x_list[i+1]]
                y_temp = [y_list[i], y_list[i+1]]
                # label 表示线的颜色
                plt.plot(x_temp, y_temp, CSL_string, linewidth=1)
                if i == q - 1:
                    x_temp = [x_list[i + 1], x_list[0]]
                    y_temp = [y_list[i + 1], y_list[0]]
                    plt.plot(x_temp, y_temp, CSL_string, label = label_value, linewidth=1)
            MC_Num = MC_Num + 1
    # 充电桩部署的位置       
    ax.scatter(SCPCoordinate[0], SCPCoordinate[1], s = 100, color = 'k',label = 'S', marker = 's')
    plt.grid()
    plt.legend(loc='upper right', edgecolor='black')
    ax.legend(loc='upper right', edgecolor='black')
    # 保存生成的图片
    
    Graph_Name = mechanism + '_Final_update.png'
    # print "Graph_Name =", Graph_Name
    origin_path = result_name
    # print "origin_path =", origin_path  
    All_path = os.path.join(origin_path, Graph_Name)
    # print "All_path =", All_path
    plt.savefig(All_path)
    plt.xlim([0 - 1, EdgeLength + 1]) #设置绘图X边界                                                                                                   
    plt.ylim([0 - 1, EdgeLength + 1]) #设置绘图Y边界
    plt.show()
    # 返回每个点集坐标序列
    return NodeCoordinateList