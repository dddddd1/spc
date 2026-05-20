import { XBAR_R_CONSTANTS } from './constants.js';

// 判异规则检查函数
export function checkConsecutiveSameSide(data, count, center) {
    for (let i = 0; i <= data.length - count; i++) {
        let sameSide = true;
        for (let j = i; j < i + count; j++) {
            if ((data[j] >= center) !== (data[i] >= center)) {
                sameSide = false;
                break;
            }
        }
        if (sameSide) return true;
    }
    return false;
}

export function checkMonotonic(data, count) {
    for (let i = 0; i <= data.length - count; i++) {
        let increasing = true;
        let decreasing = true;
        for (let j = i; j < i + count - 1; j++) {
            if (data[j] >= data[j + 1]) increasing = false;
            if (data[j] <= data[j + 1]) decreasing = false;
        }
        if (increasing || decreasing) return true;
    }
    return false;
}

export function checkAlternating(data, count) {
    for (let i = 0; i <= data.length - count; i++) {
        let alternating = true;
        for (let j = i; j < i + count - 1; j++) {
            if ((data[j] >= data[j + 1]) === (data[j + 1] >= data[j + 2])) {
                alternating = false;
                break;
            }
        }
        if (alternating) return true;
    }
    return false;
}

export function checkTwoOfThree(means, ucl, lcl, xBar) {
    const aZone = (ucl - xBar) / 3;
    const bZone = aZone * 2;
    for (let i = 0; i <= means.length - 3; i++) {
        const subset = means.slice(i, i + 3);
        const inBOrBeyond = subset.filter(m => m > xBar + bZone || m < xBar - bZone).length;
        if (inBOrBeyond >= 2) return true;
    }
    return false;
}

export function checkFourOfFive(means, ucl, lcl, xBar) {
    const cZone = (ucl - xBar) / 3;
    for (let i = 0; i <= means.length - 5; i++) {
        const subset = means.slice(i, i + 5);
        const inCOrBeyond = subset.filter(m => m > xBar + cZone || m < xBar - cZone).length;
        if (inCOrBeyond >= 4) return true;
    }
    return false;
}

export function checkInControlZone(means, ucl, lcl, xBar, count) {
    const cZone = (ucl - xBar) / 3;
    for (let i = 0; i <= means.length - count; i++) {
        const subset = means.slice(i, i + count);
        const inCZone = subset.filter(m => Math.abs(m - xBar) <= cZone).length;
        if (inCZone === count) return true;
    }
    return false;
}

export function checkEightOutsideC(means, ucl, lcl, xBar) {
    const cZone = (ucl - xBar) / 3;
    for (let i = 0; i <= means.length - 8; i++) {
        const subset = means.slice(i, i + 8);
        const outsideC = subset.filter(m => Math.abs(m - xBar) > cZone).length;
        if (outsideC >= 8) return true;
    }
    return false;
}

export function checkSevenConsecutiveTrend(data) {
    for (let i = 0; i <= data.length - 7; i++) {
        let increasing = true;
        let decreasing = true;
        for (let j = i; j < i + 6; j++) {
            if (data[j] >= data[j + 1]) increasing = false;
            if (data[j] <= data[j + 1]) decreasing = false;
        }
        if (increasing) return { type: '上升', start: i + 1, end: i + 7 };
        if (decreasing) return { type: '下降', start: i + 1, end: i + 7 };
    }
    return null;
}

// X-bar R控制图计算
export function calculateXbarR(data) {
    if (!data || data.length < 2) return null;

    const subgroupMeans = data.map(d => d.values.reduce((a, b) => a + b, 0) / d.values.length);
    const subgroupRanges = data.map(d => Math.max(...d.values) - Math.min(...d.values));
    const n = data[0].values.length;

    const xBar = subgroupMeans.reduce((a, b) => a + b, 0) / subgroupMeans.length;
    const rBar = subgroupRanges.reduce((a, b) => a + b, 0) / subgroupRanges.length;

    let a2 = 0.577;
    let d2 = 1.128; // 用于计算标准差σ
    if (XBAR_R_CONSTANTS[n]) {
        a2 = XBAR_R_CONSTANTS[n][0];  // A2系数
        d2 = XBAR_R_CONSTANTS[n][1];  // d2系数
    } else if (n > 10) {
        a2 = 3 / (n * Math.sqrt(2));
        d2 = n > 15 ? 3.472 : 3.078;
    }

    const uclX = xBar + a2 * rBar;
    const lclX = xBar - a2 * rBar;

    // 使用D3和D4系数计算R图的控制限
    let d3 = 0;  // D3系数
    let d4 = 3.267;  // D4系数
    if (XBAR_R_CONSTANTS[n]) {
        d3 = XBAR_R_CONSTANTS[n][2];  // D3系数
        d4 = XBAR_R_CONSTANTS[n][3];  // D4系数
    } else if (n > 10) {
        d3 = n > 15 ? 0.347 : 0.223;
        d4 = n > 15 ? 1.653 : 1.777;
    }
    
    const uclR = d4 * rBar;
    const lclR = Math.max(0, d3 * rBar); // LCL不能为负数

    const sigma = rBar / d2; // 使用正确的d2系数计算标准差

    return {
        xBar, rBar, uclX, lclX, uclR, lclR,
        subgroupMeans, subgroupRanges, n, sigma
    };
}

