# MongoDB & Python Integration - Homework Assignment

## Overview
This project demonstrates **Python and MongoDB integration** using PyMongo, covering all essential CRUD operations, aggregation pipelines, document counting, and data export to Pandas DataFrames.

**Subject:** Python & MongoDB Integration  
**Course:** Distributed Database Systems

---

## Assignment Topics

The assignment covers the following topics:

1. **CRUD Operations** (Create, Read, Update, Delete)
2. **find() and find_one()** - Query operations
3. **count_documents()** - Document counting with filters
4. **aggregate()** - Aggregation pipeline for complex queries
5. **DataFrame Conversion** - Export data to Pandas for analysis

---

## Project Structure

```
Python-MongoDB-Integration/
│
├── Python-MongoDB-Integration/
│   ├── crud_examples.py           # Complete CRUD implementation with MongoDB
│   ├── crud_demo.py                # Demo version (no MongoDB server required)
│   └── generate_homework_doc.py    # Word document generator
│
├── MongoDB_Homework_STU001.docx    # Generated homework submission document
├── students_demo.csv               # Sample exported data
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB 4.0 or higher (for crud_examples.py)
- pip package manager

### Step 1: Create Virtual Environment
```bash
cd Python-MongoDB-Integration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install pymongo pandas python-docx --default-timeout=1000
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 3: Start MongoDB (if using crud_examples.py)
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or if installed locally
mongod
```

---

## Files Description

### 1. `crud_examples.py` (Production Version)
**Requires:** Live MongoDB server on localhost:27017

Complete implementation with all operations:
- ✅ CREATE: insert_one(), insert_many()
- ✅ READ: find(), find_one()
- ✅ COUNT: count_documents()
- ✅ UPDATE: update_one(), update_many()
- ✅ AGGREGATE: Pipeline operations with $group, $match, $project
- ✅ DELETE: delete_one(), delete_many()
- ✅ DataFrame: Conversion and export

**Run:**
```bash
python Python-MongoDB-Integration/crud_examples.py
```

### 2. `crud_demo.py` (Demo Version - No Server Required)
**Standalone version** with mock MongoDB collection for testing.

Features all operations without requiring a running MongoDB server:
- Perfect for learning and testing
- Same API as real PyMongo
- Immediate results

**Run:**
```bash
python Python-MongoDB-Integration/crud_demo.py
```

### 3. `generate_homework_doc.py`
Generates a professional Word document (.docx) for homework submission.

**Contents:**
- Assignment purpose and objectives
- 7 query blocks with complete code examples
- Explanations for each operation
- Key MongoDB concepts
- Connection setup guide

**Run:**
```bash
python Python-MongoDB-Integration/generate_homework_doc.py
```

When prompted, enter:
- Student Number: (e.g., STU001)
- Full Name: (e.g., Your Name)

**Output:** `MongoDB_Homework_[StudentNumber].docx`

---

## MongoDB Query Examples

### 1. CREATE (Insert)
```python
# Insert single document
students.insert_one({
    "name": "Ahmed",
    "student_id": "STU001",
    "dept": "CS",
    "gpa": 3.8
})

# Insert multiple documents
students.insert_many([
    {"name": "Student 1", "student_id": "STU001"},
    {"name": "Student 2", "student_id": "STU002"}
])
```

### 2. READ (Query)
```python
# find_one() - First match
first_student = students.find_one({"dept": "CS"})

# find() - All matches
cs_students = students.find({"dept": "CS"})

# With projection (select fields)
students.find({}, {"name": 1, "gpa": 1, "_id": 0})

# With filter
students.find({"gpa": {"$gte": 3.7}})
```

### 3. COUNT
```python
# Count all
total = students.count_documents({})

# Count with filter
cs_count = students.count_documents({"dept": "CS"})

# Count with condition
high_gpa = students.count_documents({"gpa": {"$gt": 3.7}})
```

### 4. UPDATE
```python
# Update single document
students.update_one(
    {"student_id": "STU001"},
    {"$set": {"gpa": 3.9}}
)

# Update multiple documents
students.update_many(
    {"dept": "CS"},
    {"$inc": {"gpa": 0.1}}
)

# Upsert (update or insert)
students.update_one(
    {"student_id": "STU999"},
    {"$set": {"name": "New"}},
    upsert=True
)
```

### 5. AGGREGATION
```python
# Group and calculate statistics
pipeline = [
    {
        "$group": {
            "_id": "$dept",
            "avg_gpa": {"$avg": "$gpa"},
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"avg_gpa": -1}}
]
students.aggregate(pipeline)
```

### 6. DELETE
```python
# Delete single document
students.delete_one({"student_id": "STU999"})

