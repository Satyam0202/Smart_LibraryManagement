# 📚 Library Management System

A full-stack library management system built with **Python Flask**, **C++**, and **Vanilla JavaScript**. Manage books, members, issue tracking, and activity logs with an intuitive and responsive web interface.

![Library Management](static/logo.png)

---

## ✨ Features

### 📖 Book Management
- ✅ Add, view, and delete books from the library
- ✅ Search and filter books by category, author, price, and rating
- ✅ Sort books by any column (ascending/descending)
- ✅ Track book availability and issue count
- ✅ Automatic CSV persistence with proper special character handling
- ✅ Binary search for O(log n) book lookups

### 👥 Member Management
- ✅ Add new members with 4-character alphanumeric IDs (A3K9, B7M2, etc.)
- ✅ Duplicate prevention (ID, Email, Phone)
- ✅ Delete members from the system
- ✅ View member profiles with issue history
- ✅ Track total books issued and returned per member
- ✅ Hash table-based O(1) member lookups by phone

### 📤 Book Issuance & Returns
- ✅ Issue books to members with automatic date assignment
- ✅ 14-day default loan period
- ✅ Return books and mark as completed
- ✅ Overdue tracking with visual alerts
- ✅ Queue-based FIFO issue management
- ✅ View all active and returned books per member

### 📊 Activity Tracking
- ✅ Complete activity log with timestamps
- ✅ Track all operations (add, delete, issue, return)
- ✅ Stack-based LIFO activity history for recent-first display
- ✅ Filter and view historical data

### 🎨 User Interface
- ✅ Modern, responsive design
- ✅ Real-time table updates
- ✅ Color-coded status indicators
- ✅ Toast notifications for user feedback
- ✅ Modal dialogs for forms
- ✅ Search and filter functionality
- ✅ Professional dashboard with statistics

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling with flexbox and grid
- **Vanilla JavaScript** - No framework dependencies, pure ES6+
- **Fetch API** - Asynchronous HTTP requests

### Backend
- **Python Flask** - Lightweight REST API framework
- **Python subprocess** - C++ executable communication

### Data Layer
- **C++** - High-performance data operations
- **CSV Files** - Persistent data storage

### Algorithms & Data Structures Used
- **Linked List** - Book inventory management (O(n) insert/delete)
- **Hash Table** - Member fast lookup by phone (O(1) average)
- **Queue (FIFO)** - Book issuance tracking
- **Stack (LIFO)** - Activity history
- **Binary Search** - Book lookup optimization (O(log n))

---

## 📁 Project Structure

```
library/
├── app.py                          # Flask REST API endpoint
├── library.cpp                     # Core C++ data operations
├── library.exe                     # Compiled C++ executable
├── library.csv                     # Book inventory data
├── members.csv                     # Member database
├── issued_books.csv               # Book issuance tracking
├── activity.csv                   # Activity log
├── users.csv                      # User authentication
│
├── templates/
│   ├── index.html                 # Home/Login page
│   ├── signup.html                # Member signup page
│   ├── login.html                 # User login page
│   └── dashboard.html             # Main dashboard (1000+ lines)
│
└── static/
    ├── create.png                 # UI icons
    ├── image.png
    ├── logo.png
    └── /css                       # Stylesheets (included in HTML)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- C++ compiler (MinGW or GCC)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask
   ```

3. **Compile C++ code**
   ```bash
   g++ -o library.exe library.cpp
   ```

4. **Run the Flask application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 📖 Usage Guide

### Login/Signup
- Create an account to access the library system
- Credentials are stored in `users.csv`

### Adding Books
1. Go to **📚 Books** tab
2. Click **"+ Add New Book"** button
3. Fill in book details (title, author, category, price, rating)
4. Submit to add to library

### Managing Members
1. Go to **👥 Members** tab
2. Click **"+ Add New Member"** button
3. Enter member details (name, email, phone, address)
4. System auto-generates 4-char alphanumeric ID (e.g., A3K9)
5. View issued books using **"📚 View"** button

### Issuing Books
1. Go to **📚 Books** tab
2. Click **"ISSUE"** button on any book
3. Enter member ID when prompted
4. Automatic issue date + 14-day due date assigned
5. Book appears in **"Issued Books"** tab

### Returning Books
1. Go to **📋 Issued Books** tab
2. Click **"✅ Return"** button
3. Book marked as returned
4. Activity logged with timestamp

### Viewing Activity
1. Go to **📊 Activity** tab
2. See all operations with timestamps
3. Recent activities shown first (LIFO)

---

## 🔍 API Endpoints

### Books
```
GET  /get_books              → Get all books
POST /add_book               → Add new book
POST /delete_book            → Delete book by ID
POST /search_book            → Search by ID
POST /issue_book             → Issue book to member
POST /return_book            → Return book
GET  /get_issued             → Get all issued books
```

### Members
```
GET  /get_members            → Get all members
POST /add_member             → Add new member
POST /delete_member          → Delete member by phone
```

