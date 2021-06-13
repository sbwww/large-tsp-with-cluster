# -*- coding: utf-8 -*-
import geatpy as ea
import numpy as np

import parameters


class TestProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, testName, start=None, end=None):  # testName为测试集名称
        name = testName  # 初始化name
        self.flag = int(name)  # 0 则返回出发点，>0 则不返回
        # 读取城市坐标数据
        self.places = np.loadtxt(
            "data/cluster/" + testName + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
        self.start = start
        self.end = end
        M = 1  # 初始化M（目标维数）
        Dim = self.places.shape[0]  # 初始化Dim（决策变量维数）
        """================目标================"""
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        ub = [Dim - 1] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim,
                            varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        x = pop.Phen.copy()  # 得到决策变量矩阵
        con = [0, 0]  # 约束：首位，末位
        if self.flag == 0 or parameters.K == 1:
            # 添加最后回到出发地
            X = np.hstack([x, x[:, [0]]]).astype(int)
        else:
            X = x.astype(int)
        ObjV = []  # 存储所有种群个体对应的总路程
        for i in range(pop.sizes):
            journey = self.places[X[i], :]  # 按既定顺序到达的地点坐标
            distance = np.sum(
                np.sqrt(np.sum((np.diff(journey.T) ** 2), 0)))  # 计算总路程
            ObjV.append(distance)
            if self.start != None and self.end != None:
                con = np.vstack(
                    (con, [abs(X[i][0]-self.start), abs(X[i][-1]-self.end)]))
        if self.start != None and self.end != None:
            con = con[1:]
            pop.CV = con  # 采用可行性法则处理约束
        pop.ObjV = np.array([ObjV]).T
