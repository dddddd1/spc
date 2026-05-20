# SPC项目重构指南

## 📋 概述

本文档说明了如何将原始的2151行单文件HTML (`spc_web.html`) 重构为模块化Vue 3项目。

## 🎯 重构目标

1. **代码分离**: 将HTML、CSS、JavaScript分离到独立文件
2. **组件化**: 使用Vue组件封装UI模块
3. **可维护性**: 提高代码可读性和可维护性
4. **可扩展性**: 便于后续功能扩展

## 📂 文件映射关系

### 原始文件结构
```
spc_web.html (2151行)
├── <style> (约400行CSS)
├── <body> HTML结构 (约300行)
└── <script> JavaScript逻辑 (约1450行)
```

### 新文件结构
```
spc-vue/
├── src/
│   ├── styles/spc.css              ← 原<style>部分
│   ├── utils/constants.js          ← 常量定义 (XBAR_R_CONSTANTS, WE_RULES)
│   ├── utils/statistics.js         ← 统计计算函数
│   ├── components/
│   │   ├── ProjectSidebar.vue     ← 项目列表侧边栏
│   │   ├── ProjectInfo.vue        ← 项目信息卡片
│   │   ├── DataInput.vue          ← 数据录入区域
│   │   ├── AlarmPanel.vue         ← 异常报警面板
│   │   ├── StatsPanel.vue         ← 统计分析面板
│   │   ├── ChartPanel.vue         ← 控制图面板
│   │   └── HistoryPanel.vue       ← 历史数据面板
│   ├── App.vue                     ← 主应用框架 + 模态框
│   └── main.js                     ← Vue应用入口
├── index.html                      ← HTML骨架
├── vite.config.js                  ← Vite配置
└── package.json                    ← 依赖配置
```

## 🔧 核心代码迁移

### 1. CSS样式迁移

**原始位置**: `spc_web.html` 第8-397行

**新位置**: `src/styles/spc.css`

**改动**: 
- 保持不变，仅提取到独立文件
- 通过 `<style src="./styles/spc.css">` 引入

### 2. 常量定义迁移

**原始位置**: `spc_web.html` 第617-637行

```javascript
// 原始代码
const XBAR_R_CONSTANTS = { ... };
const WE_RULES = [ ... ];
```

**新位置**: `src/utils/constants.js`

```javascript
// 导出为模块
export const XBAR_R_CONSTANTS = { ... };
export const WE_RULES = [ ... ];
```

### 3. 统计函数迁移

**原始位置**: `spc_web.html` 中的以下函数:
- `calculateXbarR` (约1450行)
- `calculatePChart`
- `calculateNpChart`
- `calculateProcessCapability`
- `calculateProcessPerformance`
- 所有判异规则检查函数

**新位置**: `src/utils/statistics.js`

**改动**:
- 将所有统计函数提取为独立模块
- 使用 `export` 导出供组件调用
- 保持函数逻辑不变

### 4. 组件拆分

#### ProjectSidebar.vue
**对应原始HTML**: 第419-428行（项目列表侧边栏）

**原始JS函数**:
- `renderProjectList()`
- `selectProject()`
- `deleteCurrentProject()`

**Vue实现**:
```vue
<template>
    <div class="sidebar">
        <div v-for="(project, name) in projects" ...>
            <!-- 项目列表渲染 -->
        </div>
    </div>
</template>
```

#### ProjectInfo.vue
**对应原始HTML**: 第433-480行（项目信息卡片）

**原始JS函数**:
- `updateWorkspace()` 中的项目信息显示部分
- `toggleEditProject()`
- `saveProjectEdit()`

#### DataInput.vue
**对应原始HTML**: 第482-502行（数据录入区域）

**原始JS函数**:
- `importCSV()`
- `importExcel()`
- `runAnalysis()`
- `runCharts()`
- `clearAllData()`

#### AlarmPanel.vue
**对应原始HTML**: 第504-511行（异常报警）

**原始JS函数**:
- `updateAlarm()`
- Western Electric规则检查逻辑

#### StatsPanel.vue
**对应原始HTML**: 第513-543行（统计分析结果）

**原始JS函数**:
- `updateStats()`
- `switchTab()`
- 过程能力/性能计算显示

#### ChartPanel.vue
**对应原始HTML**: 第545-563行（控制图）

**原始JS函数**:
- `updateCharts()`
- Chart.js图表创建逻辑

#### HistoryPanel.vue
**对应原始HTML**: 第565-574行（历史数据）

**原始JS函数**:
- `updateHistory()`
- `exportHistory()`

### 5. 状态管理迁移

**原始方式**: 全局变量
```javascript
let projects = {};
let currentProject = null;
let xbarChart = null;
```

**Vue方式**: Composition API
```javascript
import { ref, computed } from 'vue';

const projects = ref({});
const currentProject = ref(null);
const currentProjectData = computed(() => {
    return currentProject.value ? projects.value[currentProject.value] : null;
});
```

### 6. localStorage操作迁移

**原始代码**:
```javascript
function loadProjects() {
    const saved = localStorage.getItem('spc_projects');
    if (saved) {
        projects = JSON.parse(saved);
    }
}

function saveProjects() {
    localStorage.setItem('spc_projects', JSON.stringify(projects));
}
```

**Vue实现** (在App.vue的setup中):
```javascript
const loadProjects = () => {
    const saved = localStorage.getItem('spc_projects');
    if (saved) {
        projects.value = JSON.parse(saved);
    }
};

const saveProjects = () => {
    localStorage.setItem('spc_projects', JSON.stringify(projects.value));
};
```

## 🚀 运行新项目

### 1. 安装依赖
```bash
cd spc-vue
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

### 3. 访问应用
浏览器自动打开 http://localhost:3000

## 📝 待完成工作

以下组件目前为占位符，需要补充完整逻辑：

1. **AlarmPanel.vue**: 
   - 实现Western Electric规则检查
   - 报警信息显示

2. **StatsPanel.vue**:
   - 过程能力指标计算和显示
   - Tab切换逻辑
   - 分析结论生成

3. **ChartPanel.vue**:
   - 集成Chart.js
   - 三种控制图渲染
   - 控制限标注

4. **HistoryPanel.vue**:
   - 历史数据表格渲染
   - Excel导出功能

## 💡 优化建议

### 已完成
✅ CSS样式分离  
✅ 常量模块化  
✅ 统计函数模块化  
✅ 基础组件结构  
✅ 项目管理功能  
✅ 数据导入功能  

### 待优化
⏳ 完整实现所有组件逻辑  
⏳ 添加TypeScript支持  
⏳ 使用Pinia进行状态管理  
⏳ 添加单元测试  
⏳ 错误处理优化  
⏳ 性能优化（虚拟滚动等）  

## 🔄 对比优势

| 特性 | 原始HTML | Vue重构后 |
|------|---------|----------|
| 文件大小 | 2151行单文件 | 模块化多文件 |
| 可维护性 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 可复用性 | ⭐ | ⭐⭐⭐⭐ |
| 可扩展性 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 团队协作 | 困难 | 容易 |
| 调试难度 | 高 | 低 |
| 学习曲线 | 低 | 中等 |

## 📚 参考资料

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Vite 官方文档](https://cn.vitejs.dev/)
- [Chart.js 文档](https://www.chartjs.org/)
- [SheetJS 文档](https://sheetjs.com/)

---

**迁移完成时间**: 2026-05-20  
**重构版本**: v1.0.0
