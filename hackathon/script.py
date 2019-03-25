from flask import Flask, render_template,request,jsonify
from apiclient.discovery import build
from pymongo import MongoClient
import datetime	
app = Flask(__name__)

@app.route('/index',methods=['POST','GET'])
def login(): 
	if request.method == 'POST': 
		q = request.form["search"] 
		api_key="AIzaSyDpqF5fYVy58DRGUkh1R1WvLWAqpHLqHPY"
		youtube=build('youtube','v3',developerKey=api_key)
		req=youtube.search().list(q=q,part='snippet',type='video',maxResults=10)
		res=req.execute()
		prev=""
		d=dict()
		c=1
		for i in res['items']:
			link=i['id']['videoId']
			d[c]=prev="https://www.youtube.com/watch?v="+link
			c+=1
		return render_template("front.html",dic=d)
		return
@app.route('/validation',methods=['POST','GET'])
def valid():
	if request.method=='POST':
		c=request.form.getlist("link")
		staff_ids=request.form['id']
	client=MongoClient()
	db=client["staff"]
	collections=db["links"]
	yt={}
	yt['staff_id']=staff_ids
	yt["youtube_links"]=c
	day=datetime.date.today()
	yt['date']=str(day.day)+"-"+str(day.month)+"-"+str(day.year)

	if(collections.insert(yt)):	
		details=""
		data=collections.find()
		#for i in data:
			#print(i)
		return "inserted"
	else:
		return "not inserted"
	
@app.route('/books',methods=['POST','GET'])
def books():
	return jsonify(request.get_json(force=True))
if __name__ == '__main__':
    app.run(debug=True)