from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
import tweepy,json
from py2neo import Graph,Node,Relationship,watch
graph=Graph()

def home(request):
	return render_to_response('tweep/base.html')

def search(request):
    if 'q' in request.GET:

		#Consumer Keys and access tokens, used for OAuth
		consumer_key = 'WDpZcbcXK6C4RASBaWPn2EsRM'
		consumer_secret = 'p2PIw953cXOhfhjeADZUdLeaPnqwlb0DoiEv5ylmSvUqv67lWr'
		access_token = '2911455882-iJf4Hs056YOAQc2P5u8aE3bAySFFW67n5SXKb6d'
		access_token_secret = '3R1mtgGpMpg13QxVuFfIxoPgpSkVODtVjTQLWSVYt82IL'

		# OAuth process, using the keys and tokens
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		# Creation of the actual interface, using authentication
		api = tweepy.API(auth)

		# Creates the user object. The me() method returns the user whose authentication keys were used.
		user = api.get_user(request.GET['q'])

		user_name=str(request.GET['q'])
		
		max_follow=graph.cypher.execute("MATCH (n)-[r:"+user_name+"tweets]->(x) WITH n, count(r) as tweet WITH max(tweet) as maxi MATCH (n)-[r:"+user_name+"tweets]->(x) With n,count(r) as counted,maxi where counted=maxi return n.name,n.id,n.statuses_count")

		i=0
		min_tweet=0
		user_list=[]
		url_list=[]
		#Get min number of tweets
		for user_id in max_follow:
			aux=int(user_id[2])
			if(i==0):
				min_tweet=aux
				i=i+1
			if(aux<min_tweet):
				min_tweet=aux

		# Get User with min number of tweets
		for user_id in max_follow:
			if(int(user_id[2])==min_tweet):
				user_list.append(user_id[0])
				user = api.get_user(user_id[1])
				url_list.append(user.profile_image_url_https)
		zipped=zip(user_list,url_list)
		context = {"name": zipped}

		return render(request, 'tweep/iterate.html', context)