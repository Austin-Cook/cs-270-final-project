import string
from src.util.FileUtils import FileUtils

class LyricToMetricConverter:
  def __init__(self):
    self.profanity_words = None
    self.punctuation = None
  
  def convert_lyrics_to_metrics(self):
    # name, first_author, track_id, lyrics, word_count, avg_line_len, word_variety, profanity_freq , country_typ_words, pop_typ_words, christian_typ_words, country_exc_words, pop_exc_words, christian_exc_words, genre
    metrics = [['name', 'first_author', 'track_id', 'lyrics', 'word_count', 'avg_line_len', 'word_variety', 'profanity_freq', 'country_typ_words', 'pop_typ_words', 'christian_typ_words', 'genre']]
    
    tracks = FileUtils.load_from_csv('files/lyrics.csv')

    def path(filename: str):
      return 'files/common_genre_words/' + filename + '.txt'
    country_typical_words = FileUtils.load_from_text(path('country_typical_words'))
    pop_typical_words = FileUtils.load_from_text(path('pop_typical_words'))
    christian_typical_words = FileUtils.load_from_text(path('christian_typical_words'))
    
    for track in tracks:
      name = track[0]
      first_author = track[1]
      track_id = track[2]
      lyrics = track[3]
      genre = track[4]
      word_count = self.word_count(lyrics)
      avg_line_len = self.avg_line_len(lyrics)
      word_variety = self.word_variety(lyrics)
      profanity_freq = self.profanity_freq(lyrics)
      country_typ_words = self.freq(country_typical_words, lyrics, word_count)
      pop_typ_words = self.freq(pop_typical_words, lyrics, word_count)
      christian_typ_words = self.freq(christian_typical_words, lyrics, word_count)
      
      metrics.append([name, first_author, track_id, lyrics, word_count, str(avg_line_len), str(word_variety), str(profanity_freq), str(country_typ_words), str(pop_typ_words), str(christian_typ_words), genre])
    
    FileUtils.save_to_csv(metrics, 'files/music_genre_classification.csv')

  def word_count(self, lyrics: str):
    return len(self.get_words(lyrics))
  
  def avg_line_len(self, lyrics: str):
    lines = lyrics.split('\n')
    
    total_chars = 0
    for line in lines:
      total_chars += len(line)

    return total_chars / len(lines)
  
  def word_variety(self, lyrics: str):
    unique_words = len(set(self.get_words(lyrics)))
    total_words = self.word_count(lyrics)

    return unique_words / total_words
  
  def profanity_freq(self, lyrics: str):
    if not self.profanity_words:
      # from https://www.cs.cmu.edu/~biglou/resources/bad-words.txt
      self.profanity_words = set(FileUtils.load_from_text("files/profanity_words.txt"))
      
    count = 0
    for word in self.get_words(lyrics):
      if word in self.profanity_words:
        count += 1
  
    total_words = self.word_count(lyrics)
    
    return count / total_words
    
  def freq(self, match_words: list, lyrics: str, word_count: int):
    count = 0
    match_words = set(match_words)
    for word in self.get_words(lyrics):
      if word in match_words:
        count += 1
    
    return count / word_count
  
  def get_words(self, lyrics: str) -> list:
    if not self.punctuation:
      self.punctuation = string.punctuation

    return [word.strip(self.punctuation) for word in lyrics.lower().split()]
