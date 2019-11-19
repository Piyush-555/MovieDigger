import pandas as pd
from scipy import sparse
ratings = pd.read_csv('dataset/ratings.csv')
movies = pd.read_csv('dataset/movies.csv')
ratings = pd.merge(movies,ratings).drop(['timestamp'],axis=1)


userRatings = ratings.pivot_table(index=['userId'],columns=['movieId'],values='rating')
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
corrMatrix = userRatings.corr(method='pearson')


def get_similar(movieId,rating):
	similar_ratings = corrMatrix[movieId]*(rating-2.5)
	similar_ratings = similar_ratings.sort_values(ascending=False)
	return similar_ratings   

def get_recommendations(movie_list):
	similar_movies = pd.DataFrame()
	
	ids=[]
	for Id,rating in movie_list:
		similar_movies = similar_movies.append(get_similar(Id,rating),ignore_index = True)
		ids.append(Id)
		
	

	similar_movies=similar_movies.sum().sort_values(ascending=False)[0:20]
	sim=pd.DataFrame(similar_movies)
	sim.movie=sim.index
	sim.reset_index(level=0, inplace=True)
	sim=sim["index"]
	sim=set(sim.tolist())
	sim=sim-set(ids)

	

	return list(sim)


def get_popular(num_movies, genre=None):
	f=pd.read_csv("dataset/popularity.csv")
	ids=[]
	if genre:
		f=f[f["genres"].str.contains(genre)].reset_index()

	else:
		f=f.reset_index()
	f=f.ix[0:num_movies,"movieId"]
	ids=f.tolist()
	return ids

if __name__=="__main__":
	def get_popularity_csv():
		userRatings2=ratings.drop("userId",axis=1)
		userRatings2=userRatings2.groupby(['movieId','genres']).sum().reset_index()
		userRatings2=userRatings2.sort_values('rating',ascending=False)
		userRatings2=userRatings2.drop(["rating"],axis=1)
		userRatings2.to_csv("dataset/popularity.csv")

	get_popularity_csv()

