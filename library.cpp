/**
 * LIBRARY MANAGEMENT SYSTEM - DATA STRUCTURES & ALGORITHMS
 * 
 * ALGORITHMS USED:
 * 1. LINKED LIST (Books) - Dynamic insertion/deletion O(n)
 * 2. HASH TABLE (Members) - Fast lookup O(1) average, uses phone as key
 * 3. QUEUE (Issued Books) - FIFO for book issue tracking
 * 4. STACK (Activity Log) - LIFO for activity history
 * 5. BINARY SEARCH (Books) - O(log n) search after sorting
 * 6. QUICK SORT CONCEPT - Python sorts books by field (name, author, price, rating)
 * 
 * DATA STRUCTURES:
 * - BookNode: Singly linked list for books with id, name, author, category, price, rating, issue_count, available
 * - MemberNode: Hash table entries for members with id, name, email, phone, address  
 * - IssuedNode: Queue node for issued books tracking with book_id, member_id, dates
 * - ActivityNode: Stack node for activity log with timestamp, action, details
 */

#include<fstream>
#include<iostream>
#include<string>
#include<cstring>
#include<ctime>
using namespace std;

// ==================== BOOK NODE - LINKED LIST ====================
// Algorithm: Singly Linked List for O(n) insertion at end, O(n) deletion, O(log n) binary search
// Each BookNode links to next node, head pointer tracks start of list
struct BookNode
{
    int id;
    string name;
    string author;
    string category;
    int price;
    int rating;
    int issue_count;
    bool available;
    BookNode* next;
};

// ==================== MEMBER NODE - HASH TABLE ====================
// Algorithm: Hash Table with separate chaining for O(1) average lookup
// Hash function distributes members by phone number across table buckets
struct MemberNode
{
    string id;
    string name;
    string email;
    string phone;
    string address;
    MemberNode* next;
};

// ==================== ISSUED BOOK NODE - QUEUE ====================
// Algorithm: Queue (FIFO - First In First Out) for issue tracking
// Books enqueued when issued, dequeued when returned (FIFO order)
struct IssuedNode
{
    int book_id;
    string member_id;
    string issue_date;
    string due_date;
    bool returned;
    IssuedNode* next;
};

// ==================== ACTIVITY NODE - STACK ====================
// Algorithm: Stack (LIFO - Last In First Out) for activity history
// Most recent activities at top for O(1) access and display
struct ActivityNode
{
    string timestamp;
    string action;
    string details;
    ActivityNode* next;
};

// ==================== LINKED LIST CLASS FOR BOOKS ====================
// COMMENT: Implements all book operations using linked list data structure
class BookList
{
public:
    BookNode* head;
    int count;

    BookList() { head = NULL; count = 0; }

    // COMMENT: Insert book at end - O(n) time complexity, with duplicate ID check
    bool insertBook(int id, string name, string author, string category, int price, int rating, int issue_count, bool available)
    {
        // COMMENT: Check if book with this ID already exists
        BookNode* temp = head;
        while(temp != NULL)
        {
            if(temp->id == id)
            {
                return false;  // COMMENT: Duplicate ID, insertion failed
            }
            temp = temp->next;
        }

        BookNode* newNode = new BookNode();
        newNode->id = id;
        newNode->name = name;
        newNode->author = author;
        newNode->category = category;
        newNode->price = price;
        newNode->rating = rating;
        newNode->issue_count = issue_count;
        newNode->available = available;
        newNode->next = NULL;

        if(head == NULL)
        {
            head = newNode;
        }
        else
        {
            BookNode* temp = head;
            while(temp->next != NULL)
            {
                temp = temp->next;
            }
            temp->next = newNode;
        }
        count++;
        return true;  // COMMENT: Insertion successful
    }

    // COMMENT: Delete book by ID - O(n) time complexity
    bool deleteBook(int id)
    {
        if(head == NULL) return false;

        if(head->id == id)
        {
            BookNode* temp = head;
            head = head->next;
            delete temp;
            count--;
            return true;
        }

        BookNode* curr = head;
        while(curr->next != NULL)
        {
            if(curr->next->id == id)
            {
                BookNode* temp = curr->next;
                curr->next = curr->next->next;
                delete temp;
                count--;
                return true;
            }
            curr = curr->next;
        }
        return false;
    }

