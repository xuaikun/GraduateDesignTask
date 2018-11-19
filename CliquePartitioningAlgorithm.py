# encoding: utf-8
import numpy as np
# 定义选择排序 A 需要为列表List
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

if __name__ == "__main__":
   # 已经知道 矩阵为方阵即 n*n的矩阵
    # 输入 数组的长度
    temp = np.loadtxt('data.txt')
    n = temp.shape[1]
    EdgeList = np.empty([n + 1, n + 1], int)
    for i in range(0, n):
        for j in range(0, n):
            EdgeList[i + 1][j + 1] = temp[i][j]
    print ("the wight is ", n)
    print ('type(EdgeList) is', type(EdgeList))
    # 验证输入的 邻接矩阵是否正确
    for i in range(1, n + 1):
        # 一行一行的打印会更清晰明了
        print EdgeList[i][1:]
    # 初始化相关数组
    # Node[n] 用于检验某个节点是否加入某个团
    Node = np.empty([n + 1, 1], int)
    # NodeList[n][n] 用于检查节点都进入了哪个NodeList，记录生成了几个NodeList
    NodeList = np.empty([n + 1, n + 1], int)

    NodeNew = np.empty([n + 1, 1], int)
    NodeListNew = np.empty([n + 1, n + 1],int)
    # 定义两个中间计算 数组（矩阵） 与师姐一样
    First = np.empty([n + 1, 1], int)
    Second = np.empty([n + 1, 1], int)

    Common_Neighbor_Sort = np.empty([1, n + 1], int)  # 对Common_Neighbor排序
    Degree = np.empty([n + 1, 1], int)                # 统计每个节点的度
    Degree_Increasing_Order = np.empty([1, n + 1], int) # 把度进行排序

    # 每次都需要把每个节点排序中的最大值拿出来
    # 将max_Degree_Increasing_Order = 0 作为while循环的终止条件
    # max_Degree_Increasing_Order = 0 意味着每个点都不再相连，可以结束查询
    max_Degree_Increasing_Order = 1
    # 当Common_Neighbor 数量最大点不止两个时，需要找出当前某两个节点的最大度
    Max_Degree = 0
    # Common_Neighbor数量最大点不止两个时，需要找出当前某两个节点删除的边的数量最少
    Min_Edge = 10000
    # 将索引加1的目的是，为了符合我们的日常想法，节点1 对应 Node[1]
    for i in range(1, n + 1):
        Node[i] = 1             # 确保每个节点都存在，Node[i] == 1时表示存在此节点，否则表示不存在
        NodeList[i][1] = i      # 确保初始化时每个节点存在于一个Clique中
        for j in range(2, n + 1): # 每个NodeList初始化时只有NodeList[i][1] = 1,j != 1时，NodeList[i][j] = 0
            # 若i节点被加入到某个Clique中，那么NodeList[i][1] = 0
            NodeList[i][j] = 0    # i = 1 to i -> n循环统计NodeList[i][1]中等于1的个数就是Clique的个数
    # 打印验证初始化是否成功
    # for i in range(1, n + 1):
    #    print ('Node[',i, ']=', Node[i])
    #    for j in range(1, n + 1):
    #        print ('NodeList[', i, '][', j, ']=', NodeList[i][j])
    # 初始化无向图中边的情况（即哪个节点与哪个节点相连）
    # 节点之间相连，则对应的两个节点之间的连线对应的值 = 1
    # Node[1] 和 Node[2] 相连 则EdgeList[1][2] = 1 否则 为 0

    EdgeListNew = np.empty([n + 1, n + 1], int)
    Edge_Delete = np.empty([n + 1, n + 1], int) # 统计被删除的边
    Common_Neighbor = np.empty([n + 1, n + 1], int) # 每条边的Common_Neighbor数量
    Common_Neighbor_New = np.empty([n + 1, n + 1], int)  # 保存Common_Neighbor的上三角
    # 备份数据
    for i in range(1, n + 1):
        NodeNew[i] = Node[i]
        for j in range(1, n + 1):
            EdgeListNew[i][j] = EdgeList[i][j]
            NodeListNew[i][j] = NodeList[i][j]

    # 以上部分，已将图初始化，节点初始化，边初始化，邻接矩阵初始化
    while max_Degree_Increasing_Order:
