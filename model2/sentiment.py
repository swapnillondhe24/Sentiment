import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

# Load the Amazon reviews data into a pandas dataframe
reviews_df = pd.read_csv('../data.csv')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Create a list to hold the sentiment analysis results for each review
results = []

# Loop through each review and perform sentiment analysis on the title, content, and author fields
for index, row in reviews_df.iterrows():
    title_sentiment = sia.polarity_scores(row['title'])
    content_sentiment = sia.polarity_scores(row['content'])
    author_sentiment = sia.polarity_scores(row['author'])
    # print(row['date'])
    date = datetime.strptime(row['date'], '%d %b %Y')
    variant = row['variant']
    images = row['images']
    verified = row['verified']
    author = row['author']
    rating = row['rating']
    product = row['product']
    url = row['url']
    
    # Calculate the overall sentiment score for the review
    overall_sentiment = (title_sentiment['compound'] + content_sentiment['compound'] + author_sentiment['compound']) / 3
    
    # Append the sentiment analysis results to the results list
    results.append({
        'date': date,
        'variant': variant,
        'images': images,
        'verified': verified,
        'author': author,
        'rating': rating,
        'product': product,
        'url': url,
        'title_sentiment': title_sentiment['compound'],
        'content_sentiment': content_sentiment['compound'],
        'author_sentiment': author_sentiment['compound'],
        'overall_sentiment': overall_sentiment
    })

# Convert the results list to a pandas dataframe
results_df = pd.DataFrame(results)

# Generate a pie chart to visualize the distribution of star ratings
rating_counts = results_df['rating'].value_counts()
rating_counts.plot(kind='pie', labels=rating_counts.index.tolist(), autopct='%1.1f%%')
plt.title('Star Rating Distribution')
plt.savefig('rating_pie_chart.png')

# Generate a line chart to visualize the trend of ratings over time
ratings_by_date = results_df.groupby('date')['rating'].mean()
ratings_by_date.plot(kind='line', color='blue')
plt.title('Average Rating Trend')
plt.xlabel('Date')
plt.ylabel('Average Rating')
plt.savefig('rating_line_chart.png')

# Generate a line chart to visualize the trend of sentiment scores over time
sentiment_by_date = results_df.groupby('date')['overall_sentiment'].mean()
sentiment_by_date.plot(kind='line', color='green')
plt.title('Average Sentiment Trend')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.savefig('sentiment_line_chart.png')

# Generate a word cloud to visualize the most common words in positive reviews
positive_reviews = ' '.join(reviews_df[reviews_df['rating'] >= 4]['content'].tolist())
positive_wordcloud = WordCloud(width=800, height=800, background_color='white').generate(positive_reviews)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(positive_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('positive_wordcloud.png')

# Generate a word cloud to visualize the most common words in negative reviews
negative_reviews = ' '.join(reviews_df[reviews_df['rating'] <= 2]['content'].tolist())
negative_wordcloud = WordCloud(width=800, height=800, background_color='white').generate(negative_reviews)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(negative_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('negative_wordcloud.png')


summary = f"""Sentiment Analysis Summary

Number of Reviews: {len(results_df)}
Average Overall Sentiment Score: {results_df['overall_sentiment'].mean():.2f}
Average Title Sentiment Score: {results_df['title_sentiment'].mean():.2f}
Average Content Sentiment Score: {results_df['content_sentiment'].mean():.2f}
Average Author Sentiment Score: {results_df['author_sentiment'].mean():.2f}
"""

print(summary)

# Save the sentiment analysis summary to a text file
print('Saving sentiment analysis summary to sentiment_analysis_summary.txt')