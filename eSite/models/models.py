from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, ARRAY
from sqlalchemy.orm import sessionmaker, relationship

# Replace with your database connection details
engine = create_engine('postgresql://user:password@host:port/database_name')

# Base class for all models
class Base:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Define your models (replace with your actual schema)
class Faculty(Base):
    __tablename__ = 'faculty'
    faculty_id = Column(Integer, primary_key=True)
    faculty_name = Column(VARCHAR, nullable=False)

class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(VARCHAR, nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id'), nullable=False)

class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer, primary_key=True)
    course_code = Column(VARCHAR, unique=True, nullable=False)
    course_name = Column(VARCHAR, nullable=False)
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)
    
    
class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(80), nullable=False)
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)

class Lecturer(Base):
    __tablename__ = 'lecturer'
    lecturer_id = Column(Integer, primary_key=True)
    full_name = Column(VARCHAR, nullable=False)
    profile_photo = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False)
    courses_taught = Column(ARRAY(Integer), nullable=False)
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)

class Class(Base):
    __tablename__ = 'class'
    class_id = Column(Integer, primary_key=True)
    class_name = Column(VARCHAR, nullable=False)
    level_of_study = Column(VARCHAR, nullable=False)
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)

class Attendance(Base):
    __tablename__ = 'attendance'
    attendance_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('class.class_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.student_id'), nullable=False)
    taken_at = Column(Date, nullable=False)
    attendance_status = Column(Boolean, nullable=False)

class Log(Base):
    __tablename__ = 'log'
    log_id = Column(Integer, primary_key=True)
    action = Column(VARCHAR, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create database tables (if not already exist)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()