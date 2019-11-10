
import pandas as pd
from scipy import sparse
ratings = pd.read_csv('dataset/ratings.csv')
movies = pd.read_csv('dataset/movies.csv')
ratings = pd.merge(movies,ratings).drop(['timestamp'],axis=1)


userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
corrMatrix = userRatings.corr(method='pearson')

def get_popularity_csv():
	userRatings2=ratings.drop("userId",axis=1)
	userRatings2=userRatings2.groupby(['movieId','genres']).sum().reset_index()
	userRatings2=userRatings2.sort_values('rating',ascending=False)
	userRatings2=userRatings2.drop(["rating"],axis=1)
	userRatings2.to_csv("dataset/popularity.csv")

get_popularity_csv()
	
def get_similar(movieId,rating):
	similar_ratings = corrMatrix[movieId]*(rating-2.5)
	similar_ratings = similar_ratings.sort_values(ascending=False)
	return similar_ratings   

def get_recommendations(movie_list):
	similar_movies = pd.DataFrame()
	for Id,rating in movie_list:
		movie=ratings.loc[ratings.movieId==Id,"title"]
		movie=movie.iloc[0]
		similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

	similar_movies=similar_movies.sum().sort_values(ascending=False)[0:10]
	sim=pd.DataFrame(similar_movies)
	
	sim.movie=sim.index
	sim.reset_index(level=0, inplace=True)
	sim=sim["index"]
	ids=[]
	for movie in sim:
		movie=ratings.loc[ratings.title==movie,"movieId"]
		movie=movie.iloc[0]
		ids.append(movie)
	

	return ids

def get_popular(num_movies, genre=None):
	f=pd.read_csv("dataset/popularity.csv")
	ids=[]
	f=f[f["genres"].str.contains(genre)].reset_index()
	f=f.ix[0:num_movies,"movieId"]
	ids=f.tolist()
	ids
	return ids



