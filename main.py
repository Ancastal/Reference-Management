import os
import colorama
import pyfiglet
from colorama import Fore, Style
from pybibtex import BibTeXFile, BibTeXEntry

colorama.init()

DATABASE_FILE = 'references.bib'


def add_reference(database):
    print("============== Add Reference ==============")
    print()
    print("Please provide the following information:")
    print()
    key = input("Reference Key: ")
    author = input("Author(s) Name: ")
    title = input("Title: ")
    year = input("Publication Year: ")
    journal = input("Journal Name: ")
    print()
    print("Adding reference...")
    print()
    fields = {"author": author, "title": title, "year": year, "journal": journal}
    database.add_entry("article", key, fields)
    database.save()
    print("Reference added successfully!")
    print()
    input("Press Enter to continue...")


def search_references(database):
    print("============== Search References ==============")
    print()
    query = input("Enter a search query (author or title): ")
    results = []
    for key, entry in database.entries.items():
        if 'author' in entry.fields and query.lower() in entry.fields['author'].lower():
            results.append((key, entry))
        elif 'title' in entry.fields and query.lower() in entry.fields['title'].lower():
            results.append((key, entry))
    if results:
        print()
        print("Search Results:")
        print()
        for index, (key, entry) in enumerate(results):
            print(f"{index + 1}. {entry.generate_citation()}")
    else:
        print()
        print("No matching references found.")
    print()
    summary_bool = input("Would you like to see a summary of the search results? (y/n): ")
    if summary_bool == "y":
        search_number = input("Enter the number of the reference to see more details (or press Enter to continue): ")
        if search_number:
            try:
                search_number = int(search_number)
                if search_number > 0 and search_number <= len(results):
                    print()
                    print()
                    summary = results[search_number - 1][1].generate_summary()
                    if summary:
                        print("Reference Details:")
                        print(summary)
                    else:
                        print("No details available.")
            except ValueError:
                print("Invalid input. Please enter a valid reference number.")
        else:
            return
    print()
    input("Press Enter to continue...")




def edit_reference(database):
    print("============== Edit Reference ==============")
    print()
    key = input("Enter the reference key to edit: ")
    field = input("Enter the field to be edited (author, title, year, or journal): ")
    value = input("Enter the new value: ")
    if key in database.entries:
        database.entries[key].fields[field] = value
        database.save()
        print()
        print("Reference edited successfully!")
    else:
        print()
        print("Reference not found.")
    print()
    input("Press Enter to continue...")


def delete_reference(database):
    print("============== Delete Reference ==============")
    print()
    key = input("Enter the reference key to delete: ")
    if key in database.entries:
        database.delete_entry(key)
        database.save()
        print()
        print("Reference deleted successfully!")
    else:
        print()
        print("Reference not found.")
    print()
    input("Press Enter to continue...")


def list_references(database):
    print("============== List References ==============")
    print()
    print("List of References:")
    print()
    for index, (key, entry) in enumerate(database.entries.items()):
        print(f"{index + 1}. {entry.generate_citation()}")
        print()
    print()
    input("Press Enter to continue...")


def filter_references(database):
    print("============== Filter References ==============")
    print()
    field = input("Enter the field to filter by (author, title, year, or journal): ")
    condition_str = input("Enter a condition (e.g., '== John Doe', '> 2000'): ")

    # Define a condition function
    condition = lambda value: eval(f"'{value}' {condition_str}")

    # Use the filter_entries function
    filtered_entries = database.filter_entries(field, condition)

    print()
    if filtered_entries:
        print("Filtered Entries:")
        print()
        for entry in filtered_entries:
            print(entry.generate_citation())
    else:
        print("No matching references found.")
    print()
    input("Press Enter to continue...")


def suggest_related_references():
    print("============== Similar References ==============")
    print()
    key = input("Enter the reference key: ")
    print()
    print("Searching for similar references...")
    print()
    from trainer import suggest_related
    suggest_related(key)
    print()
    input("Press Enter to continue...")


def load_database():
    if os.path.isfile(DATABASE_FILE):
        database = BibTeXFile(DATABASE_FILE)
        print("BibTeX file loaded successfully!")
        print(f"Total references: {len(database.entries)}")
    else:
        database = BibTeXFile(DATABASE_FILE)
    print()
    return database


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_onboarding():
    clear_screen()

    title = pyfiglet.figlet_format("RMS", font="slant")
    print(Fore.BLUE + Style.BRIGHT + title)

    print("Welcome to the Reference Management System!")
    print()
    print("This system helps you manage your references and citations efficiently.")
    print("Follow the instructions below to get started:")
    print()
    print("1. Add Reference: Enter information about a new reference.")
    print("2. Search References: Find references by author name or title.")
    print("3. Edit Reference: Modify the details of an existing reference.")
    print("4. Delete Reference: Remove a reference from the system.")
    print("5. List References: View all stored references.")
    print("6. Filter References: Filter references based on specific criteria.")
    print("7. Find Similar References: Discover related references based on a key.")
    print("8. Quit: Exit the Reference Management System.")
    print()
    input("Press Enter to continue...")


def print_menu():
    clear_screen()
    title = pyfiglet.figlet_format("RMS", font="slant")
    print(Fore.BLUE + Style.BRIGHT + title)
    print("Welcome to the Reference Management System!")
    print()
    print(Fore.GREEN + "====================== MENU ======================")
    print(Fore.CYAN + "1. Add Reference")
    print("2. Search References")
    print(Fore.YELLOW + "3. Edit Reference")
    print(Fore.MAGENTA + "4. Delete Reference")
    print(Fore.CYAN + "5. List References")
    print(Fore.GREEN + "6. Filter References")
    print(Fore.BLUE + "7. Find Similar References")
    print(Fore.RED + "8. ARXIV")
    print(Fore.RED + "9. Quit")
    print(Style.RESET_ALL)

def print_arxiv():
    clear_screen()
    title = pyfiglet.figlet_format("RMS", font="slant")
    print(Fore.BLUE + Style.BRIGHT + title)
    print("Welcome to the Reference Management System!")
    print()
    print(Fore.GREEN + "====================== ARXIV ======================")
    print(Fore.CYAN + "1. Search by Title")
    print("2. Search by Author")
    print(Fore.YELLOW + "3. Search by Year")
    print(Fore.MAGENTA + "4. Search by Journal")
    print(Fore.GREEN + "5. Search by Abstract")
    choice = input("Enter your choice (1-5): ")
    if choice == 1:
        search_title()

def main():
    show_onboarding()
    clear_screen()
    database = load_database()

    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            add_reference(database)
        elif choice == '2':
            search_references(database)
        elif choice == '3':
            edit_reference(database)
        elif choice == '4':
            delete_reference(database)
        elif choice == '5':
            list_references(database)
        elif choice == '6':
            filter_references(database)
        elif choice == '7':
            suggest_related_references()
        elif choice == '8':
            print_arxiv()
        elif choice == '9':
            print("Thank you for using RMS!")
            break
        else:
            print("Invalid choice. Please try again.")
            print()


if __name__ == '__main__':
    main()
