<template>
    <div class="card" v-if="project && project.data.length > 0">
        <div class="card-header">
            <h2>历史数据</h2>
            <button @click="exportToExcel" class="btn btn-export">📥 导出Excel</button>
        </div>
        
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>子组序号</th>
                        <th v-for="(value, idx) in maxColumns" :key="idx">X{{ idx + 1 }}</th>
                        <th>平均值</th>
                        <th>极差/不合格数</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(group, index) in displayData" :key="index">
                        <td>{{ group.index }}</td>
                        <td v-for="(value, idx) in maxColumns" :key="idx">
                            {{ group.values[idx] !== undefined ? group.values[idx].toFixed(3) : '-' }}
                        </td>
                        <td>{{ group.statistic.toFixed(3) }}</td>
                        <td>{{ group.range.toFixed(3) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue';
import * as XLSX from 'xlsx';
import { calculateXbarR } from '../utils/statistics';

export default {
    name: 'HistoryPanel',
    props: {
        project: {
            type: Object,
            default: null
        }
    },
    setup(props) {
        // 计算最大列数
        const maxColumns = computed(() => {
            if (!props.project || props.project.data.length === 0) return [];
            
            let maxLen = 0;
            props.project.data.forEach(group => {
                if (group.values.length > maxLen) {
                    maxLen = group.values.length;
                }
            });
            
            return Array(maxLen).fill(0);
        });

        // 准备显示数据
        const displayData = computed(() => {
            if (!props.project || props.project.data.length === 0) return [];

            const result = props.project.type === 'xbar-r' 
                ? calculateXbarR(props.project.data) 
                : null;

            return props.project.data.map((group, index) => {
                let statistic, range;
                
                if (props.project.type === 'xbar-r') {
                    statistic = result.subgroupMeans[index];
                    range = result.subgroupRanges[index];
                } else {
                    // p图或np图：统计不合格数
                    const defectives = group.values.filter(v => v === 1 || (typeof v === 'number' && v < 0.5)).length;
                    statistic = group.values.reduce((sum, v) => sum + v, 0) / group.values.length;
                    range = defectives;
                }

                return {
                    index: index + 1,
                    values: group.values,
                    statistic: statistic,
                    range: range
                };
            });
        });

        // 导出到Excel
        const exportToExcel = () => {
            if (!props.project || props.project.data.length === 0) {
                alert('没有数据可导出');
                return;
            }

            try {
                // 创建工作簿
                const wb = XLSX.utils.book_new();
                
                // 准备数据
                const data = [];
                
                // 添加标题行
                const headers = ['子组序号'];
                for (let i = 1; i <= maxColumns.value.length; i++) {
                    headers.push(`X${i}`);
                }
                headers.push('平均值');
                headers.push('极差/不合格数');
                data.push(headers);

                // 添加数据行
                displayData.value.forEach(row => {
                    const rowData = [row.index];
                    row.values.forEach(val => {
                        rowData.push(val);
                    });
                    // 填充空值
                    while (rowData.length - 1 < maxColumns.value.length) {
                        rowData.push(null);
                    }
                    rowData.push(row.statistic);
                    rowData.push(row.range);
                    data.push(rowData);
                });

                // 创建工作表
                const ws = XLSX.utils.aoa_to_sheet(data);
                
                // 设置列宽
                const colWidths = [{ wch: 12 }];
                for (let i = 0; i < maxColumns.value.length; i++) {
                    colWidths.push({ wch: 10 });
                }
                colWidths.push({ wch: 12 }, { wch: 15 });
                ws['!cols'] = colWidths;

                // 添加工作表到工作簿
                XLSX.utils.book_append_sheet(wb, ws, `${props.project.name}_SPC数据`);

                // 生成文件名
                const fileName = `${props.project.name}_${new Date().toISOString().slice(0, 10)}.xlsx`;
                
                // 下载文件
                XLSX.writeFile(wb, fileName);
                
                console.log('Excel导出成功:', fileName);
            } catch (error) {
                console.error('Excel导出失败:', error);
                alert('导出失败，请重试');
            }
        };

        return {
            maxColumns,
            displayData,
            exportToExcel
        };
    }
}
</script>

<style scoped>
.btn-export {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.btn-export:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.table-container {
    overflow-x: auto;
    margin-top: 15px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.data-table thead {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.data-table th {
    padding: 12px 8px;
    text-align: center;
    font-weight: 600;
    color: #495057;
    border-bottom: 2px solid #dee2e6;
}

.data-table td {
    padding: 10px 8px;
    text-align: center;
    border-bottom: 1px solid #e9ecef;
}

.data-table tbody tr:hover {
    background-color: #f8f9fa;
}

.data-table tbody tr:nth-child(even) {
    background-color: #fafbfc;
}
</style>
