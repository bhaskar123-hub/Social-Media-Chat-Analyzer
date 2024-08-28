import json
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #ff6f61;">🎉 Welcome to the Chat Analyzer Platform! 🎈</h1>
        <p style="font-size: 20px;">Analyze your chats from WhatsApp, Instagram, and Telegram effortlessly!</p>
        <img src="data:image/jpeg;base64,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" ,alt="Party Balloons" style="width: 300px;">
        </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.title("Social Media Chat Analyzer")

platform = st.sidebar.radio(
    "Select the platform for chat analysis:",
    ("WhatsApp", "Instagram", "Telegram")
)

uploaded_file = st.sidebar.file_uploader(f"Upload your {platform} chat file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    if platform == "WhatsApp":
    
        # WhatsApp chat files are typically in plain text format
        data = bytes_data.decode("utf-8")
        st.write("Processing WhatsApp chat data...")

        df=preprocessor.preprocess(data)

    st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.markdown('<h1 style="color:purple;">Top Statsistics</h1>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.markdown('<h1 style="color:blue;">Monthly Message Timeline</h1>', unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        ax.set_ylabel('Message Count')
        st.pyplot(fig)

        # daily timeline
        st.markdown('<h1 style="color:brown;">Daily Timeline</h1>', unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        ax.set_xlabel('Date')
        ax.set_ylabel('Message Count')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map

        day_colors = plt.cm.Paired(range(7))   
        st.markdown('<h1 style="color:violet;">Activity Map</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        chart_type_day = st.selectbox("Select chart type for Most Busy Day:", ("Bar Chart", "Pie Chart"), key="day_chart")
        chart_type_month = st.selectbox("Select chart type for Most Busy Month:", ("Bar Chart", "Line Chart"), key="month_chart")

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            
            fig, ax = plt.subplots()

            
            if chart_type_day == "Bar Chart":
                ax.bar(busy_day.index, busy_day.values, color='purple')
                ax.set_xlabel('Day of the Week')
                ax.set_ylabel('Message Count')
                ax.set_title('Most Busy Day (Bar Chart)')
                plt.xticks(rotation='vertical')
            elif chart_type_day == "Pie Chart":
                ax.pie(busy_day.values, labels=busy_day.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired(range(len(busy_day))))
                ax.set_title('Most Busy Day (Pie Chart)')
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            
            fig, ax = plt.subplots()
            
            if chart_type_month == "Bar Chart":
                ax.bar(busy_month.index, busy_month.values, color='orange')
                ax.set_xlabel('Month')
                ax.set_ylabel('Message Count')
                ax.set_title('Most Busy Month (Bar Chart)')
                plt.xticks(rotation='vertical')
            elif chart_type_month == "Line Chart":
                ax.plot(busy_month.index, busy_month.values, marker='o', linestyle='-', color='red')
                ax.set_xlabel('Month')
                ax.set_ylabel('Message Count')
                ax.set_title('Most Busy Month (Line Chart)')
                plt.xticks(rotation='vertical')

            st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header("Pie Chart of Most Busy Users")
                fig, ax = plt.subplots()
                ax.pie(x.values, labels=x.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab10(range(len(x))))
                ax.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle
                ax.set_title('User Activity Distribution')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)

        if df_wc:
            fig, ax = plt.subplots()
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')  # Hide the axes
            st.pyplot(fig)


        # Most common words visualization
        most_common_df = helper.most_common_words(selected_user, df)

        # Creating a barh plot
        fig, ax = plt.subplots()
        ax.barh(most_common_df['Word'], most_common_df['Frequency'], color='skyblue')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Word')
        ax.set_title('Most Common Words')

        # Optional: Invert y-axis to have the most frequent word on top
        plt.gca().invert_yaxis()

        # Display the plot in Streamlit
        st.pyplot(fig)



    

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            # Check the first few emojis and their counts for labels and values
            labels = emoji_df['Emoji'].head(10)
            sizes = emoji_df['Count'].head(10)

            # Ensure there's enough data to plot
            if not labels.empty and not sizes.empty:
                ax.pie(sizes, labels=labels, autopct="%0.2f%%", startangle=90)
                ax.set_title('Emoji Distribution')

            st.pyplot(fig)
                

    elif platform == "Instagram":
        # Instagram chat files are usually in JSON format
        data = json.loads(bytes_data.decode("utf-8"))
        st.write("Processing Instagram chat data...")
        # Add your Instagram chat processing logic here

        # Example of displaying chat participants
        for thread in data.get('inbox', []):
            st.write(f"Chat Title: {thread['title']}")
            st.write(f"Participants: {', '.join(thread['participants'])}\n")

    elif platform == "Telegram":
        # Telegram chat files can be in JSON or HTML format
        data_format = st.sidebar.radio("Select the data format:", ("JSON", "HTML"))

        if data_format == "JSON":
            data = json.loads(bytes_data.decode("utf-8"))
            st.write("Processing Telegram chat data in JSON format...")
            # Add your Telegram JSON chat processing logic here

        elif data_format == "HTML":
            data = bytes_data.decode("utf-8")
            st.write("Processing Telegram chat data in HTML format...")
            # Add your Telegram HTML chat processing logic here


    
        

        





