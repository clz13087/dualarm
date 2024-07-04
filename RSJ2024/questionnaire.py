import matplotlib.pyplot as plt
import japanize_matplotlib

conditions = ['模倣', '融合']
questions = ['記憶', '認知負荷', '学習']
ratings = {
    '模倣': {
        '記憶': [3, 2],
        '認知負荷': [5, 3],
        '学習': [2, 2]
    },
    '融合': {
        '記憶': [5, 5],
        '認知負荷': [2, 6],
        '学習': [5, 6]
    }
}
colors = {'模倣': 'white','融合': 'white'}
marker = {'模倣': 'o', '融合': 's'}

plt.figure(figsize=(4, 3))
# plt.figure()
offset = 0.15
for j, question in enumerate(questions):
    for i, condition in enumerate(conditions):
        x = [j + i * offset - offset/2] * len(ratings[condition][question])  # Centering by offset/2
        plt.scatter(x, ratings[condition][question], label=f'{condition}' if j == 0 else "", color=colors[condition], marker=marker[condition], edgecolors='k')

# Setting x-axis labels to the question names
plt.xticks([i for i in range(len(questions))], questions)
plt.tick_params(length=0)
# plt.xlabel('質問')
plt.legend(loc='upper left')
plt.ylim(1,7)
plt.savefig('/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/questionnaire.pdf')
plt.show()