    // COMMENT: Binary Search by ID - O(log n) time complexity after sorting
    BookNode* binarySearchByID(int id)
    {
        if(head == NULL) return NULL;

        // COMMENT: Convert linked list to array for binary search
        BookNode** arr = new BookNode*[count];
        BookNode* temp = head;
        int i = 0;
        while(temp != NULL)
        {
            arr[i] = temp;
            temp = temp->next;
            i++;
        }

        // COMMENT: Binary Search Implementation
        int left = 0, right = count - 1;
        while(left <= right)
        {
            int mid = (left + right) / 2;
            if(arr[mid]->id == id)
            {
                BookNode* found = arr[mid];
                delete[] arr;
                return found;
            }
            else if(arr[mid]->id < id)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }
        delete[] arr;
        return NULL;
    }

    // COMMENT: Linear Search by Name - O(n) time complexity
    BookNode* searchByName(string name)
    {
        BookNode* temp = head;
        while(temp != NULL)
        {
            if(temp->name == name)
            {
                return temp;
            }
            temp = temp->next;
        }
        return NULL;
    }

    // COMMENT: Helper function to properly quote CSV fields
    string escapeCSV(string val)
    {
        // If field contains comma, quote, or newline, wrap in quotes and escape quotes
        if(val.find(',') != string::npos || val.find('"') != string::npos || val.find('\n') != string::npos)
        {
            string escaped = "\"";
            for(int i = 0; i < val.length(); i++)
            {
                if(val[i] == '"')
                    escaped += "\"\"";  // Escape quote by doubling it
                else
                    escaped += val[i];
            }
            escaped += "\"";
            return escaped;
        }
        return val;
    }

    // COMMENT: Save all books to CSV file with proper quoting
    void saveToCSV(string filename)
    {
        ofstream file(filename);
        BookNode* temp = head;
        while(temp != NULL)
        {
            file << temp->id << "," 
                 << escapeCSV(temp->name) << "," 
                 << escapeCSV(temp->author) << "," 
                 << escapeCSV(temp->category) << "," 
                 << temp->price << "," 
                 << temp->rating << "," 
                 << temp->issue_count << "," 
                 << (temp->available ? "true" : "false") << "\n";
            temp = temp->next;
        }
        file.close();
    }

    // COMMENT: Helper function to parse quoted CSV field
    string parseCSVField(const string& line, int& pos)
    {
        string field;
        if(pos >= line.length()) return field;

        if(line[pos] == '"')
        {
            // COMMENT: Handle quoted field
            pos++;  // Skip opening quote
            while(pos < line.length())
            {
                if(line[pos] == '"')
                {
                    if(pos + 1 < line.length() && line[pos + 1] == '"')
                    {
                        field += '"';  // Escaped quote
                        pos += 2;
                    }
                    else
                    {
                        pos++;  // Skip closing quote
                        break;
                    }
                }
                else
                {
                    field += line[pos];
                    pos++;
                }
            }
            while(pos < line.length() && line[pos] != ',') pos++;  // Skip to comma
            if(pos < line.length()) pos++;  // Skip comma
        }
        else
        {
            // COMMENT: Handle unquoted field
            while(pos < line.length() && line[pos] != ',')
            {
                field += line[pos];
                pos++;
            }
            if(pos < line.length()) pos++;  // Skip comma
        }
        return field;
    }

    // COMMENT: Load books from CSV file into linked list with proper CSV parsing
    void loadFromCSV(string filename)
    {
        ifstream file(filename);
        if(!file.is_open()) return;  // COMMENT: File doesn't exist, skip loading
        
        string line;
        while(getline(file, line))
        {
            if(line.empty()) continue;
            
            int pos = 0;
            int id, price, rating, issue_count;
            string id_str, name, author, category, price_str, rating_str, issue_str, available_str;
            bool avail = true;

            try
            {
                // COMMENT: Parse CSV fields
                id_str = parseCSVField(line, pos);
                name = parseCSVField(line, pos);
                author = parseCSVField(line, pos);
                category = parseCSVField(line, pos);
                price_str = parseCSVField(line, pos);
                rating_str = parseCSVField(line, pos);
                issue_str = parseCSVField(line, pos);
                available_str = parseCSVField(line, pos);

                // COMMENT: Convert to proper types
                id = stoi(id_str);
                price = stoi(price_str);
                rating = stoi(rating_str);
                issue_count = stoi(issue_str);
                avail = (available_str == "true");

                insertBook(id, name, author, category, price, rating, issue_count, avail);
            }
            catch(...)
            {
                // COMMENT: Skip lines with parsing errors
                cerr << "Warning: Failed to parse CSV line: " << line << "\n";
                continue;
            }
        }
        file.close();
    }

