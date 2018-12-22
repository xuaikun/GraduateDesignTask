# encoding: utf-8
import numpy as np
start_point = (1, 2)  # 起始坐标
end_point = (3, 4)    # 目标坐标

n = 100               # 定义二维平面大小
# 构造二维平面
create_2D_space = np.empty([n + 1, n + 1], int)
# 初始化二维平面
# 当二维平面中位置的值不为0，1时，说明这里是障碍，就不能越过，得绕过
# 其中为0的点为空旷区域，可以随意通过
# 其中为1的点为起始点或者目标点
for i in range(1, n + 1):
    for j in range(1, n + 1):
            create_2D_space[i][j] = 0

# 将起始坐标和目的坐标加入二维平面中
create_2D_space[start_point[0]][start_point[1]] = 1
create_2D_space[end_point[0]][end_point[1]] = 1

# 检查二维平面
for i in range(1, n + 1):
    space_list = []
    for j in range(1, n + 1):
        space_list.append(create_2D_space[i][j])
        if j == n:
            print space_list


