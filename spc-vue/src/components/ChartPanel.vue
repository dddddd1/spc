<template>
    <div class="card" v-if="project && project.data.length >= 2">
        <div class="card-header">
            <h2>控制图</h2>
            <button 
                class="algorithm-toggle-btn"
                @click="showAlgorithm = !showAlgorithm"
                :title="showAlgorithm ? '隐藏算法说明' : '显示算法说明'"
            >
                {{ showAlgorithm ? '📐 隐藏算法' : '📐 查看算法' }}
            </button>
        </div>
        
        <!-- 算法说明区域 -->
        <div v-show="showAlgorithm" class="algorithm-section">
            <div class="algorithm-content">
                <h4>📊 X-bar R 控制图绘制原理</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>X-bar图（均值控制图）：</strong>
                        <ul>
                            <li><strong>目的：</strong>监控过程均值的变化趋势</li>
                            <li><strong>数据点：</strong>每个子组的平均值 X̄ᵢ</li>
                            <li><strong>中心线CL：</strong>所有子组均值的总平均 X̿</li>
                            <li><strong>控制限UCL/LCL：</strong>X̿ ± A₂ × R̄（基于3σ原则）</li>
                            <li><strong>异常判断：</strong>点超出控制限或触发判异规则</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>R图（极差控制图）：</strong>
                        <ul>
                            <li><strong>目的：</strong>监控过程变异（离散程度）的稳定性</li>
                            <li><strong>数据点：</strong>每个子组的极差 Rᵢ = max - min</li>
                            <li><strong>中心线CL：</strong>平均极差 R̄</li>
                            <li><strong>控制限UCL/LCL：</strong>D₄×R̄ / D₃×R̄</li>
                            <li><strong>注意：</strong>LCL不能为负数，取max(0, D₃×R̄)</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>系数表（A₂、D₃、D₄、d₂）：</strong>
                        <p>这些系数与子组大小n相关，用于计算控制限和估计标准差。</p>
                        <ul>
                            <li>n=2: A₂=1.880, D₃=0, D₄=3.267, d₂=1.128</li>
                            <li>n=3: A₂=1.023, D₃=0, D₄=2.574, d₂=1.693</li>
                            <li>n=4: A₂=0.729, D₃=0, D₄=2.282, d₂=2.059</li>
                            <li>n=5: A₂=0.577, D₃=0, D₄=2.114, d₂=2.326</li>
                            <li>n≥6: 查表获取精确值</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">📈 p图（不合格品率控制图）</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>适用场景：</strong>样本量可变的计数型数据
                        <ul>
                            <li><strong>数据点：</strong>第i组的不合格品率 pᵢ = dᵢ/nᵢ</li>
                            <li><strong>中心线CL：</strong>平均不合格品率 p̄ = Σdᵢ/Σnᵢ</li>
                            <li><strong>控制限：</strong>p̄ ± 3√[p̄(1-p̄)/nᵢ]（随样本量变化）</li>
                            <li><strong>特点：</strong>UCL和LCL不是直线，而是曲线</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">📉 np图（不合格品数控制图）</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>适用场景：</strong>样本量固定的计数型数据
                        <ul>
                            <li><strong>数据点：</strong>第i组的不合格品数 npᵢ</li>
                            <li><strong>中心线CL：</strong>平均不合格品数 np̄ = Σnpᵢ/k</li>
                            <li><strong>控制限：</strong>np̄ ± 3√[np̄(1-p̄)]（固定值）</li>
                            <li><strong>前提条件：</strong>所有子组样本量必须相同</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">🎨 图表颜色说明</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <ul>
                            <li><span style="color: #667eea; font-weight: bold;">● 蓝色点：</span>正常数据点（在控制限内）</li>
                            <li><span style="color: #dc3545; font-weight: bold;">● 红色点：</span>异常数据点（超出控制限）</li>
                            <li><span style="color: #28a745; font-weight: bold;">━ 绿色实线：</span>中心线（CL）</li>
                            <li><span style="color: #dc3545; font-weight: bold;">- - 红色虚线：</span>上/下控制限（UCL/LCL）</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- X-bar R图 -->
        <div v-if="project.type === 'xbar-r'" style="margin-bottom:30px;">
            <div class="chart-wrapper">
                <canvas id="xbarChart"></canvas>
            </div>
            <div class="chart-wrapper" style="margin-top:20px;">
                <canvas id="rChart"></canvas>
            </div>
        </div>
        
        <!-- p图 -->
        <div v-else-if="project.type === 'p'">
            <div class="chart-wrapper">
                <canvas id="pChart"></canvas>
            </div>
        </div>
        
        <!-- np图 -->
        <div v-else-if="project.type === 'np'">
            <div class="chart-wrapper">
                <canvas id="npChart"></canvas>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { 
    calculateXbarR, 
    calculatePChart, 
    calculateNpChart 
} from '../utils/statistics';

