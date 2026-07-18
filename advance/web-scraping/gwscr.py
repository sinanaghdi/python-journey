"""
GitHub Trending Repositories Finder
A comprehensive tool to fetch and display trending repositories from GitHub API
"""

import requests
from pprint import pprint
import time
from datetime import datetime
import json
import os


class GitHubTrendingRepositories:
    """
    Main class for fetching trending repositories from GitHub
    """
    
    def __init__(self, token=None):
        """
        Initialize the GitHub API client
        
        Args:
            token (str, optional): GitHub personal access token for higher rate limits
        """
        self.base_url = "https://api.github.com/search/repositories"
        self.repositories = []
        self.api_calls = 0
        self.token = token
        
        # Base headers - important for GitHub to recognize us as a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Add token to headers if provided
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_repositories(self, language, num_repositories, sort_by='stars', print_progress=True):
        """
        Fetch trending repositories based on language and count
        
        Args:
            language (str): Programming language (e.g., 'python', 'javascript')
            num_repositories (int): Number of repositories to fetch
            sort_by (str): Sort criteria ('stars', 'forks', 'updated')
            print_progress (bool): Show progress updates
            
        Returns:
            list: List of repository dictionaries with full information
        """
        # Input validation
        if num_repositories <= 0:
            raise ValueError("Number of repositories must be greater than 0")
        
        if not language or not language.strip():
            raise ValueError("Please enter a valid language")
        
        language = language.strip()
        self.repositories = []
        page = 1
        per_page = min(30, num_repositories)  # Max 30 per page
        
        print(f"\n🚀 Starting search for language '{language}'...")
        print(f"📊 Requested: {num_repositories} repositories")
        print("-" * 60)
        
        while len(self.repositories) < num_repositories:
            # Request parameters
            params = {
                'q': f'language:{language}',
                'sort': sort_by,
                'order': 'desc',
                'page': page,
                'per_page': per_page
            }
            
            try:
                # Send request to GitHub API
                response = requests.get(
                    self.base_url, 
                    headers=self.headers, 
                    params=params,
                    timeout=10
                )
                self.api_calls += 1
                
                # Check response status
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    total_count = data.get('total_count', 0)
                    
                    # No results found
                    if not items:
                        print(f"⚠️ No repositories found for language '{language}'!")
                        break
                    
                    # Process each repository
                    for repo in items:
                        if len(self.repositories) >= num_repositories:
                            break
                        
                        # Extract comprehensive repository information
                        repo_info = self._extract_repo_info(repo)
                        self.repositories.append(repo_info)
                        
                        if print_progress:
                            print(f"✅ {len(self.repositories)}. {repo_info['name']} ⭐ {repo_info['stars']:,}")
                    
                    # Check if we've reached the last page
                    if len(items) < per_page:
                        break
                    
                    # Move to next page
                    page += 1
                    
                    # Small delay to respect GitHub's rate limits
                    time.sleep(0.5)
                    
                elif response.status_code == 403:
                    # Rate limit error
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        reset_timestamp = int(reset_time)
                        wait_time = reset_timestamp - int(time.time())
                        if wait_time > 0:
                            print(f"⏳ Rate limit reached! Waiting {wait_time} seconds...")
                            time.sleep(wait_time + 5)
                            continue
                    
                    print(f"❌ Rate limit exceeded!")
                    print(f"💡 Add a GitHub token to increase limits")
                    break
                    
                elif response.status_code == 404:
                    print(f"❌ Language '{language}' not found!")
                    break
                    
                else:
                    print(f"❌ Server error: {response.status_code}")
                    print(f"Message: {response.text[:200]}")
                    break
                    
            except requests.exceptions.Timeout:
                print("⏰ Request timed out! Retrying...")
                time.sleep(2)
                continue
                
            except requests.exceptions.ConnectionError:
                print("🌐 Connection error! Retrying...")
                time.sleep(3)
                continue
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error: {e}")
                break
                
            except ValueError as e:
                print(f"❌ Data parsing error: {e}")
                break
        
        # Show summary
        self._show_summary(language, num_repositories)
        return self.repositories
    
    def _extract_repo_info(self, repo_data):
        """
        Extract useful information from raw GitHub data
        
        Args:
            repo_data (dict): Raw data from GitHub API
            
        Returns:
            dict: Structured repository information
        """
        return {
            'name': repo_data.get('full_name', 'N/A'),
            'name_short': repo_data.get('name', 'N/A'),
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'watchers': repo_data.get('watchers_count', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'description': repo_data.get('description', 'No description'),
            'url': repo_data.get('html_url', 'N/A'),
            'clone_url': repo_data.get('clone_url', 'N/A'),
            'language': repo_data.get('language', 'Unknown'),
            'created_at': repo_data.get('created_at', 'N/A'),
            'updated_at': repo_data.get('updated_at', 'N/A'),
            'pushed_at': repo_data.get('pushed_at', 'N/A'),
            'homepage': repo_data.get('homepage', ''),
            'license': repo_data.get('license', {}).get('name', 'No license'),
            'owner': {
                'login': repo_data.get('owner', {}).get('login', 'N/A'),
                'avatar': repo_data.get('owner', {}).get('avatar_url', 'N/A'),
                'url': repo_data.get('owner', {}).get('html_url', 'N/A')
            },
            'topics': repo_data.get('topics', []),
            'has_issues': repo_data.get('has_issues', False),
            'has_projects': repo_data.get('has_projects', False),
            'has_wiki': repo_data.get('has_wiki', False),
            'has_downloads': repo_data.get('has_downloads', False),
            'has_pages': repo_data.get('has_pages', False),
            'default_branch': repo_data.get('default_branch', 'main'),
            'size': repo_data.get('size', 0),
            'score': repo_data.get('score', 0)
        }
    
    def _show_summary(self, language, requested_count):
        """
        Display summary of results
        
        Args:
            language (str): Search language
            requested_count (int): Number of requested repositories
        """
        actual_count = len(self.repositories)
        
        print("\n" + "="*70)
        print(f"📊 Summary for '{language}':")
        print("="*70)
        print(f"✅ Retrieved: {actual_count} out of {requested_count} requested")
        print(f"📡 API calls made: {self.api_calls}")
        
        if actual_count < requested_count:
            print(f"⚠️ Note: Only {actual_count} repositories were available")
        
        if self.token:
            print("🔑 Token status: Active ✅")
        else:
            print("🔑 Token status: Inactive (60 requests/hour limit)")
        
        print("="*70)
    
    def save_to_json(self, filename='github_trending.json'):
        """
        Save results to JSON file
        
        Args:
            filename (str): Output filename
            
        Returns:
            bool: Success status
        """
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_repositories': len(self.repositories),
                'repositories': self.repositories
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Data saved to '{filename}'")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False
    
    def load_from_json(self, filename='github_trending.json'):
        """
        Load results from JSON file
        
        Args:
            filename (str): Input filename
            
        Returns:
            bool: Success status
        """
        try:
            if not os.path.exists(filename):
                print(f"❌ File '{filename}' does not exist!")
                return False
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.repositories = data.get('repositories', [])
            print(f"📂 Loaded {len(self.repositories)} repositories from '{filename}'")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def display_repositories(self, max_display=None):
        """
        Display repositories in a beautiful format
        
        Args:
            max_display (int, optional): Maximum number of repositories to display
        """
        if not self.repositories:
            print("❌ No repositories to display!")
            return
        
        display_count = min(max_display or len(self.repositories), len(self.repositories))
        
        print("\n" + "🌟"*35)
        print(f"📚 Top {display_count} repositories:")
        print("🌟"*35)
        
        for i, repo in enumerate(self.repositories[:display_count], 1):
            print(f"\n{i:2d}. 🏠 {repo['name']}")
            print(f"   ⭐ Stars: {repo['stars']:,}")
            print(f"   🍴 Forks: {repo['forks']:,}")
            print(f"   👁️ Watchers: {repo['watchers']:,}")
            
            if repo['description'] and repo['description'] != 'No description':
                desc = repo['description'][:120]
                if len(repo['description']) > 120:
                    desc += "..."
                print(f"   📝 Description: {desc}")
            
            print(f"   🔗 URL: {repo['url']}")
            print(f"   🏷️ Language: {repo['language']}")
            
            if repo['topics']:
                topics = ', '.join(repo['topics'][:5])
                if len(repo['topics']) > 5:
                    topics += f" and {len(repo['topics'])-5} more"
                print(f"   🏷️ Topics: {topics}")
            
            print(f"   👤 Owner: {repo['owner']['login']}")
            
            if repo['license'] != 'No license':
                print(f"   📜 License: {repo['license']}")
            
            # Dates
            if repo['created_at'] != 'N/A':
                created = repo['created_at'].split('T')[0]
                print(f"   📅 Created: {created}")
            
            if repo['updated_at'] != 'N/A':
                updated = repo['updated_at'].split('T')[0]
                print(f"   🔄 Updated: {updated}")
            
            print("   " + "-"*50)
    
    def get_statistics(self):
        """
        Calculate statistics from retrieved repositories
        
        Returns:
            dict: Various statistics
        """
        if not self.repositories:
            return {}
        
        total_stars = sum(repo['stars'] for repo in self.repositories)
        total_forks = sum(repo['forks'] for repo in self.repositories)
        avg_stars = total_stars / len(self.repositories)
        
        # Find best repositories
        top_starred = max(self.repositories, key=lambda x: x['stars'])
        top_forked = max(self.repositories, key=lambda x: x['forks'])
        
        # Language distribution
        languages = {}
        for repo in self.repositories:
            lang = repo['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'total_repos': len(self.repositories),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'avg_stars': round(avg_stars, 2),
            'top_starred': top_starred['name'],
            'top_starred_count': top_starred['stars'],
            'top_forked': top_forked['name'],
            'top_forked_count': top_forked['forks'],
            'languages': languages
        }
    
    def display_statistics(self):
        """
        Display statistics in a beautiful format
        """
        stats = self.get_statistics()
        
        if not stats:
            print("❌ No statistics to display!")
            return
        
        print("\n" + "📊"*30)
        print("📈 Statistics:")
        print("📊"*30)
        print(f"📚 Total repositories: {stats['total_repos']}")
        print(f"⭐ Total stars: {stats['total_stars']:,}")
        print(f"🍴 Total forks: {stats['total_forks']:,}")
        print(f"📊 Average stars: {stats['avg_stars']}")
        print(f"🥇 Most starred: {stats['top_starred']} (⭐ {stats['top_starred_count']:,})")
        print(f"🥇 Most forked: {stats['top_forked']} (🍴 {stats['top_forked_count']:,})")
        
        print("\n🏷️ Language distribution:")
        for lang, count in stats['languages'].items():
            percentage = (count / stats['total_repos']) * 100
            bar = "█" * int(percentage)
            print(f"   {lang}: {count} ({percentage:.1f}%) {bar}")
        
        print("📊"*30)


def main():
    """
    Main function - program entry point
    """
    print("\n" + "🚀"*30)
    print("🌟 GitHub Trending Repositories Finder 🌟")
    print("🚀"*30)
    
    # Get user input
    language = input("\n📝 Programming language (e.g., python, javascript): ").strip()
    
    while True:
        try:
            num_repos = int(input("🔢 Number of repositories (max 1000): "))
            if 0 < num_repos <= 1000:
                break
            else:
                print("❌ Please enter a number between 1 and 1000!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    # Choose sorting method
    print("\n📊 Sort by:")
    print("   1. Stars")
    print("   2. Forks")
    print("   3. Last updated")
    
    sort_choice = input("Choose (1-3): ").strip()
    sort_map = {'1': 'stars', '2': 'forks', '3': 'updated'}
    sort_by = sort_map.get(sort_choice, 'stars')
    
    # Ask for file saving
    save_option = input("\n💾 Save results to JSON file? (y/n): ").strip().lower()
    save_to_file = save_option in ['y', 'yes']
    
    # Ask for GitHub token (optional)
    token = input("\n🔑 Enter GitHub token (optional, press Enter to skip): ").strip()
    if not token:
        token = None
        print("ℹ️ Without token, you have 60 requests per hour limit")
    
    # Create GitHub client instance
    github = GitHubTrendingRepositories(token=token)
    
    # Fetch repositories
    start_time = time.time()
    repositories = github.get_repositories(language, num_repos, sort_by=sort_by)
    elapsed_time = time.time() - start_time
    
    # Display results
    if repositories:
        github.display_repositories()
        github.display_statistics()
        
        print(f"\n⏱️ Execution time: {elapsed_time:.2f} seconds")
        
        # Save to file if requested
        if save_to_file:
            filename = f"github_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            github.save_to_json(filename)
    else:
        print("\n❌ No repositories were retrieved!")
        print("💡 Tips:")
        print("   - Make sure the language name is correct")
        print("   - Check your internet connection")
        print("   - Some languages may have very few repositories")
    
    print("\n" + "🙏"*30)
    print("✨ Program completed successfully! ✨")
    print("🙏"*30 + "\n")


# Run the program when executed directly
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🔄 Please restart the program")