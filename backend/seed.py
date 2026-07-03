"""
Seed script: populates the database with Nigeria JSS 1 curriculum
and default badges. Run once after running migrations.

Usage:
    python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.curriculum import Subject, Term, Topic
from app.models.gamification import Badge
from app.models.quiz import Quiz, Question, DifficultyEnum


def seed_badges(db):
    badges = [
        {"name": "5-Day Streak",  "description": "Study 5 days in a row",   "icon": "🔥", "xp_bonus": 50},
        {"name": "10-Day Streak", "description": "Study 10 days in a row",  "icon": "⚡", "xp_bonus": 100},
        {"name": "30-Day Streak", "description": "Study 30 days in a row",  "icon": "🏆", "xp_bonus": 300},
        {"name": "Maths Wizard",  "description": "Score 100% on a Maths quiz", "icon": "🧮", "xp_bonus": 75},
        {"name": "Science Star",  "description": "Score 100% on a Science quiz", "icon": "🔬", "xp_bonus": 75},
        {"name": "Most Improved", "description": "Improve score by 30+ points", "icon": "📈", "xp_bonus": 100},
        {"name": "Challenge Winner", "description": "Win a class challenge", "icon": "🥇", "xp_bonus": 200},
    ]
    for b in badges:
        if not db.query(Badge).filter(Badge.name == b["name"]).first():
            db.add(Badge(**b))
    db.commit()
    print(f"  ✓ {len(badges)} badges seeded")


def seed_nigeria_jss1(db):
    subjects_data = [
        {
            "name": "Mathematics",
            "icon": "📐",
            "terms": [
                {
                    "number": 1,
                    "topics": [
                        ("Whole Numbers", "Understanding and working with whole numbers up to millions."),
                        ("Basic Operations", "Addition, subtraction, multiplication and division of whole numbers."),
                        ("Factors and Multiples", "Finding factors, multiples, HCF and LCM."),
                        ("Fractions", "Types of fractions, equivalent fractions, and basic operations."),
                    ]
                },
                {
                    "number": 2,
                    "topics": [
                        ("Decimals", "Decimal notation, place value, and operations with decimals."),
                        ("Percentages", "Converting fractions to percentages and solving percentage problems."),
                        ("Basic Algebra", "Introduction to algebraic expressions and simple equations."),
                    ]
                },
                {
                    "number": 3,
                    "topics": [
                        ("Geometry: Lines and Angles", "Types of lines, angles, and basic geometric properties."),
                        ("Perimeter and Area", "Calculating perimeter and area of common shapes."),
                        ("Statistics: Data Collection", "Collecting, organising, and presenting data."),
                    ]
                },
            ]
        },
        {
            "name": "English Language",
            "icon": "📖",
            "terms": [
                {
                    "number": 1,
                    "topics": [
                        ("Parts of Speech", "Nouns, pronouns, verbs, adjectives, adverbs, and their uses."),
                        ("Comprehension Skills", "Reading passages and answering questions accurately."),
                        ("Essay Writing: Narrative", "Writing personal and imaginative narrative essays."),
                    ]
                },
                {
                    "number": 2,
                    "topics": [
                        ("Tenses", "Present, past, and future tenses with examples."),
                        ("Punctuation", "Full stops, commas, question marks, exclamation marks."),
                        ("Letter Writing", "Formal and informal letter formats."),
                    ]
                },
                {
                    "number": 3,
                    "topics": [
                        ("Vocabulary Development", "Word meanings, synonyms, antonyms, and contextual usage."),
                        ("Oral English: Sounds", "Vowels, consonants, and basic phonetics."),
                        ("Summary Writing", "Identifying main ideas and writing concise summaries."),
                    ]
                },
            ]
        },
        {
            "name": "Basic Science",
            "icon": "🔬",
            "terms": [
                {
                    "number": 1,
                    "topics": [
                        ("Living and Non-Living Things", "Characteristics of living things and examples."),
                        ("Cells: The Unit of Life", "Plant and animal cells, their parts and functions."),
                        ("Nutrition in Plants", "Photosynthesis, mineral salts, and plant food."),
                    ]
                },
                {
                    "number": 2,
                    "topics": [
                        ("Human Digestive System", "Organs of digestion and how food is processed."),
                        ("The Skeletal System", "Bones, joints, and functions of the skeleton."),
                        ("Simple Machines", "Levers, pulleys, inclined planes, and their applications."),
                    ]
                },
                {
                    "number": 3,
                    "topics": [
                        ("States of Matter", "Solid, liquid, gas — properties and changes of state."),
                        ("Light and Sound", "Sources of light, reflection, sound production and travel."),
                        ("Basic Ecology", "Ecosystems, food chains, and environmental balance."),
                    ]
                },
            ]
        },
    ]

    for s_data in subjects_data:
        subject = db.query(Subject).filter(
            Subject.name == s_data["name"], Subject.grade == "JSS 1"
        ).first()

        if not subject:
            subject = Subject(
                name=s_data["name"],
                country="Nigeria",
                grade="JSS 1",
                icon=s_data["icon"],
            )
            db.add(subject)
            db.flush()

        for t_data in s_data["terms"]:
            term = db.query(Term).filter(
                Term.subject_id == subject.id, Term.number == t_data["number"]
            ).first()

            if not term:
                term = Term(
                    subject_id=subject.id,
                    number=t_data["number"],
                    name=f"Term {t_data['number']}",
                )
                db.add(term)
                db.flush()

            for order, (title, summary) in enumerate(t_data["topics"]):
                if not db.query(Topic).filter(
                    Topic.subject_id == subject.id,
                    Topic.term_id == term.id,
                    Topic.title == title,
                ).first():
                    topic = Topic(
                        subject_id=subject.id,
                        term_id=term.id,
                        title=title,
                        summary=summary,
                        order=order,
                    )
                    db.add(topic)
                    db.flush()

                    # Seed one practice quiz per topic
                    _seed_sample_quiz(db, topic, subject.name)

    db.commit()
    print("  ✓ Nigeria JSS 1 curriculum seeded (Mathematics, English, Basic Science)")


def _seed_sample_quiz(db, topic, subject_name):
    quiz = Quiz(
        topic_id=topic.id,
        title=f"{topic.title} — Practice Quiz",
        time_limit_seconds=300,
        is_ranked=False,
        passing_score=60,
        xp_reward=30,
    )
    db.add(quiz)
    db.flush()

    # Generic placeholder question — real questions would be authored or AI-generated
    question = Question(
        quiz_id=quiz.id,
        text=f"This is a sample question about '{topic.title}' in {subject_name}. What is the correct answer?",
        options={"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
        correct_answer="A",
        explanation=f"Option A is correct. See the topic notes on '{topic.title}' for a full explanation.",
        difficulty=DifficultyEnum.easy,
        points=1,
        order=1,
    )
    db.add(question)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Seeding database...")
        seed_badges(db)
        seed_nigeria_jss1(db)
        print("Done.")
    finally:
        db.close()
