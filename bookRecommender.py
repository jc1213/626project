import pandas as pd
from math import *


books = pd.read_csv("BX-Books.csv", encoding='cp1252', sep=';', error_bad_lines=False)
# ISBN	bookTitle	bookAuthor	yearOfPublication	publisher
ratings = pd.read_csv("BX-Book-Ratings.csv", encoding='cp1252', sep=';', error_bad_lines=False)
# userID	ISBN	bookRating
data = pd.merge(books, ratings, on='ISBN')
# print(data)
data[['User-ID', 'Book-Rating', 'ISBN', 'Book-Title']].sort_values('User-ID').to_csv('data.csv', index=False)


file = open("data.csv", 'r', encoding='cp1252')
data = {}  # contains the book and rating from every user
for line in file.readlines():
    line = line.strip().split(',')
    # If there is no user in the dictionary, the user-ID is used to create that user
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # Otherwise add the dictionary with the user-ID as the key
    else:
        data[line[0]][line[3]] = line[1]


def Euclidean(user1, user2):
    # Pull out books and ratings reviewed by two users
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    # Find books that both users have reviewed and calculate the Euclidean distance
    for key in user1_data.keys():
        if key in user2_data.keys():
            # Note that the greater the distance, the more similar the two are
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))  # The smaller the return value, the greater the similarity


# Calculates the similarity
def top10_simliar(userID):
    res = []
    for userid in data.keys():
        # Exclude similarity calculation with yourself
        if not userid == userID:
            simliar = Euclidean(userID, userid)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]


def recommend(user):
    # Users with the highest similarity
    top_sim_user = top10_simliar(user)[0][0]
    # Book viewing records of users with the highest similarity
    items = data[top_sim_user]
    recommendations = []
    # Screen out books that the user has not read and add them to the list
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # Sort by rating
    # Returns the top 3 movies
    return recommendations[:3]


# RES = top10_simliar('8')
# print(RES)
Recommendations = recommend('16')
print(Recommendations)