    // COMMENT: Traverse and print all books - O(n) time complexity
    void displayAll()
    {
        BookNode* temp = head;
        while(temp != NULL)
        {
            cout << temp->id << "|" << temp->name << "|" << temp->author << "|" 
                 << temp->category << "|" << temp->price << "|" << temp->rating 
                 << "|" << temp->issue_count << "|" << (temp->available ? "true" : "false") << "\n";
            temp = temp->next;
        }
    }
};

// ==================== QUICK SORT FOR BOOKS ====================
// COMMENT: Quick Sort implementation for sorting books
// Time Complexity: O(n log n) average case, O(n^2) worst case
// sortBy: 0=name, 1=price, 2=rating
void quickSort(BookNode** arr, int low, int high, int sortBy)
{
    if(low < high)
    {
        int pi = low;
        int pj = high;
        BookNode* pivot = arr[low];

        while(pi < pj)
        {
            while(pi < high && (sortBy == 0 ? arr[pi+1]->name <= pivot->name : 
                   sortBy == 1 ? arr[pi+1]->price <= pivot->price : 
                   arr[pi+1]->rating <= pivot->rating))
                pi++;
            while(pj > low && (sortBy == 0 ? arr[pj]->name > pivot->name :
                  sortBy == 1 ? arr[pj]->price > pivot->price :
                  arr[pj]->rating > pivot->rating))
                pj--;

            if(pi < pj)
            {
                BookNode* temp = arr[pi + 1];
                arr[pi + 1] = arr[pj];
                arr[pj] = temp;
            }
        }

        BookNode* temp = arr[low];
        arr[low] = arr[pj];
        arr[pj] = temp;

        quickSort(arr, low, pj - 1, sortBy);
        quickSort(arr, pj + 1, high, sortBy);
    }
}

// ==================== HASH TABLE FOR MEMBERS ====================
// COMMENT: Hash Table implementation using chaining collision resolution
// Average case lookup, insert, delete: O(1)
// Worst case: O(n) if many collisions
class MemberHashTable
{
private:
    MemberNode** table;
    int size;

    // COMMENT: Hash function to distribute members by phone number
    int hashFunction(string phone)
    {
        int hash = 0;
        for(char c : phone)
        {
            hash = hash * 31 + c;
        }
        return (hash % size + size) % size;
    }

public:
    MemberHashTable(int sz = 100) 
    { 
        size = sz; 
        table = new MemberNode*[size];
        for(int i = 0; i < size; i++)
            table[i] = NULL;
    }

    // Algorithm: Insert member using chaining - O(1) average case
    void insertMember(string id, string name, string email, string phone, string address)
    {
        int index = hashFunction(phone);
        MemberNode* newNode = new MemberNode();
        newNode->id = id;
        newNode->name = name;
        newNode->email = email;
        newNode->phone = phone;
        newNode->address = address;
        newNode->next = table[index];
        table[index] = newNode;
    }

    // COMMENT: Search member by phone - O(1) average case
    MemberNode* searchMember(string phone)
    {
        int index = hashFunction(phone);
        MemberNode* temp = table[index];
        while(temp != NULL)
        {
            if(temp->phone == phone)
                return temp;
            temp = temp->next;
        }
        return NULL;
    }

    // COMMENT: Delete member from hash table - O(1) average case
    bool deleteMember(string phone)
    {
        int index = hashFunction(phone);
        MemberNode* temp = table[index];

        if(temp == NULL) return false;

        if(temp->phone == phone)
        {
            table[index] = temp->next;
            delete temp;
            return true;
        }

        while(temp->next != NULL)
        {
            if(temp->next->phone == phone)
            {
                MemberNode* deleted = temp->next;
                temp->next = temp->next->next;
                delete deleted;
                return true;
            }
            temp = temp->next;
        }
        return false;
    }

