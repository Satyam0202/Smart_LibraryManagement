# Contributing to Library Management System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the Library Management System.

---

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report issues professionally

---

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/library-management.git
cd library
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask
```

### 3. Compile C++ (if modifying)
```bash
g++ -o library.exe library.cpp
```

### 4. Run Tests
```bash
python -m pytest tests/
```

---

## Development Workflow

### Creating a Branch
```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### Making Changes

1. **Keep commits focused** - One feature/fix per commit
2. **Write clear commit messages:**
   ```
   feature: Add member search functionality
   
   - Implemented full-text search for members
   - Added search filter in Members tab
   - Performance: O(n) linear search
   ```

3. **Update relevant files:**
   - Code changes
   - Updated README if functionality changed
   - Updated CHANGELOG.md

### Testing Your Changes

```bash
# Test Flask endpoints
python app.py

# Test C++ compilation
g++ -o library.exe library.cpp

# Manual testing
# 1. Open http://localhost:5000
# 2. Test the new feature
# 3. Check browser console (F12) for errors
```

---

## Code Style Guidelines

### Python (Flask)
```python
# Use PEP 8 style
def get_member_books(member_id):
    """Get all books issued to a member."""
    try:
        # Implementation
        pass
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
```

### C++
```cpp
// Use clear variable names
string member_id = argv[3];
int book_id = stoi(argv[2]);

// Add comments for complex logic
// Hash table lookup by phone number (O(1) average)
MemberNode* member = table[hashFunction(phone)];
```

### JavaScript
```javascript
// Use modern ES6+ syntax
async function issueBook(id) {
    const formData = new FormData();
    formData.append('book_id', id);
    
    const response = await fetch('/issue_book', {
        method: 'POST',
        body: formData
    });
    
    return await response.json();
}
```

---

## Pull Request Process

### 1. Before Submitting
- [ ] Your code follows the style guidelines
- [ ] You've tested your changes thoroughly
- [ ] You've updated the README (if needed)
- [ ] You've updated CHANGELOG.md
- [ ] Your commits are clear and focused
- [ ] No debug code or console.log() statements

### 2. Submit Pull Request
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How to test your changes

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] No new warnings generated
- [ ] Documentation updated
```

### 3. Review Process
- Maintainers will review your PR
- Address feedback constructively
- Make requested changes
- PR will be merged once approved

---

## Reporting Bugs

### Issue Format
```markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Go to 'X'
2. Click on 'Y'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots
(if applicable)

## Environment
- OS: Windows 10
- Python: 3.9
- Browser: Chrome 120
```

### Bug Priority
- **Critical**: System crash, data loss
- **High**: Feature broken, major UI issue
- **Medium**: Minor feature issue
- **Low**: Enhancement suggestion

---

## Feature Requests

### Template
```markdown
## Feature Description
What feature would you like?

## Use Case
Why is this needed?

## Example
How would it be used?

## Implementation Ideas
Any suggestions on how to implement?
```

---

## Documentation

### Code Documentation
```python
def add_member(name, email, phone):
    """
    Add a new member to the library.
    
    Args:
        name (str): Member's full name
        email (str): Valid email address
        phone (str): Phone number
        
    Returns:
        dict: {'status': 'success', 'member_id': 'A3K9'}
        
    Raises:
        ValueError: If email or phone already exists
    """
```

### Updating README
- Add new features to Features section
- Update API endpoints if needed
- Update data formats if modified
- Add usage examples

---

## Performance Considerations

### Benchmarks
- Binary search lookups: O(log n)
- Hash table member lookup: O(1) average
- Queue operations: O(1)
- CSV file operations: O(n)

### Optimization Tips
- Use hash table for O(1) lookups
- Avoid nested loops when possible
- String operations should be careful
- CSV parsing should be efficient

---

## Security Guidelines

- **Input Validation**: Always validate user input
- **Error Handling**: Don't expose internal errors
- **Data Privacy**: Store sensitive data securely
- **SQL Injection**: Not applicable (CSV-based)
- **XSS Prevention**: Sanitize output in templates

---

## Build & Deploy

### Local Development
```bash
python app.py
# Server runs on http://localhost:5000
```

### Testing Before Deploy
```bash
# Clear cache
rm -rf __pycache__

# Recompile C++
g++ -o library.exe library.cpp

# Full system test
python app.py
# Test all features manually
```

---

## Project Structure
```
library/
├── app.py              # Flask endpoints
├── library.cpp         # Core C++ logic
├── library.exe         # Compiled binary
├── templates/          # HTML files
│   └── dashboard.html  # Main interface
├── static/             # Images/assets
├── README.md           # Documentation
├── CONTRIBUTING.md     # This file
├── CHANGELOG.md        # Version history
└── LICENSE             # MIT License
```

---

## Roadmap

### Short Term
- [ ] Fine system for overdue books
- [ ] Email notifications
- [ ] Advanced filtering

### Medium Term
- [ ] Database migration to SQLite
- [ ] User roles (Admin/Librarian)
- [ ] Book reservations

### Long Term
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Integration with library vendors

---

## Questions?

- Check existing issues and discussions
- Open a new discussion for questions
- Email: m4740600@gmail.com

---

## Thank You!

Your contributions help make this project better. We appreciate all help! 🎉
