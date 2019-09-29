from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get(
    'MONGODB_URI', 'mongodb://<heroku_155tb7z8.playlister_bot>:<xXHN^EL85P8u2z>@ds143245.mlab.com:43245/heroku_155tb7z8')
client = MongoClient(host=f'{host}?retryWrites=false')
# client = MongoClient()
db = client.get_default_database()
playlists = db.playlists
comments = db.comments
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
        'rating': int(request.form.get('rating')),
        'created_at': datetime.now()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    '''Show a single playlist'''
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)


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
        'videos': request.form.get('videos').split(),
        'rating': int(request.form.get('rating'))
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    '''Delete a single playlist'''
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    # If this is set to a variable that is not used the insert_on does not work
    comments.insert_one(comment)
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))


@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    '''Delete a single comment'''
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
