import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Dclass import DensityPeakCluster  #导入DensityPeak类
from Kclass import KMeansCluster       #导入Kmeans类

class AlgorithmSelectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorithm Selection")      #界面标题
        self.file_path = None
        self.selected_algorithm = tk.StringVar()

        self.algorithm_label = tk.Label(self.root, text="Select Algorithm:")    #选择算法
        self.algorithm_label.pack()

        self.algorithm_options = ['K-means', 'Density Peak']    #可选算法类别
        self.algorithm_menu = tk.OptionMenu(self.root, self.selected_algorithm, *self.algorithm_options)
        self.algorithm_menu.pack()

        self.upload_button = tk.Button(self.root, text="Upload Data", command=self.upload_data) #上传数据集
        self.upload_button.pack()

        self.result_canvas = tk.Canvas(self.root, width=400, height=400)
        self.result_canvas.pack()

        self.execute_button = tk.Button(self.root, text="Execute Algorithm", command=self.execute_algorithm)
        self.execute_button.pack()

    def upload_data(self):
        self.file_path = filedialog.askopenfilename()       #上传的数据集
        messagebox.showinfo("Upload", "Data uploaded successfully!")

    def execute_algorithm(self):                            #执行算法按钮
        selected_algorithm_value = self.selected_algorithm.get()
        if selected_algorithm_value == 'K-means':           #选择执行Kmeans算法
            kmeans_cluster = KMeansCluster(self.file_path)
            kmeans_cluster.run()                            #Kmeans类里面的四大按钮，见Kmeans类
        elif selected_algorithm_value == 'Density Peak':    #选择执行DensityPeak算法
            density_peak_cluster = DensityPeakCluster(self.file_path)
            density_peak_cluster.draw_decision()            #绘制密度/距离分布图
            density_peak_cluster.draw_cluster()             #聚类中心图

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = AlgorithmSelectionApp()
    app.run()
