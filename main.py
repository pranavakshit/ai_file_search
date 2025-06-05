import yaml
from scanner.file_indexer import scan_files_and_extract_text
from search.semantic_search import search_semantically

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    folder = config["input_folder"]
    top_k = config.get("top_k", 5)

    print(f"Scanning files in: {folder}")
    documents = scan_files_and_extract_text(folder)

    if not documents:
        print("No files found or files are empty.")
        return

    query = input("Enter search query: ").strip()
    if not query:
        print("Empty query. Exiting.")
        return

    results = search_semantically(query, documents, top_k=top_k)

    if not results:
        print("No matches found.")
    else:
        for result in results:
            print("\n----------------------")
            print(f"File:     {result['file']}")
            print(f"Location: {result['position']}")
            print(f"Score:    {result['score']:.3f}")
            print(f"Text:     {result['text'][:200]}...")

if __name__ == "__main__":
    main()
