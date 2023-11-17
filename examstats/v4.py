import matplotlib
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from matplotlib import pyplot as plt

matplotlib.rcParams['font.family'] = ['WenQuanYi Zen Hei']

st.set_page_config(page_title='北京四中考试成绩分析', layout='wide')

exams = {
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
    }
}

st.sidebar.subheader('北京四中考试成绩分析')

exam = st.sidebar.selectbox('选择考试', list(exams.keys()))


t1, t2 = st.sidebar.tabs(['录入成绩', '上传成绩'])

upload = t2.file_uploader('此处可上传之前下载保存的成绩', type='csv')

if upload:
    scores = pd.read_csv(upload).to_dict(orient='records')[0]
else:
    scores = {sub: 0 for sub in exams[exam]['subject'].keys()}

scores = {
    sub: t1.number_input(
        sub, min_value=0.0, max_value=float(exams[exam]['subject'][sub]['total']),
        value=float(scores[sub]), step=1.0) for sub in exams[exam]['subject'].keys()}


t1.download_button('下载保存', pd.DataFrame(scores, index=[0]).to_csv(index=False), f'{exam}.csv', 'text/csv')


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
    percentile = scipy.stats.percentileofscore(
        np.random.normal(stats['mean'], stats['std'], 10000), scores[subject])
    rank = int((100 - percentile) / 100 * stats['count'])
    # format
    ax.set_xlim(0, stats['total']+1)
    ax.set_ylim(0, 0.1)
    ax.set_title(f'{subject} (Rank:{rank}) ({percentile:.1f}%)')
    ax.legend(loc='upper left')


@st.cache_data
def plot_subject_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, (sub, score) in enumerate(scores.items()):
        _plot_func(exam, scores, sub, ax[i])
    fig.tight_layout()
    return fig


def plot_group_distribution(exam, scores, group, ax):
    stats = exams[exam]['group'][group]
    total = sum(exams[exam]['subject'][sub]['total'] for sub in stats['include'])
    x = np.linspace(0, total, 400)
    ax.plot(x, scipy.stats.norm.pdf(x, stats['mean'], stats['std']), label='成绩分布')
    # mark mean on the curve
    ax.vlines(stats['mean'], 0, 0.1, label='平均分', color='g', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["mean"]:.0f}', (stats['mean'], 0.001), xytext=(stats['mean']+1, 0.001))
    # mark maximum on the curve
    ax.vlines(stats['max'], 0, 0.1, label='最高分', color='b', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["max"]}', (stats['max'], 0.018), xytext=(stats['max']+1, 0.018))
    # mark score on the curve
    score = sum(scores[sub] for sub in stats['include'])
    ax.vlines(score, 0, 0.1, label='我的成绩', color='r', linestyle='--', linewidth=1)
    ax.annotate(f'{score}', (score, 0.011), xytext=(score+1, 0.011), color='r')
    # calculate percentile
    percentile = scipy.stats.percentileofscore(
        np.random.normal(stats['mean'], stats['std'], 10000), score)
    rank = int((100 - percentile) / 100 * stats['count'])
    # format
    ax.set_xlim(0, total+1)
    ax.set_ylim(0, 0.02)
    ax.set_yticks([0, 0.01, 0.02])
    ax.set_title(f'{group} (Rank:{rank}) ({percentile:.1f}%)')
    ax.legend(loc='upper left')


@st.cache_data
def plot_subject_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, (sub, score) in enumerate(scores.items()):
        _plot_func(exam, scores, sub, ax[i])
    fig.tight_layout()
    return fig


@st.cache_data
def plot_group_3by3_chart(exam, scores, _plot_func):
    fig, ax = plt.subplots(3, 3, figsize=(12, 8))
    ax = ax.flatten()
    for i, grp in enumerate(exams[exam]['group'].keys()):
        _plot_func(exam, scores, grp, ax[i])
    for i in range(i+1, 9):
        ax[i].set_axis_off()
    fig.tight_layout()
    return fig


@st.cache_resource
def plot_all_subject_distribution(exam, scores):
    # plot all bell curves of 9 subjects in one chart
    fig, ax = plt.subplots(figsize=(12, 5))
    for sub in exams[exam]['subject'].keys():
        stats = exams[exam]['subject'][sub]
        x = np.linspace(0, stats['total'], 400)
        ax.plot(x, scipy.stats.norm.pdf(x, stats['mean'], stats['std']), label=sub)
    xrange = max([v['max'] for k, v in exams[exam]['subject'].items()])+1
    ax.set_xlim(0, xrange)
    ax.set_ylim(0, 0.1)
    ax.legend(loc='upper left')
    return fig


# if all scores are 0, show a warning
if all(score == 0 for score in scores.values()):
    st.warning('请在左侧输入您的成绩。')

st.write(exam)

tb1, tb2, tb3 = st.tabs(['单科分布', '组合分布', '学科分布'])
tb1.pyplot(plot_subject_3by3_chart(exam, scores, plot_subject_distribution))
tb2.pyplot(plot_group_3by3_chart(exam, scores, plot_group_distribution))
tb3.pyplot(plot_all_subject_distribution(exam, scores))
st.caption('**注意：** 移动端请用系统浏览器打开以获得最佳体验。以上分布仅供参考，不代表真实分布。排名根据正态分布估计，可能存在误差。数据仅个人可见，不会被记录。')
