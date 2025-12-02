"""
MongoDB CRUD Operations - Demo/Test Version
This version demonstrates all MongoDB operations without requiring a live MongoDB server.
Use this for testing and understanding the concepts.
"""

import pandas as pd
from datetime import datetime
import json

# Simulate MongoDB collection with in-memory storage
class MockCollection:
    """Mock MongoDB collection for demonstration"""
    def __init__(self):
        self.data = []
        self.counter = 1
    
    def insert_one(self, doc):
        doc['_id'] = self.counter
        self.counter += 1
        self.data.append(doc)
        class Result:
            def __init__(self, doc_id):
                self.inserted_id = doc_id
        return Result(doc['_id'])
    
    def insert_many(self, docs):
        ids = []
        for doc in docs:
            doc['_id'] = self.counter
            ids.append(self.counter)
            self.counter += 1
            self.data.append(doc)
        class Result:
            def __init__(self, ids):
                self.inserted_ids = ids
        return Result(ids)
    
    def find_one(self, query=None):
        if query is None:
            return self.data[0] if self.data else None
        for doc in self.data:
            if self._match(doc, query):
                return doc
        return None
    
    def find(self, query=None, projection=None):
        results = []
        for doc in self.data:
            if query is None or self._match(doc, query):
                if projection:
                    filtered = {}
                    for key, val in projection.items():
                        if val == 1 and key in doc:
                            filtered[key] = doc[key]
                    results.append(filtered)
                else:
                    results.append(doc)
        return results
    
    def count_documents(self, query=None):
        count = 0
        for doc in self.data:
            if query is None or self._match(doc, query):
                count += 1
        return count
    
    def update_one(self, query, update):
        for doc in self.data:
            if self._match(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                class Result:
                    def __init__(self):
                        self.modified_count = 1
                return Result()
        class Result:
            def __init__(self):
                self.modified_count = 0
        return Result()
    
    def update_many(self, query, update):
        modified = 0
        for doc in self.data:
            if self._match(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                elif "$inc" in update:
                    for key, val in update["$inc"].items():
                        if key in doc:
                            doc[key] += val
                modified += 1
        class Result:
            def __init__(self, count):
                self.modified_count = count
        return Result(modified)
    
    def delete_one(self, query):
        for i, doc in enumerate(self.data):
            if self._match(doc, query):
                self.data.pop(i)
                class Result:
                    def __init__(self):
                        self.deleted_count = 1
                return Result()
        class Result:
            def __init__(self):
                self.deleted_count = 0
        return Result()
    
    def delete_many(self, query):
        deleted = 0
        for doc in list(self.data):
            if self._match(doc, query):
                self.data.remove(doc)
                deleted += 1
        class Result:
            def __init__(self, count):
                self.deleted_count = count
        return Result(deleted)
    
    def _match(self, doc, query):
        for key, value in query.items():
            if key not in doc:
                return False
            if isinstance(value, dict):
                if "$gt" in value and not (doc[key] > value["$gt"]):
                    return False
                if "$gte" in value and not (doc[key] >= value["$gte"]):
                    return False
                if "$lt" in value and not (doc[key] < value["$lt"]):
                    return False
                if "$lte" in value and not (doc[key] <= value["$lte"]):
                    return False
                if "$eq" in value and doc[key] != value["$eq"]:
                    return False
            elif doc[key] != value:
                return False
        return True


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    """Main demonstration function"""
    
    print("\n" + "="*70)
    print("MONGODB CRUD OPERATIONS DEMONSTRATION (No Server Required)")
    print("="*70)
    
    # Initialize mock collection
    students = MockCollection()
    
    # ====== CREATE ======
    print("\n=== CREATE OPERATIONS ===\n")
    print("1. Insert Single Document:")
    student1 = {
        "name": "Ahmet Yılmaz",
        "student_id": "STU001",
        "age": 21,
        "dept": "CS",
        "gpa": 3.8,
        "enrolled_date": datetime.now().strftime("%Y-%m-%d")
    }
    result = students.insert_one(student1)
    print(f"   ✓ Inserted document ID: {result.inserted_id}")
    
    print("\n2. Insert Multiple Documents:")
    students_data = [
        {"name": "Fatima Ahmed", "student_id": "STU002", "age": 20, "dept": "ENG", "gpa": 3.6},
        {"name": "Hassan Ali", "student_id": "STU003", "age": 22, "dept": "CS", "gpa": 3.9},
        {"name": "Aisha Mohamed", "student_id": "STU004", "age": 21, "dept": "MATH", "gpa": 3.7},
        {"name": "Omar Ibrahim", "student_id": "STU005", "age": 20, "dept": "CS", "gpa": 3.5},
    ]
    result = students.insert_many(students_data)
    print(f"   ✓ Inserted {len(result.inserted_ids)} documents")
    
    # ====== READ ======
    print("\n=== READ OPERATIONS ===\n")
    print("1. find_one() - Get First CS Student:")
    doc = students.find_one({"dept": "CS"})
    if doc:
        print(f"   ✓ Found: {doc['name']} - {doc['student_id']}")
    
    print("\n2. find() - Get All Students:")
    all_students = students.find()
    for i, student in enumerate(all_students, 1):
        print(f"   {i}. {student['name']} ({student['student_id']}) - {student['dept']}: {student['gpa']}")
    
    print("\n3. find() with Filter (dept='CS'):")
    cs_students = students.find({"dept": "CS"})
    for student in cs_students:
        print(f"   • {student['name']}: GPA {student['gpa']}")
    
    print("\n4. find() with Projection (select specific fields):")
    docs = students.find({}, {"name": 1, "student_id": 1, "dept": 1})
    for doc in docs:
        print(f"   • {doc}")
    
    # ====== COUNT ======
    print("\n=== COUNT DOCUMENTS ===\n")
    print("1. Total Documents:")
    total = students.count_documents({})
    print(f"   ✓ Total students: {total}")
    
    print("\n2. Count by Department:")
    for dept in ["CS", "ENG", "MATH"]:
        count = students.count_documents({"dept": dept})
        print(f"   • {dept}: {count} students")
    
    print("\n3. Count with Condition (GPA >= 3.7):")
    high_gpa = students.count_documents({"gpa": {"$gte": 3.7}})
    print(f"   ✓ Students with GPA >= 3.7: {high_gpa}")
    
    # ====== UPDATE ======
    print("\n=== UPDATE OPERATIONS ===\n")
    print("1. Update Single Document:")
    result = students.update_one(
        {"student_id": "STU001"},
        {"$set": {"age": 22, "gpa": 3.85}}
    )
    print(f"   ✓ Modified: {result.modified_count} document(s)")
    
    print("\n2. Update Multiple Documents (Increment CS GPA by 0.1):")
    result = students.update_many(
        {"dept": "CS"},
        {"$inc": {"gpa": 0.1}}
    )
    print(f"   ✓ Modified: {result.modified_count} document(s)")
    
    # ====== AGGREGATION ======
    print("\n=== AGGREGATION OPERATIONS ===\n")
    print("1. Group by Department - Average GPA:")
    
    # Manual aggregation for demo
    dept_stats = {}
    for doc in students.find():
        dept = doc['dept']
        if dept not in dept_stats:
            dept_stats[dept] = {'total_gpa': 0, 'count': 0}
        dept_stats[dept]['total_gpa'] += doc['gpa']
        dept_stats[dept]['count'] += 1
    
    for dept in sorted(dept_stats.keys()):
        avg_gpa = dept_stats[dept]['total_gpa'] / dept_stats[dept]['count']
        count = dept_stats[dept]['count']
        print(f"   • {dept}: Avg GPA = {avg_gpa:.2f}, Count = {count}")
    
    print("\n2. Top Students (GPA >= 3.7):")
    top_students = sorted(
        [s for s in students.find() if s['gpa'] >= 3.7],
        key=lambda x: x['gpa'],
        reverse=True
    )
    for student in top_students:
        print(f"   • {student['name']} ({student['student_id']}): {student['gpa']}")
    
    # ====== DELETE ======
    print("\n=== DELETE OPERATIONS ===\n")
    print("1. Delete Document with GPA < 3.5:")
    result = students.delete_many({"gpa": {"$lt": 3.5}})
    print(f"   ✓ Deleted: {result.deleted_count} document(s)")
    
    # ====== DATAFRAME ======
    print("\n=== DATAFRAME CONVERSION ===\n")
    print("1. Convert All Data to DataFrame:")
    data = students.find({})
    df = pd.DataFrame(data)
    print("\nDataFrame:")
    print(df[['name', 'student_id', 'dept', 'gpa', 'age']])
    print(f"\nShape: {df.shape}")
    
    print("\n2. DataFrame Analysis:")
    print(f"\nDepartment Distribution:")
    print(df['dept'].value_counts())
    
    print(f"\nGPA Statistics:")
    print(df['gpa'].describe())
    
    print(f"\nAverage GPA by Department:")
    print(df.groupby('dept')['gpa'].mean())
    
    print("\n3. Export to CSV:")
    csv_file = "/home/abod/Workspace/Projects/Python-MongoDB-Integration/students_demo.csv"
    df.to_csv(csv_file, index=False)
    print(f"   ✓ Exported to: {csv_file}")
    
    # ====== FINAL STATUS ======
    print("\n=== FINAL STATUS ===")
    final_count = students.count_documents({})
    print(f"Remaining documents: {final_count}")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
