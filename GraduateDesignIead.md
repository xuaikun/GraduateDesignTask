# GraduateDesignIead 
# 题目：基于共享电单车的静态充电桩优化部署研究
##   继共享单车，共享汽车之后，共享运营的时代也催化了另外一种交通工具的流行，即共享电单车（Shared Ev）。国内已经出现了包括租八戒、电斑马、ebike、八点到、萌小明等一系列从事电单车租赁的公司。但是由于共享电单车主要依靠可充电电瓶维持运行，所以共享电单车的电瓶剩余能量是限制其正常工作的主要原因，这也是电单车租赁公司所面临的主要挑战。利用固定充电桩为城区中的共享电单车充电是一种合理且有效的方式，但是由于部署充电桩数量过多将占据大量城市土地资源。因此，优化城区中固定充电桩的部署位置，同时最小化所需充电桩的在共享电单车的运营中具有极其重要的现实意义。目前，在无线传感器网络中已有大量利用单个或多个静态能量源为传感器节点进行充电的研究，其能量源在二维，三维空间的优化部署是无线充电传感器网络中最核心研究问题之一。以无线传感器网络中的相关研究为基础，本次毕业设计任务即设计并实现一种针对城区共享电单车的高效合理的充电桩部署方案，该任务需要满足以下需求：
## 1）	调研相关静态能量源部署问题的研究；
## 2）	考虑将电单车投放于存在障碍的二维平面中，基于电单车的投入量，交通流量以及可行部署区域设计算法确定静态充电桩的部署区域；
## 3）	考虑充电桩具有有限能量，优化静态充电桩的部署位置与数量；
## 4）	以真实数据为输入，在MATLAB实现该充电桩优化部署方案，并进行性能分析。
## 同时，本次毕业设计还需翻译一篇与本专业相关的学术论文（不少于5000汉字）；并撰写符合中南大学信息科学与工程学院《毕业设计指导书》要求的毕业设计论文，提供程序源码及可运行的程序。

### 序号	参考资料目录
### 1	胡诚. 无线可充电传感器网络中充电规划及其可调度性研究[D]. 东南大学, 2015.
### 2	Haipeng Dai, Xiaobing Wu, et al. Minimizing the number of mobile chargers for large-scale wireless rechargeable sensor networks [J]. Computer Communications, 2014, 46: 54-65.
### 3	Guiyuan Jiang, Siew-Kei Lam, et al. Joint charging tour planning and depot positioning for wireless sensor networks using mobile chargers [J]. IEEE/ACM Transactions on Networking, 2017, 25(4): 2250-2266.
### 4	Lyes Khelladi, Djamei Djenouri, et al. Efficient on-demand multi-node charging techniques for wireless sensor networks [J]. Computer Communications, 2017, 101: 44-56.
### 5	Han G, Qian A, Jiang J, et al. A grid-based joint routing and charging algorithm for industrial wireless rechargeable sensor networks[J]. Computer Networks, 2016, 101(C):19-28.
### 6	Han G, Liu L, Jiang J, et al. Analysis of Energy-Efficient Connected Target Coverage Algorithms for Industrial Wireless Sensor Networks[J]. IEEE Transactions on Industrial Informatics, 2017, 13(1):135-143.
### 7	Dai H, Wang X, Liu A X, et al. Optimizing wireless charger placement for directional charging[C]// INFOCOM 2017 - IEEE Conference on Computer Communications, IEEE. IEEE, 2017:1-9.
### 8	Islam M M, Shareef H, Mohamed A. A review of techniques for optimal placement and sizing of electric vehicle charging stations[J]. Przegląd Elektrotechniczny, 2015, 91(8): 122-126.

### 三、毕业设计(论文)进度安排
### 阶段	工作任务内容	起止时间
### 1	查阅国内外资料，熟悉开发工具	12.20 — 1.20
### 2	方案设计	 1.21 — 3.19
### 3	仿真测试	3.20 — 4.29
### 4	完成毕业论文，准备答辩	4.30 — 5.20
### 5	论文答辩及完善	  5.21 — 6.9

#   毕业设计解决思路：
### （一） 首先完成CliquePartitioningAlgorithm分团算法，主要是解决充电桩数量问题（已解决）
### （二） 实现胡诚博士论文中对于S（充电桩）分布的算法，并多考虑是利用S的预部署还是利用S的动态部署，要看懂他的公式（待解决）
### （三） 最后考虑障碍的问题(如果存在障碍的话，可以使用A-star algorithm解决（A星算法可以用于路径导航方面）)（待解决）
### （四） 在此过程中要考虑算法选择问题，看是创建还是改进还是用原算法，可能涉及算法比较问题
### （五） 和师姐合作，考虑如何把胡诚博士论文的第五章实现

