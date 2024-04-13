import random

import matplotlib
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from matplotlib import pyplot as plt
from streamlit.components.v1 import html

matplotlib.rcParams['font.family'] = ['WenQuanYi Zen Hei']
# matplotlib.rcParams['font.family'] = ['Heiti TC']

st.set_page_config(page_title='北京四中考试成绩分析', layout='wide')

urls = [
    'https://examstats.streamlit.app',
    'https://examstats1.streamlit.app',
    'https://examstats2.streamlit.app',
    'https://examstats3.streamlit.app',
    'https://examstats4.streamlit.app',
    'https://examstats5.streamlit.app',
    'https://examstats6.streamlit.app',
    'https://examstats7.streamlit.app',
    'https://examstats8.streamlit.app',
    'https://examstats9.streamlit.app',
]
random.shuffle(urls)

st.info(f'如果服务响应缓慢，可尝试使用备份服务：{urls[0]} 或 {urls[1]}', icon='🔗')

if 'exams' not in st.session_state:
    st.session_state['exams'] = {
    '2026届高一上学期期中考试(2023-11)': {
        'subject': {
            '语文': {'total': 150, 'max': 136, 'median': 107, 'mean': 106.9, 'std': 6.9, 'count': 627},
            '数学': {'total': 150, 'max': 149, 'median': 123, 'mean': 121.2, 'std': 14.6, 'count': 626},
            '英语': {'total': 150, 'max': 145.5, 'median': 127, 'mean': 123.9, 'std': 10.1, 'count': 628},
            '物理': {'total': 100, 'max': 100, 'median': 81, 'mean': 79.7, 'std': 4.1, 'count': 626},
            '化学': {'total': 100, 'max': 100, 'median': 82, 'mean': 79.9, 'std': 14.0, 'count': 628},
            '生物': {'total': 100, 'max': 95, 'median': 73, 'mean': 71.6, 'std': 10.8, 'count': 626},
            '政治': {'total': 100, 'max': 94, 'median': 69, 'mean': 68.4, 'std': 10.2, 'count': 627},
            '历史': {'total': 100, 'max': 97, 'median': 79, 'mean': 78.1, 'std': 7.1, 'count': 628},
            '地理': {'total': 100, 'max': 94, 'median': 74, 'mean': 73.6, 'std': 9.2, 'count': 627},
        },
        'group': {
            '语数英总分': {'max': 414, 'median': 357, 'mean': 352.2, 'std': 28, 'count': 624, 'include': ['语文', '数学', '英语']},
            '9科总分': {'max': 950, 'median': 815.5, 'mean': 803.7, 'std': 87, 'count': 623, 'include': ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']},
        }
    },
    '2026届高一下学期期末考试(2024-01)': {
        'subject': {
            '语文': {'total': 150, 'max': 128, 'median': 111, 'mean': 111.1, 'std': 7.30, 'count': 628},
            '数学': {'total': 150, 'max': 147, 'median': 127, 'mean': 124.6, 'std': 11.56, 'count': 628},
            '英语': {'total': 150, 'max': 147, 'median': 133.5, 'mean': 131.2, 'std': 7.97, 'count': 627},
            '物理': {'total': 100, 'max': 100, 'median': 78, 'mean': 75.8, 'std': 15.90, 'count': 627},
            '化学': {'total': 150, 'max': 145, 'median': 122, 'mean': 117.6, 'std': 24.71, 'count': 627},
            '生物': {'total': 100, 'max': 98, 'median': 79, 'mean': 77, 'std': 12, 'count': 628},
            '政治': {'total': 100, 'max': 96, 'median': 79, 'mean': 77.2, 'std': 6.67, 'count': 628},
            '历史': {'total': 100, 'max': 100, 'median': 87.5, 'mean': 86.1, 'std': 5.2, 'count': 627},
            '地理': {'total': 100, 'max': 100, 'median': 89, 'mean': 87.5, 'std': 1.92, 'count': 626},
        },
        'group': {
            '语数英总分': {'max': 410.5, 'median': 371, 'mean': 366.5, 'std': 17.67, 'count': 627, 'include': ['语文', '数学', '英语']},
            '9科总分': {'max': 988.2, 'median': 861.7, 'mean': 848.5, 'std': 60.92, 'count': 625, 'include': ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理'], 'scale': [1, 1, 1, 1, 100.0/150, 1, 1, 1, 1]},
        }
    }
}

exams = st.session_state['exams']

st.sidebar.subheader('北京四中考试成绩分析')

exam = st.sidebar.selectbox('选择考试', list(exams.keys()), index=len(exams)-1)

t1, t2 = st.sidebar.tabs(['录入成绩', '上传成绩'])

upload = t2.file_uploader('此处可上传之前下载保存的成绩', type='csv', key=f'{exam}-upload')

if upload:
    exams[exam]['scores'] = pd.read_csv(upload).to_dict(orient='records')[0]
elif 'scores' not in exams[exam]:
    exams[exam]['scores'] = {sub: 0 for sub in exams[exam]['subject'].keys()}

exams[exam]['scores'] = {
    sub: t1.number_input(
        sub, min_value=0.0, max_value=float(exams[exam]['subject'][sub]['total']),
        value=float(exams[exam]['scores'][sub]), step=1.0, key=f'{exam}-{sub}-ni') for sub in exams[exam]['subject'].keys()}


t1.download_button('下载保存', pd.DataFrame(exams[exam]['scores'], index=[0]).to_csv(index=False), f'{exam}.csv', 'text/csv')


def plot_subject_distribution(exam, scores, subject, ax):
    stats = exams[exam]['subject'][subject]
    x = np.linspace(0, stats['total'], 400)
    ax.plot(x, scipy.stats.norm.pdf(x, stats['mean'], stats['std']), label='成绩分布')
    # mark mean on the curve
    ax.vlines(stats['mean'], 0, 0.1, label='平均分', color='g', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["mean"]:.0f}', (stats['mean'], 0.005), xytext=(stats['mean']+1, 0.005))
    # mark maximum on the curve
    ax.vlines(stats['max'], 0, 0.1, label='最高分', color='b', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["max"]}', (stats['max'], 0.09), xytext=(stats['max']+1, 0.09))
    # mark score on the curve
    ax.vlines(scores[subject], 0, 0.1, label='我的成绩', color='r', linestyle='--', linewidth=1)
    ax.annotate(f'{scores[subject]}', (scores[subject], 0.06), xytext=(scores[subject]+1, 0.06), color='r')
    # calculate percentile
    percentile = scipy.stats.norm.cdf(scores[subject], stats['mean'], stats['std']) * 100
    rank = int((100 - percentile) / 100 * stats['count'])
    # format
    ax.set_xlim(0, stats['total']+1)
    ax.set_ylim(0, 0.1)
    ax.set_title(f'{subject} (Rank:{rank}) ({percentile:.1f}%)')
    ax.legend(loc='upper left')


@st.cache_data(ttl='10m')
def plot_subject_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, (sub, score) in enumerate(scores.items()):
        _plot_func(exam, scores, sub, ax[i])
    fig.tight_layout()
    return fig


def plot_group_distribution(exam, scores, group, ax):
    stats = exams[exam]['group'][group]
    if 'scale' not in stats:
        total = sum(exams[exam]['subject'][sub]['total'] for sub in stats['include'])
        score = sum(scores[sub] for sub in stats['include'])
    else:
        total = sum(exams[exam]['subject'][sub]['total'] * stats['scale'][i] for i, sub in enumerate(stats['include']))
        score = sum(scores[sub] * stats['scale'][i] for i, sub in enumerate(stats['include']))
    x = np.linspace(0, total, 400)
    ax.plot(x, scipy.stats.norm.pdf(x, stats['mean'], stats['std']), label='成绩分布')
    # mark mean on the curve
    ax.vlines(stats['mean'], 0, 0.1, label='平均分', color='g', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["mean"]:.0f}', (stats['mean'], 0.001), xytext=(stats['mean']+1, 0.001))
    # mark maximum on the curve
    ax.vlines(stats['max'], 0, 0.1, label='最高分', color='b', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["max"]}', (stats['max'], 0.018), xytext=(stats['max']+1, 0.018))
    # mark score on the curve
    ax.vlines(score, 0, 0.1, label='我的成绩', color='r', linestyle='--', linewidth=1)
    ax.annotate(f'{score}', (score, 0.011), xytext=(score+1, 0.011), color='r')
    # calculate percentile
    percentile = scipy.stats.norm.cdf(score, stats['mean'], stats['std']) * 100
    rank = int((100 - percentile) / 100 * stats['count'])
    # format
    ax.set_xlim(0, total+1)
    ax.set_ylim(0, 0.02)
    ax.set_yticks([0, 0.01, 0.02])
    ax.set_title(f'{group} (Rank:{rank}) ({percentile:.1f}%)')
    ax.legend(loc='upper left')


@st.cache_data(ttl='10m')
def plot_subject_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, (sub, score) in enumerate(scores.items()):
        _plot_func(exam, scores, sub, ax[i])
    fig.tight_layout()
    return fig


@st.cache_data(ttl='10m')
def plot_group_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, grp in enumerate(exams[exam]['group'].keys()):
        _plot_func(exam, scores, grp, ax[i])
    for i in range(i+1, 9):
        ax[i].set_axis_off()
    fig.tight_layout()
    return fig


@st.cache_resource(ttl='1d')
def plot_all_subject_distribution(exam, scores):
    # plot all bell curves of 9 subjects in one chart
    fig, ax = plt.subplots(figsize=(12, 5))
    for sub in exams[exam]['subject'].keys():
        stats = exams[exam]['subject'][sub]
        x = np.linspace(0, stats['total'], 400)
        ax.plot(x, scipy.stats.norm.pdf(x, stats['mean'], stats['std']), label=sub)
    xrange = max([v['max'] for k, v in exams[exam]['subject'].items()])+1
    ax.set_xlim(0, xrange)
    ax.set_ylim(0, 0.10)
    ax.legend(loc='upper left')
    return fig


@st.cache_data(ttl='10m')
def plot_score_diff_waterfall_chart(exam, scores, sort=False):
    # plot stacked waterfall chart vertically showing how difference in each subject contributes to the total difference
    fig, ax = plt.subplots(figsize=(12, 5))
    # calculate difference
    diffs = {sub: scores[sub] - exams[exam]['subject'][sub]['mean'] for sub in exams[exam]['subject'].keys()}
    # sort by difference
    if sort:
        diffs = dict(sorted(diffs.items(), key=lambda item: item[1], reverse=True))
    # plot cumulative difference
    cumsum = 0
    for sub, diff in diffs.items():
        cumsum += diff
        label = f'{diff:.0f} ({cumsum:.0f})'
        if diff > 0:
            ax.vlines(sub, cumsum-diff, cumsum, color='r', linewidth=73, alpha=0.8)
            ax.text(sub, cumsum, label, ha='center', va='bottom')
        else:
            ax.vlines(sub, cumsum, cumsum-diff, color='g', linewidth=73, alpha=0.8)
            ax.text(sub, cumsum-diff, label, ha='center', va='bottom')
    # plot zero line
    ax.axhline(0, color='k', linewidth=1, linestyle='--')
    ax.set_ylabel('累计均分差异')
    ax.set_title('各学科平均分差异分析')
    ax.set_xlim(-0.5, len(diffs)-0.5)
    return fig


@st.cache_data(ttl='10m')
def plot_subject_percentile_chart(exam, scores, delta=0):
    fig, ax = plt.subplots(figsize=(12, 5))
    for sub in exams[exam]['subject'].keys():
        stats = exams[exam]['subject'][sub]
        percentile = scipy.stats.norm.cdf(scores[sub], stats['mean'], stats['std']) * 100
        rank = int((100 - percentile) / 100 * stats['count'])
        ax.vlines(sub, 0, 100, color='grey', linewidth=1, linestyle='--')
        ax.scatter(sub, percentile, color='r', s=50, zorder=3)
        if delta > 0:
            ax.annotate(f'{percentile:.1f}% ({rank})', (sub, max(0, percentile-2)), ha='center', va='top', color='r', zorder=4)
        else:
            ax.annotate(f'{percentile:.1f}% ({rank})', (sub, percentile+2), ha='center', va='bottom', color='r', zorder=4)
        if delta != 0:
            percentile2 = scipy.stats.norm.cdf(scores[sub]+delta, stats['mean'], stats['std']) * 100
            rank2 = int((100 - percentile2) / 100 * stats['count'])
            ax.scatter(sub, percentile2, color='g', s=50, zorder=3)
            label = f'{percentile2:.1f}% ({rank-rank2:+.0f})'
            if delta > 0:
                ax.annotate(label, (sub, min(100, percentile2+2)), ha='center', va='bottom', color='g', zorder=4)
            else:
                ax.annotate(label, (sub, percentile2-2), ha='center', va='top', color='g', zorder=4)
    ax.set_xlim(-0.5, len(exams[exam]['subject'])-0.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel('百分位')
    ax.set_title('各学科百分位和敏感度分析', pad=20)
    return fig


# if all scores are 0, show a warning
if all(score == 0 for score in exams[exam]['scores'].values()):
    st.warning('请在左侧输入您的成绩。')

st.write(exam)

tb1, tb2, tb3, tb4, tb5 = st.tabs(['单科分布', '组合分布', '均分差异', '学科优势', '学科分布'])
tb1.pyplot(plot_subject_3by3_chart(exam, exams[exam]['scores'], plot_subject_distribution))
tb2.pyplot(plot_group_3by3_chart(exam, exams[exam]['scores'], plot_group_distribution))
diff_sort = tb3.checkbox('按差异排序')
tb3.pyplot(plot_score_diff_waterfall_chart(exam, exams[exam]['scores'], diff_sort))
delta = tb4.slider('分数变化', -20, 20, 0)
tb4.pyplot(plot_subject_percentile_chart(exam, exams[exam]['scores'], delta))
tb5.pyplot(plot_all_subject_distribution(exam, exams[exam]['scores']))
st.caption('**注意：** 移动端请用系统浏览器打开以获得最佳体验。以上分布仅供参考，不代表真实分布。排名根据正态分布估计，可能存在误差。数据仅个人可见，不会被记录。')


#this code below is the statcounter tracking code
takip= """
<!-- Default Statcounter code for FOUR
https://examstats.streamlit.app -->
<script type="text/javascript">
var sc_project=12987808; 
var sc_invisible=1; 
var sc_security="bdb43828"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/12987808/0/bdb43828/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""
html(takip,width=1, height=1)