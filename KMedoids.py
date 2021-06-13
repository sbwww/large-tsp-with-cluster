import random
import time

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

import parameters

data = np.loadtxt('data/'+parameters.dataset+'.csv',
                  delimiter=',', encoding='UTF-8-sig')
D = pairwise_distances(data, metric='euclidean')


def kMedoids(D, k, tmax=200):
    # determine dimensions of distance matrix D
    m, n = D.shape
    if k > n:
        raise Exception('too many medoids')
    # find a set of valid initial cluster medoid indices since we
    # can't seed different clusters with two points at the same location
    valid_medoid_inds = set(range(n))
    invalid_medoid_inds = set([])
    rs, cs = np.where(D == 0)
    # the rows, cols must be shuffled because we will keep the first duplicate below
    index_shuf = list(range(len(rs)))
    np.random.shuffle(index_shuf)
    rs = rs[index_shuf]
    cs = cs[index_shuf]
    for r, c in zip(rs, cs):
        # if there are two points with a distance of 0...
        # keep the first one for cluster init
        if r < c and r not in invalid_medoid_inds:
            invalid_medoid_inds.add(c)
    valid_medoid_inds = list(valid_medoid_inds - invalid_medoid_inds)
    if k > len(valid_medoid_inds):
        raise Exception('too many medoids (after removing {} duplicate points)'.format(
            len(invalid_medoid_inds)))
    # randomly initialize an array of k medoid indices
    M = np.array(valid_medoid_inds)
    np.random.shuffle(M)
    M = np.sort(M[:k])
    # create a copy of the array of medoid indices
    Mnew = np.copy(M)
    # initialize a dictionary to represent clusters
    C = {}
    for _ in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa], C[kappa])], axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:  # 有这个语法，for 循环执行完
        # final update of cluster memberships
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]
    # return results
    return M, C


def main(argv):
    K = argv
    cnt = 0
    # split into K clusters
    M, C = kMedoids(D, K)
    print('')
    print('medoids:')
    f = open('data/cluster/0.csv',
             'w', encoding='UTF-8-sig')
    for i in range(K):  # 中心坐标
        print(str(data[M[i]][1])+','+str(data[M[i]][0]), file=f)
    f.close()
    print('clusters:')
    for i in range(K):  # 每个类的所有元素
        f = open('data/cluster/'+str(i+1)+'.csv',
                 'w', encoding='UTF-8-sig')
        for p in C[i]:
            cnt += 1
            print(str(data[p][1])+','+str(data[p][0]), file=f)
        f.close()
    print(str(K)+' clusters, '+str(cnt)+' points in total')


if __name__ == '__main__':
    start = time.process_time()
    main(parameters.K)
    end = time.process_time()
    print('finish clustering in %s' % str(end - start))