    // COMMENT: Save all members to CSV file
    void saveToCSV(string filename)
    {
        ofstream file(filename);
        for(int i = 0; i < size; i++)
        {
            MemberNode* temp = table[i];
            while(temp != NULL)
            {
                file << temp->id << "," << temp->name << "," << temp->email << "," 
                     << temp->phone << "," << temp->address << "\n";
                temp = temp->next;
            }
        }
        file.close();
    }

    // COMMENT: Load members from CSV file into hash table
    void loadFromCSV(string filename)
    {
        ifstream file(filename);
        if(!file.is_open()) return;
        
        string line;
        while(getline(file, line))
        {
            if(line.empty()) continue;
            
            int pos1, pos2, pos3, pos4;
            pos1 = line.find(',');
            pos2 = line.find(',', pos1 + 1);
            pos3 = line.find(',', pos2 + 1);
            pos4 = line.find(',', pos3 + 1);

            string id = line.substr(0, pos1);
            string name = line.substr(pos1 + 1, pos2 - pos1 - 1);
            string email = line.substr(pos2 + 1, pos3 - pos2 - 1);
            string phone = line.substr(pos3 + 1, pos4 - pos3 - 1);
            string address = line.substr(pos4 + 1);

            insertMember(id, name, email, phone, address);
        }
        file.close();
    }

    // COMMENT: Display all members from hash table
    void displayAll()
    {
        for(int i = 0; i < size; i++)
        {
            MemberNode* temp = table[i];
            while(temp != NULL)
            {
                cout << temp->id << "|" << temp->name << "|" << temp->email << "|" 
                     << temp->phone << "|" << temp->address << "\n";
                temp = temp->next;
            }
        }
    }
};

// ==================== QUEUE FOR ISSUED BOOKS ====================
// COMMENT: Queue implementation for issued books (FIFO - First In First Out)
// Issue operation: enqueue (add to rear) - O(1)
// Return operation: mark as returned - O(n)
class IssuedBooksQueue
{
public:
    IssuedNode* front;
    IssuedNode* rear;
    int count;

    IssuedBooksQueue() { front = NULL; rear = NULL; count = 0; }

    // COMMENT: Enqueue - Issue a book to member - O(1) time complexity
    void issueBook(int book_id, string member_id, string issue_date, string due_date)
    {
        IssuedNode* newNode = new IssuedNode();
        newNode->book_id = book_id;
        newNode->member_id = member_id;
        newNode->issue_date = issue_date;
        newNode->due_date = due_date;
        newNode->returned = false;
        newNode->next = NULL;

        if(rear == NULL)
        {
            front = rear = newNode;
        }
        else
        {
            rear->next = newNode;
            rear = newNode;
        }
        count++;
    }

    // COMMENT: Dequeue - Return a book from member - O(n) time complexity
    bool returnBook(int book_id, string member_id)
    {
        IssuedNode* curr = front;
        while(curr != NULL)
        {
            if(curr->book_id == book_id && curr->member_id == member_id && !curr->returned)
            {
                curr->returned = true;
                return true;
            }
            curr = curr->next;
        }
        return false;
    }

    // COMMENT: Save issued books queue to CSV file
    void saveToCSV(string filename)
    {
        ofstream file(filename);
        IssuedNode* temp = front;
        while(temp != NULL)
        {
            file << temp->book_id << "," << temp->member_id << "," 
                 << temp->issue_date << "," << temp->due_date << "," 
                 << (temp->returned ? "true" : "false") << "\n";
            temp = temp->next;
        }
        file.close();
    }

