from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists
app = Flask(__name__)

@app.route('/')
def playlists_index():
    '''Show all the playlist the the user'''
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlist_new():
    '''Show form for creating a new playlist'''
    return render_template('playlists_new.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    '''Submit new playlist from the user'''
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))

if __name__ == '__main__':
    app.run(debug=True)