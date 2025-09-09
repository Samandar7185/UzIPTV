"""
UzIPTV - IPTV Playlist Search and Player Platform
Main application entry point
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from iptv_search import IPTVSearcher
from iptv_parser import IPTVParser
from database import db, Channel, Playlist, Favorite

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uziptv-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///../uziptv.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
db.init_app(app)

# Content Security Policy
@app.after_request
def after_request(response):
    # Set CSP header to allow inline scripts and eval for development
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https: http:; "
        "media-src 'self' https: http: blob:; "
        "connect-src 'self' https: http:; "
        "font-src 'self' https://cdnjs.cloudflare.com;"
    )
    return response

# Initialize components
searcher = IPTVSearcher()
parser = IPTVParser()


@app.route('/')
def home():
    """Main page - IPTV search interface"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_playlists():
    """Search for IPTV playlists"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search for IPTV playlists
        results = searcher.search(query)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/parse', methods=['POST'])
def parse_playlist():
    """Parse M3U playlist"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'Playlist URL is required'}), 400
        
        # Parse the playlist
        channels = parser.parse(url)
        
        # Save channels to database
        with app.app_context():
            for channel_data in channels:
                channel = Channel(
                    name=channel_data['name'],
                    url=channel_data['url'],
                    category=channel_data.get('category', 'General'),
                    logo=channel_data.get('logo', '')
                )
                db.session.add(channel)
            
            db.session.commit()
        
        return jsonify({
            'success': True,
            'channels': channels,
            'count': len(channels)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/channels')
def get_channels():
    """Get all channels from database"""
    try:
        channels = Channel.query.all()
        
        channels_data = []
        for channel in channels:
            channels_data.append({
                'id': channel.id,
                'name': channel.name,
                'url': channel.url,
                'category': channel.category,
                'logo': channel.logo
            })
        
        return jsonify({
            'success': True,
            'channels': channels_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/channels/<int:channel_id>')
def get_channel(channel_id):
    """Get specific channel by ID"""
    try:
        channel = Channel.query.get_or_404(channel_id)
        
        channel_data = {
            'id': channel.id,
            'name': channel.name,
            'url': channel.url,
            'category': channel.category,
            'logo': channel.logo
        }
        
        return jsonify({
            'success': True,
            'channel': channel_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/player/<int:channel_id>')
def player(channel_id):
    """Video player page"""
    try:
        channel = Channel.query.get_or_404(channel_id)
        return render_template('player.html', channel=channel)
    
    except Exception as e:
        return f"<h1>Xatolik</h1><p>{str(e)}</p><a href='/'>Bosh sahifa</a>"


@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    """Get all saved playlists"""
    try:
        playlists = Playlist.query.all()
        
        playlists_data = []
        for playlist in playlists:
            playlists_data.append(playlist.to_dict())
        
        return jsonify({
            'success': True,
            'playlists': playlists_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/playlists', methods=['POST'])
def save_playlist():
    """Save a new playlist"""
    try:
        data = request.get_json()
        name = data.get('name', '')
        url = data.get('url', '')
        source = data.get('source', 'Manual')
        country = data.get('country', '')
        
        if not name or not url:
            return jsonify({'error': 'Name and URL are required'}), 400
        
        # Check if playlist already exists
        existing = Playlist.query.filter_by(url=url).first()
        if existing:
            return jsonify({'error': 'Playlist already exists'}), 400
        
        # Create new playlist
        playlist = Playlist(
            name=name,
            url=url,
            source=source,
            country=country
        )
        
        db.session.add(playlist)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'playlist': playlist.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/playlists/<int:playlist_id>/load', methods=['POST'])
def load_playlist(playlist_id):
    """Load channels from a saved playlist"""
    try:
        playlist = Playlist.query.get_or_404(playlist_id)
        
        # Parse the playlist
        channels = parser.parse(playlist.url)
        
        # Save channels to database
        channel_count = 0
        for channel_data in channels:
            # Check if channel already exists
            existing = Channel.query.filter_by(
                url=channel_data['url']
            ).first()
            
            if not existing:
                channel = Channel(
                    name=channel_data['name'],
                    url=channel_data['url'],
                    category=channel_data.get('category', 'General'),
                    logo=channel_data.get('logo', ''),
                    source=playlist.source,
                    playlist_id=playlist.id
                )
                db.session.add(channel)
                channel_count += 1
        
        # Update playlist channel count
        playlist.channel_count = len(channels)
        playlist.last_updated = db.func.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{channel_count} new channels loaded',
            'total_channels': len(channels)
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """Delete a saved playlist"""
    try:
        playlist = Playlist.query.get_or_404(playlist_id)
        
        # Also delete associated channels
        channels = Channel.query.filter_by(playlist_id=playlist_id).all()
        for channel in channels:
            db.session.delete(channel)
        
        db.session.delete(playlist)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Playlist deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Add channel to favorites"""
    try:
        data = request.get_json()
        channel_id = data.get('channel_id')
        user_session = data.get('user_session', 'default')
        
        if not channel_id:
            return jsonify({'error': 'Channel ID is required'}), 400
        
        # Check if already in favorites
        existing = Favorite.query.filter_by(
            user_session=user_session,
            channel_id=channel_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Already in favorites'}), 400
        
        # Add to favorites
        favorite = Favorite(
            user_session=user_session,
            channel_id=channel_id
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to favorites'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get user's favorite channels"""
    try:
        user_session = request.args.get('user_session', 'default')
        
        favorites = Favorite.query.filter_by(user_session=user_session).all()
        
        favorites_data = []
        for favorite in favorites:
            favorites_data.append(favorite.to_dict())
        
        return jsonify({
            'success': True,
            'favorites': favorites_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    
    if os.getenv('RENDER') or os.getenv('HEROKU_APP_NAME'):
        # Production mode for Render/Heroku
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
    else:
        # Development mode
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=port,
            debug=debug_mode
        )
