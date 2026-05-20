<template>
    <div class="card" v-if="project && project.data.length >= 2">
        <div class="card-header">
            <h2>统计分析结果</h2>
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
                <h4>📊 X-bar R 控制图算法</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>1. 计算子组统计量：</strong>
                        <ul>
                            <li><code>X̄ᵢ = Σxᵢⱼ / n</code> - 第i个子组的均值</li>
                            <li><code>Rᵢ = max(xᵢ) - min(xᵢ)</code> - 第i个子组的极差</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>2. 计算总体统计量：</strong>
                        <ul>
                            <li><code>X̿ = ΣX̄ᵢ / k</code> - 总均值（k为子组数）</li>
                            <li><code>R̄ = ΣRᵢ / k</code> - 平均极差</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>3. 计算控制限（使用系数A₂、D₃、D₄）：</strong>
                        <ul>
                            <li><code>UCL(X) = X̿ + A₂ × R̄</code> - X图上控制限</li>
                            <li><code>CL(X) = X̿</code> - X图中心线</li>
                            <li><code>LCL(X) = X̿ - A₂ × R̄</code> - X图下控制限</li>
                            <li><code>UCL(R) = D₄ × R̄</code> - R图上控制限</li>
                            <li><code>CL(R) = R̄</code> - R图中心线</li>
                            <li><code>LCL(R) = D₃ × R̄</code> - R图下控制限</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>4. 估计过程标准差：</strong>
                        <ul>
                            <li><code>σ = R̄ / d₂</code> - 使用R-bar/d₂方法（组内变异）</li>
                            <li>d₂为与子组大小n相关的常数</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">📈 过程能力指数（Cp/Cpk）</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>使用规格限（USL/LSL）和组内变异σ计算：</strong>
                        <ul>
                            <li><code>Cp = (USL - LSL) / (6σ)</code> - 过程能力指数</li>
                            <li><code>CPU = (USL - μ) / (3σ)</code> - 上侧能力指数</li>
                            <li><code>CPL = (μ - LSL) / (3σ)</code> - 下侧能力指数</li>
                            <li><code>Cpk = min(CPU, CPL)</code> - 过程能力指数（考虑偏移）</li>
                        </ul>
                        <p class="note">💡 Cp反映潜在能力，Cpk反映实际能力（考虑均值偏移）</p>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">🎯 过程性能指数（Pp/Ppk）</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>使用规格限（USLp/LSLp）和整体标准差σ计算：</strong>
                        <ul>
                            <li><code>σ = √[Σ(xᵢ - μ)² / N]</code> - 整体标准差（所有数据）</li>
                            <li><code>Pp = (USL - LSL) / (6σ)</code> - 过程性能指数</li>
                            <li><code>PPU = (USL - μ) / (3σ)</code> - 上侧性能指数</li>
                            <li><code>PPL = (μ - LSL) / (3σ)</code> - 下侧性能指数</li>
                            <li><code>Ppk = min(PPU, PPL)</code> - 过程性能指数（考虑偏移）</li>
                        </ul>
                        <p class="note">💡 Pp/Ppk反映长期实际性能，通常 Cpk ≥ Ppk</p>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">⚠️ Western Electric 判异规则</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>8条判异规则（基于3σ分区）：</strong>
                        <ol>
                            <li><strong>规则1：</strong>1点落在A区之外（超出±3σ控制限）</li>
                            <li><strong>规则2：</strong>连续9点在中心线同一侧</li>
                            <li><strong>规则3：</strong>连续6点递增或递减</li>
                            <li><strong>规则4：</strong>连续14点交替上下波动</li>
                            <li><strong>规则5：</strong>3点中有2点落在B区之外（±2σ以外）</li>
                            <li><strong>规则6：</strong>5点中有4点落在C区之外（±1σ以外）</li>
                            <li><strong>规则7：</strong>连续15点落在C区内（±1σ以内）</li>
                            <li><strong>规则8：</strong>连续8点落在C区外（±1σ以外）</li>
                        </ol>
                        <p class="note">💡 分区定义：A区(±2σ~±3σ)、B区(±1σ~±2σ)、C区(0~±1σ)</p>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">📉 p图和np图算法</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>p图（不合格品率控制图）：</strong>
                        <ul>
                            <li><code>p̄ = Σdᵢ / Σnᵢ</code> - 平均不合格品率</li>
                            <li><code>UCL = p̄ + 3√[p̄(1-p̄)/nᵢ]</code> - 上控制限（可变）</li>
                            <li><code>LCL = max(0, p̄ - 3√[p̄(1-p̄)/nᵢ])</code> - 下控制限</li>
                        </ul>
                    </div>
                    <div class="algorithm-item">
                        <strong>np图（不合格品数控制图，样本量固定）：</strong>
                        <ul>
                            <li><code>np̄ = Σdᵢ / k</code> - 平均不合格品数</li>
                            <li><code>UCL = np̄ + 3√[np̄(1-p̄)]</code> - 上控制限</li>
                            <li><code>LCL = max(0, np̄ - 3√[np̄(1-p̄)])</code> - 下控制限</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tab-container">
            <div class="tab-buttons">
                <button 
                    class="tab-btn" 
                    :class="{ active: activeTab === 'capability' }"
                    @click="activeTab = 'capability'"
                >
                    过程能力
                </button>
                <button 
                    class="tab-btn"
                    :class="{ active: activeTab === 'performance' }"
                    @click="activeTab = 'performance'"
                >
                    过程性能
                </button>
                <button 
                    class="tab-btn"
                    :class="{ active: activeTab === 'defect' }"
                    @click="activeTab = 'defect'"
                >
                    不合格统计
                </button>
            </div>
            
            <!-- 过程能力 Tab -->
            <div v-show="activeTab === 'capability'" class="stats-grid">
                <template v-if="project.type === 'xbar-r'">
                    <div class="stat-card">
                        <div class="stat-value">{{ xbarRResult?.xBar.toFixed(3) }}</div>
                        <div class="stat-label">X-bar（总均值）</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ xbarRResult?.rBar.toFixed(3) }}</div>
                        <div class="stat-label">R-bar（平均极差）</div>
                    </div>
                    
                    <!-- X-bar 控制限 -->
                    <div class="stat-card" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);">
                        <div class="stat-value" style="color: #1976d2;">{{ xbarRResult?.uclX.toFixed(3) }}</div>
                        <div class="stat-label">UCL(X)</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);">
                        <div class="stat-value" style="color: #388e3c;">{{ xbarRResult?.xBar.toFixed(3) }}</div>
                        <div class="stat-label">CL(X)</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);">
                        <div class="stat-value" style="color: #d32f2f;">{{ xbarRResult?.lclX.toFixed(3) }}</div>
                        <div class="stat-label">LCL(X)</div>
                    </div>
                    
                    <!-- R 控制限 -->
                    <div class="stat-card" style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);">
                        <div class="stat-value" style="color: #f57c00;">{{ xbarRResult?.uclR.toFixed(3) }}</div>
                        <div class="stat-label">UCL(R)</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);">
                        <div class="stat-value" style="color: #7b1fa2;">{{ xbarRResult?.rBar.toFixed(3) }}</div>
                        <div class="stat-label">CL(R)</div>
                    </div>
                    <div class="stat-card" style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);">
                        <div class="stat-value" style="color: #c2185b;">{{ xbarRResult?.lclR.toFixed(3) }}</div>
                        <div class="stat-label">LCL(R)</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-value">{{ xbarRResult?.sigma.toFixed(3) }}</div>
                        <div class="stat-label">σ（标准差）</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ xbarRResult?.n }}</div>
                        <div class="stat-label">子组大小 n</div>
                    </div>
                    
                    <template v-if="cpResult">
                        <div class="stat-card" :class="cpkClass">
                            <div class="stat-value">{{ cpResult.cp.toFixed(3) }}</div>
                            <div class="stat-label">Cp（过程能力）</div>
                        </div>
                        <div class="stat-card" :class="cpkClass">
                            <div class="stat-value">{{ cpResult.cpk.toFixed(3) }}</div>
                            <div class="stat-label">Cpk（能力指数）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{{ cpResult.cpu.toFixed(3) }}</div>
                            <div class="stat-label">CPU</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{{ cpResult.cpl.toFixed(3) }}</div>
                            <div class="stat-label">CPL</div>
                        </div>
                    </template>
                    <div v-else style="grid-column:1/-1;text-align:center;padding:20px;color:#999;">
                        请设置USL和LSL查看过程能力
                    </div>
                </template>
                
                <template v-else>
                    <div style="grid-column:1/-1;text-align:center;padding:20px;color:#999;">
                        ℹ️ Cp/Cpk适用于计量型数据，请设置USL/LSL查看
                    </div>
                </template>
            </div>
            
            <!-- 过程性能 Tab -->
            <div v-show="activeTab === 'performance'" class="stats-grid">
                <template v-if="ppResult">
                    <div class="stat-card">
                        <div class="stat-value">{{ ppResult.pp.toFixed(3) }}</div>
                        <div class="stat-label">Pp（过程性能）</div>
                    </div>
                    <div class="stat-card" :class="ppkClass">
                        <div class="stat-value">{{ ppResult.ppk.toFixed(3) }}</div>
                        <div class="stat-label">Ppk（性能指数）</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ ppResult.ppu.toFixed(3) }}</div>
                        <div class="stat-label">PPU</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ ppResult.ppl.toFixed(3) }}</div>
                        <div class="stat-label">PPL</div>
                    </div>
                </template>
                <div v-else style="grid-column:1/-1;text-align:center;padding:20px;color:#999;">
                    请设置过程性能规格限（USLp/LSLp）查看Pp/Ppk
                </div>
            </div>
            
            <!-- 不合格统计 Tab -->
            <div v-show="activeTab === 'defect'" class="stats-grid">
                <template v-if="project.type === 'xbar-r'">
                    <div class="stat-card">
                        <div class="stat-value">{{ totalSamples }}</div>
                        <div class="stat-label">总样本数</div>
                    </div>
                    <div class="stat-card" :class="outsideSpec > 0 ? 'warning' : 'success'">
                        <div class="stat-value">{{ outsideSpec }}</div>
                        <div class="stat-label">超规格数</div>
                    </div>
                    <div class="stat-card" :class="parseFloat(defectRate) > 0 ? 'warning' : 'success'">
                        <div class="stat-value">{{ defectRate }}%</div>
                        <div class="stat-label">不合格率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ project.data.length }}</div>
                        <div class="stat-label">子组数</div>
                    </div>
                </template>
                
                <template v-else-if="project.type === 'p'">
                    <div class="stat-card warning">
                        <div class="stat-value">{{ overallDefectRate }}%</div>
                        <div class="stat-label">总不合格率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ totalDefectives }}</div>
                        <div class="stat-label">不合格品数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ totalUnits - totalDefectives }}</div>
                        <div class="stat-label">合格品数</div>
                    </div>
                </template>
                
                <template v-else-if="project.type === 'np'">
                    <div class="stat-card warning">
                        <div class="stat-value">{{ npDefectRate }}%</div>
                        <div class="stat-label">总不合格率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ totalDefectives }}</div>
                        <div class="stat-label">不合格数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ npSampleSize }}</div>
                        <div class="stat-label">固定样本n</div>
                    </div>
                </template>
            </div>
        </div>
        
        <!-- 分析结论 -->
        <div v-if="conclusion" id="conclusionSection" style="margin-top:25px;padding-top:20px;border-top:2px solid #f1f1f1;">
            <h3 style="color:#667eea;margin-bottom:15px;font-size:16px;">📊 分析结论</h3>
            <div 
                id="conclusionContent" 
                style="background:linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);padding:20px;border-radius:12px;line-height:1.8;"
                :style="{ borderLeft: `4px solid ${conclusionColors[conclusion.status]}` }"
                v-html="conclusion.html"
            ></div>
        </div>
    </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { 
    calculateXbarR, 
    calculatePChart, 
    calculateNpChart,
    calculateProcessCapability,
    calculateProcessPerformance
} from '../utils/statistics';
import { WE_RULES } from '../utils/constants';
import {
    checkConsecutiveSameSide,
    checkMonotonic,
    checkAlternating,
    checkTwoOfThree,
    checkFourOfFive,
    checkInControlZone,
    checkEightOutsideC
} from '../utils/statistics';

