import os
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_caching import Cache


app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
app.config["MONGO_URI"] = "mongodb://localhost:27017/adverts"
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://{redis_host}:6379/0'.format(redis_host=REDIS_HOST)})

mongo = PyMongo(app)


@app.route("/")
# @cache.cached()
def home():
	adverts = mongo.db.adverts.find()
	return render_template('home.html', adverts=adverts)


@app.route('/<ObjectId:advert_id>', methods=['GET'])
# @cache.cached()
def advert_by_id(advert_id):
	if request.method == 'GET':
			adverts = mongo.db.adverts.find_one_or_404(advert_id)
			return render_template('advert.html', adverts=adverts)


@app.route('/new_advert', methods=['GET', 'POST'])
# @cache.cached()
def new_advert():
	if request.method == 'POST':
		text = request.form['text']
		advert_id = mongo.db.adverts.insert({'text': text})
		new_advert = mongo.db.adverts.find_one({'_id':advert_id})
		result_text = {'text': new_advert['text']}
		return home()
	else:
		return render_template('new_advert.html')


@app.route('/new_tag', methods=['GET', 'POST'])
# @cache.cached()
def new_tag():
	if request.method == 'POST':
		_id = request.form['id']
		if mongo.db.adverts.find_one({'_id':ObjectId(_id)}) == None:
			return 'ID does not exist'
		else:
			tag = request.form['tag']
			tag_id = mongo.db.adverts.update_one({"_id": ObjectId(_id)}, {"$addToSet": {"tags": tag}})
			new_tag = mongo.db.adverts.find_one({'_id':ObjectId(_id)})
			result_tag = {'tags': new_tag['tags']}
			return home()
	else:
		return render_template('new_tag.html')


@app.route('/tag/<ObjectId:advert_id>', methods=['GET'])
# @cache.cached()
def tag_by_id(advert_id):
	if request.method == 'GET':
			adverts = mongo.db.adverts.find_one_or_404(advert_id)
			return render_template('tag.html', adverts=adverts)


@app.route('/new_comment', methods=['GET', 'POST'])
# @cache.cached()
def new_comment():
	if request.method == 'POST':
		_id = request.form['id']
		if mongo.db.adverts.find_one({'_id':ObjectId(_id)}) == None:
			return 'ID does not exist'
		else:
			comment = request.form['comment']
			comment_id = mongo.db.adverts.update_one({"_id": ObjectId(_id)}, {"$push": {"comments": comment}})
			new_comment = mongo.db.adverts.find_one({'_id':ObjectId(_id)})
			result_tag = {'comments': new_comment['comments']}
			return home()
	else:
		return render_template('new_comment.html')


@app.route('/comment/<ObjectId:advert_id>', methods=['GET'])
# @cache.cached()
def comment_by_id(advert_id):
	if request.method == 'GET':
		adverts = mongo.db.adverts.find_one_or_404(advert_id)
		return render_template('comment.html', adverts=adverts)


@app.route('/stats/<ObjectId:advert_id>', methods=['GET'])
# @cache.cached()
def stats_by_id(advert_id):
	if request.method == 'GET':
		result = mongo.db.adverts.find_one_or_404(advert_id)
		tags = 0 
		comments = 0 
		if 'tags' in result.keys():
			tags =  len(result['tags'])
		if 'comments' in result.keys():
			comments = len(result['comments'])
		return render_template('stat_id.html', advert=result, tags=tags, comments=comments)


if __name__ == '__main__':
	app.run(debug=True)