# Step1
        # max_Degree_Increasing_Order = 0 作为程序停止的标志
        # max_Degree_Increasing_Order 节点度排序后的最大值，若最大值为0 ，则表明每个节点不相连
        # 则全部点已经全部分配到各个Clique
        # 每次执行前，将Common_Neighbor_Sort[]初始化
        for i in range(1, n + 1):
            Common_Neighbor_Sort[0][i] = 0
        Max_Degree = 0           # 为防止上次两个节点度的影响，最大度每次都得更新
        # 保证i < j 计算 选中这两个点需要删除的边的数量
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                First[j] = EdgeList[i][j]
            for k in range(i + 1, n + 1):
                # 保证这两个点是相连的，存在edge(i, j)
                if EdgeList[i][k] == 1:
                    num = 0    # 需要删除的边
                    for u in range(1, n + 1):
                        Second[u] = EdgeList[k][u]
                    for q in range(1, n + 1):
                        # 保证仅与较小点相连,该删除
                        if First[q] != Second[q] and First[q] != 0:
                            # 时刻记得这样的情况
                            # 0 0 1
                            # 0 0 0
                            # 1 0 0
                            num = num + 1
                    for c in range(1, n + 1):
                        # 对于需要删除与j相连的边
                        if EdgeList[k][c] != 0:
                            num = num + 1
                    # 为什么要减1？本身为1，但对方对应不为1，多了1条边，所以减1
                    Edge_Delete[i][k] = num - 1
                    # 其实是同一条边，删除的边是一样的
                    Edge_Delete[k][i] = Edge_Delete[i][k]
                else:
                    Edge_Delete[i][k] = 0
        # 统计每个节点的度保存到Degree[], 数组下标即为节点标号
        for i in range(1, n + 1):
            Degree[i] = 0       # 每个节点的度初始化为0
            for j in range(1, n + 1):
                Degree[i] = Degree[i] + EdgeList[i][j] # 每一行的值的总和即为某个节点的度
            # 将Degree[]的值依次存入Degree_Increasing_Order[]用于排序
            # 依旧Degree[i] 的值保持不变，方便用于查询节点
            Degree_Increasing_Order[0][i] = Degree[i]
            # print (Degree_Increasing_Order)
            # print (type(Degree_Increasing_Order))
        # 按节点度进行排序
        # Degree_Increasing_Order必须是1行多列的数组，不然不能正常排序
        SelectSort(Degree_Increasing_Order)
        max_Degree_Increasing_Order = Degree_Increasing_Order[0][1]
        # 程序结束  以获取最大节点度为0，马上终止程序
        if max_Degree_Increasing_Order == 0:
            # goto end
            print (" end ")
            break
        # 计算每条边的Common_Neighboor数量
        for i in range(1, n + 1):
            for j in range(1, n + 1):       # 控制行变化
                 First[j] = EdgeList[i][j]   # 提取第i行元素
            for k in range(1, n + 1):       # 控制列变化
                if EdgeList[i][k] == 1:     # 保证操作的两个点是相连的
                    for j in range(1, n + 1):
                         Second[j] = EdgeList[k][j]  # 提取第k行元素

                    Diff = 0                # 邻居计数
                    for u in range(1, n + 1):
                        if First[u] == Second[u] and First[u] != 0:  # 相连的两个点（edge）有共同的点（Common_Neighbor）,并且0不算相连
                           Diff = Diff + 1
                    Common_Neighbor[i][k] = Diff        # 每条边的Common_Neighbor数量
                else:
                   Common_Neighbor[i][k] = 0
        # 只获取Common_Neighbor上三角部分数据，保证Common_Neighbor[][]只保存不同边的个数
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i <= j:
                    # 将Common_Neighbor的上三角提取出来
                    Common_Neighbor_New[i][j] = Common_Neighbor[i][j]
        # 当时Common_Neighbor_Sort c出来问题
        # 将每个节点对应的最大Common_Neighbor找出来
        for i in range(1, n + 1):
            # 之前这里好像错过
            # 从对角线开始才是正确的，这个值等于0， 不然会出现随机值
            Max = Common_Neighbor_New[i][i]
            for j in range(i, n + 1):
                if max < Common_Neighbor_New[i][j]: # 若当前Max值比Common_Neighbor_New[i][j]小，则替换Max值
                    Max = Common_Neighbor_New[i][j]
            Common_Neighbor_Sort[0][i] = Max
        # 对统计出来的每个点的最大Common_Neighbor数量进行排序
        SelectSort(Common_Neighbor_Sort)

        # 首先找出Common_Neighbor最大的，如果Common_Neighbor最大值唯一，则继续，如最大值不唯一，则再比较
        # Degree[], 优先合并度最大的两个节点

        Max_Common_Neighbor_num = 0 # 统计有用最大Common_Neighbor的边的数量
        # 分别保存每条边的i，j节点
        Max_Common_Neighbor_i_Point = np.empty([n + 1, 1], int)
        Max_Common_Neighbor_j_Point = np.empty([n + 1, 1], int)
        # 当最大Common_Neighbor的边不止一条时，需要找度最大的那两个节点
        # 获取i节点，获取j节点
        Max_Common_Neighbor_i_Point_Last = 0
        Max_Common_Neighbor_j_Point_Last = 0
        # 最优的两个节点的标号
        Max_i = 0
        Max_j = 0
        Max_Common_Neighbor_num = 0
        # 一定存在Max_j > Max_i
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                # Common_Neighbor数量最大点为Common_Neighbor_Sort[0][1]
                # 每次都只拿出最大的出来比较即可
                if Common_Neighbor_Sort[0][1] == Common_Neighbor_New[i][j] and EdgeList[i][j] != 0:
                    # 找到最大Common_Neighbor的两个节点，防止最大Common_Neighbor为0时出现错误，保证选中的两个节点必须相连
                    # 统计最大Common_Neighbor数量
                    Max_Common_Neighbor_num = Max_Common_Neighbor_num + 1
                    # 统计最大Common_Neighbor位置，即：i，j两个节点标号
                    # Max_Common_Neighbor_num 可以作为index
                    Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num] = i
                    Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j
        Max_Degree = 0
        Min_Edge = 10000
        # 含有最大Common_Neighbor的边不止一条
        if Max_Common_Neighbor_num != 1:
            for k in range(1, Max_Common_Neighbor_num + 1):
                # 通过Max_Common_Neighbor_num作为index将它们一条条找出来
                # 并把选中边中度最大的找出来
                i = Max_Common_Neighbor_i_Point[k]
                j = Max_Common_Neighbor_j_Point[k]
                # 找出需要删除的边最少的两个点
                # Edge_Delete[i][j]
                if Min_Edge > Edge_Delete[i][j]:
                    Min_Edge = Edge_Delete[i][j]
                    Max_Common_Neighbor_i_Point_Last = i
                    Max_Common_Neighbor_j_Point_Last = j
            # 已经找到最大Common_Neighbor点及最大度的边Edge(i,j)
            Max_i = Max_Common_Neighbor_i_Point_Last
            Max_j = Max_Common_Neighbor_j_Point_Last
        else: # 最大Common_Neighbor的边只有一条
            # 已经找到最大Common_Neighbor点及最大度的edge(i,j)
            # Max_Common_Neighbor_num 就是index
            Max_i = Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num]
            Max_j = Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num]
