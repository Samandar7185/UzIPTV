"""
Database models for UzIPTV application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()


class Channel(db.Model):
    """Channel model for storing IPTV channels"""
    
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='General')
    logo = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(2), nullable=True)  # ISO country code
    language = db.Column(db.String(10), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to playlist
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=True)
    
    # Metadata
    source = db.Column(db.String(100), nullable=True)  # Source of the channel
    quality = db.Column(db.String(20), nullable=True)  # HD, SD, etc.
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Channel {self.name}>'
    
    def to_dict(self):
        """Convert channel to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'category': self.category,
            'logo': self.logo,
            'country': self.country,
            'language': self.language,
            'is_active': self.is_active,
            'source': self.source,
            'quality': self.quality,
            'description': self.description,
            'playlist_id': self.playlist_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Playlist(db.Model):
    """Playlist model for storing IPTV playlists"""
    
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.Text, nullable=False, unique=True)
    source = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(2), nullable=True)
    language = db.Column(db.String(10), nullable=True)
    channel_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with channels
    channels = db.relationship('Channel', backref='playlist', lazy='dynamic')
    
    def __repr__(self):
        return f'<Playlist {self.name}>'
    
    def to_dict(self):
        """Convert playlist to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'source': self.source,
            'country': self.country,
            'language': self.language,
            'channel_count': self.channel_count,
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Favorite(db.Model):
    """User favorites model"""
    
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(100), nullable=False)  # Session-based user ID
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    channel = db.relationship('Channel', backref='favorites')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_session', 'channel_id'),)
    
    def __repr__(self):
        return f'<Favorite {self.user_session}:{self.channel_id}>'
    
    def to_dict(self):
        """Convert favorite to dictionary"""
        return {
            'id': self.id,
            'user_session': self.user_session,
            'channel_id': self.channel_id,
            'channel': self.channel.to_dict() if self.channel else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SearchHistory(db.Model):
    """Search history model"""
    
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(100), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    results_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SearchHistory {self.query}>'
    
    def to_dict(self):
        """Convert search history to dictionary"""
        return {
            'id': self.id,
            'user_session': self.user_session,
            'query': self.query,
            'results_count': self.results_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ChannelCategory(db.Model):
    """Channel categories model"""
    
    __tablename__ = 'channel_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Icon class or emoji
    color = db.Column(db.String(7), nullable=True)  # Hex color code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChannelCategory {self.name}>'
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


def init_default_categories():
    """Initialize default channel categories"""
    default_categories = [
        {'name': 'General', 'icon': '📺', 'color': '#6c757d'},
        {'name': 'News', 'icon': '📰', 'color': '#dc3545'},
        {'name': 'Sports', 'icon': '⚽', 'color': '#28a745'},
        {'name': 'Movies', 'icon': '🎬', 'color': '#ffc107'},
        {'name': 'Music', 'icon': '🎵', 'color': '#e83e8c'},
        {'name': 'Kids', 'icon': '🧸', 'color': '#20c997'},
        {'name': 'Documentary', 'icon': '🎓', 'color': '#6f42c1'},
        {'name': 'Entertainment', 'icon': '🎭', 'color': '#fd7e14'},
        {'name': 'Religious', 'icon': '🕌', 'color': '#17a2b8'},
        {'name': 'Local', 'icon': '🏠', 'color': '#6c757d'}
    ]
    
    for cat_data in default_categories:
        existing = ChannelCategory.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = ChannelCategory(**cat_data)
            db.session.add(category)
    
    db.session.commit()


def init_database(app):
    """Initialize database with default data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize default categories
        init_default_categories()
        
        print("Database initialized successfully!")


# Utility functions
def get_channels_by_category(category_name):
    """Get all channels in a specific category"""
    return Channel.query.filter_by(category=category_name, is_active=True).all()


def search_channels(query):
    """Search channels by name"""
    return Channel.query.filter(
        Channel.name.ilike(f'%{query}%'),
        Channel.is_active == True
    ).all()


def get_popular_channels(limit=20):
    """Get popular channels (by favorites count)"""
    return db.session.query(Channel)\
        .join(Favorite, Channel.id == Favorite.channel_id)\
        .group_by(Channel.id)\
        .order_by(db.func.count(Favorite.id).desc())\
        .limit(limit)\
        .all()


def get_recent_channels(limit=20):
    """Get recently added channels"""
    return Channel.query\
        .filter_by(is_active=True)\
        .order_by(Channel.created_at.desc())\
        .limit(limit)\
        .all()


def get_categories_with_counts():
    """Get all categories with channel counts"""
    return db.session.query(
        ChannelCategory.name,
        ChannelCategory.icon,
        ChannelCategory.color,
        db.func.count(Channel.id).label('channel_count')
    ).outerjoin(
        Channel, 
        db.and_(Channel.category == ChannelCategory.name, Channel.is_active == True)
    ).group_by(ChannelCategory.id).all()
