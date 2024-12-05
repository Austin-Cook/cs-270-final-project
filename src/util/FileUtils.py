import csv
import json


class FileUtils:
  @staticmethod
  def save_to_json(obj: dict, json_filename: str) -> None:
    with open(json_filename, 'w') as f:
      json.dump(obj, f)

  @staticmethod
  def save_to_csv(item: list, csv_filename: str) -> None:
    with open(csv_filename, 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerows(item)
  
  @staticmethod
  def save_to_text(items: list, filename: str) -> None:
    with open(filename, 'w') as f:
      for i in range(len(items)):
        f.write(items[i] + '\n' if i < len(items) - 1 else items[i])

  @staticmethod
  def load_from_csv(csv_filename: str) -> list:
    with open(csv_filename, 'r', newline='') as f:
      return list(csv.reader(f))
    
  @staticmethod
  def load_from_json(json_filename: str) -> object:
    with open(json_filename, 'r', newline='') as f:
      return json.load(f)
    
  @staticmethod
  def load_from_text(filename: str) -> list:
    with open(filename, 'r') as f:
      text = f.read()
      
      return text.splitlines()
