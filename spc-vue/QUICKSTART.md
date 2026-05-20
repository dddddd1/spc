# SPC Vue项目 - 快速开始

## 🎉 项目已完成重构！

原始的2151行单文件HTML已成功重构为模块化Vue 3项目。

## ⚡ 三步启动

### 1️⃣ 进入项目目录
```bash
cd spc-vue
```

### 2️⃣ 安装依赖
```bash
npm install
```

### 3️⃣ 启动开发服务器
```bash
npm run dev
```

浏览器将自动打开 http://localhost:3000

## 📦 已完成的模块

✅ **核心架构**
- Vue 3 Composition API
- Vite构建工具
- 模块化项目结构

✅ **样式系统**
- CSS独立文件 (`src/styles/spc.css`)
- 响应式设计
- 现代化UI

✅ **工具函数**
- 统计计算函数 (`src/utils/statistics.js`)
- 常量定义 (`src/utils/constants.js`)
- Western Electric判异规则

✅ **UI组件**
- ProjectSidebar.vue - 项目管理侧边栏
- ProjectInfo.vue - 项目信息卡片
- DataInput.vue - 数据导入(CSV/Excel)
- AlarmPanel.vue - 报警面板（框架）
- StatsPanel.vue - 统计分析（框架）
- ChartPanel.vue - 控制图（框架）
- HistoryPanel.vue - 历史数据（框架）

✅ **核心功能**
- 项目创建/删除
- 项目参数配置(USL/LSL)
- CSV/Excel数据导入
- localStorage数据持久化

## 🔨 待完善功能

以下组件需要补充完整业务逻辑：

1. **AlarmPanel.vue** - 异常报警逻辑
2. **StatsPanel.vue** - 统计分析显示
3. **ChartPanel.vue** - Chart.js图表集成
4. **HistoryPanel.vue** - 历史数据表格和导出

参考原始文件 `spc_web.html` 中的对应函数实现。

## 📁 项目结构

```
spc-vue/
├── src/
│   ├── components/        # Vue组件
│   ├── utils/            # 工具函数
│   ├── styles/           # 样式文件
│   ├── App.vue           # 主应用
│   └── main.js           # 入口文件
├── index.html            # HTML模板
├── vite.config.js        # Vite配置
├── package.json          # 依赖配置
└── README.md            # 详细文档
```

## 📖 相关文档

- [README.md](./README.md) - 完整项目文档
- [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) - 迁移指南

## 💡 下一步建议

1. **完善组件逻辑**: 参考原始HTML实现剩余组件
2. **添加TypeScript**: 提升类型安全
3. **状态管理**: 引入Pinia管理复杂状态
4. **单元测试**: 使用Vitest编写测试
5. **部署上线**: 使用 `npm run build` 构建生产版本

## 🆘 遇到问题？

检查以下常见问题：

**Q: npm install失败？**  
A: 确保Node.js版本 >= 16，尝试清除缓存：`npm cache clean --force`

**Q: 端口3000被占用？**  
A: 修改 `vite.config.js` 中的port配置

**Q: 如何查看原始HTML版本？**  
A: 直接打开项目根目录的 `spc_web.html` 文件

---

**祝开发愉快！** 🚀
