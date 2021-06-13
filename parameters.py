dataset = 'u1432'  # TSP数据集
K = 50  # 聚类 K，K=0即普通的GA
NIND = 200  # 种群规模
MAXGEN = 800  # 最大代数
MAXKEEP = 200  # 最大保持代数
logTras = 100  # 设置每隔多少代记录日志，若设置成0则表示不记录日志

MAXTIME = 20

benchmark = {
    ### world tsp ###
    'dj38': 6656,
    'qa194': 9352,
    'uy734': 79114,
    'zi929': 95345,
    'lu980': 11340,  # includes duplications
    'eg7146': 172387,
    ### tsplib ###
    'att48': 33609,  # 10628 is fake Euclidean
    'pr136': 96772,  # significant 8 clusters
    'u159': 42080,
    'u574': 36905,
    'u1060': 224094,
    'u1432': 152970,
    'u2152': 64253,
}
