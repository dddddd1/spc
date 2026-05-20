<template>
    <div class="sidebar">
        <h3>项目列表</h3>
        <div class="project-list">
            <div 
                v-for="(project, name) in projects" 
                :key="name"
                class="project-item"
                :class="{ active: currentProject === name }"
                @click="$emit('select', name)"
            >
                <div class="project-name">{{ name }}</div>
                <div class="project-info">
                    {{ getTypeName(project.type) }} | {{ project.data.length }}组
                </div>
            </div>
            <div v-if="Object.keys(projects).length === 0" style="padding:20px;color:#999;text-align:center;">
                暂无项目
            </div>
        </div>
        <div class="btn-group">
            <button class="btn btn-primary" @click="$emit('new')">新建项目</button>
            <button class="btn btn-danger" @click="$emit('delete')" :disabled="!currentProject">删除</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProjectSidebar',
    props: {
        projects: {
            type: Object,
            required: true
        },
        currentProject: {
            type: String,
            default: null
        }
    },
    emits: ['select', 'new', 'delete'],
    methods: {
        getTypeName(type) {
            const typeMap = {
                'xbar-r': 'X-bar R',
                'p': 'p图',
                'np': 'np图'
            };
            return typeMap[type] || type;
        }
    }
}
</script>
