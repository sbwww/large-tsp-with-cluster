# -*- coding: utf-8 -*-
import random

import geatpy as ea  # import geatpy
import matplotlib.pyplot as plt
import numpy as np

import parameters
from tsp import TestProblem


def main(index, start=None, end=None):
    """===============================实例化问题对象============================"""
    problem = TestProblem(str(index), start, end)  # 生成问题对象
    places = np.loadtxt(
        "data/cluster/" + str(index) + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
    """=================================种群设置==============================="""
    Encoding = 'P'  # 编码方式
    NIND = parameters.NIND  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes,
                      problem.ranges, problem.borders)  # 创建区域描述器
    # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    population = ea.Population(Encoding, Field, NIND)
    """===============================算法参数设置=============================="""
    # class My_GA_templet(ea.soea_SGA_templet):
    # class My_GA_templet(ea.soea_GGAP_SGA_templet):
    # class My_GA_templet(ea.soea_EGA_templet):
    # class My_GA_templet(ea.soea_SEGA_templet):
    # class My_GA_templet(ea.soea_steadyGA_templet):
    class My_GA_templet(ea.soea_studGA_templet):
        def __init__(self, problem, population):
            # ea.soea_SGA_templet.__init__(self, problem, population)
            # ea.soea_GGAP_SGA_templet.__init__(self, problem, population)
            # ea.soea_EGA_templet.__init__(self, problem, population)
            # ea.soea_SEGA_templet.__init__(self, problem, population)
            # ea.soea_steadyGA_templet.__init__(self, problem, population)
            ea.soea_studGA_templet.__init__(self, problem, population)
            self.keep = 0
            self.MAXKEEP = parameters.MAXKEEP
            self.lastOPT = 0
            self.passTime = 0
            self.MAXTIME = parameters.MAXTIME

        def terminated(self, pop):  # 判断是终止进化，pop为当代种群对象
            self.stat(pop)  # 进行统计分析，更新进化记录器
            if self.BestIndi.ObjV is None:  # 没有符合约束，直接进下一代
                self.currentGen += 1
                return False
            if self.BestIndi.ObjV[0][0] == self.lastOPT:
                self.keep += 1  # 最优值保持代数
            else:
                self.keep = 0
            self.lastOPT = self.BestIndi.ObjV[0][0]
            if self.currentGen + 1 >= self.MAXGEN or self.keep >= self.MAXKEEP:
                # if self.passTime >= self.MAXTIME:
                return True
            else:
                self.currentGen += 1  # 进化代数+1returnFalse
                return False
    myAlgorithm = My_GA_templet(problem, population)
    myAlgorithm.MAXGEN = parameters.MAXGEN  # 最大进化代数
    myAlgorithm.logTras = parameters.logTras  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================根据先验知识创建先知种群========================"""
    initChrom = getInit(start, end, places.shape[0], parameters.NIND)
    prophetChrom = initChrom  # 假设已知比较优秀的染色体
    prophetPop = ea.Population(
        Encoding, Field, parameters.NIND, prophetChrom)  # 实例化种群对象（设置个体数为NIND）
    myAlgorithm.call_aimFunc(prophetPop)  # 计算先知种群的目标函数值及约束（假如有约束）
    """==========================调用算法模板进行种群进化========================="""
    [BestIndi, population] = myAlgorithm.run(
        prophetPop)  # 执行算法模板，得到最优个体以及最后一代种群
    # print('GA.py final:\n', population.Chrom)
    # [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """=================================输出结果==============================="""
    print('评价次数：%s' % myAlgorithm.evalsNum)
    print('时间已过 %s 秒' % myAlgorithm.passTime)
    if BestIndi.sizes != 0:
        print('最短路程为：%s' % BestIndi.ObjV[0][0])
        print('最佳路线为：')
        if index == 0 or parameters.K == 1:
            best_journey = np.hstack(
                [BestIndi.Phen[0, :], BestIndi.Phen[0, 0]])
        else:
            best_journey = BestIndi.Phen[0, :]
        route = []
        for i in range(len(best_journey)):
            print(int(best_journey[i]), end=' ')
            route.append(places[best_journey[i]])
        print()
        if parameters.K == 1:
            # 绘图
            plt.figure()
            plt.plot(problem.places[best_journey.astype(int), 1],
                     problem.places[best_journey.astype(int), 0], c='black')
            plt.plot(problem.places[best_journey.astype(int), 1],
                     problem.places[best_journey.astype(int), 0], 'o', c='red')
            plt.grid(True)
            plt.savefig('tsp_map.svg', dpi=600, bbox_inches='tight')
            plt.show()
        return BestIndi.ObjV[0][0], best_journey, route
    else:
        print('没找到可行解。')
        return None, None, None


def getInit(start, end, len, n):
    res = []
    print('长度：', len, '数量：', n)
    for i in range(n):
        arr = list(range(0, len))
        random.shuffle(arr)
        if start != None:
            start_index = arr.index(start)
            arr[0], arr[start_index] = arr[start_index], arr[0]
        if end != None:
            end_index = arr.index(end)
            arr[-1], arr[end_index] = arr[end_index], arr[-1]
        res.append(arr)
    return np.array(res)


if __name__ == '__main__':
    main('0')