export default {
    name: 'ChartPanel',
    props: {
        project: {
            type: Object,
            default: null
        }
    },
    setup(props) {
        const xbarChart = ref(null);
        const rChart = ref(null);
        const pChart = ref(null);
        const npChart = ref(null);
        const showAlgorithm = ref(false);

        // 销毁旧图表
        const destroyCharts = () => {
            if (xbarChart.value) {
                xbarChart.value.destroy();
                xbarChart.value = null;
            }
            if (rChart.value) {
                rChart.value.destroy();
                rChart.value = null;
            }
            if (pChart.value) {
                pChart.value.destroy();
                pChart.value = null;
            }
            if (npChart.value) {
                npChart.value.destroy();
                npChart.value = null;
            }
        };

        // 渲染X-bar R图
        const renderXbarRChart = () => {
            if (!props.project || props.project.data.length < 2) return;
            
            const result = calculateXbarR(props.project.data);
            if (!result) return;

            const labels = props.project.data.map((_, i) => `${i + 1}`);
            
            // X-bar图点颜色
            const pointColors = result.subgroupMeans.map(m =>
                m > result.uclX || m < result.lclX ? 'rgba(220, 53, 69, 1)' : 'rgba(102, 126, 234, 1)'
            );

            // X-bar图
            xbarChart.value = new Chart(document.getElementById('xbarChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'X-bar',
                            data: result.subgroupMeans,
                            borderColor: 'rgba(102, 126, 234, 1)',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 2,
                            pointBackgroundColor: pointColors,
                            pointBorderColor: pointColors,
                            pointRadius: 6,
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'UCL',
                            data: Array(result.subgroupMeans.length).fill(result.uclX),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        },
                        {
                            label: 'CL',
                            data: Array(result.subgroupMeans.length).fill(result.xBar),
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 2,
                            pointRadius: 0
                        },
                        {
                            label: 'LCL',
                            data: Array(result.subgroupMeans.length).fill(result.lclX),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: { display: true, text: 'X-bar 控制图', font: { size: 16, weight: 'bold' } },
                        legend: { position: 'top' }
                    },
                    scales: { y: { beginAtZero: false } }
                }
            });

            // R图点颜色
            const rPointColors = result.subgroupRanges.map(r =>
                r > result.uclR || r < result.lclR ? 'rgba(220, 53, 69, 1)' : 'rgba(255, 193, 7, 1)'
            );

            // R图
            rChart.value = new Chart(document.getElementById('rChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'R',
                            data: result.subgroupRanges,
                            borderColor: 'rgba(255, 193, 7, 1)',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)',
                            borderWidth: 2,
                            pointBackgroundColor: rPointColors,
                            pointBorderColor: rPointColors,
                            pointRadius: 6,
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'UCL',
                            data: Array(result.subgroupRanges.length).fill(result.uclR),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        },
                        {
                            label: 'CL',
                            data: Array(result.subgroupRanges.length).fill(result.rBar),
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 2,
                            pointRadius: 0
                        },
                        {
                            label: 'LCL',
                            data: Array(result.subgroupRanges.length).fill(result.lclR),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: { display: true, text: 'R 控制图', font: { size: 16, weight: 'bold' } },
                        legend: { position: 'top' }
                    },
                    scales: { y: { beginAtZero: true } }
                }
            });
        };

        // 渲染p图
        const renderPChart = () => {
            if (!props.project || props.project.data.length < 2) return;
            
            const result = calculatePChart(props.project.data);
            if (!result) return;

            const labels = props.project.data.map((_, i) => `${i + 1}`);
            
            // 点颜色
            const pointColors = result.proportions.map((p, i) =>
                p > result.uclP[i] || p < result.lclP[i] ? 'rgba(220, 53, 69, 1)' : 'rgba(255, 193, 7, 1)'
            );

            pChart.value = new Chart(document.getElementById('pChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'p值',
                            data: result.proportions,
                            borderColor: 'rgba(255, 193, 7, 1)',
                            backgroundColor: 'rgba(255, 193, 7, 0.1)',
                            borderWidth: 2,
                            pointBackgroundColor: pointColors,
                            pointBorderColor: pointColors,
                            pointRadius: 6,
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'UCL',
                            data: result.uclP,
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        },
                        {
                            label: 'CL',
                            data: Array(result.proportions.length).fill(result.pBar),
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 2,
                            pointRadius: 0
                        },
                        {
                            label: 'LCL',
                            data: result.lclP,
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: { display: true, text: 'p 控制图', font: { size: 16, weight: 'bold' } },
                        legend: { position: 'top' }
                    },
                    scales: { y: { beginAtZero: true } }
                }
            });
        };

        // 渲染np图
        const renderNpChart = () => {
            if (!props.project || props.project.data.length < 2) return;
            
            const n = Math.round(
                props.project.data[0].values.reduce((a, b) => a + b, 0) / 
                props.project.data[0].values.filter(v => v >= 0).length
            ) || 50;
            
            const result = calculateNpChart(props.project.data, n);
            if (!result) return;

            const labels = props.project.data.map((_, i) => `${i + 1}`);
            
            // 点颜色
            const pointColors = result.defectives.map(np =>
                np > result.uclNp || np < result.lclNp ? 'rgba(220, 53, 69, 1)' : 'rgba(108, 117, 125, 1)'
            );

            npChart.value = new Chart(document.getElementById('npChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'np值',
                            data: result.defectives,
                            borderColor: 'rgba(108, 117, 125, 1)',
                            backgroundColor: 'rgba(108, 117, 125, 0.1)',
                            borderWidth: 2,
                            pointBackgroundColor: pointColors,
                            pointBorderColor: pointColors,
                            pointRadius: 6,
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'UCL',
                            data: Array(result.defectives.length).fill(result.uclNp),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        },
                        {
                            label: 'CL',
                            data: Array(result.defectives.length).fill(result.npBar),
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 2,
                            pointRadius: 0
                        },
                        {
                            label: 'LCL',
                            data: Array(result.defectives.length).fill(result.lclNp),
                            borderColor: 'rgba(220, 53, 69, 1)',
                            borderDash: [5, 5],
                            borderWidth: 1.5,
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: { display: true, text: 'np 控制图', font: { size: 16, weight: 'bold' } },
                        legend: { position: 'top' }
                    },
                    scales: { y: { beginAtZero: true } }
                }
            });
        };

        // 更新图表
        const updateCharts = async () => {
            destroyCharts();
            await nextTick();
            
            if (!props.project || props.project.data.length < 2) return;

            if (props.project.type === 'xbar-r') {
                renderXbarRChart();
            } else if (props.project.type === 'p') {
                renderPChart();
            } else if (props.project.type === 'np') {
                renderNpChart();
            }
        };

        // 监听项目数据变化
        watch(() => props.project, () => {
            updateCharts();
        }, { deep: true });

        // 组件挂载时初始化
        onMounted(() => {
            updateCharts();
        });

        return {
            showAlgorithm
        };
    }
}
</script>
