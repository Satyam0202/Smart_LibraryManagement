import requests
import json

# Test sorting
try:
    print("Testing sorting by name (asc)...")
    response = requests.get("http://localhost:5000/sort_books?sort_by=name&order=asc")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✅ Sorted {len(books)} books by name (asc)")
        print("\nFirst 3 books after sorting:")
        for book in books[:3]:
            print(f"  {book['name']} by {book['author']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Exception: {str(e)}")

print("\n" + "="*60 + "\n")

try:
    print("Testing sorting by price (desc)...")
    response = requests.get("http://localhost:5000/sort_books?sort_by=price&order=desc")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"✅ Sorted {len(books)} books by price (desc)")
        print("\nFirst 3 books by highest price:")
        for book in books[:3]:
            print(f"  {book['name']} - ₹{book['price']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Exception: {str(e)}")
