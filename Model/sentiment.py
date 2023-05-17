import io
from matplotlib import image
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import wordcloud
matplotlib.use('Agg')
import networkx as nx
from fpdf import FPDF
from io import BytesIO
import nltk
from PIL import Image
# nltk.download('stopwords')
from nltk.corpus import stopwords

def generate_sentiment():
    # Load the data
    try:
        df = pd.read_csv('../data.csv')
    except:
        df = pd.read_csv('data.csv')

    data = df.copy()

    # Clean the data
    data.dropna(subset=['content'], inplace=True)
    data = data[['content', 'rating','date','variant']]

    # Define function to generate charts
    def generate_chart(dat, title, chart_type):
        data = dat.copy()
        try:    
            if chart_type == 'pie':
                chart = plt.pie(data.value_counts(), labels=data.value_counts().index, autopct='%1.1f%%')
            elif chart_type == 'bar':
                # chart = sns.countplot(data=data)
                rating_counts = data['rating'].value_counts().sort_index()

                # Set the Seaborn style
                sns.set_style("whitegrid")

                # Create the bar chart using Seaborn
                chart = sns.barplot(x=rating_counts.index, y=rating_counts.values)
            elif chart_type == 'line':
                data = data['date','rating']
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


    bar_chart = generate_chart(data, 'Rating Distribution Bar chart', 'bar')


    pie_chart = generate_chart(data['rating'], 'Rating Distribution Pie chart', 'pie')
    line_chart = generate_chart(data, 'Rating Distribution Line chart', 'line')
    scatter_plot = generate_chart(data, 'Top Reviews - Rating over Time', 'scatter')
    # Generate charts for top positive reviews
    heatmap = generate_chart(data, 'Top Reviews - Rating Heatmap', 'heatmap')
    
    data.iloc[1:]['rating'] = data.iloc[1:]['rating'].astype(float)
    
    top_pos = data[data['rating'] >= 4]
    # bar_chart = generate_chart(top_pos['rating'], 'Top Positive Reviews - Rating Count', 'bar')
    wordcloud_chart = generate_chart(top_pos, 'Top Positive Reviews - Wordcloud', 'wordcloud')
    network_chart = generate_chart(top_pos, 'Top Positive Reviews - Network Diagram', 'network')



    # Generate charts for top negative reviews
    top_neg = data[data['rating'] <=2]

    wordcloud_chart_neg = generate_chart(top_neg, 'Top Negative Reviews - Wordcloud', 'wordcloud')
    network_chart_neg = generate_chart(top_neg, 'Top Negative Reviews - Network Diagram', 'network')

    # Generate charts for top neutral reviews
    top_neu = data[data['rating'] == 3]

    wordcloud_chart_neu = generate_chart(top_neu, 'Top Neutral Reviews - Wordcloud', 'wordcloud')
    network_chart_neu = generate_chart(top_neu, 'Top Neutral Reviews - Network Diagram', 'network')




    # Initialize PDF document


    def write_to_image_and_pdf(name,chart,x,y,w,h):
        try:
            chart_image = Image.open(io.BytesIO(chart.getvalue()))
            chart_image = chart_image.convert('RGB')
            chart_image.save(name+'_chart.png')
            # pdf.image(name+'_chart.png', x=x, y=y, w=w, h=h)
        except:
            pass




    write_to_image_and_pdf('pie',pie_chart, x=10, y=10, w=100, h=100)
    write_to_image_and_pdf("bar",bar_chart, x=5, y=120, w=100, h=100)
    write_to_image_and_pdf("line",line_chart, x=5, y=235, w=100, h=100)
    write_to_image_and_pdf("heatmap",heatmap, x=120, y=5, w=100, h=100)
    write_to_image_and_pdf("scatter",scatter_plot, x=120, y=120, w=100, h=100)
    write_to_image_and_pdf("wordcloud",wordcloud_chart, x=250, y=250, w=200, h=200)

    # write_to_image_and_pdf("pie_neu", pie_chart_neu, x=400, y=10, w=100, h=100)
    # write_to_image_and_pdf("bar_neu", bar_chart_neu, x=400, y=120, w=100, h=100)

    write_to_image_and_pdf("wordcloud_neu", wordcloud_chart_neu, x=650, y=250, w=200, h=200)
    write_to_image_and_pdf("network_neu", network_chart_neu, x=650, y=250, w=200, h=200)




    write_to_image_and_pdf("wordcloud_neg", wordcloud_chart_neg, x=250, y=475, w=200, h=200)
    write_to_image_and_pdf("network_neg", network_chart_neg, x=50, y=550, w=500, h=500)


    from nltk.sentiment import SentimentIntensityAnalyzer

    def sentiment_report():
        df = data.copy()
        # print(df.head())
        sid = SentimentIntensityAnalyzer()
        df['content_sentiment_scores'] = df['content'].apply(lambda x: sid.polarity_scores(x))

    # Extract sentiment labels
        # df['title_sentiment_label'] = df['title_sentiment_scores'].apply(lambda x: 'positive' if x['compound'] > 0.2 else ('negative' if x['compound'] < -0.2 else 'neutral'))
        df['content_sentiment_label'] = df['content_sentiment_scores'].apply(lambda x: 'positive' if x['compound'] > 0.2 else ('negative' if x['compound'] < -0.2 else 'neutral'))

        # Create a new DataFrame with the required columns
        result_df = df[['content', 'content_sentiment_label']]

        # Convert the DataFrame to JSON
        result_json = result_df.to_json(orient='records')
        return result_json

    sentiment_report = sentiment_report()

    print('Sentiment report generated successfully!')
    return sentiment_report


if __name__ == '__main__':
    print(generate_sentiment())