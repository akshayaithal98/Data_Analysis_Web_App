def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    medal_tally["total"]=medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]
    for i in medal_tally.select_dtypes(exclude="object"):
        medal_tally[i]=medal_tally[i].astype("int")
    return medal_tally

def country_year_list(df):
    years=df["Year"].unique().tolist()
    years.sort()
    years.insert(0,"overall")
    country=df["region"].dropna().unique().tolist()
    country.sort()
    country.insert(0,"overall")
    return years,country

def fetch_medal_tally(df,year,country):
    flag=0
    medal_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    if year=="overall" and country=="overall":
        temp_df=medal_df
    if year=="overall" and country!="overall":
        flag=1
        temp_df=medal_df[medal_df["region"]==country]
    if year!="overall" and country=="overall":
        temp_df=medal_df[medal_df["Year"]==int(year)]
    if year!="overall" and country!="overall":
        temp_df=medal_df[(medal_df["Year"]==int(year))&(medal_df["region"]==country)]
    if flag==1:
        x=temp_df.groupby("Year").sum()[["Gold","Silver","Bronze"]].sort_values("Year").reset_index()
    else:
        x=temp_df.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    x["total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    for i in x.select_dtypes(exclude="object"):
        x[i]=x[i].astype("int")
    return x

def n_country_year(df,col):
    a=df.drop_duplicates([col,"Year"])["Year"].value_counts().reset_index().sort_values("index")
    a.rename(columns={'index':'Edition',"Year":col},inplace=True)
    return a


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final