"""
IPTV Parser - Parse M3U/M3U8 playlist files
"""

import requests
import re
from urllib.parse import urljoin, urlparse
import m3u8


class IPTVParser:
    """Parse M3U/M3U8 IPTV playlist files"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse(self, url_or_content):
        """
        Parse M3U playlist from URL or content
        
        Args:
            url_or_content (str): URL to M3U file or M3U content as string
            
        Returns:
            list: List of channel dictionaries
        """
        try:
            # Determine if input is URL or content
            if self._is_url(url_or_content):
                content = self._fetch_content(url_or_content)
                base_url = self._get_base_url(url_or_content)
            else:
                content = url_or_content
                base_url = None
            
            # Parse the M3U content
            channels = self._parse_m3u_content(content, base_url)
            
            return channels
            
        except Exception as e:
            print(f"Parse error: {e}")
            return []
    
    def _is_url(self, text):
        """Check if text is a URL"""
        return text.startswith(('http://', 'https://'))
    
    def _fetch_content(self, url):
        """Fetch content from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Handle encoding
            if response.encoding is None:
                response.encoding = 'utf-8'
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch content from {url}: {e}")
    
    def _get_base_url(self, url):
        """Get base URL for resolving relative URLs"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path.rsplit('/', 1)[0]}/"
    
    def _parse_m3u_content(self, content, base_url=None):
        """Parse M3U content and extract channel information"""
        channels = []
        try:
            # Try using m3u8 library first (for M3U8 format)
            if '#EXTM3U' in content and '#EXT-X-' in content:
                channels = self._parse_m3u8_format(content, base_url)
            else:
                # Parse as standard M3U format
                channels = self._parse_standard_m3u(content, base_url)
            
        except Exception as e:
            print(f"Content parsing error: {e}")
            # Fallback to manual parsing
            channels = self._parse_manual(content, base_url)
        
        return channels
    
    def _parse_m3u8_format(self, content, base_url=None):
        """Parse M3U8 format using m3u8 library"""
        channels = []
        
        try:
            playlist = m3u8.loads(content, uri=base_url)
            
            for segment in playlist.segments:
                if segment.uri:
                    # Extract channel info from segment
                    channel = {
                        'name': self._extract_name_from_uri(segment.uri),
                        'url': self._resolve_url(segment.uri, base_url),
                        'duration': getattr(segment, 'duration', None),
                        'category': 'Live TV'
                    }
                    channels.append(channel)
                    
        except Exception as e:
            print(f"M3U8 parsing error: {e}")
        
        return channels
    
    def _parse_standard_m3u(self, content, base_url=None):
        """Parse standard M3U format"""
        channels = []
        lines = content.strip().split('\n')
        
        current_channel = {}
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith('#EXTM3U'):
                continue
            
            if line.startswith('#EXTINF:'):
                # Parse EXTINF line
                current_channel = self._parse_extinf_line(line)
                
            elif line.startswith('#EXTGRP:'):
                # Parse group/category
                current_channel['category'] = line.replace('#EXTGRP:', '').strip()
                
            elif line.startswith('#EXTVLCOPT:'):
                # Parse VLC options (skip for now)
                continue
                
            elif not line.startswith('#'):
                # This should be the stream URL
                if current_channel:
                    current_channel['url'] = self._resolve_url(line, base_url)
                    
                    # Validate channel has required fields
                    if 'name' not in current_channel:
                        current_channel['name'] = self._extract_name_from_uri(line)
                    
                    if 'category' not in current_channel:
                        current_channel['category'] = 'General'
                    
                    channels.append(current_channel)
                    current_channel = {}
        
        return channels
    
    def _parse_extinf_line(self, line):
        """Parse EXTINF line to extract channel information"""
        channel = {}
        
        # Remove #EXTINF: prefix
        info = line.replace('#EXTINF:', '').strip()
        
        # Extract duration (first part before comma)
        parts = info.split(',', 1)
        if len(parts) >= 2:
            duration_part = parts[0].strip()
            name_part = parts[1].strip()
            
            # Try to extract duration
            try:
                channel['duration'] = float(duration_part)
            except:
                pass
            
            # Extract channel name and other attributes
            channel.update(self._extract_channel_attributes(name_part))
        
        return channel
    
    def _extract_channel_attributes(self, text):
        """Extract channel attributes from EXTINF text"""
        attributes = {}
        
        # Common patterns for channel attributes
        patterns = {
            'logo': r'tvg-logo=["\']([^"\']+)["\']',
            'category': r'group-title=["\']([^"\']+)["\']',
            'id': r'tvg-id=["\']([^"\']+)["\']',
            'name': r'tvg-name=["\']([^"\']+)["\']'
        }
        
        # Extract attributes using regex
        for attr, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                attributes[attr] = match.group(1)
        
        # Extract channel name (usually at the end)
        # Remove attribute patterns to get clean name
        clean_text = re.sub(r'\w+=["\'][^"\']*["\']', '', text).strip()
        if not attributes.get('name') and clean_text:
            attributes['name'] = clean_text
        
        return attributes
    
    def _parse_manual(self, content, base_url=None):
        """Manual parsing fallback"""
        channels = []
        lines = content.strip().split('\n')
        
        current_name = None
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith('#EXTM3U'):
                continue
            
            if line.startswith('#'):
                # Try to extract name from comment
                if 'EXTINF' in line:
                    # Extract name after the last comma
                    if ',' in line:
                        current_name = line.split(',')[-1].strip()
            else:
                # This should be a URL
                if self._is_valid_stream_url(line):
                    channel = {
                        'name': current_name or self._extract_name_from_uri(line),
                        'url': self._resolve_url(line, base_url),
                        'category': 'General'
                    }
                    channels.append(channel)
                    current_name = None
        
        return channels
    
    def _resolve_url(self, url, base_url=None):
        """Resolve relative URLs to absolute URLs"""
        if not url:
            return url
            
        if url.startswith(('http://', 'https://')):
            return url
        
        if base_url:
            return urljoin(base_url, url)
        
        return url
    
    def _extract_name_from_uri(self, uri):
        """Extract a reasonable name from URI"""
        if not uri:
            return 'Unknown Channel'
        
        # Get filename from path
        path = urlparse(uri).path
        filename = path.split('/')[-1]
        
        # Remove extension and clean up
        name = filename.replace('.m3u8', '').replace('.m3u', '').replace('.ts', '')
        name = re.sub(r'[_-]', ' ', name)
        name = re.sub(r'\d+', '', name)  # Remove numbers
        name = name.title().strip()
        
        return name if name else 'Unknown Channel'
    
    def _is_valid_stream_url(self, url):
        """Check if URL looks like a valid stream URL"""
        if not url or url.startswith('#'):
            return False
        
        # Check for common streaming URL patterns
        stream_patterns = [
            r'\.(m3u8?|ts)($|\?)',
            r'://.*:\d+/',  # IP:Port pattern
            r'rtmp://',
            r'rtsp://',
            r'http[s]?://.*\.(tv|stream|live)'
        ]
        
        for pattern in stream_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return True  # Default to True for permissive parsing
    
    def validate_playlist(self, url_or_content):
        """
        Validate if the playlist is properly formatted
        
        Returns:
            dict: Validation result with success status and details
        """
        try:
            channels = self.parse(url_or_content)
            
            if not channels:
                return {
                    'valid': False,
                    'error': 'No channels found in playlist'
                }
            
            # Check for common issues
            issues = []
            working_channels = 0
            
            for channel in channels:
                if not channel.get('name'):
                    issues.append('Some channels have no name')
                
                if not channel.get('url'):
                    issues.append('Some channels have no URL')
                elif self._test_stream_url(channel['url']):
                    working_channels += 1
            
            return {
                'valid': True,
                'total_channels': len(channels),
                'working_channels': working_channels,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def _test_stream_url(self, url):
        """Test if stream URL is accessible (basic check)"""
        try:
            response = requests.head(url, headers=self.headers, timeout=5)
            return response.status_code < 400
        except:
            return False