# Step2
        # //对Max_i 和Max_j 进行处理 就是对Clique分团进行处理，Node[],NodeList[][]都要进行处理
        # 		//Madx_i 和Max_j 表示最大Common_Neighbor 并有最大度的两个连接点 edge(Max_i,Max_j)
        # 		//Node[] == 1时表示这个点未受到处理，Node[] == 0时表示已经加入某个Clique
        # 		//NodeList[i][1] == 1时表示这里有一个Clique NodeList[i][1] == 0时表示这里不存在Clique
        #
        # 		//Clique[Max_i][Max_j].EdgeList 需要被处理
        # 		//存在于Clique[Max_i][]但不存在与Clique[Max_j][]中的点均为0
        # 		//Clique[Max_j][].EdgeList全部为0
        #
        # 		//已经得到 Max_i  Max_j 目前仅对它们两个点进行操作  ************************
        #
        # 		//对加入CLique进行处理  一定存在 Max_i < Max_j

        temp = 0
        # 若Max_i较大，则互换Max_i和Max_j的值
        if Max_i > Max_j:
            temp = Max_j
            Max_j = Max_i
            Max_i = temp
        NodeList[Max_j][1] = 0  # 减少一个Clique
        Node[Max_j] = 0         # 减少一个Node 均表示将Max_j与Max_i合并为Max_i
        # 保存同在一个团里面 考虑一个问题
        # 就是当原来的Max_i > Max_j时要把Max_i与Max_j互换
        # NodeList[Max_j][i]的值也得保存的要保存到NodeList[Max_i][i]
        NodeList[Max_i][Max_j] = Max_j # 主要时NodeList[Max_j][1] = Max_j
        # 将属于NodeList[Max_j][i]归并到NodeList[Max_i][i]中
        for i in range(2, n + 1):
            if NodeList[Max_j][i] != 0:
                NodeList[Max_i][i] = i
        # NodeList[Max_j][i]中的点已经被归并到NodeList[Max_i][i],将NodeList[Max_j][i]清零
        for i in range(1, n + 1):
            NodeList[Max_j][i] = 0
