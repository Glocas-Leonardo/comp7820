import numpy as np
import matplotlib.pyplot as plt
import csv #可以导入csv文件

#封装DensityPeak算法，初始化类
class DensityPeakCluster:
    def __init__(self, file_name):
        self.file_name = file_name
        self.datas = self.load_data(file_name)
        self.dists = self.get_distance_matrix(self.datas)
        self.dc = self.select_dc(self.dists)
        self.rho = self.get_density(self.dists, self.dc, method="Gaussian")
        self.deltas, self.nearest_neiber = self.get_deltas(self.dists, self.rho)
        self.centers = self.find_centers_K(self.rho, self.deltas, 3)
        self.labs = self.cluster_PD(self.rho, self.centers, self.nearest_neiber)
        self.draw_decision(self.rho, self.deltas, file_name + "_decision.jpg")
        self.draw_cluster(self.datas, self.labs, self.centers, file_name + "_cluster.jpg")
        #self.draw_decision()
        #self.draw_cluster()

    def load_data(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
        lines = [line.split(",")[:2] for line in lines]
        datas = np.array(lines).astype(np.float32)
        return datas

# 计算数据点两两之间的距离
    def get_distance_matrix(self, datas):
        N, D = np.shape(datas)
        dists = np.zeros([N, N])
        for i in range(N):
            for j in range(N):
                vi = datas[i, :]
                vj = datas[j, :]
                dists[i, j] = np.sqrt(np.dot((vi - vj), (vi - vj)))
        return dists

    # 找到密度计算的阈值dc
    # 要求平均每个点周围距离小于dc的点的数目占总点数的1%-2%
    def select_dc(self, dists):
        '''算法1'''
        N = np.shape(dists)[0]
        tt = np.reshape(dists, N * N)
        percent = 2.0
        position = int(N * (N - 1) * percent / 100)
        dc = np.sort(tt)[position + N]
        return dc

    # 计算每个点的局部密度
    def get_density(self, dists, dc, method=None):
        N = np.shape(dists)[0]
        rho = np.zeros(N)
        for i in range(N):
            if method is None:
                rho[i] = np.where(dists[i, :] < dc)[0].shape[0] - 1
            else:
                rho[i] = np.sum(np.exp(-(dists[i, :] / dc) ** 2)) - 1
        return rho

    # 计算每个数据点的密度距离
    # 即对每个点，找到密度比它大的所有点
    # 再在这些点中找到距离其最近的点的距离
    def get_deltas(self, dists, rho):
        N = np.shape(dists)[0]
        deltas = np.zeros(N)
        nearest_neiber = np.zeros(N)
         # 将密度从大到小排序
        index_rho = np.argsort(-rho)
        for i, index in enumerate(index_rho):
            # 对于密度最大的点
            if i == 0:
                continue

            # 对于其他的点
            # 找到密度比其大的点的序号
            index_higher_rho = index_rho[:i]
            # 获取这些点距离当前点的距离,并找最小值
            deltas[index] = np.min(dists[index, index_higher_rho])

            # 保存最近邻点的编号
            index_nn = np.argmin(dists[index, index_higher_rho])
            nearest_neiber[index] = index_higher_rho[index_nn].astype(int)

        deltas[index_rho[0]] = np.max(deltas)
        return deltas, nearest_neiber

    # 通过阈值选取 rho与delta都大的点
    # 作为聚类中心    
    def find_centers_auto(rho, deltas):
        rho_threshold = (np.min(rho) + np.max(rho)) / 2
        delta_threshold = (np.min(deltas) + np.max(deltas)) / 2
        N = np.shape(rho)[0]
 
        centers = []
        for i in range(N):
            if rho[i] >= rho_threshold and deltas[i] > delta_threshold:
                centers.append(i)
        return np.array(centers)
    
    # 选取 rho与delta乘积较大的点作为
    # 聚类中心  
    def find_centers_K(self, rho, deltas, K):
        rho_delta = rho * deltas
        centers = np.argsort(-rho_delta)
        return centers[:K]


    def cluster_PD(self, rho, centers, nearest_neiber):
        K = np.shape(centers)[0]
        if K == 0:
            print("can not find centers")
            return
        
        N = np.shape(rho)[0]
        labs = -1 * np.ones(N).astype(int)

        # 首先对几个聚类中进行标号
        for i, center in enumerate(centers):
            labs[center] = i

        ## 从密度大的点进行标号
        index_rho = np.argsort(-rho)
        for i, index in enumerate(index_rho):
            if labs[index] == -1:
            # 如果没有被标记过
            # 那么聚类标号与距离其最近且密度比其大
            # 的点的标号相同
                labs[index] = labs[int(nearest_neiber[index])]
        return labs

    def draw_decision(self, rho, deltas, name):
        plt.cla()
        for i in range(np.shape(self.datas)[0]):
            plt.scatter(rho[i], deltas[i], s=16., color=(0, 0, 0))
            plt.annotate(str(i), xy=(rho[i], deltas[i]), xytext=(rho[i], deltas[i]))
            plt.xlabel("rho")
            plt.ylabel("deltas")
        plt.savefig(name)
        #plt.show()

    def draw_cluster(self, datas, labs, centers, name):
        plt.cla()
        dic_colors = {0: (.8, 0, 0), 1: (0, .8, 0), 2: (0, 0, .8), 3: (.8, .8, 0), 4: (.8, 0, .8), 5: (0, .8, .8), 6: (0, 0, 0)}
        K = np.shape(centers)[0]
        for k in range(K):
            sub_index = np.where(labs == k)
            sub_datas = datas[sub_index]
            # 画数据点
            plt.scatter(sub_datas[:, 0], sub_datas[:, 1], s=16., color=dic_colors[k])
            # 画聚类中心
            plt.scatter(datas[centers[k], 0], datas[centers[k], 1], color="k", marker="+", s=200.)
        plt.savefig(name)
        #plt.show()

#if __name__ == "__main__":
   # file_name = 'dpc_dataset.txt'
  #  dp_cluster = DensityPeakCluster(file_name)



