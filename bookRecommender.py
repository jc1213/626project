import pandas as pd
import numpy as np
from math import *

"""
books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="cp1252")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="cp1252")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-Book-ratings.csv', sep=';', error_bad_lines=False, encoding="cp1252")
ratings.columns = ['userID', 'ISBN', 'bookRating']

# Data cleaning

# We do not need image urls for this project, so delete those
books.drop(['imageUrlS', 'imageUrlM', 'imageUrlL'],axis=1,inplace=True)

# Make sure texts are fully displayed
pd.set_option('display.max_colwidth', -1)

# Replace 'nAn' with 'unknown'
books.loc[(books.ISBN == '9627982032'),'bookAuthor'] = 'unknown'
books.loc[(books.ISBN == '193169656X'),'publisher'] = 'unknown'
books.loc[(books.ISBN == '1931696993'),'publisher'] = 'unknown'

# Fix Values that are placed in the wrong columns
books.loc[books.ISBN == '078946697X','bookTitle'] = "DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)"
books.loc[books.ISBN == '078946697X','bookAuthor'] = "Michael Teitelbaum"
books.loc[books.ISBN == '078946697X','yearOfPublication'] = 2000
books.loc[books.ISBN == '078946697X','publisher'] = "DK Publishing Inc"

books.loc[books.ISBN == '0789466953','bookTitle'] = "DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)"
books.loc[books.ISBN == '0789466953','bookAuthor'] = "James Buckley"
books.loc[books.ISBN == '0789466953','yearOfPublication'] = 2000
books.loc[books.ISBN == '0789466953','publisher'] = "DK Publishing Inc"

books.loc[books.ISBN == '2070426769','bookTitle'] = "Peuple du ciel, suivi de 'Les Bergers"
books.loc[books.ISBN == '2070426769','bookAuthor'] = "Jean-Marie Gustave Le ClÃ?Â©zio"
books.loc[books.ISBN == '2070426769','yearOfPublication'] = 2003
books.loc[books.ISBN == '2070426769','publisher'] = "Gallimard"

# Redefine data type for yearOfPublication
books.yearOfPublication = pd.to_numeric(books.yearOfPublication, errors='coerce')

# Dump years that are greater than 2004(dataset publication year) or equal to 0
books.loc[(books.yearOfPublication > 2004) | (books.yearOfPublication == 0),'yearOfPublication'] = np.NAN
# Replace these years with the average
books.yearOfPublication.fillna(round(books.yearOfPublication.mean()), inplace=True)
# Redefine yearOfPublication as int32
books.yearOfPublication = books.yearOfPublication.astype(np.int32)

# User whose age is greater than 90 or less than 5 are not considered
users.loc[(users.Age > 90) | (users.Age < 5), 'Age'] = np.nan
# Replace these ages with the average
users.Age = users.Age.fillna(users.Age.mean())
# Redefine data type as int32
users.Age = users.Age.astype(np.int32)
# To maintain consistency/validity for three datasets, we have to check if there are any new data in [ratings] dataset
ratings_bANDr = ratings[ratings.ISBN.isin(books.ISBN)]
ratings_uANDr = ratings[ratings.userID.isin(users.userID)]
# We will use [books] & [ratings] cross dataset
ratings = ratings_bANDr
books.to_csv("Books.csv", sep='\t')
users.to_csv("Users.csv", sep='\t')
ratings.to_csv("Ratings.csv", sep='\t')

data = pd.merge(books, ratings, on='ISBN')
# print(data) with sorting id
data[['userID', 'bookRating', 'ISBN', 'bookTitle']].sort_values('userID').to_csv('data.csv', index=False)
print(data.head())
print(data.shape)
"""

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
        if not userid == userID and not userid == "userID":
            simliar = Euclidean(userID, userid)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:10]


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



menuOption = '0'
while menuOption != '3':
    print("---------------------Book Recommender System---------------------")
    print("Menu")
    print("1. See the top 10 similar users")
    print("2. Check top three recommendation books")
    print("3. Exit")
    menuOption = input("Please choose from menu options.\n")
    type(menuOption)
    if menuOption == '1':
        while True:
            try:
                userId = input("Please enter the userID.\n")
                RES = top10_simliar(userId)
            except:
                print("User does not exist. Please try again.")
                continue
            else:
                break
        print("User ID" + "         " + "Distance")
        for similarUser in RES:
            print(similarUser)
    elif menuOption == '2':
        while True:
            try:
                userId = input("Please enter the userID.\n")
                Recommendations = recommend(userId)
            except:
                print("User does not exist. Please try again.")
                continue
            else:
                break
        print("Book Title" + "         " + "Rating")
        for book in Recommendations:
            print(book)
    elif menuOption == '3':
        exit()
    else:
        print("Option does not exist. Please choose again.")

