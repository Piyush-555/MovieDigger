
def pre_process():
	ratings = pd.read_csv('dataset/ratings.csv')
	movies = pd.read_csv('dataset/movies.csv')
	ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)


	userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
	userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
	corrMatrix = userRatings.corr(method='pearson')
	return corrMatrix,ratings

def get_similar(movieId,rating,corrMatrix):
	similar_ratings = corrMatrix[movieId]*(rating-2.5)
	similar_ratings = similar_ratings.sort_values(ascending=False)
	return similar_ratings   

def get_recommendations(action_lover):
	import pandas as pd

	from scipy import sparse
	print(action_lover)
	corrMatrix,ratings=pre_process()
	print(corrMatrix.head())
	print(ratings.head())

	similar_movies = pd.DataFrame()
	for Id,rating in action_lover:
		movie=ratings.loc[ratings.movieId==Id,"title"]
		movie=movie.iloc[0]
		similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

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
	




