<template>
    <div class="card">
        <div class="card-header">
            <h2>项目信息</h2>
            <button v-if="currentProject" class="btn btn-secondary btn-small" @click="toggleEdit">
                ✏️ 编辑
            </button>
        </div>
        
        <div v-if="!currentProject" class="empty-state">
            <p>请选择或创建一个项目</p>
        </div>

        <div v-else-if="!isEditing">
            <div class="form-row">
                <div class="form-group">
                    <label>项目名称</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;font-weight:600;">
                        {{ currentProject }}
                    </div>
                </div>
                <div class="form-group">
                    <label>数据类型</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;">
                        {{ getTypeName(project.type) }}
                    </div>
                </div>
                <div class="form-group">
                    <label>数据组数</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;font-weight:600;color:#667eea;">
                        {{ project.data.length }}
                    </div>
                </div>
            </div>
            
            <div v-if="project.usl && project.lsl" class="form-row">
                <div class="form-group">
                    <label>规格上限 USL</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;">{{ project.usl }}</div>
                </div>
                <div class="form-group">
                    <label>规格下限 LSL</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;">{{ project.lsl }}</div>
                </div>
                <div class="form-group">
                    <label>规格范围</label>
                    <div style="padding:10px;background:#f8f9fa;border-radius:8px;">
                        {{ (project.usl - project.lsl).toFixed(3) }}
                    </div>
                </div>
            </div>
        </div>

        <div v-else style="padding-top:15px;border-top:1px dashed #ddd;margin-top:15px;">
            <div class="form-row">
                <div class="form-group">
                    <label>规格上限 USL</label>
                    <input type="number" step="0.001" v-model.number="editForm.usl" placeholder="例如：10.5">
                </div>
                <div class="form-group">
                    <label>规格下限 LSL</label>
                    <input type="number" step="0.001" v-model.number="editForm.lsl" placeholder="例如：9.5">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>性能规格上限 USLp（用于Pp/Ppk）</label>
                    <input type="number" step="0.001" v-model.number="editForm.uslp" placeholder="用于Pp/Ppk计算">
                </div>
                <div class="form-group">
                    <label>性能规格下限 LSLp（用于Pp/Ppk）</label>
                    <input type="number" step="0.001" v-model.number="editForm.lslp" placeholder="用于Pp/Ppk计算">
                </div>
            </div>
            <div class="btn-group">
                <button class="btn btn-primary" @click="saveEdit">💾 保存修改</button>
                <button class="btn btn-secondary" @click="toggleEdit">取消</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProjectInfo',
    props: {
        currentProject: {
            type: String,
            default: null
        },
        project: {
            type: Object,
            default: null
        }
    },
    emits: ['update'],
    data() {
        return {
            isEditing: false,
            editForm: {
                usl: null,
                lsl: null,
                uslp: null,
                lslp: null
            }
        };
    },
    methods: {
        getTypeName(type) {
            const typeMap = {
                'xbar-r': 'X-bar R图（计量型）',
                'p': 'p图（计数型）',
                'np': 'np图（计数型）'
            };
            return typeMap[type] || type;
        },
        toggleEdit() {
            if (!this.isEditing && this.project) {
                this.editForm = {
                    usl: this.project.usl || null,
                    lsl: this.project.lsl || null,
                    uslp: this.project.uslp || null,
                    lslp: this.project.lslp || null
                };
            }
            this.isEditing = !this.isEditing;
        },
        saveEdit() {
            this.$emit('update', { ...this.editForm });
            this.isEditing = false;
        }
    }
}
</script>
