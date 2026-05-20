<template>
    <div class="container">
        <header>
            <h1>SPC统计分析工具</h1>
            <p>统计过程控制 - 控制图分析 - 过程能力分析 - 异常报警</p>
        </header>

        <div class="main-content">
            <!-- 项目侧边栏 -->
            <ProjectSidebar 
                :projects="projects"
                :current-project="currentProject"
                @select="selectProject"
                @new="showNewProjectModal = true"
                @delete="deleteCurrentProject"
            />

            <!-- 工作区 -->
            <div class="workspace">
                <!-- 项目信息 -->
                <ProjectInfo 
                    :current-project="currentProject"
                    :project="currentProjectData"
                    @update="handleProjectUpdate"
                />

                <!-- 数据录入 -->
                <DataInput 
                    v-if="currentProject"
                    :current-project="currentProject"
                    @import="handleDataImport"
                    @analysis="runAnalysis"
                    @charts="runCharts"
                    @clear="clearAllData"
                />

                <!-- 异常报警 -->
                <AlarmPanel 
                    v-if="currentProject && currentProjectData?.data.length >= 2"
                    :project="currentProjectData"
                />

                <!-- 统计分析 -->
                <StatsPanel 
                    v-if="currentProject && currentProjectData?.data.length >= 2"
                    :project="currentProjectData"
                />

                <!-- 控制图 -->
                <ChartPanel 
                    v-if="currentProject && currentProjectData?.data.length >= 2"
                    :project="currentProjectData"
                />

                <!-- 历史数据 -->
                <HistoryPanel 
                    v-if="currentProject"
                    :project="currentProjectData"
                />
            </div>
        </div>

        <!-- 新建项目模态框 -->
        <div class="modal" :class="{ active: showNewProjectModal }">
            <div class="modal-content">
                <h2>新建SPC项目</h2>
                <div class="form-group">
                    <label>项目名称</label>
                    <input type="text" v-model="newProject.name" placeholder="例如：产品A尺寸监控">
                </div>
                <div class="form-group">
                    <label>数据类型</label>
                    <select v-model="newProject.type">
                        <option value="xbar-r">X-bar R图（计量型数据）</option>
                        <option value="p">p图（计数型数据）</option>
                        <option value="np">np图（计数型数据）</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>规格上限 USL（可选）</label>
                    <input type="number" step="0.001" v-model.number="newProject.usl" placeholder="例如：10.5">
                </div>
                <div class="form-group">
                    <label>规格下限 LSL（可选）</label>
                    <input type="number" step="0.001" v-model.number="newProject.lsl" placeholder="例如：9.5">
                </div>
                <div class="form-group">
                    <label>性能规格上限 USLp（可选）</label>
                    <input type="number" step="0.001" v-model.number="newProject.uslp" placeholder="用于Pp/Ppk计算">
                </div>
                <div class="form-group">
                    <label>性能规格下限 LSLp（可选）</label>
                    <input type="number" step="0.001" v-model.number="newProject.lslp" placeholder="用于Pp/Ppk计算">
                </div>
                <div class="btn-group">
                    <button class="btn btn-primary" @click="createProject">创建</button>
                    <button class="btn btn-secondary" @click="showNewProjectModal = false">取消</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import ProjectSidebar from './components/ProjectSidebar.vue';
import ProjectInfo from './components/ProjectInfo.vue';
import DataInput from './components/DataInput.vue';
import AlarmPanel from './components/AlarmPanel.vue';
import StatsPanel from './components/StatsPanel.vue';
import ChartPanel from './components/ChartPanel.vue';
import HistoryPanel from './components/HistoryPanel.vue';

export default {
    name: 'App',
    components: {
        ProjectSidebar,
        ProjectInfo,
        DataInput,
        AlarmPanel,
        StatsPanel,
        ChartPanel,
        HistoryPanel
    },
    setup() {
        const projects = ref({});
        const currentProject = ref(null);
        const showNewProjectModal = ref(false);
        const newProject = ref({
            name: '',
            type: 'xbar-r',
            usl: null,
            lsl: null,
            uslp: null,
            lslp: null
        });

        // 从localStorage加载项目
        const loadProjects = () => {
            const saved = localStorage.getItem('spc_projects');
            if (saved) {
                projects.value = JSON.parse(saved);
            }
        };

        // 保存项目到localStorage
        const saveProjects = () => {
            localStorage.setItem('spc_projects', JSON.stringify(projects.value));
        };

        // 当前项目数据
        const currentProjectData = computed(() => {
            return currentProject.value ? projects.value[currentProject.value] : null;
        });

        // 选择项目
        const selectProject = (name) => {
            currentProject.value = name;
        };

        // 创建项目
        const createProject = () => {
            if (!newProject.value.name.trim()) {
                alert('请输入项目名称');
                return;
            }
            if (projects.value[newProject.value.name]) {
                alert('项目名称已存在');
                return;
            }

            projects.value[newProject.value.name] = {
                type: newProject.value.type,
                usl: newProject.value.usl || null,
                lsl: newProject.value.lsl || null,
                uslp: newProject.value.uslp || null,
                lslp: newProject.value.lslp || null,
                data: [],
                created: new Date().toISOString()
            };

            saveProjects();
            currentProject.value = newProject.value.name;
            showNewProjectModal.value = false;
            
            // 重置表单
            newProject.value = {
                name: '',
                type: 'xbar-r',
                usl: null,
                lsl: null,
                uslp: null,
                lslp: null
            };
        };

        // 删除项目
        const deleteCurrentProject = () => {
            if (!currentProject.value) return;
            if (confirm(`确定删除项目 "${currentProject.value}" 吗？`)) {
                delete projects.value[currentProject.value];
                currentProject.value = null;
                saveProjects();
            }
        };

        // 更新项目参数
        const handleProjectUpdate = (specs) => {
            if (currentProject.value) {
                projects.value[currentProject.value] = {
                    ...projects.value[currentProject.value],
                    ...specs
                };
                saveProjects();
            }
        };

        // 导入数据
        const handleDataImport = (data) => {
            if (currentProject.value) {
                projects.value[currentProject.value].data.push(...data);
                saveProjects();
            }
        };

        // 清空数据
        const clearAllData = () => {
            if (!currentProject.value) return;
            if (confirm('确定要清空所有数据吗?此操作不可恢复!')) {
                projects.value[currentProject.value].data = [];
                saveProjects();
            }
        };

        // 执行分析
        const runAnalysis = () => {
            if (!currentProject.value) {
                alert('请先选择项目');
                return;
            }
            const project = projects.value[currentProject.value];
            if (project.data.length < 2) {
                alert(`数据不足，当前只有 ${project.data.length} 组，请至少添加2组数据`);
                return;
            }
            // 触发子组件更新
        };

        // 生成图表
        const runCharts = () => {
            if (!currentProject.value) {
                alert('请先选择项目');
                return;
            }
            const project = projects.value[currentProject.value];
            if (project.data.length < 2) {
                alert(`数据不足，当前只有 ${project.data.length} 组，请至少添加2组数据`);
                return;
            }
            // 触发子组件更新
        };

        // 初始化
        onMounted(() => {
            loadProjects();
        });

        return {
            projects,
            currentProject,
            currentProjectData,
            showNewProjectModal,
            newProject,
            selectProject,
            createProject,
            deleteCurrentProject,
            handleProjectUpdate,
            handleDataImport,
            clearAllData,
            runAnalysis,
            runCharts
        };
    }
}
</script>

<style src="./styles/spc.css"></style>
