from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    return render_template('playlists_new.html', playlist={}, title="New Playlist")

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    '''Submit new playlist from the user'''
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'rating': int(request.form.get('rating'))
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    '''Show a single playlist'''
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    '''Show the edit form for the user to edit a specific playlist'''
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title="Edit Playlist")

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

if __name__ == '__main__':
    app.run(debug=True)