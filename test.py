# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt

# 圆的基本信息
# 1.圆半径
r = 2.0
# 2.圆心坐标
a = 0.
b = 0.
theta = np.arange(0, 2*np.pi, 0.01)
x = a + r * np.cos(theta)
y = b + r * np.sin(theta)
# 绘图
plt.plot(x, y)
# 生成的圆会看起来也是圆形，坐标间隔是相等的
plt.axis('equal')
plt.show()