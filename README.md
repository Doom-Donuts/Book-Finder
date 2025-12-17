# Book-Finder v0.9.1.7
Team members: Nathan Bradley, Tristan Fox, James Headrick

**Description:**
A program to help recommend books based on the users preferences using books in the database.

**Core Modules:**
The core modules are the Books database, the Search page, the Filtering system, the Recommendation system, the Review system, the asyncronous API, and the Logging system.

**Architecture:**
We used a layered architecture with the following 4 layers: UI Layer, Event Handler Layer, Async API Layer, and Data Access Layer.

**Using Book-Finder**

When Book-Finder is opened, a search page with a list of books in the database is opened.
<img width="1503" height="975" alt="image" src="https://github.com/user-attachments/assets/9b43e066-891c-4650-8343-9a089ee599c9" />

At the top in "File" there are options to toggle darkmode or quit with keyboard shortcuts for each.
Below that, it shows the page that the user is in. In the image, the user is on the search page.
Then, there are the filters to filter for books based on genre, which is listed as categories in the info section, or filter based on years.
The filters must be typed, and then the filter button must be pressed.
Next to the filter button, there is the recommend books button, and the reset button.
The recommend books button selects the book with the highest review score, and then filters books based on the genres of that book.
The reset button clears all filters and resets to the initial book list.
There is also the search bar below those buttons and the "Enter" button must be pressed to run the search.

On the left below the search bar, is the list of books that is displayed and can be scrolled down to view more books.
To the right of the list, is the info section that displays all of the information about a selected book.
A book can be selected by clicking a book in the list.
When a book is selected, the user can click the add review or edit review buttons in the info section.
This creates a popup where a user can type in their review and a score.
By clicking the create review button, a review is created that will be displayed in the info section.
A review can only be added if there is *not* already a review, which means the review score and review text both say "None".
Also, a review can only be edited if there *is* already a review.
<img width="1195" height="812" alt="image" src="https://github.com/user-attachments/assets/2a33c9c4-4b8b-4a68-b1ed-bfb673f957a8" />
