import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

import preprocessor,helper
df= preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")

user_menu=st.sidebar.radio("select an option",("medal tally","overall analysis","country-wise-analysis","athlete-wise-analysis"))

if user_menu=="medal tally":
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country=="overall" and selected_year=="overall":
        st.title("Overall Medal Tally ")
    if selected_country!="overall " and selected_year=="overall":
        st.title("Medal Tally of "+selected_country)
    if selected_country=="overall" and selected_year!="overall":
        st.title("Medal Tally in "+str(selected_year))  
    if selected_country!="overall" and selected_year!="overall":
        st.title("Medal Tally of "+selected_country+"in"+str(selected_year))
    #st.dataframe(medal_tally)
    st.table(medal_tally)

if user_menu=="overall analysis":
    editions=df["Year"].nunique()-1
    cities=df["City"].nunique()
    sports=df["Sport"].nunique()
    events=df["Event"].nunique()
    players=df["Name"].nunique()
    countries=df["region"].nunique()
    st.title("Overall Stats")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.header("Editions")
        st.title(editions)
    with c2:
        st.header("Hosts")
        st.title(cities)
    with c3:
        st.header("Sports")
        st.title(sports)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.header("Events")
        st.title(events)
    with c2:
        st.header("Athletes")
        st.title(players)
    with c3:
        st.header("Nations")
        st.title(countries)

    a=helper.n_country_year(df,"region")
    fig=px.line(a,x="Edition",y="region")
    st.title("Participating Nations Per Year")
    st.plotly_chart(fig)

    a=helper.n_country_year(df,"Event")
    fig=px.line(a,x="Edition",y="Event")
    st.title("Events per Year")
    st.plotly_chart(fig)

    a=helper.n_country_year(df,"Name")
    fig=px.line(a,x="Edition",y="Name")
    st.title("Number of participating Athletes over time")
    st.plotly_chart(fig)

    x=df.drop_duplicates(["Year","Event","Sport"])
    fig,ax=plt.subplots(figsize=(20,20))
    st.title("Number of events per Sport Over Time")
    ax=sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes:")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport:',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'country-wise-analysis':

    st.sidebar.title('country-wise-analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " : Medals per Sports over Time")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'athlete-wise-analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)