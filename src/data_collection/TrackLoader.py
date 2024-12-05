import re
import requests
from src.util.FileUtils import FileUtils
from settings import SPOTIFY_SCRAPER_API_KEY


SPOTIFY_SCRAPER_API_KEY = "c85fcaaad1msh9fe205b5e6fe8b3p12fd2bjsnbf29f4ab4ac4"

class TrackLoader:
  @staticmethod
  def load_country_track(i_playlist: int, i_track: int, useCachedCsv: bool = True):
    csv_playlist_filename = 'country/country_playlist_' + str(i_playlist) + '.csv'
    json_track_filename = 'country/' + str(i_playlist) + '/' + str(i_track) + '.json'
    csv_track_filename = 'country/' + str(i_playlist) + '/' + str(i_track) + '.csv'
    
    TrackLoader._load_track(i_track, csv_playlist_filename, json_track_filename,
                               csv_track_filename, useCachedCsv)

  @staticmethod
  def load_pop_track(i_playlist: int, i_track: int, useCachedCsv: bool = True):
    csv_playlist_filename = 'pop/pop_playlist_' + str(i_playlist) + '.csv'
    json_track_filename = 'pop/' + str(i_playlist) + '/' + str(i_track) + '.json'
    csv_track_filename = 'pop/' + str(i_playlist) + '/' + str(i_track) + '.csv'
    
    TrackLoader._load_track(i_track, csv_playlist_filename, json_track_filename,
                               csv_track_filename, useCachedCsv)

  @staticmethod
  def load_christian_track(i_playlist: int, i_track: int, useCachedCsv: bool = True):
    csv_playlist_filename = 'christian/christian_playlist_' + str(i_playlist) + '.csv'
    json_track_filename = 'christian/' + str(i_playlist) + '/' + str(i_track) + '.json'
    csv_track_filename = 'christian/' + str(i_playlist) + '/' + str(i_track) + '.csv'

    TrackLoader._load_track(i_track, csv_playlist_filename, json_track_filename,
                               csv_track_filename, useCachedCsv)

  @staticmethod
  def _load_track(i_track: int, csv_playlist_filename: str, json_track_filename: str,
                  csv_track_filename: str, useCachedCsv: bool):
    csv_playlist_filename = 'files/playlists/' + csv_playlist_filename
    json_track_filename = 'files/tracks/' + json_track_filename
    csv_track_filename = 'files/tracks/' + csv_track_filename
    
    # lookup cached track info under its json playlist
    playlist = FileUtils.load_from_csv(csv_playlist_filename)
    track = playlist[i_track]
    name = track[0]
    first_author = track[1]
    track_id = track[2]
    
    if useCachedCsv:
      # use lyrics from pre-cached csv
      lyrics: str = FileUtils.load_from_csv(csv_track_filename)[0][3]
    else:
      # fetch from API
      lyrics: str = TrackLoader._fetch_lyrics(track_id)

    lyrics: str = TrackLoader._remove_timestamps(lyrics)
      
    FileUtils.save_to_csv([[name, first_author, track_id, lyrics]], csv_track_filename)

  @staticmethod
  def _fetch_lyrics(track_id: str) -> str:
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/lyrics"
    querystring = {"trackId":track_id,"format":"lrc"}
    headers = {
      "x-rapidapi-key": SPOTIFY_SCRAPER_API_KEY,
      "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if not response.ok:
      raise Exception("Error grabbing track with id: " + track_id + ", Message: " + response.text)
    
    return response.text
  
  @staticmethod
  def _remove_timestamps(lyrics: str) -> str:
    res = re.sub(r'\[.*?\]', '', lyrics)
    res = res.rstrip()
    
    return res
  