from storage import init_db, search_pages, get_dead_links
from crawler import crawl


if __name__ == "__main__":
    # Keep the command-line entry point small: collect input, run crawl, show results.
    start_url = input("Enter a URL: ").strip()
    if not start_url:
        raise ValueError("Please enter a URL")

    while True:
        try:
            max_pages = int(input("Max pages: "))
            max_depth = int(input("Max depth: "))
            if max_depth < 0:
                raise ValueError("Max depth can't be a negative number.")
            if max_pages <= 0:
                raise ValueError("Max pages must be higher than 0.")
            break
        except ValueError as error:
            print(error)

    search_query = input("Searching for: ").strip()

    init_db()

    crawl(start_url, max_pages, max_depth)
    print(search_pages(search_query))
    print(get_dead_links())
