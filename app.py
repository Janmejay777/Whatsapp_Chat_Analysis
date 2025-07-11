import streamlit as st
import preprocessing, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
      bytes_data = uploaded_file.getvalue()
      data = bytes_data.decode("utf-8")
      df = preprocessing.preprocessor(data)

      st.dataframe(df)

      # Fetch Unique Users
      user_list = df['user'].unique().tolist()
      user_list.remove('group_notification')
      user_list.sort()
      user_list.insert(0,"Overall")

      selected_user = st.sidebar.selectbox("Show analyst wrt",user_list)

      if st.sidebar.button("Show Analysis"):

            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.title("Top Statistics")
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
                  st.header("Link Shared")
                  st.title(num_links)

            #Monthly_Timeline
            st.title("Monthly_timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation=90)
            st.pyplot(fig)

            #Daily_Timeline
            st.title("Daily_timeline")
            daily_timeline = helper.daily_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation=90)
            st.pyplot(fig)

            #Activity_map
            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                  st.header("Most Busy Day")
                  busy_day = helper.week_activity_map(selected_user,df)
                  fig, ax = plt.subplots()
                  ax.bar(busy_day.index, busy_day.values)
                  plt.xticks(rotation=90)
                  st.pyplot(fig)

            with col2:
                  st.header("Most Busy Week")
                  busy_month = helper.month_activity_map(selected_user,df)
                  fig, ax = plt.subplots()
                  ax.bar(busy_month.index, busy_month.values, color='Orange')
                  plt.xticks(rotation=90)
                  st.pyplot(fig)

            st.title("Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)



            # finding the busiest users in the group(Group level)
            if selected_user == "Overall":
                  st.title("Most Busy Users")
                  x,new_df = helper.most_busy_users(df)
                  fig, ax = plt.subplots()

                  col1, col2 = st.columns(2)

                  with col1:
                      ax.bar(x.index,x.values,color='blue')
                      plt.xticks(rotation=90)
                      st.pyplot(fig)
                  with col2:
                        st.dataframe(new_df)

            #WordCloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            #Most common words
            most_common_df = helper.most_common_words(selected_user,df)

            fig, ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation=90)

            st.title("Most Common Words")
            st.pyplot(fig)

            #Most_Common_emojis

            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emojis_Analysis")

            col1, col2 = st.columns(2)

            with col1:
               st.dataframe(emoji_df)
            with col2:
                  fig, ax = plt.subplots()
                  ax.pie(emoji_df[1].head(3),labels=emoji_df[0].head(3),autopct='%0.2f%%')
                  st.pyplot(fig)