// p控制图计算
export function calculatePChart(data) {
    if (!data || data.length < 2) return null;

    const defectives = data.map(d => {
        const n = d.values.length;
        const defectiveCount = d.values.filter(v => v === 1 || (typeof v === 'number' && v < 0.5)).length;
        return { count: defectiveCount, n: n };
    });

    const totalDefectives = defectives.reduce((sum, d) => sum + d.count, 0);
    const totalSize = defectives.reduce((sum, d) => sum + d.n, 0);
    const pBar = totalDefectives / totalSize;

    const proportions = defectives.map(d => d.count / d.n);
    const uclP = defectives.map(d => {
        const sigma = Math.sqrt(pBar * (1 - pBar) / d.n);
        return pBar + 3 * sigma;
    });
    const lclP = defectives.map(d => {
        const sigma = Math.sqrt(pBar * (1 - pBar) / d.n);
        return Math.max(0, pBar - 3 * sigma);
    });

    return { pBar, uclP, lclP, proportions, defectives };
}

// np控制图计算
export function calculateNpChart(data, n) {
    if (!data || data.length < 2) return null;

    const defectives = data.map(d => d.values.filter(v => v === 1 || (typeof v === 'number' && v < 0.5)).length);
    const npBar = defectives.reduce((a, b) => a + b, 0) / defectives.length;
    const pBar = npBar / n;

    const uclNp = npBar + 3 * Math.sqrt(npBar * (1 - pBar));
    const lclNp = Math.max(0, npBar - 3 * Math.sqrt(npBar * (1 - pBar)));

    return { npBar, uclNp, lclNp, defectives, n };
}

// 过程能力计算（使用组内变异估计的σ）
export function calculateProcessCapability(data, usl, lsl) {
    if (!data || !usl || !lsl) return null;

    const allValues = data.flatMap(d => d.values);
    const mean = allValues.reduce((a, b) => a + b, 0) / allValues.length;
    
    // 对于X-bar R图，使用R-bar/d2估计σ（组内变异）
    const subgroupRanges = data.map(d => Math.max(...d.values) - Math.min(...d.values));
    const rBar = subgroupRanges.reduce((a, b) => a + b, 0) / subgroupRanges.length;
    const n = data[0].values.length;
    
    let d2 = 1.128; // d2系数
    if (XBAR_R_CONSTANTS[n]) {
        d2 = XBAR_R_CONSTANTS[n][1];  // d2系数
    } else if (n > 10) {
        d2 = n > 15 ? 3.472 : 3.078;
    }
    
    const sigma = rBar / d2; // 使用R-bar/d2估计σ

    if (sigma === 0) return null;

    const cp = (usl - lsl) / (6 * sigma);
    const cpu = (usl - mean) / (3 * sigma);
    const cpl = (mean - lsl) / (3 * sigma);
    const cpk = Math.min(cpu, cpl);

    return { cp, cpk, cpu, cpl, sigma, mean, usl, lsl };
}

// 过程性能计算
export function calculateProcessPerformance(data, usl, lsl) {
    if (!data || !usl || !lsl) return null;

    const allValues = data.flatMap(d => d.values);
    const mean = allValues.reduce((a, b) => a + b, 0) / allValues.length;
    const variance = allValues.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / allValues.length;
    const sigma = Math.sqrt(variance);

    if (sigma === 0) return null;

    const pp = (usl - lsl) / (6 * sigma);
    const ppu = (usl - mean) / (3 * sigma);
    const ppl = (mean - lsl) / (3 * sigma);
    const ppk = Math.min(ppu, ppl);

    return { pp, ppk, ppu, ppl, sigma, mean, usl, lsl };
}