export default {
    name: 'StatsPanel',
    props: {
        project: {
            type: Object,
            default: null
        }
    },
    setup(props) {
        const activeTab = ref('capability');
        const showAlgorithm = ref(false);
        
        // 计算属性
        const xbarRResult = computed(() => {
            if (props.project?.type === 'xbar-r') {
                return calculateXbarR(props.project.data);
            }
            return null;
        });

        const cpResult = computed(() => {
            if (props.project?.usl && props.project?.lsl) {
                return calculateProcessCapability(props.project.data, props.project.usl, props.project.lsl);
            }
            return null;
        });

        const ppResult = computed(() => {
            if (props.project?.uslp && props.project?.lslp) {
                return calculateProcessPerformance(props.project.data, props.project.uslp, props.project.lslp);
            }
            return null;
        });

        const cpkClass = computed(() => {
            if (!cpResult.value) return '';
            return cpResult.value.cpk >= 1.33 ? 'success' : cpResult.value.cpk >= 1.0 ? 'warning' : 'danger';
        });

        const ppkClass = computed(() => {
            if (!ppResult.value) return '';
            return ppResult.value.ppk >= 1.33 ? 'success' : ppResult.value.ppk >= 1.0 ? 'warning' : 'danger';
        });

        // 不合格统计
        const totalSamples = computed(() => {
            if (!props.project) return 0;
            return props.project.data.flatMap(d => d.values).length;
        });

        const outsideSpec = computed(() => {
            if (!props.project || !props.project.usl || !props.project.lsl) return 0;
            const allValues = props.project.data.flatMap(d => d.values);
            return allValues.filter(v => v > props.project.usl || v < props.project.lsl).length;
        });

        const defectRate = computed(() => {
            if (totalSamples.value === 0) return '0.00';
            return ((outsideSpec.value / totalSamples.value) * 100).toFixed(2);
        });

        const pResult = computed(() => {
            if (props.project?.type === 'p') {
                return calculatePChart(props.project.data);
            }
            return null;
        });

        const totalUnits = computed(() => {
            if (!pResult.value) return 0;
            return pResult.value.defectives.reduce((sum, d) => sum + d.n, 0);
        });

        const totalDefectives = computed(() => {
            if (!pResult.value) return 0;
            return pResult.value.defectives.reduce((sum, d) => sum + d.count, 0);
        });

        const overallDefectRate = computed(() => {
            if (totalUnits.value === 0) return '0.000';
            return ((totalDefectives.value / totalUnits.value) * 100).toFixed(3);
        });

        const npResult = computed(() => {
            if (props.project?.type === 'np' && props.project.data.length > 0) {
                const n = props.project.data[0].values.length || 50;
                return calculateNpChart(props.project.data, n);
            }
            return null;
        });

        const npSampleSize = computed(() => {
            return npResult.value?.n || 0;
        });

        const npDefectRate = computed(() => {
            if (!npResult.value || npResult.value.defectives.length === 0) return '0.000';
            const rate = (totalDefectives.value / (npResult.value.defectives.length * npResult.value.n)) * 100;
            return rate.toFixed(3);
        });

        // 生成分析结论
        const conclusion = computed(() => {
            if (!props.project || props.project.data.length < 2) return null;

            let conclusionParts = [];
            let overallStatus = 'success';

            if (props.project.type === 'xbar-r' && xbarRResult.value) {
                const result = xbarRResult.value;
                
                // 1. 过程稳定性评估
                const outOfControlPoints = result.subgroupMeans.filter(m => m > result.uclX || m < result.lclX).length;
                const totalPoints = result.subgroupMeans.length;

                if (outOfControlPoints === 0) {
                    conclusionParts.push(`<strong>✅ 过程稳定性：</strong>所有${totalPoints}个子组均在控制限内，过程处于统计控制状态。`);
                } else {
                    conclusionParts.push(`<strong>⚠️ 过程稳定性：</strong>有${outOfControlPoints}个子组(${((outOfControlPoints/totalPoints)*100).toFixed(1)}%)超出控制限，过程存在异常波动，需要调查原因。`);
                    overallStatus = 'danger';
                }

                // 2. WE规则检查
                let ruleViolations = [];
                const means = result.subgroupMeans;
                const checks = [
                    () => checkConsecutiveSameSide(means, 9, result.xBar),
                    () => checkMonotonic(means, 6),
                    () => checkAlternating(means, 14),
                    () => checkTwoOfThree(means, result.uclX, result.lclX, result.xBar),
                    () => checkFourOfFive(means, result.uclX, result.lclX, result.xBar),
                    () => checkInControlZone(means, result.uclX, result.lclX, result.xBar, 15),
                    () => checkEightOutsideC(means, result.uclX, result.lclX, result.xBar)
                ];

                checks.forEach((check, idx) => {
                    if (check()) {
                        ruleViolations.push(WE_RULES[idx + 1].name);
                    }
                });

                if (ruleViolations.length > 0) {
                    conclusionParts.push(`<strong>🔍 判异规则：</strong>触发以下Western Electric规则：${ruleViolations.join('、')}，表明过程可能存在特殊原因变异。`);
                    overallStatus = 'danger';
                } else {
                    conclusionParts.push(`<strong>🔍 判异规则：</strong>未触发任何Western Electric判异规则，过程表现良好。`);
                }

                // 3. 过程能力评估
                if (cpResult.value) {
                    let capabilityLevel = '';
                    if (cpResult.value.cpk >= 1.67) {
                        capabilityLevel = '优秀（Cpk≥1.67）';
                        conclusionParts.push(`<strong>💪 过程能力：</strong>Cpk=${cpResult.value.cpk.toFixed(3)}，能力等级为<strong style="color:#28a745">${capabilityLevel}</strong>，过程能力非常充足。`);
                    } else if (cpResult.value.cpk >= 1.33) {
                        capabilityLevel = '良好（1.33≤Cpk<1.67）';
                        conclusionParts.push(`<strong>💪 过程能力：</strong>Cpk=${cpResult.value.cpk.toFixed(3)}，能力等级为<strong style="color:#17a2b8">${capabilityLevel}</strong>，过程能力充足。`);
                    } else if (cpResult.value.cpk >= 1.0) {
                        capabilityLevel = '一般（1.0≤Cpk<1.33）';
                        conclusionParts.push(`<strong>💪 过程能力：</strong>Cpk=${cpResult.value.cpk.toFixed(3)}，能力等级为<strong style="color:#ffc107">${capabilityLevel}</strong>，建议改进过程以减少变异。`);
                        overallStatus = overallStatus === 'danger' ? 'danger' : 'warning';
                    } else {
                        capabilityLevel = '不足（Cpk<1.0）';
                        conclusionParts.push(`<strong>💪 过程能力：</strong>Cpk=${cpResult.value.cpk.toFixed(3)}，能力等级为<strong style="color:#dc3545">${capabilityLevel}</strong>，过程能力严重不足，必须立即改进！`);
                        overallStatus = 'danger';
                    }

                    // 偏移分析
                    const centeringRatio = Math.abs(cpResult.value.mean - (props.project.usl + props.project.lsl) / 2) / ((props.project.usl - props.project.lsl) / 2);
                    if (centeringRatio > 0.25) {
                        conclusionParts.push(`<strong>📍 中心位置：</strong>过程均值相对规格中心偏移${(centeringRatio*100).toFixed(1)}%，建议调整工艺参数使过程居中。`);
                    } else {
                        conclusionParts.push(`<strong>📍 中心位置：</strong>过程均值接近规格中心，居中良好。`);
                    }
                } else {
                    conclusionParts.push(`<strong>ℹ️ 过程能力：</strong>未设置规格限（USL/LSL），无法计算Cpk。建议在项目信息中设置规格限以评估过程能力。`);
                }

                // 4. 变异程度
                const cv = (result.sigma / result.xBar * 100).toFixed(2);
                if (cv < 5) {
                    conclusionParts.push(`<strong>📊 变异程度：</strong>变异系数CV=${cv}%，过程变异较小，一致性良好。`);
                } else if (cv < 10) {
                    conclusionParts.push(`<strong>📊 变异程度：</strong>变异系数CV=${cv}%，过程变异在可接受范围内。`);
                } else {
                    conclusionParts.push(`<strong>📊 变异程度：</strong>变异系数CV=${cv}%，过程变异较大，需要减少波动。`);
                    if (overallStatus === 'success') overallStatus = 'warning';
                }

            } else if (props.project.type === 'p' || props.project.type === 'np') {
                const defectives = props.project.data.reduce((sum, d) => {
                    return sum + d.values.filter(v => v === 1 || (typeof v === 'number' && v < 0.5)).length;
                }, 0);
                const units = props.project.data.reduce((sum, d) => sum + d.values.length, 0);
                const rate = (defectives / units * 100).toFixed(2);

                if (parseFloat(rate) < 1) {
                    conclusionParts.push(`<strong>✅ 质量水平：</strong>不合格率为${rate}%，质量表现优秀。`);
                } else if (parseFloat(rate) < 5) {
                    conclusionParts.push(`<strong>⚠️ 质量水平：</strong>不合格率为${rate}%，质量表现一般，仍有改进空间。`);
                    overallStatus = 'warning';
                } else {
                    conclusionParts.push(`<strong>❌ 质量水平：</strong>不合格率为${rate}%，质量表现较差，需要重点改进。`);
                    overallStatus = 'danger';
                }

                conclusionParts.push(`<strong>📈 数据统计：</strong>共检验${units}个产品，发现${defectives}个不合格品，子组数为${props.project.data.length}。`);
            }

            // 总体评价
            conclusionParts.push('<hr style="margin:15px 0;border:none;border-top:1px solid #ddd;">');
            
            if (overallStatus === 'success') {
                conclusionParts.push(`<strong style="color:#28a745;font-size:15px;">🎯 综合评价：</strong>该过程整体表现<strong style="color:#28a745">良好</strong>，处于受控状态，建议继续保持当前工艺条件，定期监控即可。`);
            } else if (overallStatus === 'warning') {
                conclusionParts.push(`<strong style="color:#ffc107;font-size:15px;">🎯 综合评价：</strong>该过程存在<strong style="color:#ffc107">一定风险</strong>，建议：①加强过程监控频率；②分析变异来源；③考虑优化工艺参数以提升过程能力。`);
            } else {
                conclusionParts.push(`<strong style="color:#dc3545;font-size:15px;">🎯 综合评价：</strong>该过程存在<strong style="color:#dc3545">严重问题</strong>，建议：①立即停止生产并排查异常原因；②对已生产产品进行全检；③重新验证工艺参数；④制定纠正预防措施(CAPA)。`);
            }

            return {
                html: conclusionParts.join('<br><br>'),
                status: overallStatus
            };
        });

        const conclusionColors = {
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545'
        };

        return {
            activeTab,
            showAlgorithm,
            xbarRResult,
            cpResult,
            ppResult,
            cpkClass,
            ppkClass,
            totalSamples,
            outsideSpec,
            defectRate,
            totalUnits,
            totalDefectives,
            overallDefectRate,
            npSampleSize,
            npDefectRate,
            conclusion,
            conclusionColors,
        };
    }
}
</script>
