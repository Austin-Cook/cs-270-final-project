import time
from src.data_collection.TrackLoader import TrackLoader
from src.data_collection.TrackCombiner import TrackCombiner
from src.data_processing.CommonGenreWords import CommonGenreWords
from src.data_processing.LyricToMetricConverter import LyricToMetricConverter


# for playlist in range(12, 15):
#   print("Playlist #" + str(playlist))
#   for track in range(0, 100):
#     time.sleep(0.55)
#     try:
#       TrackLoader.load_christian_track(playlist, track, useCachedCsv=False)
#     except Exception as e:
#       print(str(track) + ": " + str(e))


CommonGenreWords.save_common_genre_words()
LyricToMetricConverter().convert_lyrics_to_metrics()
