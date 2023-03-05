## ApnaMart Backend Assignment

---

- Django REST, Postgresql, redis

## database

- For now, Only 3 tables are there in database

1. **User** (Student) - Custom Django User Model
2. **Subject**
3. **SubjectExam**

   | Student    | Subject     | SubjectExam     |
   | ---------- | ----------- | --------------- |
   | id (PK)    | Id (PK)     | Id (PK)         |
   | email      | name        | student_id (FK) |
   | password   | Code        | subject_id (FK) |
   | title      | description | marks           |
   | first_name | created_at  | exam_type       |
   | last_name  | updated_at  | created_at      |
   | gender     |             | updated_at      |
   | created_at |             |                 |
   | updated_at |             |                 |
   | is_active  |             |                 |
   | is_admin   |             |                 |

## Redis Cache

- add cache at 3 place

1. get all subjects from DB
2. get all subject_exam from DB
3. on performance API which calculating overall exam report

## API collection

### 6 APIs

- For Auth
  - register (POST)
  - login(POST)

All APIs protected by JWT access tokens are listed below (TOKEN_LIFETIME = half day - 720min)

- For get Student Profile
  - profile (GET)
- For Subject & Subject Exam
  - subjects (GET) - get all subjects
  - subject-exam (POST) - enter subject exam marks (Only admin have access)
- Result (Performance)
  - performance (POST)

### Register - POST

Body

```json
{
  "title": "Mr",
  "first_name": "Eren",
  "last_name": "Yeager",
  "gender": "Male",
  "email": "eren@student.com",
  "password": "eren@student.com"
}
```

Response

```json
{
  "message": "Registration successful",
  "data": {
    "title": "Mr",
    "first_name": "Eren",
    "last_name": "Yeager",
    "gender": "Male",
    "email": "eren@student.com"
  }
}
```

### Login (JWT Token Authentication) - POST

Body

```json
{
  "email": "eren@student.com",
  "password": "eren@student.com"
}
```

Response

```json
{
  "message": "Login successful",
  "tokens": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MDc3NjExLCJpYXQiOjE2NzgwMzQ0MTEsImp0aSI6IjM5NjcxMTE5YjM4NDRhODc4NGEyNDQ1OWY2MTBjNzRmIiwidXNlcl9pZCI6M30.MPHI4feetL9Mk61fJqlmDYYr9SDFTRyO_I46xg-gBfE"
  }
}
```

### Student Profile - GET

Header

```header
Authorization: Bearer <access_token>
```

Response

```json
{
  "id": 3,
  "email": "eren@student.com",
  "title": "Mr",
  "first_name": "Eren",
  "last_name": "Yeager",
  "gender": "Male"
}
```

### subject-exam - POST (enter subject exam marks) only admin can access

Header

```header
Authorization: Bearer <access_token>
```

Body

```json
{
  "subjectExamData": [
    {
      "subject_id": 2,
      "student_id": 3,
      "marks": 26,
      "exam_type": "MID-2"
    },
    {
      "subject_id": 1,
      "student_id": 3,
      "marks": 86,
      "exam_type": "MID-3"
    }
  ]
}
```

### performance - GET

Header

```header
Authorization: Bearer <access_token>
```

Response **(CACHED)**

```json
{
  "Overall Percentage": {
    "value": 49.11,
    "type": "percentage"
  },
  "Lowest Exam Score": {
    "student_id": 2,
    "subject_id": 1,
    "marks": 12.0,
    "exam_type": "MID-2",
    "subject_name": "Operating Systems"
  },
  "Highest Exam Score": {
    "student_id": 2,
    "subject_id": 1,
    "marks": 86.0,
    "exam_type": "MID-3",
    "subject_name": "Operating Systems"
  },
  "Highest Exam Score Board": [
    {
      "student_id": 2,
      "subject_id": 1,
      "marks": 86.0,
      "exam_type": "MID-3",
      "subject_name": "Operating Systems"
    },
    {
      "student_id": 2,
      "subject_id": 5,
      "marks": 79.0,
      "exam_type": "MID-3",
      "subject_name": "Database Management Systems"
    }
  ]
}
```
