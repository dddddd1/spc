<template>
    <div class="card" v-if="project && project.data.length >= 2">
        <div class="card-header">
            <h2>异常报警</h2>
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
            alarms
        };
    }
}
</script>
