import matplotlib
import numpy as np
import pandas as pd
import scipy
import streamlit as st
from matplotlib import pyplot as plt

matplotlib.rcParams['font.family'] = ['WenQuanYi Zen Hei']

st.set_page_config(page_title='Grade Viewer', layout='wide')

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
            '语数英': {'total': 450, 'max': 414, 'median': 357, 'mean': 352.2, 'std': 18, 'count': 624},
        }
    }
}

st.sidebar.subheader('北京四中考试成绩分析')

exam = st.sidebar.selectbox('选择考试', list(exams.keys()))


t1, t2 = st.sidebar.tabs(['录入成绩', '上传成绩'])

upload = t2.file_uploader('上传成绩', type='csv')

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
    ax.annotate(f'{stats["mean"]:.0f}', (stats['mean'], 0.1), xytext=(stats['mean'], 0.001))
    # mark maximum on the curve
    ax.vlines(stats['max'], 0, 0.1, label='最高分', color='b', linestyle='--', linewidth=1)
    ax.annotate(f'{stats["max"]}', (stats['max'], 0.1), xytext=(stats['max'], 0.001))
    # mark score on the curve
    ax.vlines(scores[subject], 0, 0.1, label='我的成绩', color='r', linestyle='--', linewidth=1)
    ax.annotate(f'{scores[subject]}', (scores[subject], 0.1), xytext=(scores[subject], 0.001))
    # calculate percentile
    percentile = scipy.stats.percentileofscore(
        np.random.normal(stats['mean'], stats['std'], 10000), scores[subject])
    rank = int((100 - percentile) / 100 * stats['count'])
    # format
    ax.set_xlim(0, stats['total']+1)
    ax.set_ylim(0, 0.1)
    ax.set_title(f'{subject} (Rank:{rank}) ({percentile:.1f}%)')
    ax.legend(loc='upper left')


fig, ax = plt.subplots(3, 3, figsize=(12, 8))
ax = ax.flatten()
for i, (sub, score) in enumerate(scores.items()):
    plot_subject_distribution(exam, scores, sub, ax[i])
fig.tight_layout()
st.pyplot(fig)
st.caption('**注意：** 以上分布仅供参考，不代表真实分布。排名根据正态分布估计，可能存在误差。数据仅个人可见，不会被保存。')
