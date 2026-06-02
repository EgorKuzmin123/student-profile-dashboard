import pandas as pd
import numpy as np
import random

# Настройки
NUM_STUDENTS = 500
WEEKS = 12
FACULTIES = ['IT', 'Economics', 'Law']
COURSES = [1, 2, 3, 4]

# 1. Генерация студентов (students.csv)
students_data = []
for i in range(1, NUM_STUDENTS + 1):
    fac = random.choice(FACULTIES)
    course = random.choice(COURSES)
    group = f"{fac}-{course}0{random.randint(1, 3)}"

    # Распределение по паттернам: 0 - норма, 1 - плавный спад (15%), 2 - резкий обвал (5%)
    pattern = np.random.choice([0, 1, 2], p=[0.80, 0.15, 0.05])
    students_data.append([i, fac, course, group, pattern])

df_students = pd.DataFrame(students_data, columns=['student_id', 'faculty', 'course', 'group', 'pattern'])

# 2. Генерация академических данных и LMS (academic.csv, lms.csv)
academic_data = []
lms_data = []
offers_data = []

for _, student in df_students.iterrows():
    s_id = student['student_id']
    pattern = student['pattern']
    course = student['course']

    current_debts = 0

    for week in range(1, WEEKS + 1):
        # Базовые значения
        attendance = random.randint(80, 100)
        lms_views = random.randint(120, 300)  # минут в неделю
        hw_submitted = random.choice([1, 1, 1, 0])

        if pattern == 1:  # Плавный спад
            attendance = max(0, attendance - (week * random.randint(3, 5)))
            lms_views = max(0, lms_views - (week * random.randint(10, 20)))
            if week > 3 and random.random() < 0.3: current_debts += 1

        elif pattern == 2:  # Резкий обвал (например, с 8 недели)
            if week >= 8:
                attendance = random.randint(0, 30)
                lms_views = random.randint(0, 40)
                current_debts += random.randint(0, 1)

        # Запись Academic
        avg_score = max(2.0, 5.0 - (current_debts * 0.5) - ((100 - attendance) * 0.02))
        academic_data.append([s_id, week, attendance, current_debts, round(avg_score, 1)])

        # Запись LMS
        tests_attempts = random.randint(1, 3) if lms_views > 50 else 0
        lms_data.append([s_id, week, lms_views, hw_submitted, tests_attempts])

    # 3. Офферы (только 3-4 курс)
    if course in [3, 4]:
        num_offers = random.randint(1, 4)
        for o in range(num_offers):
            offer_id = f"OFF-{random.randint(100, 999)}"
            # Студенты в зоне риска реже смотрят офферы
            view_prob = 0.8 if pattern == 0 else 0.2
            viewed = 1 if random.random() < view_prob else 0
            responded = 1 if (viewed and random.random() < 0.3) else 0
            offers_data.append([s_id, offer_id, viewed, responded])

# Сохранение файлов (убираем служебную колонку pattern для чистоты эксперимента)
df_students.drop(columns=['pattern']).to_csv('students.csv', index=False)
pd.DataFrame(academic_data, columns=['student_id', 'week', 'attendance', 'debts', 'avg_score']).to_csv('academic.csv',
                                                                                                       index=False)
pd.DataFrame(lms_data, columns=['student_id', 'week', 'lms_views_min', 'hw_submitted', 'test_attempts']).to_csv(
    'lms.csv', index=False)
pd.DataFrame(offers_data, columns=['student_id', 'offer_id', 'viewed', 'responded']).to_csv('offers.csv', index=False)

print("Синтетические данные успешно сгенерированы: students.csv, academic.csv, lms.csv, offers.csv")