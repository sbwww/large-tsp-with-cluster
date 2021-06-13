import time

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

import GA
import KMedoids
import parameters

total_route = []


def get_dis(a, b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


def get_nearest(a, b):
    # a.csv 和 b.csv 中找出最近的点对 (pa,pb)这里是序号
    # a 的中点为 pa，b 的起点为 pb
    # 返回最近点对序号和距离
    point_list_a = np.loadtxt(
        "data/cluster/" + str(a) + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
    point_list_b = np.loadtxt(
        "data/cluster/" + str(b) + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
    D = pairwise_distances(point_list_a, point_list_b, metric='euclidean')
    min_index = np.unravel_index(D.argmin(), D.shape)
    # 返回     本类终点     下一类起点    最小距离
    return min_index[0], min_index[1], np.min(D)


def get_2nd_nearest(a, b):
    # a.csv 和 b.csv 中找出第二近的点对 (pa,pb)这里是序号
    print('called 2nd nearest')
    point_list_a = np.loadtxt(
        "data/cluster/" + str(a) + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
    point_list_b = np.loadtxt(
        "data/cluster/" + str(b) + ".csv", delimiter=",", usecols=(0, 1), encoding='UTF-8-sig')
    D = pairwise_distances(point_list_a, point_list_b, metric='euclidean')
    min_index = np.unravel_index(D.argmin(), D.shape)
    print('D min: ', D.min(), 'at ', min_index)
    Dcopy = D.copy()
    Dcopy[min_index[0]][:] = np.full(Dcopy.shape[1], float('inf'))
    min_index = np.unravel_index(Dcopy.argmin(), Dcopy.shape)
    print('D 2nd min:', Dcopy.min(), 'at ', min_index)
    # 返回     本类终点     下一类起点    最小距离
    return min_index[0], min_index[1], np.min(Dcopy)


def main():
    KMedoids.main(parameters.K)

    in_dis = 0  # 类内
    out_dis = 0  # 类间

    if parameters.K == 1:
        in_dis, _, route = GA.main(1)
    else:
        _, cluster_index, cluster_route = GA.main(0)  # 类间
        last_end, next_start, cluster_dis = get_nearest(
            cluster_index[-2]+1, cluster_index[0]+1)  # 第一个cluster的起点
        out_dis += cluster_dis
        for i in range(parameters.K):  # [0, K-1]
            print('第'+str(i)+'个：'+str(cluster_index[i]))

            start = next_start
            if i < parameters.K-1:
                # i终点  i+1起点
                end, next_start, cluster_dis = get_nearest(
                    cluster_index[i]+1, cluster_index[i+1]+1)
                if start == end:
                    end, next_start, cluster_dis = get_2nd_nearest(
                        cluster_index[i]+1, cluster_index[i+1]+1)
                out_dis += cluster_dis
            else:
                end = last_end
            dis = None  # 与后面判断GA是否有可行解相关
            while dis is None:
                dis, _, route = GA.main(cluster_index[i]+1, start, end)
            total_route.append(route)
            in_dis += dis
    print('----------final answer----------')
    total_dis = in_dis+out_dis
    print('类内距离', in_dis, '总距离', total_dis)
    optimal = parameters.benchmark[parameters.dataset]
    print('最优', optimal)
    print('误差', abs(total_dis-optimal)/optimal)
    f = open('data/final_ans.csv',
             'w', encoding='UTF-8-sig')
    for r in total_route:
        for i in r:
            print(','.join(map(str, i)), file=f)


if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print('finish all in %s' % str(end - start))
