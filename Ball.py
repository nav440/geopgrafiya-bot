import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class GeographyBot:
    def __init__(self):
        self.students = {}
        self.history_file = "student_history.json"
        self.load_history()
        
        # 1-5 sinf geografiya savollar
        self.junior_questions = {
            "1": {
                "question": "Yer nechta qitaga bo'linadi?",
                "options": ["5", "6", "7", "8"],
                "answer": 1,  # 6
                "difficulty": 1
            },
            "2": {
                "question": "O'zbekiston qaysi qitada joylashgan?",
                "options": ["Afrika", "Osiyo", "Yevropa", "Avstraliya"],
                "answer": 1,  # Osiyo
                "difficulty": 1
            },
            "3": {
                "question": "Eng katta okeani nomi nima?",
                "options": ["Atlantik", "Hind", "Okhotsk", "Tinch"],
                "answer": 3,  # Tinch
                "difficulty": 2
            },
            "4": {
                "question": "Samarqand qaysi shahar?",
                "options": ["Bosh shahar", "Farg'ona viloyati", "Samarqand viloyati", "Bukhoro viloyati"],
                "answer": 2,  # Samarqand viloyati
                "difficulty": 2
            },
            "5": {
                "question": "Qaysi tog'lar O'zbekiston va Qirgiziston chegarasida?",
                "options": ["Tyan-Shan", "Pamir", "Altay", "Kavkaz"],
                "answer": 0,  # Tyan-Shan
                "difficulty": 3
            }
        }
        
        # 6-8 sinf geografiya savollar
        self.middle_questions = {
            "1": {
                "question": "O'zbekiston aholisining taxminiy soni qancha?",
                "options": ["20 million", "30 million", "35 million", "40 million"],
                "answer": 2,  # 35 million
                "difficulty": 2
            },
            "2": {
                "question": "Aral dengizi keng tushida qaysi ikki davlat joylashgan?",
                "options": ["O'zbekiston va Qozog'iston", "O'zbekiston va Qirgiziston", "Qozog'iston va Turkmaniston", "O'zbekiston va Turkmaniston"],
                "answer": 0,  # O'zbekiston va Qozog'iston
                "difficulty": 3
            },
            "3": {
                "question": "Amu-Daryo daryosi qaysi davlatlardan o'tib ketadi?",
                "options": ["O'zbekiston", "O'zbekiston, Afg'oniston, Qozog'iston", "Qirgiziston, O'zbekiston", "Turkmaniston, Qozog'iston"],
                "answer": 1,  # O'zbekiston, Afg'oniston, Qozog'iston
                "difficulty": 3
            },
            "4": {
                "question": "Qashqadaryo viloyatining merkazi qaysi shahar?",
                "options": ["Kitob", "Qarshi", "Shahrisabz", "Koson"],
                "answer": 1,  # Qarshi
                "difficulty": 2
            },
            "5": {
                "question": "Qo'qon qaysi viloyatida joylashgan?",
                "options": ["Andijon", "Farg'ona", "Namangan", "Jizzax"],
                "answer": 1,  # Farg'ona
                "difficulty": 2
            }
        }
        
        # 9-11 sinf geografiya savollar
        self.senior_questions = {
            "1": {
                "question": "Dunyoning eng baland cho'qqisi qaysi tog'da?",
                "options": ["K2", "Cho'molunga", "Kilimanjaro", "Elbrus"],
                "answer": 1,  # Cho'molunga
                "difficulty": 2
            },
            "2": {
                "question": "O'zbekiston qay sohali oqtilgan asosiy o'simliklari?",
                "options": ["Tog' o'rmonlari", "Tundra", "Cho'l o'simliklari", "Stepp o'simliklari"],
                "answer": 2,  # Cho'l o'simliklari
                "difficulty": 3
            },
            "3": {
                "question": "Dunyoning eng uzoq daryosi qaysi?",
                "options": ["Nil", "Amazon", "Yangtze", "Ob'"],
                "answer": 0,  # Nil
                "difficulty": 2
            },
            "4": {
                "question": "O'zbekiston mineral boyligining asosiy manbasi?",
                "options": ["Neft", "Temir", "Oltin va kumush", "Ko'mir"],
                "answer": 2,  # Oltin va kumush
                "difficulty": 3
            },
            "5": {
                "question": "Qashkadaryo basinining iqlimi qanday?",
                "options": ["Mot iqlim", "O'rtacha cho'l iqlimi", "Suvli tropik", "Suvsiz cho'l iqlimi"],
                "answer": 3,  # Suvsiz cho'l iqlimi
                "difficulty": 3
            }
        }

    def get_student_grade(self, student_id: str) -> int:
        """O'quvchining sinfini qaytaradi"""
        if student_id in self.students:
            return self.students[student_id].get("grade", 1)
        return 1

    def register_student(self, name: str, student_id: str, grade: int):
        """O'quvchini ro'yxatga oladi"""
        self.students[student_id] = {
            "name": name,
            "grade": grade,
            "total_questions": 0,
            "correct_answers": 0,
            "score": 0,
            "history": [],
            "registered_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_history()
        return f"✅ {name} muvaffaqiyatli ro'yxatdan o'tdi (sinf: {grade})"

    def get_questions_by_grade(self, grade: int) -> Dict:
        """Sinfga qarab savollarni qaytaradi"""
        if 1 <= grade <= 5:
            return self.junior_questions
        elif 6 <= grade <= 8:
            return self.middle_questions
        else:  # 9-11
            return self.senior_questions

    def ask_question(self, student_id: str) -> Tuple[str, List[str], str]:
        """Tasodifiy savol beradi"""
        if student_id not in self.students:
            return "❌ O'quvchi topilmadi!", [], ""
        
        grade = self.get_student_grade(student_id)
        questions = self.get_questions_by_grade(grade)
        
        q_id = str(len(self.students[student_id]["history"]) % len(questions) + 1)
        q_data = questions[q_id]
        
        return q_data["question"], q_data["options"], q_id

    def check_answer(self, student_id: str, q_id: str, answer_index: int, grade: int) -> Tuple[bool, str, int]:
        """Javobni tekshiradi"""
        if student_id not in self.students:
            return False, "❌ O'quvchi topilmadi!", 0
        
        questions = self.get_questions_by_grade(grade)
        q_data = questions[q_id]
        
        is_correct = answer_index == q_data["answer"]
        
        self.students[student_id]["total_questions"] += 1
        
        if is_correct:
            points = (q_data["difficulty"] * 10)
            self.students[student_id]["correct_answers"] += 1
            self.students[student_id]["score"] += points
            message = f"✅ To'g'ri! +{points} ball"
        else:
            message = f"❌ Noto'g'ri! To'g'ri javob: {q_data['options'][q_data['answer']]}"
        
        # Tarixga qo'shish
        self.students[student_id]["history"].append({
            "question": q_data["question"],
            "user_answer": q_data["options"][answer_index],
            "correct_answer": q_data["options"][q_data["answer"]],
            "is_correct": is_correct,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.save_history()
        return is_correct, message, self.students[student_id]["score"]

    def get_statistics(self, student_id: str) -> str:
        """O'quvchining statistikasini beradi"""
        if student_id not in self.students:
            return "❌ O'quvchi topilmadi!"
        
        student = self.students[student_id]
        total = student["total_questions"]
        
        if total == 0:
            return f"📊 {student['name']} uchun statistika:\nHali testlar o'tish boshlanmagan"
        
        correct = student["correct_answers"]
        percentage = (correct / total) * 100
        
        stats = f"""
📊 {student['name']} ning statistikasi (Sinf: {student['grade']}):
━━━━━━━━━━━━━━━━━━━━━━━━
✅ To'g'ri javoblar: {correct}/{total}
📈 Foiz: {percentage:.1f}%
🏆 Jami ball: {student['score']}
📅 Ro'yxatdan o'tilgan: {student['registered_date']}
"""
        return stats

    def get_progress(self, student_id: str) -> str:
        """O'quvchining taraqqiyotini ko'rsatadi"""
        if student_id not in self.students:
            return "❌ O'quvchi topilmadi!"
        
        student = self.students[student_id]
        history = student["history"]
        
        if not history:
            return f"📈 {student['name']} hali tarix yo'q"
        
        last_5 = history[-5:]
        progress = f"📈 {student['name']} ning so'nggi {len(last_5)} ta savoli:\n"
        progress += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for i, item in enumerate(last_5, 1):
            status = "✅" if item["is_correct"] else "❌"
            progress += f"{i}. {status} {item['question'][:40]}...\n"
        
        return progress

    def get_leaderboard(self) -> str:
        """Top o'quvchilarni ko'rsatadi"""
        if not self.students:
            return "📋 Hali o'quvchi ro'yxatda yo'q"
        
        sorted_students = sorted(
            self.students.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        leaderboard = "🏆 TOP O'QUVCHILAR:\n"
        leaderboard += "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for i, (sid, student) in enumerate(sorted_students[:10], 1):
            leaderboard += f"{i}. {student['name']} - {student['score']} ball\n"
        
        return leaderboard

    def save_history(self):
        """O'quvchilarin ma'lumotlarini saqlaydi"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.students, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Saqlangan ma'lumotlarni yuklaydi"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.students = json.load(f)
            except:
                self.students = {}


def main():
    """Bot interfeysi"""
    bot = GeographyBot()
    
    print("🌍 GEOGRAFIYA O'RGANISH BOTI 🌍")
    print("=" * 40)
    print("1. Ro'yxatdan o'tish")
    print("2. Test o'tish")
    print("3. Statistikani ko'rish")
    print("4. Taraqqiyotni ko'rish")
    print("5. TOP O'QUVCHILAR")
    print("6. Chiqish")
    print("=" * 40)
    
    while True:
        choice = input("\nTanlang (1-6): ").strip()
        
        if choice == "1":
            print("\n📝 RO'YXATDAN O'TISH")
            name = input("F.I.Sh: ").strip()
            student_id = input("O'quvchi ID: ").strip()
            grade = int(input("Sinf (1-11): ").strip())
            print(bot.register_student(name, student_id, grade))
        
        elif choice == "2":
            print("\n❓ TEST O'TISH")
            student_id = input("O'quvchi ID: ").strip()
            
            if student_id not in bot.students:
                print("❌ O'quvchi topilmadi!")
                continue
            
            while True:
                question, options, q_id = bot.ask_question(student_id)
                print(f"\n📌 Savol: {question}")
                
                for i, opt in enumerate(options, 1):
                    print(f"   {i}. {opt}")
                
                try:
                    answer = int(input("\nJavobingiz (1-4): ").strip()) - 1
                    grade = bot.get_student_grade(student_id)
                    is_correct, message, score = bot.check_answer(student_id, q_id, answer, grade)
                    print(message)
                    print(f"🏆 Jami ball: {score}")
                    
                    next_q = input("\nDavom etasiz? (ha/yo'q): ").lower()
                    if next_q != "ha":
                        break
                except ValueError:
                    print("❌ Noto'g'ri kirish!")
        
        elif choice == "3":
            print("\n📊 STATISTIKA")
            student_id = input("O'quvchi ID: ").strip()
            print(bot.get_statistics(student_id))
        
        elif choice == "4":
            print("\n📈 TARAQQIYOT")
            student_id = input("O'quvchi ID: ").strip()
            print(bot.get_progress(student_id))
        
        elif choice == "5":
            print(bot.get_leaderboard())
        
        elif choice == "6":
            print("\n👋 Xayron! O'qishni davom ettiring!")
            break
        
        else:
            print("❌ Noto'g'ri tanlov!")


if __name__ == "__main__":
    main()
