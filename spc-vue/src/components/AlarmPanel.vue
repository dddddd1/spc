<template>
    <div class="card" v-if="project && project.data.length >= 2">
        <div class="card-header">
            <h2>异常报警</h2>
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
                <h4>⚠️ Western Electric 判异规则详解</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>3σ分区概念：</strong>
                        <ul>
                            <li><strong>A区（警戒区）：</strong>±2σ ~ ±3σ（控制限外）</li>
                            <li><strong>B区（警告区）：</strong>±1σ ~ ±2σ</li>
                            <li><strong>C区（正常区）：</strong>0 ~ ±1σ（中心线附近）</li>
                        </ul>
                        <p class="note">💡 正常情况下，约68%的点在C区，95%在B区内，99.7%在A区内</p>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则1：1点超出控制限（A区外）</strong>
                        <ul>
                            <li><strong>判断条件：</strong>X̄ᵢ > UCL 或 X̄ᵢ < LCL</li>
                            <li><strong>含义：</strong>过程出现特殊原因变异</li>
                            <li><strong>概率：</strong>正态分布下仅0.27%</li>
                            <li><strong>行动：</strong>立即调查并消除特殊原因</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则2：连续9点在中心线同一侧</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续9个点都 > X̿ 或都 < X̿</li>
                            <li><strong>含义：</strong>过程均值发生偏移</li>
                            <li><strong>概率：</strong>(0.5)⁹ ≈ 0.2%</li>
                            <li><strong>行动：</strong>检查工艺参数是否改变</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则3：连续6点递增或递减</strong>
                        <ul>
                            <li><strong>判断条件：</strong>X̄₁ < X̄₂ < ... < X̄₆ 或相反</li>
                            <li><strong>含义：</strong>过程存在趋势性变化</li>
                            <li><strong>可能原因：</strong>工具磨损、温度漂移等</li>
                            <li><strong>行动：</strong>查找趋势产生的系统性原因</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则4：连续14点交替上下波动</strong>
                        <ul>
                            <li><strong>判断条件：</strong>X̄₁↑X̄₂↓X̄₃↑X̄₄↓...交替14次</li>
                            <li><strong>含义：</strong>过程存在周期性干扰</li>
                            <li><strong>可能原因：</strong>两个不同批次混料、设备交替故障</li>
                            <li><strong>行动：</strong>识别并消除交替影响因素</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则5：3点中有2点在B区外（±2σ外）</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续3点中≥2点满足|X̄ᵢ-X̿| > 2σ</li>
                            <li><strong>含义：</strong>过程变异增大</li>
                            <li><strong>概率：</strong>约0.3%</li>
                            <li><strong>行动：</strong>检查原材料、设备状态</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则6：5点中有4点在C区外（±1σ外）</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续5点中≥4点满足|X̄ᵢ-X̿| > σ</li>
                            <li><strong>含义：</strong>过程离散程度增加</li>
                            <li><strong>概率：</strong>约0.5%</li>
                            <li><strong>行动：</strong>分析变异来源，优化工艺</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则7：连续15点在C区内（±1σ内）</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续15点都满足|X̄ᵢ-X̿| ≤ σ</li>
                            <li><strong>含义：</strong>过程变异过小，可能存在数据造假或分层抽样</li>
                            <li><strong>注意：</strong>看似"太好"也可能是问题</li>
                            <li><strong>行动：</strong>验证数据采集真实性</li>
                        </ul>
                    </div>
                    
                    <div class="algorithm-item">
                        <strong>规则8：连续8点在C区外（±1σ外）</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续8点都满足|X̄ᵢ-X̿| > σ</li>
                            <li><strong>含义：</strong>过程呈现双峰分布或混合分布</li>
                            <li><strong>可能原因：</strong>两台设备、两批原料混用</li>
                            <li><strong>行动：</strong>检查是否存在多个过程混合</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">🔍 其他检测方法</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <strong>连续7点趋势检测：</strong>
                        <ul>
                            <li><strong>判断条件：</strong>连续7点单调递增或递减</li>
                            <li><strong>与规则3区别：</strong>更严格的趋势判断（7点vs6点）</li>
                            <li><strong>应用场景：</strong>早期预警过程漂移</li>
                        </ul>
                    </div>
                </div>
                
                <h4 style="margin-top: 20px;">📋 报警处理流程</h4>
                <div class="algorithm-grid">
                    <div class="algorithm-item">
                        <ol>
                            <li><strong>发现报警：</strong>系统自动检测并显示报警信息</li>
                            <li><strong>确认异常：</strong>核实数据采集是否正确</li>
                            <li><strong>查找原因：</strong>使用鱼骨图、5Why等方法分析根本原因</li>
                            <li><strong>采取措施：</strong>制定纠正和预防措施（CAPA）</li>
                            <li><strong>验证效果：</strong>监控后续数据确认改进有效</li>
                            <li><strong>标准化：</strong>将有效措施纳入标准作业程序</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        
        <div v-if="alarms.length === 0" class="empty-state">
            <p>✅ 暂无报警信息，过程稳定</p>
        </div>
        
        <div v-else class="alarm-box">
            <h4>⚠️ 报警信息（共{{ alarms.length }}条）</h4>
            <div 
                v-for="(alarm, index) in alarms" 
                :key="index"
                class="alarm-item"
                :class="alarm.type"
            >
                {{ alarm.message }}
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';
import { 
    calculateXbarR, 
    calculatePChart, 
    calculateNpChart,
    checkSevenConsecutiveTrend 
} from '../utils/statistics';
import { WE_RULES } from '../utils/constants';

