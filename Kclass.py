import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#封装Kmeans类
class KMeansCluster:
    def __init__(self, data_set_file):
        self.data_set = self.load_data_set(data_set_file)
        self.color = ["pink", "blue", "green", "orange", "purple"]
        self.marker = ['^', '+', 'p', 's', '*']
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.my_centroids, self.bnext, self.bcolor, self.bskip, self.bkmeans = self.drawScatter()

        self.cluster = []
        self.min_dist = np.inf
        self.min_index = -1
        self.i = 0

    def load_data_set(self, file_name):
        data_mat = []
        with open(file_name) as fr:
            #按行读出文件内数据
            for line in fr.readlines():
                cur_line = line.strip().split(',')  # 去掉末尾的’\n‘，返回一个列表
                flt_line = list(map(lambda x: float(x), cur_line))  # map 与 lambda
                data_mat.append(flt_line)
        return np.array(data_mat)

    # 函数功能：画出样本的散点图
    def drawScatter(self):
        # 显示数据集
        point_x = self.data_set[:, 0]   # 取所有行的第0个数据
        point_y = self.data_set[:, 1]   # 取所有行的第1个数据
        self.ax.scatter(point_x, point_y, s=30, c="red", marker="o", label="sample point")  # 绘制散点图 s为点的大小
        self.ax.legend()    # 显示图例
        self.ax.set_xlabel("factor1")
        self.ax.set_ylabel("factor2")

        # 增加按钮
        plt.subplots_adjust(bottom=0.2)

        # 确定按钮位置
        ax_next = plt.axes([0.82, 0.05, 0.05, 0.05])
        ax_color = plt.axes([0.75, 0.05, 0.06, 0.05])
        ax_skip = plt.axes([0.69, 0.05, 0.05, 0.05])
        ax_kmeans = plt.axes([0.62, 0.05, 0.06, 0.05])

        # 按钮文字和颜色信息
        bnext = Button(ax_next, 'next', color='khaki', hovercolor='yellow')
        bcolor = Button(ax_color, 'classify', color='khaki', hovercolor='yellow')
        bskip = Button(ax_skip, 'skip', color='khaki', hovercolor='yellow')
        bkmeans = Button(ax_kmeans, 'kMeans', color='khaki', hovercolor='yellow')

        # 获取鼠标点击位置，并画出质心
        my_centroids = self.draw_centroids()
        return my_centroids, bnext, bcolor, bskip, bkmeans

    # 函数功能：通过鼠标单击，添加质心并保存，以及画出质心
    def draw_centroids(self):
        pos_set = []
        k = int(input("Enter the number of centroids (k): "))   # 创建列表存放质心
        for i in range(k):
            pos = plt.ginput(1, timeout=-1)     # 获得鼠标点击位置——使用ginput函数
            self.ax.scatter(pos[0][0], pos[0][1], s=100, c=self.color[i], marker=self.marker[i], label="centroids") #pos[0][0]为鼠标点击后获取到的横坐标
            pos_set.append(pos[0])  # 保存质心
        print(f"Initial centroids: {pos_set}")
        return pos_set

    def draw_ax(self):
        self.ax.clear()     # 清除ax
        self.ax.scatter(self.data_set[:, 0], self.data_set[:, 1], s=30, c="red", marker="o", label="sample point")
        plt.pause(0.1)

        # 画上质心
        for i in range(len(self.my_centroids)):
            self.ax.scatter(self.my_centroids[i][0], self.my_centroids[i][1], s=100, c=self.color[i], marker=self.marker[i], label="sample point")

        # 改变已分类的点的颜色
        if len(self.cluster):
            index = 0
            for i in self.cluster:
                self.ax.scatter(self.data_set[index][0], self.data_set[index][1], s=30, c=self.color[i], marker="o", label="sample point")
                index += 1

        legend_labels = ["sample point", "centroids"]
        self.ax.legend(legend_labels)

        plt.pause(0.1)
        self.fig.canvas.draw()

    # 函数功能：计算两个向量之间欧氏距离
    def dist_eclud(self, vecA, vecB):
        vecB = np.append(vecB, np.zeros(len(vecA) - len(vecB)))
        dist = np.sqrt(np.sum((vecA - vecB) ** 2))
        return dist
        # vec_square = []
        # for element in vecA - vecB:
        #     element = element ** 2
        #     vec_square.append(element)
        # return sum(vec_square) ** 0.5

    # next按钮的功能
    def draw_dist(self, event):
        if self.i == len(self.data_set):
            print("Dataset has been fully traversed. Please click the 'kMeans' button!")
            return

        print(f"Traversing the {self.i}th sample point! ")
        dot = self.data_set[self.i]
        plt.pause(0.1)

        for k in range(len(self.my_centroids)):
            x = [dot[0], self.my_centroids[k][0]]
            y = [dot[1], self.my_centroids[k][1]]
            self.ax.plot(x, y, c="black")   # 绘制直线
            dist = self.dist_eclud(dot, self.my_centroids[k])   # 计算距离
            if dist < self.min_dist:
                self.min_dist = dist        # 最小距离
                self.min_index = k          # 下标
        # 保存该点的质心
        print(f"The element numbers in the cluster:{len(self.cluster)}")
        if len(self.cluster) < len(self.data_set):
            self.cluster.append(self.min_index)
            print("Classified sample points+1")
        else:
            self.cluster[self.i] = self.min_index
        print(f"{self.i}sample point belongs to cluster{self.min_index}.")
        self.i += 1
        
        #改变最短距离的颜色
        x = [dot[0], self.my_centroids[self.min_index][0]]
        y = [dot[1], self.my_centroids[self.min_index][1]]
        self.ax.plot(x, y, c="red")
        plt.pause(0.1)

        #重新初始化
        self.min_dist = np.inf
        self.min_index = -1
        self.i += 1


        self.fig.canvas.draw()

    def change_color(self, event):      #classify按钮的功能
        self.draw_ax()
        print("Color of sample points has been changed.")

    #函数功能：跳过接下来未完成的分类
    def skip_change(self, event):
        if self.i + 1 == len(self.data_set):
            print("Dataset has been fully traversed. Please click the 'kMeans' button!")
            return
        self.cluster = []       #初始化已分类样本点集
        # 计算所有的点到所有质心的距离，分类，保存结果
        for j in range(len(self.data_set)):
            self.min_dist = np.inf
            self.min_index = -1
            for k in range(len(self.my_centroids)):
                dist = self.dist_eclud(self.data_set[j], self.my_centroids[k])  #计算距离
                if dist < self.min_dist:
                    self.min_dist = dist
                    self.min_index = k
            self.cluster.append(self.min_index)
        plt.pause(0.1)
        self.draw_ax()  #重新绘制
        self.i = len(self.data_set) - 1
        print("Skipped the traversal process of data samples.")


    # 函数功能：根据分类结果重新计算质心
    def kMeans(self, event):
        print("\n------kMeans-------")
        # cluster中已经保存了每个数据的分类结果，根据相同的分类，把坐标相加，重新计算质心，比较质心是否改变
        centroids_change = []
        for k in range(len(self.my_centroids)): # 遍历每个质心
            sum_x = 0
            sum_y = 0
            count = 0
            for i in range(len(self.cluster)):  # 遍历分类结果集
                if self.cluster[i] == k:
                    sum_x += self.data_set[i][0]
                    sum_y += self.data_set[i][1]
                    count += 1
            avg_x = sum_x / count
            avg_y = sum_y / count
            avg = (avg_x, avg_y)
            centroids_change.append(avg)    # 产生新的质心坐标

        if self.my_centroids == centroids_change:   # 如果质心不改变
            print("Experiment completed!")
            plt.savefig('./kMeans.jpg')
            return
        
        # 根据新的质心重新绘图
        self.my_centroids = centroids_change
        print(f"Cluster centroids updated!\nNew centroids: {self.my_centroids}")
        self.draw_ax()
        plt.pause(0.1)
        # 重新分类，一切归零
        self.i = 0

        self.fig.canvas.draw()

    def run(self):
        self.bnext.on_clicked(self.draw_dist)       #next按钮
        self.bcolor.on_clicked(self.change_color)   #classify按钮
        self.bskip.on_clicked(self.skip_change)     #skip按钮
        self.bkmeans.on_clicked(self.kMeans)        #Kmeans按钮
        plt.show()

# if __name__ == '__main__':
#     kmeans_cluster = KMeansCluster("kmeans_dataset.txt")
#     kmeans_cluster.run()





