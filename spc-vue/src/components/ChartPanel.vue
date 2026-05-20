<template>
    <div class="card" v-if="project && project.data.length >= 2">
        <div class="card-header">
            <h2>控制图</h2>
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

        return {};
    }
}
</script>
