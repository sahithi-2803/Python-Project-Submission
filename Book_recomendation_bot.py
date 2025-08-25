import requests 
import pandas as pd
import random

# Suggested genres
ALLOWED_GENRES = ['thriller', 'horror', 'fantasy', 'cooking', 'romance', 'mystery', 'history']

#exception to handle the undefined genere
class InvalidGenreError(Exception):
    pass

# API URL
API_URL = "https://openlibrary.org/subjects/{genre}.json?limit=300"
# Function to fetch books dataset based on genre
def fetch_books_by_genre(genre):
  
    genre = genre.lower()
#If user selected the Invalid Genre
    if genre not in ALLOWED_GENRES:
        raise InvalidGenreError(f"'{genre}' is not a valid genre. Choose from: {', '.join(ALLOWED_GENRES)}")
# Tp get the Data based on user selected Genre
    try:
        response = requests.get(API_URL.format(genre=genre))
        response.raise_for_status()
        data = response.json()
        books = data.get("works", [])

        book_list = []
        for book in books:
            book_info = {
                "title": book.get("title", "N/A"),
                "authors": ", ".join([author['name'] for author in book.get("authors", [])]),
                "genre": genre,
                "first_publish_year": book.get("first_publish_year", "N/A"),
                "edition_count": book.get("edition_count", 0),
                "cover_edition_key": book.get("cover_edition_key", ""),
                "key": book.get("key", "")
            }
            book_list.append(book_info)

        df = pd.DataFrame(book_list)
        df.to_csv(f"{genre}_books.csv", index=False)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
#Function to filter books based on Year & Popularity
def filter_books(df, year=None, popularity=None):
    
    try:
        if year:
            df = df[df['first_publish_year'] == year]
        if popularity:
            df = df[df['edition_count'] == popularity]
        return df
    except Exception as e:
        print(f"Error filtering data: {e}")
        return df
# Function to return a random book from filtered list
def random_book_suggestion(df):
    
    try:
        if df.empty:
            return "No books available to suggest."
        book = df.sample(n=1).iloc[0]
        return (
            f"Title: {book['title']}\n"
            f"Author(s): {book['authors']}\n"
            f"Year: {book['first_publish_year']}\n"
            f"Popularity (Editions): {book['edition_count']}"
        )
    except Exception as e:
        return f"Error generating suggestion: {e}"
#main function to call the sub-functions according to user inputs
def main():
    
    print("Hi !! Welcome to the Book Recommendation Bot!")
    print("Available genres:", ", ".join(ALLOWED_GENRES))
    print("Type 'exit' anytime to quit.")

    df = pd.DataFrame()
    while df.empty:
        genre = input("Enter a genre from the list above: ").strip().lower()
        if genre == 'exit':
            print("Thanks for using the Book Recommendation Bot.")
            return  # Exits the program

        try:
            df = fetch_books_by_genre(genre)
            if df.empty:
                print(f"No data found for genre '{genre}'. Try another genre.")
        except InvalidGenreError as e:
            print(e)
            continue

    filter_choice = input("\nWould you like to filter the results? (yes/no): ").strip().lower()
    year = None
    popularity = None

    if filter_choice.lower() == 'exit':
        print("Exiting as requested.")
        return
    if filter_choice == 'yes':
        # Show available years
        available_years = sorted(df['first_publish_year'].dropna().unique())
        print("\nAvailable publication years:")
        print(", ".join(str(int(y)) for y in available_years if str(y).isdigit()))

        # Validate year input
        while True:
            year_input = input("Enter a publication year to filter (or leave blank to skip): ").strip()
            if year_input.lower() == 'exit':
                print("Exiting as requested.")
                return
            if not year_input:
                break
            try:
                year = int(year_input)
                if year in available_years:
                    break
                else:
                    print(f"'{year}' is not in the available list.")
                    print("Available years:", ", ".join(str(int(y)) for y in available_years))
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Only ask for popularity if year is selected
        if year:
            year_df = df[df['first_publish_year'] == year]
            year_popularity = sorted(year_df['edition_count'].dropna().unique())
            if year_popularity:
                print("\nAvailable popularity (edition counts) for selected year:")
                print(", ".join(str(int(p)) for p in year_popularity))

                while True:
                    popularity_input = input("Enter minimum popularity (edition count) or leave blank: ").strip()
                    if popularity_input.lower() == 'exit':
                        print("Exiting as requested.")
                        return
                    if not popularity_input:
                        break
                    try:
                        popularity = int(popularity_input)
                        if popularity in year_popularity:
                            break
                        else:
                            print(f"'{popularity}' is not in the available list.")
                            print("Available popularity (edition counts) for selected year:", ", ".join(str(int(y)) for y in year_popularity))
                    except ValueError:
                        print("Invalid popularity input. Skipping popularity filter.")

    # Apply filters
    filtered_df = filter_books(df, year=year, popularity=popularity)
    print(f"\nFound {len(filtered_df)} books after filtering.")

    # Show random book suggestion
    print("\nRandom book suggestion:")
    print(random_book_suggestion(filtered_df))


# Run the script
if __name__ == "__main__":
    main()