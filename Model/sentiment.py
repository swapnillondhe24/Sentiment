import io
from matplotlib import image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import wordcloud

import networkx as nx
from fpdf import FPDF
from io import BytesIO
import nltk
from PIL import Image
nltk.download('stopwords')
from nltk.corpus import stopwords
# Load the data
data = pd.read_csv('../Scraper/data.csv')

# Clean the data
data.dropna(subset=['content'], inplace=True)
data = data[['content', 'rating','date','variant']]

# Define function to generate charts
def generate_chart(data, title, chart_type):
    try:    
        if chart_type == 'pie':
            chart = plt.pie(data.value_counts(), labels=data.value_counts().index, autopct='%1.1f%%')
        elif chart_type == 'bar':
            chart = sns.countplot(data=data)
        elif chart_type == 'line':
            chart = sns.lineplot(data=data)
        elif chart_type == 'heatmap':
            pivot_table = pd.pivot_table(data, values='rating', index=['date'], columns=['variant'], aggfunc=np.mean)
            chart = sns.heatmap(pivot_table, cmap="YlGnBu")
        elif chart_type == 'scatter':
            data['date'] = pd.to_datetime(data['date'],format='mixed').dt.strftime('%m/%d')
            plt.xticks(rotation=90)
            chart = sns.scatterplot(data=data, x='date', y='rating')

        elif chart_type == 'wordcloud':
            data = data['content'].str.lower()
            text = ' '.join(data.values.astype(str))
            wc = wordcloud.WordCloud(width=800, height=800, background_color='white').generate(text)
            chart = plt.imshow(wc, interpolation='bilinear')

        elif chart_type == 'network':
            # Create network diagram
            data = data['content'].str.lower()
            text = ' '.join(data.values.astype(str))
            text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
            words = text.split()
            word_pairs = list(zip(words, words[1:]))
            word_graph = nx.Graph()
            word_graph.add_edges_from(word_pairs)
            chart = nx.draw(word_graph, with_labels=True)
    except:
        return None
    
    plt.title(title)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

pie_chart = generate_chart(data['rating'], 'Rating Distribution Pie chart', 'pie')

# Generate charts for top positive reviews
top_pos = data[data['rating'] >= 4]

bar_chart = generate_chart(top_pos['rating'], 'Top Positive Reviews - Rating Count', 'bar')
line_chart = generate_chart(top_pos, 'Top Positive Reviews - Rating over Time', 'line')
heatmap = generate_chart(top_pos, 'Top Positive Reviews - Rating Heatmap', 'heatmap')
scatter_plot = generate_chart(top_pos, 'Top Positive Reviews - Rating over Time', 'scatter')
wordcloud_chart = generate_chart(top_pos, 'Top Positive Reviews - Wordcloud', 'wordcloud')
network_chart = generate_chart(top_pos, 'Top Positive Reviews - Network Diagram', 'network')



# Generate charts for top negative reviews
top_neg = data[data['rating'] <=2]
# pie_chart_neg = generate_chart(top_neg['rating'], 'Top Negative Reviews - Rating Distribution', 'pie')
# bar_chart_neg = generate_chart(top_neg['rating'], 'Top Negative Reviews - Rating Count', 'bar')
line_chart_neg = generate_chart(top_neg, 'Top Negative Reviews - Rating over Time', 'line')
heatmap_neg = generate_chart(top_neg, 'Top Negative Reviews - Rating Heatmap', 'heatmap')
scatter_plot_neg = generate_chart(top_neg, 'Top Negative Reviews - Rating over Time', 'scatter')
wordcloud_chart_neg = generate_chart(top_neg, 'Top Negative Reviews - Wordcloud', 'wordcloud')
network_chart_neg = generate_chart(top_neg, 'Top Negative Reviews - Network Diagram', 'network')

# Generate charts for top neutral reviews
top_neu = data[data['rating'] == 3]
# pie_chart_neu = generate_chart(top_neu['rating'], 'Top Neutral Reviews - Rating Distribution', 'pie')
bar_chart_neu = generate_chart(top_neu['rating'], 'Top Neutral Reviews - Rating Count', 'bar')
line_chart_neu = generate_chart(top_neu, 'Top Neutral Reviews - Rating over Time', 'line')
heatmap_neu = generate_chart(top_neu, 'Top Neutral Reviews - Rating Heatmap', 'heatmap')
scatter_plot_neu = generate_chart(top_neu, 'Top Neutral Reviews - Rating over Time', 'scatter')
wordcloud_chart_neu = generate_chart(top_neu, 'Top Neutral Reviews - Wordcloud', 'wordcloud')
network_chart_neu = generate_chart(top_neu, 'Top Neutral Reviews - Network Diagram', 'network')




# Initialize PDF document
pdf = FPDF()
pdf.add_page()


def write_to_image_and_pdf(name,chart,x,y,w,h):
    try:
        chart_image = Image.open(io.BytesIO(chart.getvalue()))
        chart_image = chart_image.convert('RGB')
        chart_image.save(name+'_chart.png')
        pdf.image(name+'_chart.png', x=x, y=y, w=w, h=h)
    except:
        pass




write_to_image_and_pdf('pie',pie_chart, x=10, y=10, w=100, h=100)
write_to_image_and_pdf("bar",bar_chart, x=5, y=120, w=100, h=100)
write_to_image_and_pdf("line",line_chart, x=5, y=235, w=100, h=100)
write_to_image_and_pdf("heatmap",heatmap, x=120, y=5, w=100, h=100)
write_to_image_and_pdf("scatter",scatter_plot, x=120, y=120, w=100, h=100)
write_to_image_and_pdf("wordcloud",wordcloud_chart, x=250, y=250, w=200, h=200)

# write_to_image_and_pdf("pie_neu", pie_chart_neu, x=400, y=10, w=100, h=100)
write_to_image_and_pdf("bar_neu", bar_chart_neu, x=400, y=120, w=100, h=100)
write_to_image_and_pdf("line_neu", line_chart_neu, x=400, y=235, w=100, h=100)
write_to_image_and_pdf("heatmap_neu", heatmap_neu, x=520, y=5, w=100, h=100)
write_to_image_and_pdf("scatter_neu", scatter_plot_neu, x=520, y=120, w=100, h=100)
write_to_image_and_pdf("wordcloud_neu", wordcloud_chart_neu, x=650, y=250, w=200, h=200)


# write_to_image_and_pdf("bar_neg", bar_chart_neg, x=5, y=350, w=100, h=100)
write_to_image_and_pdf("line_neg", line_chart_neg, x=5, y=465, w=100, h=100)
write_to_image_and_pdf("heatmap_neg", heatmap_neg, x=120, y=240, w=100, h=100)
write_to_image_and_pdf("scatter_neg", scatter_plot_neg, x=120, y=350, w=100, h=100)
write_to_image_and_pdf("wordcloud_neg", wordcloud_chart_neg, x=250, y=475, w=200, h=200)
write_to_image_and_pdf("network_neg", network_chart_neg, x=50, y=550, w=500, h=500)







pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Top Neutral Category Network Diagram', 0, 1)
# pdf.image(network_chart, x=50, y=50, w=500, h=500)
write_to_image_and_pdf("network",network_chart, x=50, y=50, w=500, h=500)

pdf.output('Sentiment_Report.pdf', 'F')

print('Sentiment report generated successfully!')