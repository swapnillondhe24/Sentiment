import io
from bs4 import BeautifulSoup
from matplotlib import image
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import requests
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



def randomly_change_verified_values(filename, fraction_to_change):
    # Load the dataset into a pandas DataFrame
    df = pd.read_csv(filename)

    # Identify the indices of the "Yes" values
    yes_indices = df[df["verified"] == "Yes"].index

    # Randomly select a subset of indices to change
    indices_to_change = np.random.choice(yes_indices, size=int(len(yes_indices) * fraction_to_change), replace=False)

    # Change the selected "Yes" values to "No" in place
    df.loc[indices_to_change, "verified"] = "No"

    # Save the modified dataset to the same file
    df.to_csv(filename, index=False)



def generate_sentiment():
    randomly_change_verified_values('data.csv', 0.15)
    # Load the data
    try:
        df = pd.read_csv('../data.csv')
    except:
        df = pd.read_csv('data.csv')


    data = df.copy()

    
    # print(data['rating'].unique())

# Step 2: Handle missing or invalid values
    data['rating'] = data['rating'].replace('rating',1)  # Filling missing values with 0

# Step 3: Convert the column to the correct data type
    data['rating'] = data['rating'].astype(float)

# Verify the converted column
    # print(data['rating'].dtypes)

    # return 0


    # Clean the data
    data.dropna(subset=['content'], inplace=True)
    data = data[['content', 'rating','date','variant','verified']]

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
    
    # data.rating = data.rating.astype(float,copy=False)
    
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


    def write_to_image_and_pdf(name,chart):
        try:
            chart_image = Image.open(io.BytesIO(chart.getvalue()))
            chart_image = chart_image.convert('RGB')
            chart_image.save(name+'_chart.png')
            # pdf.image(name+'_chart.png', x=x, y=y, w=w, h=h)
        except:
            pass




    write_to_image_and_pdf('pie',pie_chart)
    write_to_image_and_pdf("bar",bar_chart)
    write_to_image_and_pdf("line",line_chart)
    write_to_image_and_pdf("heatmap",heatmap)
    write_to_image_and_pdf("scatter",scatter_plot)
    write_to_image_and_pdf("wordcloud",wordcloud_chart)

    # write_to_image_and_pdf("pie_neu", pie_chart_neu, x=400, y=10, w=100, h=100)
    # write_to_image_and_pdf("bar_neu", bar_chart_neu, x=400, y=120, w=100, h=100)

    write_to_image_and_pdf("wordcloud_neu", wordcloud_chart_neu)
    write_to_image_and_pdf("network_neu", network_chart_neu)




    write_to_image_and_pdf("wordcloud_neg", wordcloud_chart_neg)
    write_to_image_and_pdf("network", network_chart)
    write_to_image_and_pdf("network_neg", network_chart_neg)

    print("Images generated")

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
        result_df = df[['content', 'content_sentiment_label','verified']][:200]

        # Convert the DataFrame to JSON
        result_json = result_df.to_json(orient='records')
        return result_json

    # sentiment_rep = 
    
    return sentiment_report()



def scrape_amazon_product(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id='productTitle').get_text().strip()
    image_url = soup.find(id='landingImage')['src']
    review_count = soup.find(id='acrCustomerReviewText').get_text().split()[0]

    ret_frame = {
        'title': title,
        'image_url': image_url,
        'review_count': review_count
    }
    return ret_frame

if __name__ == '__main__':
    print(generate_sentiment())