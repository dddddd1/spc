#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class SPCDataManager:
    def __init__(self, data_file='spc_data.json'):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_project(self, name, data_type, usl=None, lsl=None):
        self.data[name] = {
            'type': data_type,
            'usl': usl,
            'lsl': lsl,
            'data': [],
            'created': datetime.now().isoformat()
        }
        self.save_data()

    def add_data(self, project_name, subgroup_data):
        if project_name in self.data:
            self.data[project_name]['data'].append({
                'timestamp': datetime.now().isoformat(),
                'values': subgroup_data
            })
            self.save_data()
            return True
        return False

    def delete_project(self, name):
        if name in self.data:
            del self.data[name]
            self.save_data()
            return True
        return False

    def get_project(self, name):
        return self.data.get(name)

    def get_all_projects(self):
        return list(self.data.keys())


class SPCAnalyzer:
    XBAR_R_CONSTANTS = {
        2: (0.577, 1.88, 0.00, 3.27),
        3: (0.484, 1.02, 0.00, 2.57),
        4: (0.429, 0.73, 0.00, 2.28),
        5: (0.395, 0.58, 0.04, 2.11),
        6: (0.370, 0.48, 0.10, 2.00),
        7: (0.351, 0.42, 0.16, 1.92),
        8: (0.337, 0.37, 0.22, 1.86),
        9: (0.325, 0.34, 0.27, 1.82),
        10: (0.315, 0.31, 0.31, 1.78)
    }

    @staticmethod
    def calculate_xbar_r(data):
        if not data or len(data) < 2:
            return None

        subgroup_means = [np.mean(d['values']) for d in data]
        subgroup_ranges = [max(d['values']) - min(d['values']) for d in data]

        x_bar = np.mean(subgroup_means)
        r_bar = np.mean(subgroup_ranges)
        n = len(data[0]['values'])

        if n in SPCAnalyzer.XBAR_R_CONSTANTS:
            a2 = SPCAnalyzer.XBAR_R_CONSTANTS[n][0]
        else:
            a2 = 3 / (n * np.sqrt(2))

        ucl_x = x_bar + a2 * r_bar
        lcl_x = x_bar - a2 * r_bar

        d3 = 0
        d4 = 2.459 if n <= 10 else 2.114 if n <= 15 else 1.964
        ucl_r = d4 * r_bar
        lcl_r = d3 * r_bar

        sigma = r_bar / 1.128 if n == 5 else r_bar / (SPCAnalyzer.XBAR_R_CONSTANTS.get(n, [0])[1] if n <= 10 else 2.059)

        return {
            'x_bar': x_bar,
            'r_bar': r_bar,
            'ucl_x': ucl_x,
            'lcl_x': lcl_x,
            'ucl_r': ucl_r,
            'lcl_r': lcl_r,
            'subgroup_means': subgroup_means,
            'subgroup_ranges': subgroup_ranges,
            'sigma': sigma,
            'n': n
        }

    @staticmethod
    def calculate_p_chart(data, subgroup_sizes=None):
        if not data:
            return None

        defectives = []
        sizes = []

        for d in data:
            values = d['values']
            if subgroup_sizes:
                n = subgroup_sizes[data.index(d)]
            else:
                n = len(values)

            defective_count = sum(1 for v in values if v == 1 or (isinstance(v, (int, float)) and v < 0.5))
            defectives.append(defective_count)
            sizes.append(n)

        p_bar = sum(defectives) / sum(sizes) if sum(sizes) > 0 else 0

        ucl_p = []
        lcl_p = []
        for n in sizes:
            if n > 0:
                sigma_p = np.sqrt(p_bar * (1 - p_bar) / n)
                ucl_p.append(p_bar + 3 * sigma_p)
                lcl_p.append(max(0, p_bar - 3 * sigma_p))
            else:
                ucl_p.append(1)
                lcl_p.append(0)

        return {
            'p_bar': p_bar,
            'ucl_p': ucl_p,
            'lcl_p': lcl_p,
            'defectives': defectives,
            'sizes': sizes,
            'proportions': [d/n if n > 0 else 0 for d, n in zip(defectives, sizes)]
        }

    @staticmethod
    def calculate_process_capability(data, usl, lsl):
        if not data:
            return None

        all_values = []
        for d in data:
            all_values.extend(d['values'])

        x_bar = np.mean(all_values)
        sigma = np.std(all_values, ddof=1)

        if sigma == 0:
            return None

        cp = (usl - lsl) / (6 * sigma)
        cpu = (usl - x_bar) / (3 * sigma)
        cpl = (x_bar - lsl) / (3 * sigma)
        cpk = min(cpu, cpl)

        return {
            'cp': cp,
            'cpk': cpk,
            'cpu': cpu,
            'cpl': cpl,
            'sigma': sigma,
            'mean': x_bar,
            'usl': usl,
            'lsl': lsl
        }


class SPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPC分析工具")
        self.root.geometry("1000x700")

        self.data_manager = SPCDataManager()
        self.analyzer = SPCAnalyzer()

        self.current_project = None
        self.setup_ui()

    def setup_ui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入CSV", command=self.import_csv)
        file_menu.add_command(label="导出数据", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        ttk.Label(left_frame, text="项目列表", font=('', 12, 'bold')).pack(pady=10)

        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.project_listbox = tk.Listbox(listbox_frame, height=15)
        self.project_listbox.pack(fill=tk.BOTH, expand=True)
        self.project_listbox.bind('<<ListboxSelect>>', self.on_project_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="新建项目", command=self.new_project).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="删除项目", command=self.delete_project).pack(fill=tk.X, pady=2)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.info_frame = ttk.LabelFrame(right_frame, text="项目信息", padding=10)
        self.info_frame.pack(fill=tk.X, pady=(0, 10))

        self.input_frame = ttk.LabelFrame(right_frame, text="数据录入", padding=10)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))

        self.chart_frame = ttk.LabelFrame(right_frame, text="控制图", padding=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = None
        self.update_project_list()

    def update_project_list(self):
        self.project_listbox.delete(0, tk.END)
        for name in self.data_manager.get_all_projects():
            self.project_listbox.insert(tk.END, name)

    def on_project_select(self, event):
        selection = self.project_listbox.curselection()
        if selection:
            self.current_project = self.project_listbox.get(selection[0])
            self.update_project_info()
            self.update_data_input()
            self.plot_control_chart()

    def update_project_info(self):
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        if not self.current_project:
            return

        project = self.data_manager.get_project(self.current_project)
        if project:
            info_text = f"类型: {project['type']}  |  数据点数: {len(project['data'])}"
            if project['usl']:
                info_text += f"  |  USL: {project['usl']}  |  LSL: {project['lsl']}"
            ttk.Label(self.info_frame, text=info_text).pack(anchor=tk.W)

            if project['data']:
                ttk.Button(self.info_frame, text="计算过程能力", command=self.calculate_capability).pack(anchor=tk.E, pady=(10, 0))

    def update_data_input(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if not self.current_project:
            return

        project = self.data_manager.get_project(self.current_project)
        if not project:
            return

        ttk.Label(self.input_frame, text="输入数据（用逗号分隔）:").pack(anchor=tk.W)
        input_frame = ttk.Frame(self.input_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.data_entry = ttk.Entry(input_frame, width=50)
        self.data_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(input_frame, text="添加", command=self.add_data).pack(side=tk.LEFT)
        ttk.Button(self.input_frame, text="导入Excel", command=self.import_excel).pack(anchor=tk.E)

    def new_project(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("新建项目")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="项目名称:").pack(pady=(20, 5))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack()

        ttk.Label(dialog, text="数据类型:").pack(pady=(10, 5))
        type_var = tk.StringVar(value="X-bar R图")
        ttk.Radiobutton(dialog, text="X-bar R图（计量型）", variable=type_var, value="X-bar R图").pack()
        ttk.Radiobutton(dialog, text="p图（计数型）", variable=type_var, value="p图").pack()

        ttk.Label(dialog, text="规格限（可选）:").pack(pady=(10, 5))
        spec_frame = ttk.Frame(dialog)
        spec_frame.pack()
        ttk.Label(spec_frame, text="USL:").pack(side=tk.LEFT)
        usl_entry = ttk.Entry(spec_frame, width=10)
        usl_entry.pack(side=tk.LEFT, padx=(5, 15))
        ttk.Label(spec_frame, text="LSL:").pack(side=tk.LEFT)
        lsl_entry = ttk.Entry(spec_frame, width=10)
        lsl_entry.pack(side=tk.LEFT, padx=5)

        def create_project():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入项目名称")
                return
            if name in self.data_manager.get_all_projects():
                messagebox.showerror("错误", "项目名称已存在")
                return

            data_type = type_var.get()
            usl = float(usl_entry.get()) if usl_entry.get() else None
            lsl = float(lsl_entry.get()) if lsl_entry.get() else None

            self.data_manager.add_project(name, data_type, usl, lsl)
            self.update_project_list()
            self.current_project = name
            self.update_project_info()
            self.update_data_input()
            self.plot_control_chart()
            dialog.destroy()

        ttk.Button(dialog, text="创建", command=create_project).pack(pady=20)

    def delete_project(self):
        if not self.current_project:
            return
        if messagebox.askyesno("确认", f"确定删除项目 '{self.current_project}' 吗？"):
            self.data_manager.delete_project(self.current_project)
            self.current_project = None
            self.update_project_list()
            for widget in self.info_frame.winfo_children():
                widget.destroy()
            for widget in self.input_frame.winfo_children():
                widget.destroy()
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.canvas = None

    def add_data(self):
        if not self.current_project:
            return

        data_str = self.data_entry.get().strip()
        if not data_str:
            messagebox.showerror("错误", "请输入数据")
            return

        try:
            values = [float(x.strip()) for x in data_str.split(',')]
            self.data_manager.add_data(self.current_project, values)
            self.data_entry.delete(0, tk.END)
            self.update_project_info()
            self.plot_control_chart()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字，用逗号分隔")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                if len(df.columns) > 0:
                    first_col = df.columns[0]
                    values = df[first_col].dropna().tolist()
                    if self.current_project:
                        for v in values:
                            self.data_manager.add_data(self.current_project, [float(v)])
                        self.update_project_info()
                        self.plot_control_chart()
                        messagebox.showinfo("成功", f"导入了 {len(values)} 条数据")
                    else:
                        messagebox.showinfo("提示", "请先创建项目")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}")

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if len(df.columns) > 0:
                    first_col = df.columns[0]
                    values = df[first_col].dropna().tolist()
                    if self.current_project:
                        for v in values:
                            self.data_manager.add_data(self.current_project, [float(v)])
                        self.update_project_info()
                        self.plot_control_chart()
                        messagebox.showinfo("成功", f"导入了 {len(values)} 条数据")
                    else:
                        messagebox.showinfo("提示", "请先创建项目")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}")

    def export_data(self):
        if not self.current_project:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            project = self.data_manager.get_project(self.current_project)
            if project and project['data']:
                df = pd.DataFrame([
                    {'subgroup': i+1, 'mean': np.mean(d['values']), 'range': max(d['values']) - min(d['values']), 'values': ','.join(map(str, d['values']))}
                    for i, d in enumerate(project['data'])
                ])
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                messagebox.showinfo("成功", "数据已导出")

    def calculate_capability(self):
        if not self.current_project:
            return

        project = self.data_manager.get_project(self.current_project)
        if not project or not project['data']:
            messagebox.showwarning("警告", "没有足够的数据")
            return

        if not project['usl'] or not project['lsl']:
            messagebox.showwarning("警告", "请先设置规格限（USL和LSL）")
            return

        result = self.analyzer.calculate_process_capability(
            project['data'],
            project['usl'],
            project['lsl']
        )

        if result:
            msg = f"Cp = {result['cp']:.3f}\n"
            msg += f"Cpk = {result['cpk']:.3f}\n"
            msg += f"CPU = {result['cpu']:.3f}\n"
            msg += f"CPL = {result['cpl']:.3f}\n"
            msg += f"σ = {result['sigma']:.3f}\n"
            msg += f"均值 = {result['mean']:.3f}"
            messagebox.showinfo("过程能力分析", msg)

    def plot_control_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not self.current_project:
            return

        project = self.data_manager.get_project(self.current_project)
        if not project or not project['data']:
            ttk.Label(self.chart_frame, text="暂无数据，请添加数据").pack()
            return

        data = project['data']
        data_type = project['type']

        if data_type == "X-bar R图":
            result = self.analyzer.calculate_xbar_r(data)
            if result:
                fig = Figure(figsize=(10, 6))
                ax1 = fig.add_subplot(211)
                ax2 = fig.add_subplot(212)

                subgroups = range(1, len(data) + 1)

                ax1.plot(subgroups, result['subgroup_means'], 'b-o', markersize=5)
                ax1.axhline(y=result['x_bar'], color='g', linestyle='-', linewidth=2, label=f'CL={result["x_bar"]:.3f}')
                ax1.axhline(y=result['ucl_x'], color='r', linestyle='--', linewidth=1.5, label=f'UCL={result["ucl_x"]:.3f}')
                ax1.axhline(y=result['lcl_x'], color='r', linestyle='--', linewidth=1.5, label=f'LCL={result["lcl_x"]:.3f}')
                ax1.set_title('X-bar 控制图')
                ax1.set_xlabel('子组')
                ax1.set_ylabel('X-bar')
                ax1.legend(loc='upper right')
                ax1.grid(True, alpha=0.3)

                for i, mean in enumerate(result['subgroup_means']):
                    if mean > result['ucl_x'] or mean < result['lcl_x']:
                        ax1.plot(i+1, mean, 'ro', markersize=10)

                ax2.plot(subgroups, result['subgroup_ranges'], 'b-o', markersize=5)
                ax2.axhline(y=result['r_bar'], color='g', linestyle='-', linewidth=2, label=f'CL={result["r_bar"]:.3f}')
                ax2.axhline(y=result['ucl_r'], color='r', linestyle='--', linewidth=1.5, label=f'UCL={result["ucl_r"]:.3f}')
                ax2.axhline(y=result['lcl_r'], color='r', linestyle='--', linewidth=1.5, label=f'LCL={result["lcl_r"]:.3f}')
                ax2.set_title('R 控制图')
                ax2.set_xlabel('子组')
                ax2.set_ylabel('Range')
                ax2.legend(loc='upper right')
                ax2.grid(True, alpha=0.3)

                fig.tight_layout()

        elif data_type == "p图":
            result = self.analyzer.calculate_p_chart(data)
            if result:
                fig = Figure(figsize=(10, 5))
                ax = fig.add_subplot(111)

                subgroups = range(1, len(data) + 1)

                ax.plot(subgroups, result['proportions'], 'b-o', markersize=5)
                ax.axhline(y=result['p_bar'], color='g', linestyle='-', linewidth=2, label=f'CL={result["p_bar"]:.4f}')
                ax.plot(subgroups, result['ucl_p'], 'r--', linewidth=1.5, label='UCL')
                ax.plot(subgroups, result['lcl_p'], 'r--', linewidth=1.5, label='LCL')
                ax.set_title('p 控制图')
                ax.set_xlabel('子组')
                ax.set_ylabel('不合格率')
                ax.legend(loc='upper right')
                ax.grid(True, alpha=0.3)

                for i, p in enumerate(result['proportions']):
                    if p > result['ucl_p'][i] or p < result['lcl_p'][i]:
                        ax.plot(i+1, p, 'ro', markersize=10)

                fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = SPCApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
