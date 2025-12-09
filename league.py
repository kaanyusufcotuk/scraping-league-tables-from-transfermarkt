import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_multiple_seasons():
    # URL and header for the request function
    base_url = f"https://www.transfermarkt.com/laliga/tabelle/wettbewerb/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_seasons_data = []
    
    # Last 10 seasons (2015-2024)
    leagues= ["GB1", "ES1", "L1", "IT1","FR1","BE1","NL1","PO1","TS1", "TR1"]
    seasons = list(range(2000, 2025))
    
    for season in seasons:
        for league in leagues:
            print(f"Scraping season {season}...") # We need to check whether the season is being scraped or not.
            url = base_url + league + "?saison_id=" + str(season)
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'class': 'items'}) # Find league table
                
                if not table:
                    print(f"Table not found for season {season}")
                    continue
                
                # Extract rows
                for row in table.find('tbody').find_all('tr'):
                    columns = row.find_all('td')
                    
                    if len(columns) > 1:
                        team_data = {
                            'season': f"{season}-{season+1}",
                            'league': league,
                            'position': columns[0].get_text(strip=True),
                            'team': columns[2].get_text(strip=True),
                            'matches': columns[3].get_text(strip=True),
                            'wins': columns[4].get_text(strip=True),
                            'draws': columns[5].get_text(strip=True),
                            'losses': columns[6].get_text(strip=True),
                            'goals scored': columns[7].get_text(strip=True).split(":")[0],
                            'goals conceided': columns[7].get_text(strip=True).split(":")[1],
                            'goal_difference': columns[8].get_text(strip=True),
                            'points': columns[9].get_text(strip=True)
                        }
                        all_seasons_data.append(team_data)
                
                # Be respectful - add delay between requests
                time.sleep(2)
                
            except requests.RequestException as e:
                print(f"Error fetching season {season}: {e}")
                continue
        
    return pd.DataFrame(all_seasons_data)

# Usage
df = scrape_multiple_seasons()
if df is not None:
    print(f"Scraped {len(df)} records across multiple seasons")
    print(df.head())
    df.to_csv('last_24_seasons.csv', index=False)