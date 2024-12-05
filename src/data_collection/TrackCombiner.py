from src.util.FileUtils import FileUtils


class TrackCombiner:
  @staticmethod
  def save_all_tracks_to_single_csv():
    all_tracks = []
    
    genres = ['country', 'pop', 'christian']
    for genre in genres:
      count = 0
      for playlist in range(15):
        for track in range(100):
          track_filename = 'files/tracks/' + str(genre) + '/' + str(playlist) + '/' + str(track) + '.csv'
          
          try:
            track_csv_entry = FileUtils.load_from_csv(track_filename)[0]
            track_csv_entry.append(genre)
            all_tracks.append(track_csv_entry)
            count += 1
          except Exception as e:
            print(genre, " ", str(playlist), ":", str(track))
          if count >= 1400:
            break
        if count >= 1400:
          break
            
    FileUtils.save_to_csv(all_tracks, "files/lyrics.csv")
