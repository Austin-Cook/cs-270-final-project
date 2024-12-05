from collections import Counter
import string
from nltk.corpus import stopwords
from src.util.FileUtils import FileUtils

custom_stop_words = ['i\'m', 'like', 'yeah', 'got', 'know', 'little', 'get', 'back', 'go', 'one', 'i\'ve', 'oh', 'i\'ll']

class CommonGenreWords:
  """
  Genre Typical Words: Top 200 words ine ach genre not appearing more than 500 times in either other genre
  Genre Exclusive Words: ALL words in each genre appearing 0 times in either other genre
  """

  @staticmethod
  def save_common_genre_words():
    country_exclusive_words, pop_explusive_words, christian_exclusive_words, country_typical_words, pop_typical_words, christian_typical_words = CommonGenreWords.load_common_genre_words()
    counters = [
      (country_exclusive_words, 'country_exclusive_words'), 
      (pop_explusive_words, 'pop_explusive_words'), 
      (christian_exclusive_words, 'christian_exclusive_words'),
      (country_typical_words, 'country_typical_words'), 
      (pop_typical_words, 'pop_typical_words'), 
      (christian_typical_words, 'christian_typical_words')
    ]
    
    for words, title in counters:
      FileUtils.save_to_text(words, 'files/common_genre_words/' + title + '.txt')

  @staticmethod
  def load_common_genre_words():
    punctuation = string.punctuation
    tracks = FileUtils.load_from_csv("files/lyrics.csv")
    stop_words = set(stopwords.words('english'))
    stop_words.update(custom_stop_words)
    
    # count words in each genre
    country_counter = Counter()
    pop_counter = Counter()
    christian_counter = Counter()
    
    for track in tracks:
      lyrics = track[3]
      genre = track[4]
      
      words = lyrics.lower().split()
      words = [word.strip(punctuation) for word in words if word.strip(punctuation) not in stop_words]
      
      if genre == 'country':
        country_counter.update(words)
      elif genre == 'pop':
        pop_counter.update(words)
      elif genre == 'christian':
        christian_counter.update(words)
    
    # (1) GENRE EXCLUSIVE WORDS
    exc_country_counter = country_counter.copy()
    exc_pop_counter = pop_counter.copy()
    exc_christian_counter = christian_counter.copy()
  
    CommonGenreWords.remove_words_in_multiple_genres(exc_country_counter, exc_pop_counter, exc_christian_counter, 0)
    
    country_exclusive_words = [entry[0] for entry in exc_country_counter.most_common()]
    pop_explusive_words = [entry[0] for entry in exc_pop_counter.most_common()]
    christian_exclusive_words = [entry[0] for entry in exc_christian_counter.most_common()]
    
    # (2) GENRE TYPICAL WORDS
    # remove words appearing > 300 times in another genre
    CommonGenreWords.remove_words_in_multiple_genres(country_counter, pop_counter, christian_counter, 500)
    
    n_top_typical = 200
    country_typical_words = [entry[0] for entry in country_counter.most_common(n_top_typical)]
    pop_typical_words = [entry[0] for entry in pop_counter.most_common(n_top_typical)]
    christian_typical_words = [entry[0] for entry in christian_counter.most_common(n_top_typical)]

    return country_exclusive_words, pop_explusive_words, christian_exclusive_words, country_typical_words, pop_typical_words, christian_typical_words
    
  @staticmethod
  def remove_words_in_multiple_genres(a: dict, b: dict, c: dict, n: int):
    '''n: # times appearing in other genre to remove'''
    to_pop = set()
    # n: num times it can appear in another playlist to not be considered exclusive
    for key in a:
      if (key in c and c[key] > n) or (key in b and b[key] > n):
        to_pop.add(key)
    for key in b:
      if (key in c and c[key] > n) or (key in a and a[key] > n):
        to_pop.add(key)
    for key in c:
      if (key in a and a[key] > n) or (key in b and b[key] > n):
        to_pop.add(key)

    for key in to_pop:
      c.pop(key, None)
      a.pop(key, None)
      b.pop(key, None)