##  课程设计进度：
### 2018年11月18日：
  开始我的毕业设计，将之前做过的CliquePartitioningAlgorithm算法程序重新用python实现一次，它是毕业设计的一部分，而且是非常重要的一部分

### 2018年11月19日：
  在使用Numpy过程中完成数组的初始化，之后在实现CLiqePartitioningAlgorithm算法中大有作用。
今天看看能不能把CliquePartitioningAlgorithm算法的一部分21完成，目前文件已经能够正常读取，回去再优化，今晚尽量把算法实验完成

### 2018年11月20日：
    发现python跑的程序和c++跑的程序结果不一样，发现原因竟是：Max_Common_Neighbor_num遍历顺序不一样    
  用python实现了最原始的CliquePartitioningAlgorithm问题，当Common_Neighbor最大值不唯一时，选择（合并）删除边最少的那两个节点。
  今晚回去把选择合并两个节点时删除最大度的的两个节点~

### 2018年12月7日：
看胡诚博士论文（第五章）后的想法(收获)：
MMCP（Minimize Mobile Chargers Problem）最小化MC问题
解决最少需要几个MC能完成使命
DVRP（Distance-constrainted Vehicle Routing Problem）距离约束路径问题 
DVRP问题是指：给定一个网络G=（E,V），一个站点B及一个距离约束D，求用最少数量的回路来覆盖整个网络的节点V，使得每个回路都经过B并且回路的长度不超过D（D涉及耗能，D不能太远（长）否则MC还没回到S就死亡了），还没达到一个周期前，MC到S后可以瞬间充满电，然后继续离开，给下一个节点充电。
覆盖整个网络需要几个回路，它的解主要还是体现在到底有几个回路
只考虑一个周期的情况，所以一个周期解决不了的就得增加MC的数量

### 2018年12月9日：
要解决MMCP问题：（完成截止日期为：2018年12月16日，一个星期的时间）
首先，解决TCP问题（仅解决了其中的一部分）
再实现TAP问题（未解决）
TCP问题包含：（1）回路可调度判定 （2）LKH算法实现 （3）整合代码就等于TCP问题
今天初步实现胡诚博士论文中回路可调度判定算法，目前在考虑LKH算法实现

### 2018年12月16日：
考虑如何实现LKH算法（加快进度），2018年12月21日要去中南大学参加张艺雯师姐的中期报告。（放弃使用LKH算法）


### 2018年12月22日：师姐给了个实验（从简单做起）
（1）用A星算法获取两辆电单车之间的距离
（2）将所有电单车的功率进行排序（按从小到大排序),构建回路H
（3）判断所选择的子回路是否满足充分必要条件


# 课程设计过程中遇到的问题：
### 2018年11月19日：
    在使用python中调用numpy库，在数组操作时出现了n多意外，
import numpy as np
NodeList = np.empty([n1,n2],int)，
### 初始化一个n1行n2列，元素为整形的二维数组
特别注意两种情况：
Node = np.empty([n,1],int)
这说明定义了一个n行的数组
如：
Node =[
[1],
[2],
[n]]
Node访问元素的时候，直接用Node[i]或者Node[i][0] 那个列的这项，可以要可以不要
NodeList = np.empty([1,n],int)
这说明定义了一个n列的数组
如：
NodeList =[
[1,2,3,4,5,6, ,, n]]
NodeList 访问元素的时候，需要用NodeList[0][i]，前面那个表示行，不可以省略
所以对NodeList进行选择排序的时候，需要这样
### 必须体现它是哪一行的，不然就是错的
def SelectSort(A):
    lenght = A.shape[1]

    for i in range(1, lenght - 1):
        max = i
        temp = 0
        for j in range(i + 1, lenght):
            if A[0][max] < A[0][j]:
                max = j
        temp = A[0][max]
        A[0][max] = A[0][i]
        A[0][i] = temp
    return
    
 .py文件里面的几个东西的解释：
 Edge_Delete[i][k] = x 表明选中i和k两个节点时，需要删除的边的数目为x
 Degree[0][i] = Degree[0][i] + EdgeList[i][j] 表示i节点的度，即每一行中1的个数
 （1）删除边的数量
 （2）找出节点的度
