import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Dclass import DensityPeakCluster  # 导入 DensityPeak 类
from Kclass import KMeansCluster       # 导入 Kmeans 类

class AlgorithmSelectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorithm Selection")      # 界面标题
        self.root.geometry("800x400")  # 设置窗口大小
        self.file_path_kmeans = None
        self.file_path_density_peak = None

        self.kmeans_frame = tk.Frame(self.root)
        self.kmeans_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.kmeans_label = tk.Label(self.kmeans_frame, text="K-means Data Set:")
        self.kmeans_label.pack()
        self.kmeans_upload_button = tk.Button(self.kmeans_frame, text="Upload Data", command=self.upload_kmeans_data)
        self.kmeans_upload_button.pack()
        self.kmeans_execute_button = tk.Button(self.kmeans_frame, text="Execute K-means", command=self.execute_kmeans_algorithm)
        self.kmeans_execute_button.pack()

        self.density_peak_frame = tk.Frame(self.root)
        self.density_peak_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.density_peak_label = tk.Label(self.density_peak_frame, text="Density Peak Data Set:")
        self.density_peak_label.pack()
        self.density_peak_upload_button = tk.Button(self.density_peak_frame, text="Upload Data", command=self.upload_density_peak_data)
        self.density_peak_upload_button.pack()
        self.density_peak_execute_button = tk.Button(self.density_peak_frame, text="Execute Density Peak", command=self.execute_density_peak_algorithm)
        self.density_peak_execute_button.pack()

    def upload_kmeans_data(self):
        self.file_path_kmeans = filedialog.askopenfilename()  # 上传 K-means 的数据集
        if not self.file_path_kmeans:
            messagebox.showerror("Error", "Failed to upload K-means data!")
        else:
            messagebox.showinfo("Upload", "K-means data uploaded successfully!")

    def upload_density_peak_data(self):
        self.file_path_density_peak = filedialog.askopenfilename()  # 上传 Density Peak 的数据集
        if not self.file_path_density_peak:
            messagebox.showerror("Error", "Failed to upload Density Peak data!")
        else:
            messagebox.showinfo("Upload", "Density Peak data uploaded successfully!")

    def execute_kmeans_algorithm(self):
        if self.file_path_kmeans:
            try:
                kmeans_cluster = KMeansCluster(self.file_path_kmeans)
                messagebox.showinfo("Execution", "K-means algorithm executed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute K-means algorithm: {e}")
        else:
            messagebox.showerror("Error", "Please upload K-means data first!")


    def execute_density_peak_algorithm(self):
        if self.file_path_density_peak:
            try:
                density_peak_cluster = DensityPeakCluster(self.file_path_density_peak)
                messagebox.showinfo("Execution", "Density Peak algorithm executed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute Density Peak algorithm: {e}")
        else:
            messagebox.showerror("Error", "Please upload Density Peak data first!")


    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = AlgorithmSelectionApp()
    app.run()