# Step3
        # 对边进行操作 删除仅与Max_i相连的边（师姐解释的，第三个点仅与其中一个点相连，它们的边删除）
        for j in range(1, n + 1):
            # 控制行变化
            First[j] = EdgeList[Max_i][j]  # 提取第Max_i行元素
            Second[j] = EdgeList[Max_j][j] # 提取第Max_j行元素
        for u in range(1, n + 1):
            # 已经明确Max_i和Max_j是相连的，查看它们对应邻接矩阵的Max_i行和Max_j行
            # 对应列是否相等，相等且等于1表示第三个点k与Max_i、Max_j相连
            # 则Edge(Max_i,k)(如果k>Max_i时 则为Edge(k, Max_i))不需要删除，反之需要删除
            if First[u] != Second[u] and First[u] == 1:
                # 存在一个点仅与相连的Max_i点相连 即 Clique[Max_i][u].EdgeList = 1;
                # 生成的时无向图，需要置对称的两个值为零，即为删除边
                EdgeList[Max_i][u] = 0
                EdgeList[u][Max_i] = 0
        # 将与标号大的点与Mai_j相连的边全部删掉
        # 这样做少一些工作，比较好理解，可能直接说不通
        for i in range(1, n + 1):
            # 生成的是无向图，需要置对称的两个值为0，即为删除边
            EdgeList[Max_j][i] = 0
            EdgeList[i][Max_j] = 0
# Step4
        # Max_i 和 Max_j 合并为Max_i
        Max_i