// 导入判异规则检查函数
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
    name: 'AlarmPanel',
    props: {
        project: {
            type: Object,
            default: null
        }
    },
    setup(props) {
        const alarms = ref([]);
        const showAlgorithm = ref(false);

        // 检查Western Electric规则
        const checkWERules = (means, ucl, lcl, xBar) => {
            const violations = [];
            
            // 规则1: 1点落在A区之外
            means.forEach((m, i) => {
                if (m > ucl || m < lcl) {
                    violations.push({
                        type: 'rule-violation',
                        message: `规则1: 第${i + 1}组X-bar(${m.toFixed(3)})超出控制限`
                    });
                }
            });

            // 规则2-8
            const ruleChecks = [
                { rule: WE_RULES[1], check: () => checkConsecutiveSameSide(means, 9, xBar) },
                { rule: WE_RULES[2], check: () => checkMonotonic(means, 6) },
                { rule: WE_RULES[3], check: () => checkAlternating(means, 14) },
                { rule: WE_RULES[4], check: () => checkTwoOfThree(means, ucl, lcl, xBar) },
                { rule: WE_RULES[5], check: () => checkFourOfFive(means, ucl, lcl, xBar) },
                { rule: WE_RULES[6], check: () => checkInControlZone(means, ucl, lcl, xBar, 15) },
                { rule: WE_RULES[7], check: () => checkEightOutsideC(means, ucl, lcl, xBar) }
            ];

            ruleChecks.forEach(({ rule, check }) => {
                if (check()) {
                    violations.push({
                        type: 'rule-violation',
                        message: `${rule.name}: ${rule.desc}`
                    });
                }
            });

            return violations;
        };

        // 更新报警信息
        const updateAlarms = () => {
            if (!props.project || props.project.data.length < 2) {
                alarms.value = [];
                return;
            }

            const newAlarms = [];

            if (props.project.type === 'xbar-r') {
                const result = calculateXbarR(props.project.data);
                if (result) {
                    // 检查WE规则
                    const weViolations = checkWERules(
                        result.subgroupMeans, 
                        result.uclX, 
                        result.lclX, 
                        result.xBar
                    );
                    newAlarms.push(...weViolations);

                    // 检查连续趋势
                    const trend = checkSevenConsecutiveTrend(result.subgroupMeans);
                    if (trend) {
                        newAlarms.push({
                            type: 'trend-violation',
                            message: `趋势报警: 第${trend.start}-${trend.end}组连续7点${trend.type}`
                        });
                    }
                }
            } else if (props.project.type === 'p') {
                const result = calculatePChart(props.project.data);
                if (result) {
                    result.proportions.forEach((p, i) => {
                        if (p > result.uclP[i] || p < result.lclP[i]) {
                            newAlarms.push({
                                type: 'rule-violation',
                                message: `第${i + 1}组p值(${p.toFixed(4)})超出控制限`
                            });
                        }
                    });
                }
            } else if (props.project.type === 'np') {
                const n = Math.round(
                    props.project.data[0].values.reduce((a, b) => a + b, 0) / 
                    props.project.data[0].values.filter(v => v >= 0).length
                ) || 50;
                
                const result = calculateNpChart(props.project.data, n);
                if (result) {
                    result.defectives.forEach((np, i) => {
                        if (np > result.uclNp || np < result.lclNp) {
                            newAlarms.push({
                                type: 'rule-violation',
                                message: `第${i + 1}组np值(${np})超出控制限`
                            });
                        }
                    });
                }
            }

            alarms.value = newAlarms;
        };

        // 监听项目数据变化
        watch(() => props.project, () => {
            updateAlarms();
        }, { deep: true });

        // 初始化
        updateAlarms();

        return {
            alarms,
            showAlgorithm
        };
    }
}
</script>