# Delete multiple documents
students.delete_many({"gpa": {"$lt": 3.5}})
```

### 7. DATAFRAME
```python
import pandas as pd

# Convert to DataFrame
data = list(students.find({}))
df = pd.DataFrame(data)

# Export
df.to_csv("students.csv")
df.to_excel("students.xlsx")
```

---

## MongoDB Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$gt` | Greater than | `{"gpa": {"$gt": 3.5}}` |
| `$gte` | Greater or equal | `{"gpa": {"$gte": 3.7}}` |
| `$lt` | Less than | `{"age": {"$lt": 25}}` |
| `$lte` | Less or equal | `{"age": {"$lte": 22}}` |
| `$eq` | Equal | `{"dept": {"$eq": "CS"}}` |
| `$ne` | Not equal | `{"dept": {"$ne": "CS"}}` |
| `$in` | In array | `{"dept": {"$in": ["CS", "ENG"]}}` |
| `$nin` | Not in array | `{"dept": {"$nin": ["CS"]}}` |

---

## Aggregation Pipeline Stages

| Stage | Purpose | Example |
|-------|---------|---------|
| `$match` | Filter documents | `{"$match": {"gpa": {"$gte": 3.7}}}` |
| `$project` | Select fields | `{"$project": {"name": 1, "gpa": 1}}` |
| `$group` | Group by field | `{"$group": {"_id": "$dept"}}` |
| `$sort` | Sort results | `{"$sort": {"gpa": -1}}` |
| `$limit` | Limit results | `{"$limit": 10}` |
| `$skip` | Skip documents | `{"$skip": 5}` |
| `$unwind` | Unwind array | `{"$unwind": "$array_field"}` |

---

## Output Examples

### CSV Export
```csv
name,student_id,age,dept,gpa,enrolled_date
Ahmet Yılmaz,STU001,21,CS,3.8,2024-11-26
Fatima Ahmed,STU002,20,ENG,3.6,2024-11-26
Hassan Ali,STU003,22,CS,3.9,2024-11-26
```

### DataFrame Display
```
           name student_id  age dept   gpa
0  Ahmet Yılmaz     STU001   21   CS  3.80
1  Fatima Ahmed     STU002   20  ENG  3.60
2    Hassan Ali     STU003   22   CS  3.90
```

---

## Troubleshooting

### MongoDB Connection Refused
**Error:** `Connection refused` when running crud_examples.py

**Solution:**
1. Ensure MongoDB is running
2. Check connection string: `mongodb://localhost:27017`
3. Verify MongoDB port: Default is 27017
4. Use Docker: `docker run -d -p 27017:27017 mongo:latest`

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'pymongo'`

**Solution:**
```bash
source venv/bin/activate
pip install pymongo pandas python-docx
```

### CSV Export Issues
**Error:** When exporting, ensure the path is writable

**Solution:**
```bash
# Change to project directory
cd /home/abod/Workspace/Projects/Python-MongoDB-Integration
python Python-MongoDB-Integration/crud_demo.py
```

---

## Homework Submission

### Generate Your Submission Document

1. Run the document generator:
```bash
python Python-MongoDB-Integration/generate_homework_doc.py
```

2. Enter your details when prompted:
   - Student Number
   - Full Name

3. A Word document will be created: `MongoDB_Homework_[StudentNumber].docx`

### Document Contents
- ✅ Assignment purpose
- ✅ Query blocks for all 7 topics
- ✅ Complete code examples
- ✅ Explanations
- ✅ MongoDB concepts reference
- ✅ Timestamp and student info

### File Requirements
- **Format:** .docx (Word)
- **Naming:** MongoDB_Homework_[StudentNumber].docx
- **Example:** MongoDB_Homework_STU001.docx

---

## Key Learning Outcomes

After completing this assignment, you should be able to:

✅ Connect to MongoDB using PyMongo  
✅ Implement CRUD operations  
✅ Use find() and find_one() for queries  
✅ Count documents with filters  
✅ Use aggregation pipelines for complex analysis  
✅ Convert MongoDB data to Pandas DataFrames  
✅ Export data to CSV and Excel formats  

---

## Additional Resources

- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python-docx Documentation](https://python-docx.readthedocs.io/)

---

## Notes

- All scripts use Python 3.8+ syntax
- MongoDB collections are JSON-like documents
- Ensure virtual environment is activated before running
- For production use, implement proper error handling and validation
- Use `crud_demo.py` for learning without MongoDB dependency

---

**Assignment Status:** Complete ✅