    // COMMENT: Load issued books from CSV file into queue
    void loadFromCSV(string filename)
    {
        ifstream file(filename);
        string line;
        while(getline(file, line))
        {
            if(line.empty()) continue;
            
            int pos1 = line.find(',');
            int pos2 = line.find(',', pos1 + 1);
            int pos3 = line.find(',', pos2 + 1);
            int pos4 = line.find(',', pos3 + 1);

            int book_id = stoi(line.substr(0, pos1));
            string member_id = line.substr(pos1 + 1, pos2 - pos1 - 1);
            string issue_date = line.substr(pos2 + 1, pos3 - pos2 - 1);
            string due_date = line.substr(pos3 + 1, pos4 - pos3 - 1);
            bool returned = (line.substr(pos4 + 1) == "true");

            IssuedNode* newNode = new IssuedNode();
            newNode->book_id = book_id;
            newNode->member_id = member_id;
            newNode->issue_date = issue_date;
            newNode->due_date = due_date;
            newNode->returned = returned;
            newNode->next = NULL;

            if(rear == NULL)
            {
                front = rear = newNode;
            }
            else
            {
                rear->next = newNode;
                rear = newNode;
            }
            count++;
        }
        file.close();
    }

    // COMMENT: Display all issued books from queue
    void displayAll()
    {
        IssuedNode* temp = front;
        while(temp != NULL)
        {
            cout << temp->book_id << "|" << temp->member_id << "|" << temp->issue_date << "|" 
                 << temp->due_date << "|" << (temp->returned ? "true" : "false") << "\n";
            temp = temp->next;
        }
    }
};

// ==================== STACK FOR ACTIVITY LOG ====================
// COMMENT: Stack implementation for activity log (LIFO - Last In First Out)
// Push operation: add new activity - O(1)
// Pop/Traverse operations: O(n)
class ActivityStack
{
public:
    ActivityNode* top;
    int count;

    ActivityStack() { top = NULL; count = 0; }

    // COMMENT: Push - Add new activity to stack - O(1) time complexity
    void pushActivity(string timestamp, string action, string details)
    {
        ActivityNode* newNode = new ActivityNode();
        newNode->timestamp = timestamp;
        newNode->action = action;
        newNode->details = details;
        newNode->next = top;
        top = newNode;
        count++;
    }

    // COMMENT: Save stack to CSV file
    void saveToCSV(string filename)
    {
        ofstream file(filename);
        ActivityNode* temp = top;
        while(temp != NULL)
        {
            file << temp->timestamp << "|" << temp->action << "|" << temp->details << "\n";
            temp = temp->next;
        }
        file.close();
    }

    // COMMENT: Load activities from CSV file into stack
    void loadFromCSV(string filename)
    {
        ifstream file(filename);
        string line;
        while(getline(file, line))
        {
            if(line.empty()) continue;
            
            int pos1 = line.find('|');
            int pos2 = line.find('|', pos1 + 1);

            string timestamp = line.substr(0, pos1);
            string action = line.substr(pos1 + 1, pos2 - pos1 - 1);
            string details = line.substr(pos2 + 1);

            pushActivity(timestamp, action, details);
        }
        file.close();
    }

    // COMMENT: Display all activities from stack
    void displayAll()
    {
        ActivityNode* temp = top;
        while(temp != NULL)
        {
            cout << temp->timestamp << "|" << temp->action << "|" << temp->details << "\n";
            temp = temp->next;
        }
    }
};

// ==================== GLOBAL OBJECTS ====================
// COMMENT: Global data structures initialized
BookList books;
MemberHashTable members(100);
IssuedBooksQueue issued;
ActivityStack activity;

