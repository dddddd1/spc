# SPC Vue 项目

这是一个基于 Vue 3 的统计过程控制（SPC）分析工具，已从原始的单文件HTML重构为模块化Vue组件架构。

## 📁 项目结构

```
spc-vue/
├── src/
│   ├── components/          # Vue组件
│   │   ├── ProjectSidebar.vue    # 项目侧边栏
│   │   ├── ProjectInfo.vue       # 项目信息卡片
│   │   ├── DataInput.vue         # 数据录入组件
│   │   ├── AlarmPanel.vue        # 报警面板（待创建）
│   │   ├── StatsPanel.vue        # 统计分析面板（待创建）
│   │   ├── ChartPanel.vue        # 控制图面板（待创建）
│   │   └── HistoryPanel.vue      # 历史数据面板（待创建）
│   ├── utils/               # 工具函数
│   │   ├── constants.js          # 常量定义
│   │   └── statistics.js         # 统计计算函数
│   ├── styles/              # 样式文件
│   │   └── spc.css               # 全局样式
│   └── App.vue              # 主应用组件
├── package.json
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd spc-vue
npm install
```

### 2. 需要安装的额外依赖

```bash
npm install chart.js xlsx
```

### 3. 运行开发服务器

```bash
npm run dev
```

## 📦 核心功能模块

### 1. 项目管理
- 创建、删除SPC项目
- 支持三种图表类型：X-bar R图、p图、np图
- 项目参数配置（USL/LSL规格限）

### 2. 数据导入
- 支持CSV文件导入
- 支持Excel文件导入（.xlsx, .xls）
- 批量数据录入

### 3. 统计分析
- **过程能力分析**：Cp, Cpk, CPU, CPL
- **过程性能分析**：Pp, Ppk, PPU, PPL
- **不合格统计**：超规格数、不合格率

### 4. 控制图
- X-bar R控制图（计量型数据）
- p控制图（计数型数据）
- np控制图（计数型数据）
- 自动标注控制限（UCL/LCL/CL）

### 5. 异常报警
- Western Electric 8条判异规则
- 连续趋势检测
- 实时报警提示

### 6. 历史数据
- 数据历史记录
- 状态标记（正常/警告/危险）
- 数据导出为Excel

## 🔧 技术栈

- **Vue 3**: 渐进式JavaScript框架
- **Chart.js**: 图表库
- **SheetJS (xlsx)**: Excel文件处理
- **原生CSS**: 样式管理

## 📝 组件说明

### ProjectSidebar.vue
项目列表侧边栏，负责显示和管理所有SPC项目。

**Props:**
- `projects`: 项目对象集合
- `currentProject`: 当前选中的项目名称

**Events:**
- `select`: 选择项目
- `new`: 新建项目
- `delete`: 删除项目

### ProjectInfo.vue
显示和编辑项目信息，包括规格限设置。

**Props:**
- `currentProject`: 当前项目名称
- `project`: 项目详细信息对象

**Events:**
- `update`: 更新项目参数

### DataInput.vue
数据导入和录入组件，支持CSV和Excel格式。

**Props:**
- `currentProject`: 当前项目名称

**Events:**
- `import`: 导入数据
- `analysis`: 执行统计分析
- `charts`: 生成控制图
- `clear`: 清空数据

### AlarmPanel.vue (待创建)
显示异常报警信息，基于Western Electric规则。

### StatsPanel.vue (待创建)
展示统计分析结果，包括过程能力、性能和不合格统计。

### ChartPanel.vue (待创建)
渲染控制图，使用Chart.js绘制。

### HistoryPanel.vue (待创建)
显示历史数据表格，支持导出功能。

## 🎯 使用示例

### 创建新项目

```javascript
// 在App.vue中
const createProject = (name, type, specs) => {
    projects.value[name] = {
        type: type,
        usl: specs.usl || null,
        lsl: specs.lsl || null,
        uslp: specs.uslp || null,
        lslp: specs.lslp || null,
        data: [],
        created: new Date().toISOString()
    };
    saveProjects();
};
```

### 导入数据

```javascript
// 在DataInput.vue中
const handleImport = (data) => {
    projects[currentProject].data.push(...data);
    saveProjects();
    updateProjectInfo();
};
```

### 执行统计分析

```javascript
import { calculateXbarR, calculateProcessCapability } from '@/utils/statistics';

const result = calculateXbarR(project.data);
const cpResult = calculateProcessCapability(project.data, project.usl, project.lsl);
```

## 📊 统计方法

### X-bar R控制图
适用于子组大小2-10的计量型数据，监控过程均值和变异。

### p控制图
用于监控不合格品率，适用于可变样本大小的计数型数据。

### np控制图
用于监控不合格品数，适用于固定样本大小的计数型数据。

### 过程能力指数
- **Cp**: 过程潜力指数
- **Cpk**: 过程能力指数（考虑偏移）
- **Pp/Ppk**: 过程性能指数

## 🔄 从HTML迁移

原单文件HTML (`spc_web.html`) 已拆分为：
1. **样式** → `src/styles/spc.css`
2. **常量** → `src/utils/constants.js`
3. **统计函数** → `src/utils/statistics.js`
4. **UI组件** → `src/components/*.vue`
5. **主应用** → `src/App.vue`

## 📌 注意事项

1. 数据存储使用浏览器localStorage
2. 需要现代浏览器支持ES6+特性
3. Chart.js和xlsx需要通过npm安装
4. 建议Node.js版本 >= 16

## 🛠️ 后续优化建议

1. 添加TypeScript支持
2. 使用Pinia进行状态管理
3. 添加单元测试
4. 实现数据持久化到后端
5. 添加用户认证系统
6. 支持更多控制图类型（I-MR, c图等）

## 📄 许可证

MIT License
