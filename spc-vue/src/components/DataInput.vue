<template>
    <div class="card" v-if="currentProject">
        <div class="card-header">
            <h2>数据录入</h2>
        </div>
        
        <div class="alert-box" :class="alertType" v-if="alertMessage" style="display: block;">
            {{ alertMessage }}
        </div>

        <div class="import-section">
            <button class="btn btn-secondary btn-small" @click="$refs.csvInput.click()">导入CSV</button>
            <button class="btn btn-secondary btn-small" @click="$refs.excelInput.click()">导入Excel</button>
            <input ref="csvInput" type="file" class="file-input" accept=".csv" @change="importCSV">
            <input ref="excelInput" type="file" class="file-input" accept=".xlsx,.xls" @change="importExcel">
        </div>

        <div class="analysis-section" style="margin-top:15px;padding-top:15px;border-top:1px dashed #ddd;">
            <div class="btn-group">
                <button class="btn btn-primary" @click="$emit('analysis')" style="flex:1;">📊 生成统计分析</button>
                <button class="btn btn-secondary" @click="$emit('charts')" style="flex:1;">📈 生成控制图</button>
                <button class="btn btn-danger" @click="$emit('clear')" style="flex:1;">🗑️ 清空数据</button>
            </div>
        </div>
    </div>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
    name: 'DataInput',
    props: {
        currentProject: {
            type: String,
            default: null
        }
    },
    emits: ['import', 'analysis', 'charts', 'clear'],
    data() {
        return {
            alertMessage: '',
            alertType: ''
        };
    },
    methods: {
        showAlert(message, type) {
            this.alertMessage = message;
            this.alertType = type;
            setTimeout(() => {
                this.alertMessage = '';
            }, 3000);
        },
        importCSV(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const text = e.target.result;
                    const lines = text.split('\n').filter(l => l.trim());
                    if (lines.length === 0) {
                        this.showAlert('CSV文件为空', 'error');
                        return;
                    }
                    
                    const data = [];
                    lines.forEach(line => {
                        const values = line.split(',').map(v => parseFloat(v.trim()));
                        if (!values.some(isNaN) && values.length > 0) {
                            data.push({
                                values: values,
                                timestamp: new Date().toISOString()
                            });
                        }
                    });
                    
                    this.$emit('import', data);
                    this.showAlert(`成功导入 ${data.length} 组数据`, 'success');
                } catch (e) {
                    this.showAlert('CSV解析错误', 'error');
                }
            };
            reader.readAsText(file);
            event.target.value = '';
        },
        importExcel(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });

                    const importedData = [];
                    jsonData.forEach(row => {
                        if (row.length > 0) {
                            const values = row.map(v => parseFloat(v)).filter(v => !isNaN(v));
                            if (values.length > 0) {
                                importedData.push({
                                    values: values,
                                    timestamp: new Date().toISOString()
                                });
                            }
                        }
                    });

                    if (importedData.length === 0) {
                        this.showAlert('没有有效的数据', 'error');
                        return;
                    }

                    this.$emit('import', importedData);
                    this.showAlert(`成功导入 ${importedData.length} 组数据`, 'success');
                } catch (e) {
                    this.showAlert('Excel解析错误: ' + e.message, 'error');
                }
            };
            reader.readAsArrayBuffer(file);
            event.target.value = '';
        }
    }
}
</script>