### Activity
```
GET  /get_activity           → Get activity log
```

### Authentication
```
POST /login                  → User login
POST /signup                 → User registration
```

---

## 🗄️ Data Formats

### library.csv (Books)
```
ID,Name,Author,Category,Price,Rating,Issue_Count,Available
1001,To Kill a Mockingbird,Harper Lee,Fiction,299,4.8,1,true
1002,1984,George Orwell,Fiction,350,4.7,0,true
```

### members.csv (Members)
```
ID,Name,Email,Phone,Address
A3K9,satyam,m4740600@gmail.com,7209809471,bgbdgkjs
B7M2,john,john@example.com,9876543210,New York
```

### issued_books.csv (Issuance Tracking)
```
book_id,member_id,issue_date,due_date,returned
1001,A3K9,2024-01-15,2024-01-29,true
1001,A3K9,2026-04-02,2026-04-16,false
```

### activity.csv (Activity Log)
```
timestamp,action,details
1700000000,ADD_BOOK,Added book: To Kill a Mockingbird
1700000100,ISSUE_BOOK,Book 1001 issued to member A3K9
```

---

## 🎯 Key Algorithms

### Binary Search (Book Lookup)
- **Time Complexity**: O(log n)
- **Use Case**: Fast book ID lookup
- **Implementation**: Sorted book list with binary search

### Hash Table (Member Lookup)
- **Time Complexity**: O(1) average, O(n) worst
- **Hash Key**: Member phone number
- **Use Case**: Quick member retrieval by phone

### Queue (FIFO)
- **Operations**: Enqueue (issue), Dequeue (return)
- **Use Case**: Track book issuance in order
- **Time Complexity**: O(1) for both operations

### Stack (LIFO)
- **Operations**: Push (log activity), Pop (display)
- **Use Case**: Activity history (recent first)
- **Time Complexity**: O(1) for both operations

---

## 🐛 Bug Fixes & Improvements

### Version History

**v1.0 - Initial Release**
- ✅ Fixed CSV parsing for titles with commas
- ✅ Implemented member alphanumeric ID generation
- ✅ Fixed book issuance with string member IDs
- ✅ Added comprehensive duplicate prevention
- ✅ Removed 77+ comments from codebase
- ✅ Added detailed algorithm documentation

---

## 📝 Code Examples

### JavaScript - Issue Book
```javascript
async function issueBook(id) {
    let member = prompt("Enter Member ID:");
    if(!member) return;

    let formData = new FormData();
    formData.append('book_id', id);
    formData.append('member_id', member);
    formData.append('issue_date', new Date().toISOString().split('T')[0]);
    formData.append('due_date', new Date(Date.now() + 14*24*60*60*1000).toISOString().split('T')[0]);

    let response = await fetch('/issue_book', {method: 'POST', body: formData});
    let data = await response.json();
    
    if(data.status === 'success') {
        toast("📤 Book Issued Successfully");
        await loadBooks();
        render();
    }
}
```

### C++ - Queue Data Structure
```cpp
class IssuedBooksQueue {
public:
    IssuedNode* front;
    IssuedNode* rear;
    
    void issueBook(int book_id, string member_id, string issue_date, string due_date) {
        IssuedNode* newNode = new IssuedNode();
        newNode->book_id = book_id;
        newNode->member_id = member_id;
        newNode->issue_date = issue_date;
        newNode->due_date = due_date;
        newNode->returned = false;
        
        if(rear == NULL) {
            front = rear = newNode;
        } else {
            rear->next = newNode;
            rear = newNode;
        }
    }
};
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Guidelines
- Follow existing code style
- Add comments for complex logic
- Update README for new features
- Test thoroughly before submitting

---

## 📋 Future Enhancements

- [ ] Fine system for overdue books
- [ ] Email notifications for due dates
- [ ] Book recommendations based on member history
- [ ] Database migration from CSV to SQLite/MongoDB
- [ ] User roles (Admin, Librarian, Member)
- [ ] Book reservations system
- [ ] Member renewal/expiry dates
- [ ] Advanced reporting and statistics
- [ ] REST API documentation with Swagger
- [ ] Docker containerization

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👨‍💻 Author

**Satyam** - Full Stack Developer

- GitHub: [@yourgithubusername](https://github.com/yourgithubusername)
- Email: m4740600@gmail.com

---

## 🙏 Acknowledgments

- Clean Code principles
- Data Structures & Algorithms best practices
- Responsive web design patterns
- C++ STL containers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact via email
- Check existing issues for solutions

---

## 📊 Statistics

- **Book Database**: 93+ books
- **Data Structures**: 4 (Linked List, Hash Table, Queue, Stack)
- **API Endpoints**: 10+
- **Code Lines**: 2000+
- **HTML/CSS/JS**: 1000+ lines
- **C++**: 500+ lines

---

**⭐ If you found this helpful, please give it a star on GitHub!**

Happy Reading! 📚✨
