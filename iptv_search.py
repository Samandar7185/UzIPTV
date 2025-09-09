"""
IPTV Searcher - Search for IPTV playlists across the internet
"""

import requests
from bs4 import BeautifulSoup
import re
import validators
from urllib.parse import urljoin, urlparse
import time
import random


class IPTVSearcher:
    """Search for IPTV playlists from various sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Common IPTV playlist search sources
        self.search_sources = [
            'https://github.com/search?q={query}+m3u+iptv&type=code',
            'https://raw.githubusercontent.com/search?q={query}+m3u&type=code'
        ]
        
        # Common IPTV playlist hosting patterns
        self.m3u_patterns = [
            r'https?://[^\s<>"]+\.m3u8?[^\s<>"]*',
            r'https?://[^\s<>"]+/[^\s<>"]*\.m3u[^\s<>"]*',
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.m3u[8]?'
        ]
    
    def search(self, query):
        """
        Search for IPTV playlists based on query
        
        Args:
            query (str): Search query (e.g., "uzbekistan", "tv", "sport")
            
        Returns:
            list: List of found playlist URLs with metadata
        """
        results = []
        
        try:
            # Search GitHub for M3U files
            github_results = self._search_github(query)
            results.extend(github_results)
            
            # Search common IPTV aggregator sites
            aggregator_results = self._search_aggregators(query)
            results.extend(aggregator_results)
            
            # Search Pastebin-like services
            paste_results = self._search_paste_sites(query)
            results.extend(paste_results)
            
            # Remove duplicates and validate URLs
            unique_results = self._deduplicate_and_validate(results)
            
            return unique_results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _search_github(self, query):
        """Search GitHub for M3U files"""
        results = []
        
        try:
            search_url = f"https://api.github.com/search/code?q={query}+extension:m3u"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('items', [])[:10]:  # Limit to 10 results
                    raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                    
                    results.append({
                        'url': raw_url,
                        'title': item['name'],
                        'source': 'GitHub',
                        'repository': item['repository']['full_name'],
                        'score': item.get('score', 0)
                    })
            
            # Add small delay to be respectful
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"GitHub search error: {e}")
        
        return results
    
    def _search_aggregators(self, query):
        """Search common IPTV aggregator websites"""
        results = []
        
        # List of known IPTV aggregator sites (add more as needed)
        aggregator_sites = [
            'https://iptv-org.github.io/',
            'https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u'
        ]
        
        try:
            # Search the main IPTV-org playlist
            if 'uzbek' in query.lower() or 'uz' in query.lower():
                results.append({
                    'url': 'https://iptv-org.github.io/iptv/countries/uz.m3u',
                    'title': 'Uzbekistan IPTV Channels',
                    'source': 'IPTV-ORG',
                    'country': 'UZ',
                    'score': 100
                })
            
            # Add global playlist
            results.append({
                'url': 'https://iptv-org.github.io/iptv/index.m3u',
                'title': 'Global IPTV Channels',
                'source': 'IPTV-ORG',
                'country': 'Global',
                'score': 80
            })
            
        except Exception as e:
            print(f"Aggregator search error: {e}")
        
        return results
    
    def _search_paste_sites(self, query):
        """Search paste sites for IPTV playlists"""
        results = []
        
        try:
            # This is a placeholder - in real implementation, you'd search
            # paste sites like Pastebin, GitHub Gists, etc.
            # Note: Be respectful of rate limits and terms of service
            
            # Example search patterns for common paste sites
            paste_patterns = [
                f"site:pastebin.com {query} m3u",
                f"site:gist.github.com {query} iptv",
            ]
            
            # This would require implementing proper web scraping
            # with respect to robots.txt and rate limits
            
        except Exception as e:
            print(f"Paste site search error: {e}")
        
        return results
    
    def _extract_m3u_urls(self, text, base_url=None):
        """Extract M3U URLs from text content"""
        urls = []
        
        for pattern in self.m3u_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # Clean up the URL
                url = match.strip()
                
                # Make relative URLs absolute if base_url provided
                if base_url and not url.startswith(('http://', 'https://')):
                    url = urljoin(base_url, url)
                
                # Validate URL
                if validators.url(url):
                    urls.append(url)
        
        return urls
    
    def _deduplicate_and_validate(self, results):
        """Remove duplicates and validate URLs"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result['url']
            
            if url not in seen_urls:
                seen_urls.add(url)
                
                # Validate URL
                if validators.url(url):
                    # Test if URL is accessible (optional, can be slow)
                    if self._test_url_accessibility(url):
                        unique_results.append(result)
        
        # Sort by score (if available)
        unique_results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return unique_results
    
    def _test_url_accessibility(self, url):
        """Test if URL is accessible (basic check)"""
        try:
            response = requests.head(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return True  # Assume accessible if test fails (to avoid false negatives)
    
    def search_by_country(self, country_code):
        """Search for IPTV playlists by country code"""
        country_queries = {
            'uz': 'uzbekistan iptv',
            'ru': 'russia iptv',
            'us': 'usa america iptv',
            'uk': 'united kingdom iptv',
            'de': 'germany deutschland iptv',
            'fr': 'france iptv',
            'tr': 'turkey türkiye iptv',
            'kz': 'kazakhstan iptv'
        }
        
        query = country_queries.get(country_code.lower(), f'{country_code} iptv')
        return self.search(query)
    
    def get_popular_playlists(self):
        """Get list of popular/reliable IPTV playlists"""
        popular_lists = [
            {
                'url': 'https://iptv-org.github.io/iptv/index.m3u',
                'title': 'IPTV-ORG Global Channels',
                'source': 'IPTV-ORG',
                'description': 'Curated list of publicly available IPTV channels',
                'score': 100
            },
            {
                'url': 'https://iptv-org.github.io/iptv/countries/uz.m3u',
                'title': 'Uzbekistan TV Channels',
                'source': 'IPTV-ORG',
                'description': 'Uzbek television channels',
                'score': 95
            }
        ]
        
        return popular_lists
