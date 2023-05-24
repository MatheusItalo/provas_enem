from MongoConnect import MongoConnect
from PyPDF2 import PdfReader
import re

class ExtractEnem:

  def __init__(self):
     self.mongo_connect = MongoConnect()

  def text_extract(self, file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    text = re.sub(
       r'\d\s+LC\s+-\s+\d°\s+dia\s+|\s+Caderno\s+\d\s+-\s+ROSA\s+-\s+\dª\s+Aplica\w\wo[\s+ENEM\s+\d{4}]+',
       '',
       text,
       flags=re.DOTALL
    )

    return text
  
  def questions_extract(self, text_raw, book_id):
    collection_questions = self.mongo_connect.get_collection("questions")

    questions = re.finditer(
      r'(?P<text_question>QUEST\wO\s+\d{2}.*?)(?P<text_options>A A.*?)((?=QUEST\wO)|RASCUNHO)',
      text_raw, 
      flags=re.DOTALL
    )

    number_question = 0

    for question in questions:

      number_question += 1
       
      question_doc = {
        "book_id" : book_id,
        "text_question" : question.group("text_question"),
        "number_question" : number_question,
        "options_question" : []
      }

      text_options = question.group("text_options")

      options = re.finditer(
        r'[A-Z]\s+(?P<option>[A-Z]?)\s+(?P<text_option>.*?)\.',
        text_options,
        flags=re.DOTALL
      )

      for option in options:
          option_doc = {
             "option" : option.group("option"),
             "text_option" : option.group("text_option")
          }

          question_doc["options_question"].append(option_doc)

      collection_questions.insert_one(question_doc)
      print("########### QUESTION SAVE #############")

  def get_books(self):
     collection_books = self.mongo_connect.get_collection("books")

     books = list(collection_books.aggregate(
        [
            {
              "$lookup" : {
                  "from" : "questions",
                  "localField" : "_id",
                  "foreignField" : "book_id",
                  "as" : "questions"
              }
            }
        ]
     ))

     return books