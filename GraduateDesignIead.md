# GraduateDesignIead 
# 题目：基于共享电单车的静态充电桩优化部署研究
##   继共享单车，共享汽车之后，共享运营的时代也催化了另外一种交通工具的流行，即共享电单车（Shared Ev）。国内已经出现了包括租八戒、电斑马、ebike、八点到、萌小明等一系列从事电单车租赁的公司。但是由于共享电单车主要依靠可充电电瓶维持运行，所以共享电单车的电瓶剩余能量是限制其正常工作的主要原因，这也是电单车租赁公司所面临的主要挑战。利用固定充电桩为城区中的共享电单车充电是一种合理且有效的方式，但是由于部署充电桩数量过多将占据大量城市土地资源。因此，优化城区中固定充电桩的部署位置，同时最小化所需充电桩的在共享电单车的运营中具有极其重要的现实意义。目前，在无线传感器网络中已有大量利用单个或多个静态能量源为传感器节点进行充电的研究，其能量源在二维，三维空间的优化部署是无线充电传感器网络中最核心研究问题之一。以无线传感器网络中的相关研究为基础，本次毕业设计任务即设计并实现一种针对城区共享电单车的高效合理的充电桩部署方案，该任务需要满足以下需求：
## 1）	调研相关静态能量源部署问题的研究；
## 2）	考虑将电单车投放于存在障碍的二维平面中，基于电单车的投入量，交通流量以及可行部署区域设计算法确定静态充电桩的部署区域；
## 3）	考虑充电桩具有有限能量，优化静态充电桩的部署位置与数量；
## 4）	以真实数据为输入，在MATLAB实现该充电桩优化部署方案，并进行性能分析。
## 同时，本次毕业设计还需翻译一篇与本专业相关的学术论文（不少于5000汉字）；并撰写符合中南大学信息科学与工程学院《毕业设计指导书》要求的毕业设计论文，提供程序源码及可运行的程序。

序号	参考资料目录
1	胡诚. 无线可充电传感器网络中充电规划及其可调度性研究[D]. 东南大学, 2015.
2	Haipeng Dai, Xiaobing Wu, et al. Minimizing the number of mobile chargers for large-scale wireless rechargeable sensor networks [J]. Computer Communications, 2014, 46: 54-65.
3	Guiyuan Jiang, Siew-Kei Lam, et al. Joint charging tour planning and depot positioning for wireless sensor networks using mobile chargers [J]. IEEE/ACM Transactions on Networking, 2017, 25(4): 2250-2266.
4	Lyes Khelladi, Djamei Djenouri, et al. Efficient on-demand multi-node charging techniques for wireless sensor networks [J]. Computer Communications, 2017, 101: 44-56.
5	Han G, Qian A, Jiang J, et al. A grid-based joint routing and charging algorithm for industrial wireless rechargeable sensor networks[J]. Computer Networks, 2016, 101(C):19-28.
6	Han G, Liu L, Jiang J, et al. Analysis of Energy-Efficient Connected Target Coverage Algorithms for Industrial Wireless Sensor Networks[J]. IEEE Transactions on Industrial Informatics, 2017, 13(1):135-143.
7	Dai H, Wang X, Liu A X, et al. Optimizing wireless charger placement for directional charging[C]// INFOCOM 2017 - IEEE Conference on Computer Communications, IEEE. IEEE, 2017:1-9.
8	Islam M M, Shareef H, Mohamed A. A review of techniques for optimal placement and sizing of electric vehicle charging stations[J]. Przegląd Elektrotechniczny, 2015, 91(8): 122-126.

三、毕业设计(论文)进度安排
阶段	工作任务内容	起止时间
1	查阅国内外资料，熟悉开发工具	12.20 — 1.20
2	方案设计	 1.21 — 3.19
3	仿真测试	3.20 — 4.29
4	完成毕业论文，准备答辩	4.30 — 5.20
5	论文答辩及完善	  5.21 — 6.9


（一） 首先完成CliquePartitioningAlgorithm分团算法，主要是解决充电桩数量问题
（二） 实现胡诚博士论文中对于S（充电桩）分布的算法，并多考虑是利用S的预部署还是利用S的动态部署，要看懂他的公式
（三） 最后考虑障碍的问题
（四） 在此过程中要考虑算法选择问题，看是创建还是改进还是用原算法，可能涉及算法比较问题
（五） 想接手师姐的任务，必须和师姐合作。考虑如何把胡诚博士论文的第五章实现
