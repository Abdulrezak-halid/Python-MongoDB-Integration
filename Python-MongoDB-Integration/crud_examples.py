"""
MongoDB CRUD Operations with PyMongo
Subject: Python & MongoDB Integration
Topics: CRUD, aggregate(), find_one(), count_documents(), DataFrame conversion
Student No: [INSERT YOUR STUDENT NUMBER]
"""

from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Connection
client = MongoClient("mongodb://localhost:27017")
db = client["school"]
students = db["students"]


# ============================================================================
# 1. CREATE (INSERT) OPERATIONS
# ============================================================================

def create_operations():
    """Create/Insert documents into MongoDB collection"""
    print("\n=== CREATE OPERATIONS ===\n")
    
    # Insert single document
    print("1. Insert Single Document:")
    student1 = {
        "name": "Ahmet Yılmaz",
        "student_id": "STU001",
        "age": 21,
        "dept": "CS",
        "gpa": 3.8,
        "enrolled_date": datetime.now()
    }
    result = students.insert_one(student1)
    print(f"   Inserted document ID: {result.inserted_id}")
    
    # Insert multiple documents
    print("\n2. Insert Multiple Documents:")
    students_data = [
        {
            "name": "Fatima Ahmed",
            "student_id": "STU002",
            "age": 20,
            "dept": "ENG",
            "gpa": 3.6,
            "enrolled_date": datetime.now()
        },
        {
            "name": "Hassan Ali",
            "student_id": "STU003",
            "age": 22,
            "dept": "CS",
            "gpa": 3.9,
            "enrolled_date": datetime.now()
        },
        {
            "name": "Aisha Mohamed",
            "student_id": "STU004",
            "age": 21,
            "dept": "MATH",
            "gpa": 3.7,
            "enrolled_date": datetime.now()
        }
    ]
    result = students.insert_many(students_data)
    print(f"   Inserted {len(result.inserted_ids)} documents")
    print(f"   IDs: {result.inserted_ids}")


# ============================================================================
# 2. READ OPERATIONS (find, find_one)
# ============================================================================

def read_operations():
    """Read documents from MongoDB collection"""
    print("\n=== READ OPERATIONS ===\n")
    
    # find_one: Get first matching document
    print("1. find_one() - Get Single Document:")
    doc = students.find_one({"dept": "CS"})
    if doc:
        print(f"   Found: {doc['name']} - {doc['student_id']}")
    
    # find: Get all documents
    print("\n2. find() - Get All Documents:")
    count = 0
    for student in students.find():
        count += 1
        print(f"   {count}. {student['name']} ({student['student_id']}) - {student['dept']}")
    
    # find with filter
    print("\n3. find() with Filter (dept='CS'):")
    cs_students = students.find({"dept": "CS"})
    for student in cs_students:
        print(f"   - {student['name']}: GPA {student['gpa']}")
    
    # find with projection
    print("\n4. find() with Projection (select specific fields):")
    docs = students.find({}, {"name": 1, "student_id": 1, "dept": 1, "_id": 0})
    for doc in docs:
        print(f"   {doc}")


# ============================================================================
# 3. COUNT DOCUMENTS
# ============================================================================

def count_operations():
    """Count documents in collection"""
    print("\n=== COUNT DOCUMENTS ===\n")
    
    # Count all documents
    print("1. Total Documents in Collection:")
    total = students.count_documents({})
    print(f"   Total: {total}")
    
    # Count with filter
    print("\n2. Count Documents by Department:")
    cs_count = students.count_documents({"dept": "CS"})
    eng_count = students.count_documents({"dept": "ENG"})
    math_count = students.count_documents({"dept": "MATH"})
    
    print(f"   CS: {cs_count}")
    print(f"   ENG: {eng_count}")
    print(f"   MATH: {math_count}")
    
    # Count with complex filter
    print("\n3. Count with Condition (GPA > 3.7):")
    high_gpa = students.count_documents({"gpa": {"$gt": 3.7}})
    print(f"   Students with GPA > 3.7: {high_gpa}")


# ============================================================================
# 4. UPDATE OPERATIONS
# ============================================================================

def update_operations():
    """Update documents in MongoDB collection"""
    print("\n=== UPDATE OPERATIONS ===\n")
    
    # Update single document
    print("1. Update Single Document:")
    result = students.update_one(
        {"student_id": "STU001"},
        {"$set": {"age": 22, "gpa": 3.85}}
    )
    print(f"   Modified: {result.modified_count} document(s)")
    
    # Update multiple documents
    print("\n2. Update Multiple Documents (Increment GPA for CS students):")
    result = students.update_many(
        {"dept": "CS"},
        {"$inc": {"gpa": 0.1}}
    )
    print(f"   Modified: {result.modified_count} document(s)")
    
    # Upsert operation
    print("\n3. Upsert Operation (Update or Insert):")
    result = students.update_one(
        {"student_id": "STU999"},
        {"$set": {
            "name": "New Student",
            "student_id": "STU999",
            "dept": "CS",
            "gpa": 3.5
        }},
        upsert=True
    )
    print(f"   Upserted: {result.upserted_id if result.upserted_id else 'Updated'}")


