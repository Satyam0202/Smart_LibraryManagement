import requests
import json

# Test the get_books endpoint
response = requests.get("http://localhost:5000/get_books")
books = response.json()

print(f"✅ Total books in library: {len(books)}")
print("\nFirst 10 books:")
print("-" * 80)
for book in books[:10]:
    print(f"ID: {book['id']:4} | {book['name'][:50]:50} | {book['author'][:20]:20}")
print("-" * 80)
print(f"\nLast 10 books:")
print("-" * 80)
for book in books[-10:]:
    print(f"ID: {book['id']:4} | {book['name'][:50]:50} | {book['author'][:20]:20}")
