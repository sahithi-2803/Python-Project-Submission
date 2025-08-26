**Book Recommendation Bot**

**Description of the Project:**

This is a Python project that helps to find books to read based on the favorite genre. We can also choose to filter books by year or popularity and get a random book suggestion.

**Scope of this Project:**

        •	It suggests you pick a book genre (like horror, fantasy, or cooking)
        •	Gets real book data from the internet using Open Library
        •	It filters books by:
                o	Published Year of the book 
                o	Popularity (how many editions the book has)
        •	Shows a random book recommendation
        •	Saves the list of books to a CSV file (so you can open it in Excel)

**Software & Libraries Used:**

        •	Python 3 - Programming language            
        •	Requests - To get book data from a website 
        •	Pandas - To work with book data easily   

**Install Dependencies:**

        •	pip install pandas & requests

**How to Run:**

        •	Book_recommendation_bot.py

**How It Works:**

        1. Welcome User
                • Shows a greeting and list of available genres.
        2. Get Genre Input
                • Accepts genre input from the user.
                • Keeps prompting if input is invalid.
        3. Fetch Data from Open Library
                • Sends an API request like: https://openlibrary.org/subjects/fantasy.json?limit=300
        4. Filter Books 
                • User can filter the book list:
                        o By year
                        o By edition count (popularity)
        5. Recommend a Book
                • Picks one book at random from the (filtered) list.
                • Displays the title, author(s), publication year, and edition count.
        6. Save to CSV 
                • The full dataset is optionally saved as a CSV file like fantasy_books.csv.

**Sample Data Fields (for Random book):**

•  Title: "The Hobbit"
•  Authors:"J.R.R. Tolkien"
•  Genre: "fantasy"
•  Year: 1937
•  Popularity: 56
