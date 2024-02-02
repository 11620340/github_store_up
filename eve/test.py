import pandas
import numpy


df_rating = pandas.read_csv(
    "./datas/movielens-1m/ratings.dat",
    sep="::",
    engine='python',
    names="UserID::MovieID::Rating::Timestamp".split("::")
)


df_users = pandas.read_csv(
    "./datas/movielens-1m/users.dat",
    sep="::",
    engine='python',
    names="UserID::Gender::Age::Occupation::Zip-code".split("::")
)


df_ru = pandas.merge(
    df_rating, df_users, left_on="UserID", right_on="UserID", how="inner"
)




print(df_ru.head())