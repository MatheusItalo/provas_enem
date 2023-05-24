from ExtractEnem import ExtractEnem
from MongoConnect import MongoConnect

def main():
  mongo_connect = MongoConnect()
  collection_books = mongo_connect.get_collection("books")

  extract = ExtractEnem()
  books = [
    "2022_PV_impresso_D1_CD4.pdf",
    "2022_PV_impresso_D1_CD1.pdf",
    "2022_PV_impresso_D1_CD2.pdf",
    "2022_PV_impresso_D1_CD3.pdf",
    "2022_PV_impresso_D2_CD8.pdf",
    "2022_PV_impresso_D2_CD6.pdf",
    "2022_PV_impresso_D2_CD5.pdf",
    "2022_PV_impresso_D2_CD7.pdf"
  ]

  for book in books:
    book_detals = book.replace(".pdf", "").split("_")

    book_doc = {
      "year" : book_detals[0],
      "day" : book_detals[3],
      "type" : book_detals[4],
      "file_name" : book
    }

    book_text = extract.text_extract(book)

    book_inserted = collection_books.insert_one(book_doc)

    extract.questions_extract(book_text, book_inserted.inserted_id)

    print("######### BOOK INSERTED ##########")

if __name__ == "__main__":
  main()