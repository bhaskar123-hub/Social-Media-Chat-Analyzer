from turtle import st
from urlextract import URLExtract # type: ignore
from wordcloud import WordCloud # type: ignore
import pandas as pd
from collections import Counter
import emoji # type: ignore
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    # Load additional stop words from a file
    with open('stop_hinglish.txt', 'r') as f:
        additional_stop_words = f.read().splitlines()

    # Combine NLTK stopwords with additional stop words
    stop_words = set(stopwords.words('english')).union(additional_stop_words)

    # Filter the DataFrame for the selected user if needed
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Exclude system notifications and media placeholders using regex
    temp = df[
        (df['user'] != 'group_notification') &
        (~df['message'].str.contains(r'\b(file attached|this edited|media omitted)\b', regex=True, case=False))
    ]

    # Define a function to clean and tokenize text
    def clean_and_tokenize(message):
        # Lowercase and tokenize
        tokens = word_tokenize(message.lower())
        # Filter out stop words and non-alphanumeric tokens
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        return " ".join(filtered_tokens)

    # Clean and tokenize messages
    temp['clean_message'] = temp['message'].apply(clean_and_tokenize)

    # Check if temp['clean_message'] is not empty before generating the word cloud
    if temp['clean_message'].str.strip().empty:
        st.warning("No valid words to generate a word cloud.")
        return None

    # Generate word cloud from the clean messages
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['clean_message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user, df):
    # Load additional stop words from a file
    with open('stop_hinglish.txt', 'r') as f:
        additional_stop_words = f.read().splitlines()

    # Combine NLTK stopwords with additional stop words
    stop_words = set(stopwords.words('english')).union(additional_stop_words)

    # Filter DataFrame for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out unwanted messages
    temp = df[
        (df['user'] != 'group_notification') &
        (~df['message'].str.contains(r'\b(file attached|this message was deleted|media omitted)\b', regex=True, case=False))
    ]

    # Define a function to clean and tokenize text
    def clean_and_tokenize(message):
        # Lowercase and tokenize
        tokens = word_tokenize(message.lower())
        # Filter out non-alphanumeric tokens, stop words, and phone numbers
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words and not re.match(r'\d+', word)]
        return filtered_tokens

    # Collect words from each message
    all_words = [word for message in temp['message'] for word in clean_and_tokenize(message)]

    # Check if any words were collected
    if not all_words:
        return pd.DataFrame(columns=['Word', 'Frequency'])

    # Count the most common words
    most_common_df = pd.DataFrame(Counter(all_words).most_common(20), columns=['Word', 'Frequency'])

    return most_common_df

'''def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df'''


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    # Count the emojis and create a DataFrame
    emoji_count = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_count.items(), columns=['Emoji', 'Count'])

    # Sort the DataFrame by count in descending order
    emoji_df = emoji_df.sort_values(by='Count', ascending=False).reset_index(drop=True)

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Order the days of the week correctly
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return df['day_name'].value_counts().reindex(ordered_days, fill_value=0)

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Map month names to numbers for sorting
    df['month_name'] = pd.to_datetime(df['date']).dt.strftime('%B')
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    return df['month_name'].value_counts().reindex(ordered_months, fill_value=0)



def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap














