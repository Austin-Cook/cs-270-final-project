

import requests
from src.util.FileUtils import FileUtils
from settings import SPOTIFY_SCRAPER_API_KEY


class PlaylistLoader:
  country_playlist_ids = [
    "2TVjvI4Si2ghhzeAjDlM9k", # 1-100
    "6jcrEcIOIO8kD4WpbQNU2b",
    "0eMxmvdsywn2c5NI1auEUV",
    "4TgLTV3zqCdBNP9Ulkr2nS",
    "7oykcC9nCol2quLqRnpBaY",
    "2nfS7RIJKPz8EuNUIy5QDu", # 501-600
    "2KSq2Lxg1VR84kY12AVtsT",
    "5n95KbD1BmqtLinu1Z99BL",
    "0CNnuqHZhsNJxcCPQ1LQLN",
    "4lfzL4Uhc9Jm3il25Z548R",
    "6W3kgcYALQ4VlToHWJRhCj", # 1001-1100
    "1CvY9VFbLhWx6b6qxqROwv",
    "5FFMyeMsBLKnovH3Y2MfdO",
    "4m5MClEkoKpQ8S8K49RQpt",
    "0MToMEO171ZW55sLdKAi6i"
  ]
  
  pop_playlist_ids = [
    "5gPVWv9LxergE1yQa44ZV8", # 1-100
    "25rPiDcuMudu8T5KmGv4d4",
    "4KlHPh7H1WfAcmuiLRllg0",
    "5iWuZpyUgVBbKSjvTK1jKN",
    "4fCUzMh3wqLFjIPefJZAt6",
    "7u6T5sGK2wvVtuIOmiSWRU", # 501-600
    "0erBiFhDFTahqHnsgMOSXn",
    "2xlGNQ6WmddgcXBI4TwQpK",
    "3qO3OTKSvatCgrBOoyuica",
    "1HkAQGAooErPg1qobJRbzr",
    "3RBGnt7heetouJAj3awAXH", # 1001-1100
    "7xZdwtDObNbooAQMrGyHa9",
    "5fw6oX2X62x2xBHAPPki37",
    "6dFFMgJjkxbe1rFJ990muo",
    "5sZV7OmLXCuev9AVZxjFmw"
  ]
  
  christian_playlist_ids = [
    "2RC0XiToPmlpBL7zbsM8QH", # 1-100
    "4vJ5CHMpFABTLzVRuo8Uj4",
    "4Plb6DqPqUMTM5ZLnxFdXp",
    "15PjPxtELFN5v3lofnOw33",
    "2Qmnkzhil0eM8dmM8VIN3V",
    "4brLjCcTBSDIdqMGPdw7tj", # 501-600
    "3ijRVoJcMfwnEQYfbHUi0D",
    "5D3QerLwc0OgcvjrSDBd29",
    "4aoC5yPrzHeg4wCbjxf3po",
    "25N2p3AR0Dp7na2lhAoHif",
    "4xwZefC9evzLYIbDSoc4hM", # 1001-1100
    "1Q9BMylpY00HPWm766rZ5s",
    "1uXrCnh0eTDQG8xcTCU4SR",
    "3ADWAjalAVHELPfrS8XIrt",
    "4wm7DuIJo51AWgZvGmHwag"
  ]
  
  @staticmethod
  def load_country_playlist(index: int, useCachedJson: bool = True):
    playlist_id = PlaylistLoader.country_playlist_ids[index]
    json_filename = 'country/country_playlist_' + str(index) + '.json'
    csv_filename = 'country/country_playlist_' + str(index) + '.csv'
    
    PlaylistLoader._load_playlist(playlist_id, json_filename, csv_filename, useCachedJson)

  @staticmethod
  def load_pop_playlist(index: int, useCachedJson: bool = True):
    playlist_id = PlaylistLoader.pop_playlist_ids[index]
    json_filename = 'pop/pop_playlist_' + str(index) + '.json'
    csv_filename = 'pop/pop_playlist_' + str(index) + '.csv'
    
    PlaylistLoader._load_playlist(playlist_id, json_filename, csv_filename, useCachedJson)
    
  @staticmethod
  def load_christian_playlist(index: int, useCachedJson: bool = True):
    playlist_id = PlaylistLoader.christian_playlist_ids[index]
    json_filename = 'christian/christian_playlist_' + str(index) + '.json'
    csv_filename = 'christian/christian_playlist_' + str(index) + '.csv'
    
    PlaylistLoader._load_playlist(playlist_id, json_filename, csv_filename, useCachedJson)
    
  @staticmethod
  def _load_playlist(playlist_id: str, json_filename: str, csv_filename: str, useCachedJson: bool):
    json_filename = 'files/playlists/' + json_filename
    csv_filename = 'files/playlists/' + csv_filename
    
    if useCachedJson:
      # load pre-fetched json
      playlist = FileUtils.load_from_json(json_filename)
    else:
      # fetch json from API 
      playlist = PlaylistLoader._fetch_playlist(playlist_id)
      FileUtils.save_to_json(playlist, json_filename)
    songs = PlaylistLoader._extract_tracks(playlist)
    FileUtils.save_to_csv(songs, csv_filename)

  @staticmethod
  def _fetch_playlist(playlist_id: str) -> dict:
    url = "https://spotify-scraper.p.rapidapi.com/v1/playlist/contents"
    querystring = {"playlistId": playlist_id}
    headers = {
      "x-rapidapi-key": SPOTIFY_SCRAPER_API_KEY,
      "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if not response.ok:
      raise Exception("Error grabbing playlist with id: " + playlist_id + ", Message: " +
                      response.text)

    return response.json()

  @staticmethod
  def _extract_tracks(playlist: dict) -> list:
    '''[[name, id],...]'''
    # create csv: name, id
    tracks = []
    items = playlist['contents']['items']
    for item in items:
      name = item['name']
      track_id = item['id']
      first_author_name = item['artists'][0]['name']
      tracks.append([name, first_author_name, track_id])

    return tracks