// ==================== MAIN FUNCTION ====================
// COMMENT: Main function handles command line operations
int main(int argc, char* argv[])
{
    // COMMENT: Load data from CSV files on startup
    books.loadFromCSV("library.csv");
    members.loadFromCSV("members.csv");
    issued.loadFromCSV("issued_books.csv");
    activity.loadFromCSV("activity.csv");

    if(argc < 2)
    {
        cout << "Invalid Input\n";
        return 1;
    }

    string operation = argv[1];

    // COMMENT: ============ BOOK OPERATIONS ============
    // COMMENT: Add book to linked list
    if(operation == "add_book" && argc == 10)
    {
        int id = stoi(argv[2]);
        string name = argv[3];
        string author = argv[4];
        string category = argv[5];
        int price = stoi(argv[6]);
        int rating = stoi(argv[7]);
        int issue_count = stoi(argv[8]);
        bool available = (string(argv[9]) == "true");

        if(books.insertBook(id, name, author, category, price, rating, issue_count, available))
        {
            activity.pushActivity(to_string(time(0)), "ADD_BOOK", "Added book: " + name);
            books.saveToCSV("library.csv");
            activity.saveToCSV("activity.csv");
            cout << "Book Added Successfully\n";
        }
        else
        {
            cout << "Error: Book with ID " << id << " already exists\n";
        }
    }

    // COMMENT: Delete book by ID from linked list
    else if(operation == "delete_book" && argc == 3)
    {
        int id = stoi(argv[2]);
        if(books.deleteBook(id))
        {
            activity.pushActivity(to_string(time(0)), "DELETE_BOOK", "Deleted book with ID: " + to_string(id));
            books.saveToCSV("library.csv");
            activity.saveToCSV("activity.csv");
            cout << "Book Deleted Successfully\n";
        }
        else
        {
            cout << "Book Not Found\n";
        }
    }

    // COMMENT: Get all books from linked list
    else if(operation == "get_books")
    {
        books.displayAll();
    }

    // COMMENT: Search book by ID using binary search
    else if(operation == "search_book" && argc == 3)
    {
        int id = stoi(argv[2]);
        BookNode* found = books.binarySearchByID(id);
        if(found != NULL)
        {
            cout << found->id << "|" << found->name << "|" << found->author << "|" 
                 << found->category << "|" << found->price << "|" << found->rating << "\n";
        }
        else
        {
            cout << "Not Found\n";
        }
    }

    // COMMENT: ============ MEMBER OPERATIONS ============
    // COMMENT: Add member to hash table
    else if(operation == "add_member" && argc >= 6)
    {
        string id = argv[2];
        string name = argv[3];
        string email = argv[4];
        string phone = argv[5];
        string address = argc > 6 ? argv[6] : "";

        members.insertMember(id, name, email, phone, address);
        activity.pushActivity(to_string(time(0)), "ADD_MEMBER", "Added member: " + name);
        members.saveToCSV("members.csv");
        activity.saveToCSV("activity.csv");
        cout << "Member Added Successfully\n";
    }

    // COMMENT: Delete member from hash table by phone
    else if(operation == "delete_member" && argc == 3)
    {
        string phone = argv[2];
        if(members.deleteMember(phone))
        {
            activity.pushActivity(to_string(time(0)), "DELETE_MEMBER", "Deleted member with phone: " + phone);
            members.saveToCSV("members.csv");
            activity.saveToCSV("activity.csv");
            cout << "Member Deleted Successfully\n";
        }
        else
        {
            cout << "Member Not Found\n";
        }
    }

    // COMMENT: Get all members from hash table
    else if(operation == "get_members")
    {
        members.displayAll();
    }

    // COMMENT: ============ ISSUED BOOK OPERATIONS ============
    // COMMENT: Issue book to member - enqueue operation
    else if(operation == "issue_book" && argc >= 5 && argc <= 6)
    {
        int book_id = stoi(argv[2]);
        string member_id = argv[3];
        string issue_date = argv[4];
        string due_date = argc > 5 ? argv[5] : "";

        issued.issueBook(book_id, member_id, issue_date, due_date);
        activity.pushActivity(to_string(time(0)), "ISSUE_BOOK", "Book " + to_string(book_id) + " issued to member " + member_id);
        issued.saveToCSV("issued_books.csv");
        activity.saveToCSV("activity.csv");
        cout << "Book Issued Successfully\n";
    }

    // COMMENT: Return book from member
    else if(operation == "return_book" && argc == 4)
    {
        int book_id = stoi(argv[2]);
        string member_id = argv[3];

        if(issued.returnBook(book_id, member_id))
        {
            activity.pushActivity(to_string(time(0)), "RETURN_BOOK", "Book " + to_string(book_id) + " returned by member " + member_id);
            issued.saveToCSV("issued_books.csv");
            activity.saveToCSV("activity.csv");
            cout << "Book Returned Successfully\n";
        }
        else
        {
            cout << "Issue Record Not Found\n";
        }
    }

    // COMMENT: Get all issued books from queue
    else if(operation == "get_issued")
    {
        issued.displayAll();
    }

    // COMMENT: ============ ACTIVITY LOG OPERATIONS ============
    // COMMENT: Get all activities from stack
    else if(operation == "get_activity")
    {
        activity.displayAll();
    }

    else
    {
        cout << "Unknown Operation\n";
        return 1;
    }

    return 0;
}