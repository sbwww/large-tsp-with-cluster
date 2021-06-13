# 基于聚类和遗传算法的大规模 TSP 求解优化

## 1. 关键点

- GA 求解大规模 TSP 效率极低
  - 为什么？
    1. 解空间太大
    2. GA 容易局部最优
  - 怎么办？
    1. ~~用其他方法，比如 [LKH](https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic)~~
    2. 分而治之（本仓库内容）
- 所以将大规模 TSP 分解为多个小规模问题
  - 为什么？
    1. 每个子问题的解空间都不太大
    2. 子问题顺序也可以当做 TSP
    3. 子问题的求解是独立的，可以并行求解（尚未实现）
  - 怎么分？
    1. 聚类

## 2. 大致流程

1. K-Medoids 聚类划分子问题
2. GA 求解类间 TSP
3. 确定每个类的起点和终点
4. GA 求解每个类内 TSP
5. 按序合并子问题的解

## 3. 代码文件

- [parameters.py](parameters.py)
  需要的参数，其他所有（带有参数的）代码都要 import 它
- [KMedoids.py](KMedoids.py) K-Medoids 聚类
  参考 [letiantian/kmedoids](https://github.com/letiantian/kmedoids)
- [tsp.py](tsp.py) TSP 问题类
  参考 [geatpy tsp_test tsp.py](https://github.com/geatpy-dev/geatpy/blob/master/geatpy/testbed/tsp_test/tsp.py)
  包含起点终点约束
- [GA.py](GA.py) GA 模板
  参考 [geatpy tsp_test main.py](https://github.com/geatpy-dev/geatpy/blob/master/geatpy/testbed/tsp_test/main.py)
  包含自定义终止条件
- [run.py](run.py)
  总体流程（运行这玩意）
  ~~因为全是自己写的所以这个代码就很乱~~

## 4. 改进方向

1. 现在的代码涉及大量的文件读写，很耗时~~我好菜~~
2. TSP 子问题可以并行地求解，还不会实现~~我好菜~~
3. 子问题起点和终点选择的优化，目前是找出两个类间的最近点对，然后把这些点设为 GA 的等式约束，可能影响精确度，而且等式约束会使 GA 可行个体变少，效率降低，~~我好菜~~
