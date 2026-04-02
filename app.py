from flask import Flask, request, render_template, jsonify
import subprocess
import json
import os

app = Flask(__name__)

# COMMENT: Helper function to run C++ executable and get output
def run_cpp_command(operation, *args):
    try:
        # COMMENT: Convert all args to strings and pass to C++ executable
        cmd = ["library", operation] + [str(arg) for arg in args]
        print(f"DEBUG: Running command: {cmd}")  # COMMENT: Log the command
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        print(f"DEBUG: Return code: {result.returncode}")  # COMMENT: Log return code
        print(f"DEBUG: Stdout: {result.stdout}")  # COMMENT: Log output
        print(f"DEBUG: Stderr: {result.stderr}")  # COMMENT: Log errors
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except FileNotFoundError:
        return "Error: library executable not found. Make sure to compile library.cpp"
    except Exception as e:
        return f"Error: {str(e)}"

# COMMENT: Helper function to parse pipe-separated output from C++
def parse_cpp_output(output):
    lines = output.strip().split('\n')
    data = []
    for line in lines:
        if line and '|' in line:
            parts = line.split('|')
            data.append(parts)
    return data

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login_page')
def login_page():
    return render_template("login.html")

# COMMENT: Dashboard route - renders dashboard.html after login
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# COMMENT: Endpoint to populate 100 sample books into library
@app.route('/populate_sample_data', methods=['POST'])
def populate_sample_data():
    sample_books = [
        ("To Kill a Mockingbird", "Harper Lee", "Fiction", 300, 5),
        ("1984", "George Orwell", "Fiction", 350, 5),
        ("Pride and Prejudice", "Jane Austen", "Romance", 280, 5),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 400, 4),
        ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 320, 4),
        ("Moby Dick", "Herman Melville", "Adventure", 450, 4),
        ("War and Peace", "Leo Tolstoy", "Historical", 500, 5),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 380, 5),
        ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 550, 5),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 350, 5),
        ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fantasy", 360, 5),
        ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", "Fantasy", 370, 5),
        ("Harry Potter and the Goblet of Fire", "J.K. Rowling", "Fantasy", 400, 5),
        ("Harry Potter and the Order of the Phoenix", "J.K. Rowling", "Fantasy", 450, 4),
        ("Harry Potter and the Half-Blood Prince", "J.K. Rowling", "Fantasy", 420, 5),
        ("Harry Potter and the Deathly Hallows", "J.K. Rowling", "Fantasy", 480, 5),
        ("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "C.S. Lewis", "Fantasy", 320, 5),
        ("Dune", "Frank Herbert", "Science Fiction", 480, 5),
        ("Foundation", "Isaac Asimov", "Science Fiction", 400, 5),
        ("I, Robot", "Isaac Asimov", "Science Fiction", 300, 4),
        ("Brave New World", "Aldous Huxley", "Science Fiction", 380, 4),
        ("The Time Machine", "H.G. Wells", "Science Fiction", 250, 4),
        ("Twenty Thousand Leagues Under the Sea", "Jules Verne", "Adventure", 420, 4),
        ("Journey to the Center of the Earth", "Jules Verne", "Adventure", 380, 4),
        ("Around the World in Eighty Days", "Jules Verne", "Adventure", 350, 4),
        ("The Three Musketeers", "Alexandre Dumas", "Adventure", 420, 4),
        ("The Count of Monte Cristo", "Alexandre Dumas", "Adventure", 480, 5),
        ("A Tale of Two Cities", "Charles Dickens", "Historical", 450, 4),
        ("Oliver Twist", "Charles Dickens", "Fiction", 400, 4),
        ("Great Expectations", "Charles Dickens", "Fiction", 420, 4),
        ("Jane Eyre", "Charlotte Brontë", "Romance", 380, 5),
        ("Wuthering Heights", "Emily Brontë", "Romance", 360, 4),
        ("The Scarlet Letter", "Nathaniel Hawthorne", "Historical", 300, 3),
        ("The Hunchback of Notre-Dame", "Victor Hugo", "Historical", 420, 4),
        ("Les Misérables", "Victor Hugo", "Historical", 500, 5),
        ("Frankenstein", "Mary Shelley", "Science Fiction", 320, 4),
        ("Dracula", "Bram Stoker", "Horror", 380, 4),
        ("The Picture of Dorian Gray", "Oscar Wilde", "Fiction", 300, 4),
        ("Alice's Adventures in Wonderland", "Lewis Carroll", "Fantasy", 280, 4),
        ("Through the Looking-Glass", "Lewis Carroll", "Fantasy", 290, 4),
        ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle", "Mystery", 350, 5),
        ("A Study in Scarlet", "Arthur Conan Doyle", "Mystery", 320, 4),
        ("The Odyssey", "Homer", "Epic", 450, 4),
        ("The Iliad", "Homer", "Epic", 480, 4),
        ("Beowulf", "Anonymous", "Epic", 350, 4),
        ("Don Quixote", "Miguel de Cervantes", "Fiction", 500, 4),
        ("Robinson Crusoe", "Daniel Defoe", "Adventure", 320, 4),
        ("Gulliver's Travels", "Jonathan Swift", "Adventure", 380, 3),
        ("The Invisible Man", "H.G. Wells", "Science Fiction", 280, 4),
        ("Treasure Island", "Robert Louis Stevenson", "Adventure", 320, 4),
        ("Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson", "Horror", 280, 4),
        ("The Strange Case of Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson", "Horror", 290, 4),
        ("Robinson Crusoe", "Daniel Defoe", "Adventure", 320, 4),
        ("Ivanhoe", "Sir Walter Scott", "Historical", 450, 4),
        ("A Christmas Carol", "Charles Dickens", "Fiction", 200, 5),
        ("The Pickwick Papers", "Charles Dickens", "Fiction", 450, 4),
        ("Bleak House", "Charles Dickens", "Fiction", 500, 4),
        ("Little Women", "Louisa May Alcott", "Fiction", 380, 5),
        ("Jo's Boys", "Louisa May Alcott", "Fiction", 350, 4),
        ("The Swiss Family Robinson", "Johann David Wyss", "Adventure", 380, 4),
        ("Black Beauty", "Anna Sewell", "Fiction", 300, 4),
        ("Anne of Green Gables", "L.M. Montgomery", "Fiction", 350, 5),
        ("The Secret Garden", "Frances Hodgson Burnett", "Fiction", 320, 5),
        ("Heidi", "Johanna Spyri", "Fiction", 300, 4),
        ("The Boy Who Harnessed the Wind", "William Kamkwamba", "Biography", 380, 5),
        ("The 7 Habits of Highly Effective People", "Stephen Covey", "Self-Help", 450, 5),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 480, 5),
        ("Educated", "Tara Westover", "Biography", 420, 5),
        ("Atomic Habits", "James Clear", "Self-Help", 400, 5),
        ("The Lean Startup", "Eric Ries", "Business", 380, 4),
        ("Good to Great", "Jim Collins", "Business", 450, 5),
        ("Start with Why", "Simon Sinek", "Business", 380, 5),
        ("Deep Work", "Cal Newport", "Self-Help", 350, 5),
        ("The Man Who Mistook His Wife for a Hat", "Oliver Sacks", "Psychology", 380, 4),
        ("Mindset", "Carol S. Dweck", "Psychology", 320, 5),
        ("Man's Search for Meaning", "Viktor E. Frankl", "Philosophy", 280, 5),
        ("The Brothers Karamazov", "Fyodor Dostoevsky", "Fiction", 500, 5),
        ("Crime and Punishment", "Fyodor Dostoevsky", "Fiction", 480, 5),
        ("Anna Karenina", "Leo Tolstoy", "Romance", 500, 5),
        ("Madame Bovary", "Gustave Flaubert", "Romance", 380, 4),
        ("The Stranger", "Albert Camus", "Fiction", 300, 4),
        ("Beloved", "Toni Morrison", "Fiction", 380, 5),
        ("The Handmaid's Tale", "Margaret Atwood", "Science Fiction", 400, 5),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", "Magical Realism", 450, 5),
        ("The Marvelous Adventures of Catullus Kelly", "Andy Weir", "Science Fiction", 350, 4),
        ("The Martian", "Andy Weir", "Science Fiction", 400, 5),
        ("Catch-22", "Joseph Heller", "Satire", 420, 4),
        ("Slaughterhouse-Five", "Kurt Vonnegut", "Fiction", 360, 4),
        ("The Bell Jar", "Sylvia Plath", "Fiction", 320, 4),
        ("A Clockwork Orange", "Anthony Burgess", "Fiction", 380, 4),
        ("Lolita", "Vladimir Nabokov", "Fiction", 400, 3),
        ("American Psycho", "Bret Easton Ellis", "Thriller", 450, 3),
        ("Fight Club", "Chuck Palahniuk", "Thriller", 380, 4)
    ]
    
    try:
        # COMMENT: Add each book to library using C++ backend
        added_count = 0
        failed_books = []
        for idx, (title, author, category, price, rating) in enumerate(sample_books, 1):
            book_id = 1000 + idx  # IDs from 1001-1100
            result = run_cpp_command('add_book', book_id, title, author, category, price, rating, 0, 'true')
            
            # COMMENT: Check for errors - stop if any book fails
            if "Error" in result or "already exists" in result:
                failed_books.append({'id': book_id, 'title': title, 'error': result})
            else:
                added_count += 1
        
        # COMMENT: Return result with details about failures
        if failed_books:
            return jsonify({
                'status': 'partial', 
                'message': f'Added {added_count} books successfully. {len(failed_books)} books failed.',
                'added': added_count,
                'failed': len(failed_books),
                'failed_books': failed_books
            })
        elif added_count == 0:
            return jsonify({'status': 'error', 'message': 'No books were added'})
        else:
            return jsonify({'status': 'success', 'message': f'Added {added_count} sample books successfully!', 'count': added_count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")

# COMMENT: ============ BOOK OPERATIONS ============

# COMMENT: Add book - calls C++ linked list insertion
@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        author = request.form.get('author')
        category = request.form.get('category')
        price = request.form.get('price')
        rating = request.form.get('rating', '0')
        issue_count = request.form.get('issue_count', '0')
        available = request.form.get('available', 'true')

        # COMMENT: Validate required fields
        if not id or not name or not author:
            return jsonify({'status': 'error', 'message': 'Missing required fields'})

        output = run_cpp_command("add_book", id, name, author, category, price, rating, issue_count, available)
        
        # COMMENT: Check if C++ execution was successful
        if "Error" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: Get all books - calls C++ linked list traversal
@app.route('/get_books', methods=['GET'])
def get_books():
    try:
        output = run_cpp_command("get_books")
        books_data = []
        
        # COMMENT: Parse pipe-separated output from C++
        for line in output.split('\n'):
            if line and '|' in line:
                parts = line.split('|')
                if len(parts) >= 8:
                    try:
                        books_data.append({
                            'id': int(parts[0]),
                            'name': parts[1],
                            'author': parts[2],
                            'category': parts[3],
                            'price': int(parts[4]),
                            'rating': int(parts[5]),
                            'issue_count': int(parts[6]),
                            'available': parts[7] == 'true'
                        })
                    except ValueError:
                        continue  # COMMENT: Skip invalid rows
        
        print(f"DEBUG: Loaded {len(books_data)} books")  # COMMENT: Log count
        return jsonify(books_data)
    except Exception as e:
        print(f"DEBUG: Error loading books: {str(e)}")
        return jsonify([])

# COMMENT: Sort books - calls C++ quickSort algorithm
@app.route('/sort_books', methods=['GET'])
def sort_books():
    try:
        sort_by = request.args.get('sort_by', 'name')  # name, author, price, rating
        order = request.args.get('order', 'asc')  # asc or desc
        
        # COMMENT: Get all books first
        output = run_cpp_command("get_books")
        books_data = []
        
        # COMMENT: Parse pipe-separated output from C++
        for line in output.split('\n'):
            if line and '|' in line:
                parts = line.split('|')
                if len(parts) >= 8:
                    try:
                        books_data.append({
                            'id': int(parts[0]),
                            'name': parts[1],
                            'author': parts[2],
                            'category': parts[3],
                            'price': int(parts[4]),
                            'rating': int(parts[5]),
                            'issue_count': int(parts[6]),
                            'available': parts[7] == 'true'
                        })
                    except ValueError:
                        continue
        
        # COMMENT: Sort based on requested field (using Python sort for efficiency)
        if sort_by == 'name':
            books_data.sort(key=lambda x: x['name'].lower(), reverse=(order == 'desc'))
        elif sort_by == 'author':
            books_data.sort(key=lambda x: x['author'].lower(), reverse=(order == 'desc'))
        elif sort_by == 'price':
            books_data.sort(key=lambda x: x['price'], reverse=(order == 'desc'))
        elif sort_by == 'rating':
            books_data.sort(key=lambda x: x['rating'], reverse=(order == 'desc'))
        
        print(f"DEBUG: Sorted {len(books_data)} books by {sort_by} ({order})")
        return jsonify(books_data)
    except Exception as e:
        print(f"DEBUG: Error sorting books: {str(e)}")
        return jsonify([])

# COMMENT: Delete book - calls C++ linked list deletion
@app.route('/delete_book', methods=['POST'])
def delete_book():
    try:
        id = request.form.get('id')
        
        if not id:
            return jsonify({'status': 'error', 'message': 'Book ID required'})
        
        output = run_cpp_command("delete_book", id)
        
        if "Error" in output or "Not Found" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: Search book by ID - calls C++ binary search
@app.route('/search_book', methods=['GET'])
def search_book():
    id = request.args.get('id')
    output = run_cpp_command("search_book", id)
    
    if "Not Found" in output:
        return jsonify({'status': 'error', 'message': 'Book not found'})
    
    if '|' in output:
        parts = output.split('|')
        book_data = {
            'id': int(parts[0]),
            'name': parts[1],
            'author': parts[2],
            'category': parts[3],
            'price': int(parts[4]),
            'rating': int(parts[5])
        }
        return jsonify({'status': 'success', 'data': book_data})
    
    return jsonify({'status': 'error', 'message': 'Search failed'})

# COMMENT: ============ MEMBER OPERATIONS ============

# COMMENT: Add member - calls C++ hash table insertion with duplicate checking
@app.route('/add_member', methods=['POST'])
def add_member():
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address', '')

        if not id or not name or not email or not phone:
            return jsonify({'status': 'error', 'message': 'Missing required fields'})

        # Check for duplicate membership ID, email, or phone
        output = run_cpp_command("get_members")
        for line in output.split('\n'):
            if line and '|' in line:
                parts = line.split('|')
                if len(parts) >= 5:
                    existing_id = parts[0]
                    existing_email = parts[2]
                    existing_phone = parts[3]
                    
                    if existing_id == id:
                        return jsonify({'status': 'error', 'message': f'Membership ID {id} already exists'})
                    if existing_email == email:
                        return jsonify({'status': 'error', 'message': f'Email {email} already registered'})
                    if existing_phone == phone:
                        return jsonify({'status': 'error', 'message': f'Phone {phone} already registered'})

        output = run_cpp_command("add_member", id, name, email, phone, address)
        
        if "Error" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: Get all members - calls C++ hash table traversal
@app.route('/get_members', methods=['GET'])
def get_members():
    output = run_cpp_command("get_members")
    members_data = []
    for line in output.split('\n'):
        if line and '|' in line:
            parts = line.split('|')
            if len(parts) >= 5:
                members_data.append({
                    'id': parts[0],
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'address': parts[4]
                })
    return jsonify(members_data)

# COMMENT: Delete member - calls C++ hash table deletion
@app.route('/delete_member', methods=['POST'])
def delete_member():
    try:
        phone = request.form.get('phone')
        
        if not phone:
            return jsonify({'status': 'error', 'message': 'Phone number required'})
        
        output = run_cpp_command("delete_member", phone)
        
        if "Error" in output or "Not Found" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: ============ ISSUED BOOK OPERATIONS ============

# COMMENT: Issue book - calls C++ queue enqueue operation
@app.route('/issue_book', methods=['POST'])
def issue_book():
    try:
        book_id = request.form.get('book_id')
        member_id = request.form.get('member_id')
        issue_date = request.form.get('issue_date')
        due_date = request.form.get('due_date', '')

        if not book_id or not member_id or not issue_date:
            return jsonify({'status': 'error', 'message': 'Missing required fields'})

        output = run_cpp_command("issue_book", book_id, member_id, issue_date, due_date)
        
        if "Error" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: Return book - calls C++ queue dequeue operation
@app.route('/return_book', methods=['POST'])
def return_book():
    try:
        book_id = request.form.get('book_id')
        member_id = request.form.get('member_id')

        if not book_id or not member_id:
            return jsonify({'status': 'error', 'message': 'Book ID and Member ID required'})

        output = run_cpp_command("return_book", book_id, member_id)
        
        if "Error" in output or "Not Found" in output:
            return jsonify({'status': 'error', 'message': output})
        
        return jsonify({'status': 'success', 'message': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

# COMMENT: Get all issued books - calls C++ queue traversal
@app.route('/get_issued', methods=['GET'])
def get_issued():
    output = run_cpp_command("get_issued")
    issued_data = []
    for line in output.split('\n'):
        if line and '|' in line:
            parts = line.split('|')
            if len(parts) >= 5:
                issued_data.append({
                    'book_id': int(parts[0]),
                    'member_id': parts[1],
                    'issue_date': parts[2],
                    'due_date': parts[3],
                    'returned': parts[4] == 'true'
                })
    return jsonify(issued_data)

# COMMENT: ============ ACTIVITY LOG OPERATIONS ============

# COMMENT: Get activity log - calls C++ stack traversal
@app.route('/get_activity', methods=['GET'])
def get_activity():
    output = run_cpp_command("get_activity")
    activity_data = []
    for line in output.split('\n'):
        if line and '|' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                activity_data.append({
                    'timestamp': parts[0],
                    'action': parts[1],
                    'details': parts[2]
                })
    return jsonify(activity_data)

# COMMENT: ============ USER MANAGEMENT ============

# COMMENT: User signup - validates and stores in users.csv
@app.route('/signup', methods=['POST'])
def signup():
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone'] 
    email = request.form['email']
    password = request.form['pass']
    con_pass = request.form['con_pass']

    if password != con_pass:
        return jsonify({'status': 'error', 'message': 'Password do not match!'})
    
    try:
        with open('users.csv', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 5:
                    existing_phone = data[2]
                    existing_email = data[3]

                    if phone == existing_phone:
                        return jsonify({'status': 'error', 'message': 'Phone Number Is Already Registered!'})
                    if email == existing_email:
                        return jsonify({'status': 'error', 'message': 'Email Already Registered!'})
    except FileNotFoundError:
        pass
    
    with open('users.csv', 'a') as f:
        f.write(f"{fname},{lname},{phone},{email},{password}\n")
    
    return jsonify({'status': 'success', 'message': 'Account Created Successfully!'})

# COMMENT: User login - validates against users.csv
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        with open('users.csv', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) == 5:
                    saved_email = data[3]
                    saved_password = data[4]
                    if email == saved_email and password == saved_password:
                        return jsonify({'status': 'success', 'message': 'Login Successful!', 'user': data[0] + ' ' + data[1]})
        return jsonify({'status': 'error', 'message': 'Invalid Email or Password!'})
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No users found. Please signup first!'})

# COMMENT: Get user profile by email - fetch from users.csv
@app.route('/get_profile', methods=['GET'])
def get_profile():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'status': 'error', 'message': 'Email required'})
    
    try:
        with open('users.csv', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 4 and data[3] == email:
                    # COMMENT: Return user profile data from CSV
                    profile = {
                        'fullName': data[0] + ' ' + data[1],
                        'phone': data[2],
                        'email': data[3],
                        'role': 'Administrator',
                        'department': 'Library Management'
                    }
                    return jsonify({'status': 'success', 'data': profile})
        
        return jsonify({'status': 'error', 'message': 'User not found'})
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'Users database not found'})

if __name__ == '__main__':
    app.run(debug=True)