# Step5
        # 由于节点被修改，每个节点的度也被修改，重新计算度的值
        for i in range(1, n + 1):
            # 每个节点的度初始化为0
            Degree[i] = 0
            for j in range(1, n + 1):
                # 每一行的值的总和即为某个节点的度
                Degree[i] = Degree[i] + EdgeList[i][j]
            # 将Degree[]的值依次存入Degree_Increasing_Order[]用于排序
            # 依旧保存Degree[]不变， 方便“查询节点时”使用
            Degree_Increasing_Order[0][i] = Degree[i]
        SelectSort(Degree_Increasing_Order)         # 将节点的度进行排序
        max_Degree_Increasing_Order = Degree_Increasing_Order[0][1]
        # 保证i < j 计算选中这两个点后需要删除的边的数量
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                First[j] = EdgeList[i][j]
            for k in range(i + 1, n + 1):
                # 保证这两个点是相连的，存在edge（i，j）
                if EdgeList[i][k] == 1:
                    num = 0
                    for u in range(1, n + 1):
                        Second[u] = EdgeList[k][u]
                    for q in range(1, n + 1):
                        # 保证仅与较小点i相连，该删除
                        if First[q] != Second[q] and First[q] != 0:
                            num = num + 1
                    for c in range(1, n + 1):
                        # 对于需要删除与j相连的边
                        if EdgeList[k][c] != 0:
                            num = num + 1
                    Edge_Delete[i][k] = num - 1
                    # 其实是同一条边，删除的边是一样的
                    Edge_Delete[k][i] = Edge_Delete[i][k]
                else:
                    Edge_Delete[i][k] = 0
        if max_Degree_Increasing_Order == 0:
            # 以获取最大节点度为0，马上终止程序，Max_i已经单独存在
            # goto end
            print ("Max_i is ioslate")
        # 如果Max_i节点独立了，另选一条边，即另外两个点
        if Degree[Max_i] == 0:
            # goto Step1
            print ("continue")
        else: #还有与Max_i相连的边
            # 计算包含Max_i节点的边的Common_Neighbor的最大值情况
            for j in range(1, n + 1): # 控制行变化
                First[j] = EdgeList[Max_i][j]  # 提取第i行元素
            for k in range(1, n + 1): # 控制列变化
                if EdgeList[Max_i][k] == 1: # 保证操作的两个点是相连的
                    for j in range(1, n + 1):
                        Second[j] = EdgeList[k][j] # 提取第k行元素
                    Diff = 0  # 邻居计数
                    for u in range(1, n + 1):
                        # 相连的两个点 有共同的点（Common_Neighbor），并且0不算相连
                        if First[u] == Second[u] and First[u] != 0:
                            Diff = Diff + 1
                    Common_Neighbor[Max_i][k] = Diff  # 每条边的Common_Neighbor数量
                else:
                    Common_Neighbor[Max_i][k] = 0
            # 只获取Common_Neighbor上三角部分数据，保证Common_Neighbor[][]只保存不同边的个数
            # 不知道Max_i 和 j 谁大谁小
            for j in range(1, n + 1):
                # 将Common_Neighbor的上三角提取出来
                Common_Neighbor_New[Max_i][j] = Common_Neighbor[Max_i][j]
            # 已经获得Common_Neighbor_New[][]
            Max = Common_Neighbor_New[Max_i][1]
            for j in range(2, n + 1):
                if Max < Common_Neighbor_New[Max_i][j]:
                    # 若当前Max值Common_Neighbor_New[Max_i][j]小，则替换Max值
                    Max = Common_Neighbor_New[Max_i][j]
            Common_Neighbor_Sort[0][1] = Max
            # 最大的Common_Neighbor = Max
            # 两个顶点分别为 Max_i Max_j 判断Max是否唯一
            Max_Common_Neighbor_num = 0
            for j in range(1, n + 1):
                # Common_Neighbor数量最大点为Common_Neighbor_Sort[1]
                # 每次都只拿最大的出来比较即可
                if Common_Neighbor_Sort[0][1] == Common_Neighbor_New[Max_i][j] and EdgeList[Max_i][j] != 0:
                    # 找到最大Common_Neighbor的两个节点 防止最大Common_Neighbor为0时出现错误，保证选中的两个节点必须相连
                    # 统计最大Common_Neighbor数量
                    Max_Common_Neighbor_num = Max_Common_Neighbor_num + 1
                    # 统计最大Common_Neighbor位置 即：两个节点标号
                    # Max_Common_Neighbor_num可以作为index
                    Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j
            Max_Degree = 0
            Min_Edge = 10000
            # 含有最大Common_Neighbor的边不止一条
            if Max_Common_Neighbor_num != 1:
                # 通过Max_Common_Neighbor_num 作为index将它们一条条找出来
                for k in range(1, Max_Common_Neighbor_num + 1):
                    # 并把选中边中度最大的找出来
                    j = Max_Common_Neighbor_j_Point[k]
                    if Min_Edge > Edge_Delete[Max_i][j]: # 找出删除最少边的两个点
                        Min_Edge = Edge_Delete[Max_i][j]
                        Max_Common_Neighbor_j_Point_Last = j
                Max_j = Max_Common_Neighbor_j_Point_Last
            else:
                # 最大Common_Neighbor的边只有一条
                # Max_Common_Neihbor_num 就是index
                # 已经找到最大Common_Neighbor点及最大度的的edge(i, j)
                Max_j = Max_Common_Neighbor_j_Point_Last[Max_Common_Neighbor_num]
            # 重新获得Max_i 和 Max_j 两个节点为最优选择点
            # Max_i
            # Max_j
            # goto Step2
    # end while()
    # 计算Clique的个数
    Clique_Count = 0
    print ("*********************")
    for i in range(1, n + 1):
        # Clique保存在NodeList[][]中NodeList[i][1] = 1表示这里有一个团
        # NodeList[i][1] = 0 表示这里没有团
        if NodeList[i][1] != 0:
            Clique_Count = Clique_Count + 1
    print ("print Clique_Count = ", Clique_Count)
    for i in range(1, n + 1):
        if NodeList[i][1] != 0:
            # 保证这点的根节点一定存在
            print ("Clqiue[", i, ']:(', i, ',') # 在检查它其中还包含哪些节点
            for j in range(i + 1, n + 1):
                if NodeList[i][j] != 0:
                    print j
            print ")"




'''
Degree_Increasing_Order = np.empty([1, 6], int)
Degree_Increasing_Order[0][0] = 0
Degree_Increasing_Order[0][1] = 1
Degree_Increasing_Order[0][2] = 6
Degree_Increasing_Order[0][3] = 12
Degree_Increasing_Order[0][4] = 2
Degree_Increasing_Order[0][5] = 8
print (type(Degree_Increasing_Order))
print (Degree_Increasing_Order)
SelectSort(Degree_Increasing_Order)

print Degree_Increasing_Order.shape[1]
for i in range(1, 6):
    print Degree_Increasing_Order[0][i]
'''
