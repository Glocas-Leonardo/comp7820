'''
@Time:2024/3/17 0:47
@Author:Glocas
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# 函数功能：画出样本的散点图
def drawScatter(data_set, ax):
    # 显示数据集
    point_x = data_set[:, 0]  # 取所有行的第0个数据
    point_y = data_set[:, 1]  # 取所有行的第1个数据
    ax.scatter(point_x, point_y, s=30, c="red", marker="o", label="sample point")  # 绘制散点图 s为点的大小
    ax.legend()  # 显示图例
    ax.set_xlabel("factor1")
    ax.set_ylabel("factor2")
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
    my_centroids = draw_centroids(ax)  # centroids是列表，其中的元素是元组
    return my_centroids, bnext, bcolor, bskip, bkmeans

# 函数功能：通过鼠标单击，添加质心并保存，以及画出质心
def draw_centroids(ax):
    global color
    global marker
    k = int(input("请输入添加的质心数量k: "))
    pos_set = []        # 创建列表存放质心

    for i in range(k):
        pos = plt.ginput(1,timeout=-1)     # 获得鼠标点击位置——使用ginput函数
        ax.scatter(pos[0][0], pos[0][1], s=100, c=color[i], marker=marker[i], label="centroids") #pos[0][0]为鼠标点击后获取到的横坐标
        pos_set.append(pos[0])  # 保存质心
    print(f"初始质心：{pos_set}")
    return pos_set

def draw_ax(ax):
    global my_centroids
    global cluster

    # 清除ax
    ax.clear()

    # 画上数据集
    data_x = data_set[:, 0]
    data_y = data_set[:, 1]
    ax.scatter(data_x, data_y, s=30, c="red", marker="o", label="sample point")
    plt.pause(0.1)

    # 画上质心
    for i in range(len(my_centroids)):
        ax.scatter(my_centroids[i][0], my_centroids[i][1], s=100, c=color[i], marker=marker[i], label="sample point")

    # 改变已分类的点的颜色
    if len(cluster):
        index = 0
        for i in cluster:
            ax.scatter(data_x[index], data_y[index], s=30, c=color[i], marker="o", label="sample point")
            index += 1
    plt.pause(0.1)

# 函数功能：计算两个向量之间欧氏距离
def dist_eclud(vecA, vecB):
    vecB = np.append(vecB, np.zeros(len(vecA) - len(vecB)))
    dist = np.sqrt(np.sum((vecA - vecB) ** 2))
    return dist
    # vec_square = []
    # for element in vecA - vecB:
    #     element = element ** 2
    #     vec_square.append(element)
    # return sum(vec_square) ** 0.5

def load_data_set(file_name):
    data_mat = []
    with open(file_name) as fr:
        # 按行读出文件内数据
        for line in fr.readlines():
            curLine = line.strip().split(',')  # 去掉末尾的’\n‘，返回一个列表
            fltLine = list(map(lambda x: float(x), curLine))  # map 与 lambda
            data_mat.append(fltLine)
    return np.array(data_mat)

# 按钮的功能:
# （1）点击->连线1个点和所有质心，计算距离并保存最小的距离和质心，并记录该点属于哪一个簇->找到最短的距离，改变该线段的颜色
# （2）点击->根据簇，改变该点的颜色，并删除所有的线段
class button:
    global ax
    global data_set
    global color
    global marker
    min_dist = np.inf
    min_index = -1
    i = 0  # 遍历的data_set下标

    # def draw_dist(self, event, ax, dot, centroids):  这是错误写法
    # 注意在括号内写上event，event表示点击按钮 后 触发
    def draw_dist(self, event):  # next按钮的功能
        global my_centroids
        global cluster
        print("\n-------next-------")
        if button.i + 1 == len(data_set):
            print("数据集已遍历完毕，请点击kMeans按钮！")
            return
        print(f"正在遍历第{button.i}个样本点！")
        dot = data_set[button.i]
        plt.pause(0.1)

        for k in range(len(my_centroids)):
            x = [dot[0], my_centroids[k][0]]
            y = [dot[1], my_centroids[k][1]]
            ax.plot(x, y, c="black")  # 绘制直线
            dist = dist_eclud(dot, my_centroids[k])  # 计算距离
            if dist < button.min_dist:
                button.min_dist = dist  # 最小距离
                button.min_index = k  # 下标
        # 保存该点的质心
        print(f"cluster中的元素数量：{len(cluster)}")
        if len(cluster) < len(data_set):
            cluster.append(button.min_index)
            print("已分类的样本点数+1")
        else:
            cluster[button.i] = button.min_index
        print(f"第{button.i}个样本点属于簇{button.min_index}。")
        button.i += 1
        # 改变最短距离的颜色
        x = [dot[0], my_centroids[button.min_index][0]]
        y = [dot[1], my_centroids[button.min_index][1]]
        ax.plot(x, y, c="red")
        plt.pause(0.1)

        # 重新初始化
        button.min_dist = np.inf
        button.min_index = -1
        return

    def change_color(self, event):  # classify按钮的功能
        print("\n-----classify------")
        draw_ax(ax)
        print("已更改样本点颜色")

    # 函数功能： 跳过接下来未完成的分类
    def skip_change(self, event):
        global my_centroids
        global cluster
        print("\n-------skip--------")
        if button.i + 1 == len(data_set):
            print("数据集已遍历完毕，请点击kMeans按钮！")
            return
        cluster = []  # 初始化已分类样本点集
        # 计算所有的点到所有质心的距离，分类，保存结果
        for j in range(len(data_set)):
            button.min_dist = np.inf
            button.min_index = -1
            for k in range(len(my_centroids)):
                dist = dist_eclud(data_set[j], my_centroids[k])  # 计算距离
                if dist < button.min_dist:
                    button.min_dist = dist
                    button.min_index = k
            cluster.append(button.min_index)
        plt.pause(0.1)
        draw_ax(ax)  # 重新绘制
        button.i = len(data_set) - 1
        print("已成功跳过数据样本的遍历过程！")

    # 函数功能：根据分类结果重新计算质心
    def kMeans(self, event):
        global my_centroids
        global cluster
        print("\n------kMeans-------")
        # cluster中已经保存了每个数据的分类结果，根据相同的分类，把坐标相加，重新计算质心，比较质心是否改变
        centroids_change = []
        for k in range(len(my_centroids)):  # 遍历每个质心
            sum_x = 0
            sum_y = 0
            count = 0
            for i in range(len(cluster)):  # 遍历分类结果集
                if cluster[i] == k:
                    sum_x += data_set[i][0]
                    sum_y += data_set[i][1]
                    count += 1
            avg_x = sum_x / count
            avg_y = sum_y / count
            avg = (avg_x, avg_y)
            centroids_change.append(avg)  # 产生新的质心坐标
        if my_centroids == centroids_change:  # 如果质心不改变
            print("实验已完成！")
            plt.savefig('./kMeans.jpg')
            return
        # 根据新的质心重新绘图
        my_centroids = centroids_change
        print(f"簇质心更改成功！\n新的簇质心: {my_centroids}")
        draw_ax(ax)
        plt.pause(0.1)
        # 重新分类，一切归零
        button.i = 0

# color可选参数
color = ["pink", "blue", "green", "orange", "purple"]
# marker可选参数
marker = ['^', '+', 'p', 's', '*']
# 全局变量（因为按钮的函数里不能带参，所以只能用全局变量了）
# 从文件中读取数据
data_set = load_data_set("kmeans_dataset.txt")
# 使用matplotlib，画出数据集和按钮
fig, ax = plt.subplots(figsize=(8, 8))
my_centroids, bnext, bcolor, bskip, bkmeans = drawScatter(data_set, ax)
# 保存样本点所属的簇
cluster = []

def main():
    # 使用next按钮
    bnext.on_clicked(button().draw_dist)  # 不能写参数，不能加()
    # 使用classify按钮
    bcolor.on_clicked(button().change_color)
    # 使用skip按钮
    bskip.on_clicked(button().skip_change)
    # 使用kMeans按钮
    bkmeans.on_clicked(button().kMeans)
    plt.pause(300)  # 显示秒数
    plt.close()

if __name__ == '__main__':
    main()