# ============================================================================
# 5. AGGREGATION PIPELINE
# ============================================================================

def aggregation_operations():
    """Aggregate data using MongoDB aggregation pipeline"""
    print("\n=== AGGREGATION OPERATIONS ===\n")
    
    # Group by department and calculate average GPA
    print("1. Group by Department - Average GPA:")
    pipeline1 = [
        {
            "$group": {
                "_id": "$dept",
                "avg_gpa": {"$avg": "$gpa"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"avg_gpa": -1}}
    ]
    
    for doc in students.aggregate(pipeline1):
        print(f"   {doc['_id']}: Avg GPA={doc['avg_gpa']:.2f}, Count={doc['count']}")
    
    # Match and project
    print("\n2. Filter (Match) and Select Fields:")
    pipeline2 = [
        {"$match": {"gpa": {"$gte": 3.7}}},
        {"$project": {"name": 1, "student_id": 1, "gpa": 1, "_id": 0}},
        {"$sort": {"gpa": -1}}
    ]
    
    for doc in students.aggregate(pipeline2):
        print(f"   {doc['name']} ({doc['student_id']}): {doc['gpa']}")
    
    # Complex aggregation
    print("\n3. Complex Aggregation - Top Students by Dept:")
    pipeline3 = [
        {"$sort": {"gpa": -1}},
        {"$group": {
            "_id": "$dept",
            "top_student": {"$first": "$name"},
            "highest_gpa": {"$first": "$gpa"},
            "students": {"$sum": 1}
        }},
        {"$project": {
            "department": "$_id",
            "top_student": 1,
            "highest_gpa": 1,
            "students": 1,
            "_id": 0
        }}
    ]
    
    for doc in students.aggregate(pipeline3):
        print(f"   {doc['department']}: {doc['top_student']} (GPA: {doc['highest_gpa']})")


# ============================================================================
# 6. DELETE OPERATIONS
# ============================================================================

def delete_operations():
    """Delete documents from MongoDB collection"""
    print("\n=== DELETE OPERATIONS ===\n")
    
    # Delete single document
    print("1. Delete Single Document (STU999):")
    result = students.delete_one({"student_id": "STU999"})
    print(f"   Deleted: {result.deleted_count} document(s)")
    
    # Delete multiple documents
    print("\n2. Delete Multiple Documents (GPA < 3.5):")
    result = students.delete_many({"gpa": {"$lt": 3.5}})
    print(f"   Deleted: {result.deleted_count} document(s)")


# ============================================================================
# 7. PANDAS DATAFRAME CONVERSION
# ============================================================================

def dataframe_operations():
    """Convert MongoDB data to Pandas DataFrame"""
    print("\n=== DATAFRAME CONVERSION ===\n")
    
    # Fetch all data and convert to DataFrame
    print("1. Convert All Data to DataFrame:")
    data = list(students.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    print("\nDataFrame:")
    print(df)
    print(f"\nShape: {df.shape}")
    
    # DataFrame operations
    print("\n2. DataFrame Analysis:")
    print(f"\nDepartment Distribution:")
    print(df['dept'].value_counts())
    
    print(f"\nGPA Statistics:")
    print(df['gpa'].describe())
    
    print(f"\nAverage GPA by Department:")
    print(df.groupby('dept')['gpa'].mean())
    
    # Export to CSV
    print("\n3. Export to CSV:")
    csv_file = "/home/abod/Workspace/Projects/Python-MongoDB-Integration/students.csv"
    df.to_csv(csv_file, index=False)
    print(f"   Exported to: {csv_file}")
    
    # Export to Excel
    print("\n4. Export to Excel:")
    excel_file = "/home/abod/Workspace/Projects/Python-MongoDB-Integration/students.xlsx"
    try:
        df.to_excel(excel_file, index=False, sheet_name="Students")
        print(f"   Exported to: {excel_file}")
    except Exception as e:
        print(f"   Note: Excel export requires openpyxl ({e})")
    
    return df


# ============================================================================
# 8. COMPLETE WORKFLOW
# ============================================================================

def main():
    """Main function to run all operations"""
    
    print("\n" + "="*70)
    print("MONGODB CRUD OPERATIONS WITH PYMONGO")
    print("="*70)
    
    # Clear collection for fresh start
    students.delete_many({})
    print("\n[Database cleaned - Starting fresh]")
    
    # Run all operations
    create_operations()
    read_operations()
    count_operations()
    aggregation_operations()
    update_operations()
    dataframe_operations()
    
    # Final count
    print("\n=== FINAL STATUS ===")
    print(f"Total documents in collection: {students.count_documents({})}")
    
    print("\n" + "="*70)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure MongoDB is running on localhost:27017")
