import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'college.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ── intents table ──────────────────────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS intents (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT UNIQUE NOT NULL,
            response TEXT NOT NULL
        )
    ''')

    # ── training_phrases table ─────────────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS training_phrases (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            intent_id INTEGER NOT NULL,
            phrase    TEXT NOT NULL,
            FOREIGN KEY (intent_id) REFERENCES intents(id)
        )
    ''')

    # ── SEED DATA ──────────────────────────────────────────────────────────────
    data = [
        {
            "name": "greet",
            "response": (
                "👋 Hello! Welcome to SREC Nandyal Assistant.\n\n"
                "I can help you with:\n"
                "• Admissions & eligibility\n"
                "• Fee structure\n"
                "• Courses & departments\n"
                "• Placements & packages\n"
                "• Hostel & facilities\n"
                "• Contact & location\n\n"
                "What would you like to know? 😊"
            ),
            "phrases": [
                "hi", "hello", "hey", "good morning", "good afternoon",
                "good evening", "hii", "helo", "namaste", "hai", "sup",
                "howdy", "greetings", "what's up", "help me", "start"
            ]
        },
        {
            "name": "admission",
            "response": (
                "📋 Admission Process at SREC\n\n"
                "Eligibility: 10+2 / Intermediate with Physics, Chemistry & Maths (min 45%)\n\n"
                "Via AP EAMCET:\n"
                "→ Register at apeamcet.nic.in\n"
                "→ Attend web counselling with rank\n"
                "→ Select SREC Nandyal in college choices\n\n"
                "Management Quota:\n"
                "→ Direct admission available\n"
                "→ Visit admissions office with documents\n\n"
                "Key Dates 2025:\n"
                "• EAMCET Exam: May 2025\n"
                "• Counselling: June–July 2025\n"
                "• Classes Begin: August 2025\n\n"
                "📞 Admissions: +91-8514-233933"
            ),
            "phrases": [
                "admission", "apply", "how to join", "eligibility", "eamcet",
                "jee", "counselling", "enroll", "registration", "last date",
                "joining", "how to get admission", "admission process",
                "when is admission", "admission open", "direct admission",
                "management quota", "application form", "documents required"
            ]
        },
        {
            "name": "fees",
            "response": (
                "💰 Fee Structure 2025–26\n\n"
                "Branch → Annual Fee:\n"
                "• CSE → ₹95,000\n"
                "• ECE → ₹90,000\n"
                "• EEE → ₹85,000\n"
                "• Mech (ME) → ₹85,000\n"
                "• Civil (CE) → ₹82,000\n\n"
                "Hostel: ₹55,000/year (meals included)\n\n"
                "Scholarships:\n"
                "✓ AP SC/ST/BC fee reimbursement\n"
                "✓ Merit-based scholarships\n"
                "✓ Minority scholarships\n\n"
                "💡 Fees may vary slightly. Contact office for latest details."
            ),
            "phrases": [
                "fee", "fees", "tuition", "cost", "charges", "payment",
                "scholarship", "cse fee", "ece fee", "eee fee", "mechanical fee",
                "civil fee", "how much", "fee structure", "annual fee",
                "total fee", "fee per year", "hostel fee", "fee details",
                "how much does it cost", "what is the fee"
            ]
        },
        {
            "name": "placements",
            "response": (
                "🏢 Placement Highlights 2024\n\n"
                "Top Recruiters:\n"
                "TCS · Infosys · Wipro · Cognizant · HCL · Tech Mahindra · Capgemini · Hexaware · Accenture\n\n"
                "Stats:\n"
                "• Placement rate: 95%+ (CSE/ECE)\n"
                "• Highest package: ₹18 LPA\n"
                "• Average package: ₹4.5 LPA\n"
                "• Companies visited: 50+\n\n"
                "Pre-Placement Training:\n"
                "→ Aptitude & coding bootcamps\n"
                "→ Mock interviews & GDs\n"
                "→ Soft skills & communication\n\n"
                "📩 placements@srec.ac.in"
            ),
            "phrases": [
                "placement", "job", "recruit", "company", "hire", "campus",
                "package", "salary", "lpa", "offer", "tcs", "infosys",
                "wipro", "cognizant", "placement rate", "highest package",
                "average package", "campus recruitment", "job offers",
                "companies visiting", "placement cell"
            ]
        },
        {
            "name": "hostel",
            "response": (
                "🏨 Hostel Facilities\n\n"
                "Boys Hostel: 4 blocks · 1,200 capacity\n"
                "Girls Hostel: 2 blocks · 600 capacity\n\n"
                "Amenities:\n"
                "✓ High-speed Wi-Fi (10 Mbps)\n"
                "✓ Hygienic mess – 3 meals/day\n"
                "✓ Medical room + doctor on-call\n"
                "✓ 24/7 security & CCTV\n"
                "✓ Indoor games & gym\n"
                "✓ Laundry facility\n"
                "✓ Common rooms & study halls\n\n"
                "Annual Fee: ₹55,000 (all meals included)\n\n"
                "📞 Hostel Office: +91-8514-233935"
            ),
            "phrases": [
                "hostel", "accommodation", "stay", "room", "mess", "food",
                "boys hostel", "girls hostel", "lodge", "boarding",
                "dormitory", "hostel fee", "hostel facilities", "hostel food",
                "hostel wifi", "hostel security", "is hostel available"
            ]
        },
        {
            "name": "courses",
            "response": (
                "📚 Programmes at SREC\n\n"
                "B.Tech (4 Years):\n"
                "• CSE – Computer Science & Engineering\n"
                "• ECE – Electronics & Communication\n"
                "• EEE – Electrical & Electronics\n"
                "• ME – Mechanical Engineering\n"
                "• CE – Civil Engineering\n\n"
                "M.Tech (2 Years):\n"
                "• CSE, VLSI Design, Structural Engineering\n\n"
                "MBA (2 Years):\n"
                "• Business Administration\n\n"
                "Total Intake: ~1,200 seats/year\n\n"
                "All programmes AICTE approved & affiliated to JNTUA University."
            ),
            "phrases": [
                "course", "branch", "department", "programme", "b.tech",
                "m.tech", "mba", "mca", "btech", "stream", "cse", "ece",
                "eee", "mechanical", "civil", "what courses", "available courses",
                "which branch", "engineering branches", "specialization",
                "computer science", "electronics"
            ]
        },
        {
            "name": "contact",
            "response": (
                "📞 Contact SREC Nandyal\n\n"
                "🏛️ Address:\n"
                "Santhiram Engineering College\n"
                "Nandyal, Kurnool Dist.\n"
                "Andhra Pradesh – 518 501\n\n"
                "📱 Phone: +91-8514-233933\n"
                "✉️ Email: info@srec.ac.in\n"
                "🌐 Web: www.srec.ac.in\n\n"
                "Office Hours:\n"
                "Mon–Fri: 9:00 AM – 5:00 PM\n"
                "Sat: 9:00 AM – 1:00 PM\n\n"
                "📍 3 km from Nandyal Railway Station"
            ),
            "phrases": [
                "contact", "phone", "email", "address", "location",
                "where", "how to reach", "map", "office", "principal",
                "number", "phone number", "college address", "contact details",
                "how to contact", "reach srec", "college location"
            ]
        },
        {
            "name": "facilities",
            "response": (
                "🏫 Campus Facilities\n\n"
                "🔬 Labs: 40+ well-equipped modern labs\n"
                "📖 Library: 50,000+ books & digital journals\n"
                "🏋️ Sports: Cricket, Football, Basketball, Volleyball\n"
                "🌐 Internet: 1 Gbps campus-wide Wi-Fi\n"
                "🏥 Medical: On-campus clinic + visiting doctor\n"
                "🍽️ Canteen: Multi-cuisine food court\n"
                "🚌 Transport: College buses from city areas\n"
                "🎭 Auditorium: 2,000-seat capacity"
            ),
            "phrases": [
                "facility", "facilities", "lab", "library", "sports",
                "gym", "canteen", "campus", "infrastructure", "internet",
                "wifi", "wi-fi", "auditorium", "transport", "bus",
                "medical", "clinic", "campus life", "labs available"
            ]
        },
        {
            "name": "about",
            "response": (
                "🎓 About SREC Nandyal\n\n"
                "Santhiram Engineering College was established in 2001, "
                "located in Nandyal, Andhra Pradesh.\n\n"
                "Key Facts:\n"
                "• Affiliated to JNTU Anantapur\n"
                "• Approved by AICTE, New Delhi\n"
                "• NBA Accredited departments\n"
                "• NAAC 'B++' Grade\n"
                "• 25+ years of excellence\n"
                "• 15,000+ proud alumni worldwide\n\n"
                "Vision: To be a globally recognised institution for technical education, innovation, and research."
            ),
            "phrases": [
                "about", "srec", "college", "established", "founded",
                "rank", "naac", "nba", "accreditation", "history", "info",
                "tell me about", "what is srec", "college details",
                "santhiram", "about the college", "college info"
            ]
        },
        {
            "name": "transport",
            "response": (
                "🚌 Transport Facilities\n\n"
                "SREC operates college buses covering major routes in and around Nandyal.\n\n"
                "Routes available from:\n"
                "• Nandyal City\n"
                "• Kurnool\n"
                "• Atmakur\n"
                "• Banaganapalle\n"
                "• Allagadda\n\n"
                "Annual Bus Pass: ₹15,000 – ₹22,000 (varies by distance)\n\n"
                "📞 Transport Office: +91-8514-233933 Ext. 204"
            ),
            "phrases": [
                "transport", "bus", "bus route", "college bus", "commute",
                "how to come", "distance", "conveyance", "vehicle",
                "travel", "pick up", "drop"
            ]
        },
        {
            "name": "thanks",
            "response": (
                "😊 You're welcome! I'm always here to help.\n\n"
                "Feel free to ask if you have any more questions about SREC. "
                "Good luck with your future! 🎓"
            ),
            "phrases": [
                "thank", "thanks", "thank you", "ok", "okay", "great",
                "perfect", "got it", "noted", "helpful", "bye", "goodbye",
                "see you", "that's all", "done", "amazing", "awesome"
            ]
        }
    ]

    for item in data:
        # Insert or ignore intent
        c.execute(
            "INSERT OR IGNORE INTO intents (name, response) VALUES (?, ?)",
            (item["name"], item["response"])
        )
        # Get its id
        c.execute("SELECT id FROM intents WHERE name = ?", (item["name"],))
        intent_id = c.fetchone()["id"]

        # Insert phrases (skip duplicates)
        for phrase in item["phrases"]:
            c.execute(
                "SELECT 1 FROM training_phrases WHERE intent_id=? AND phrase=?",
                (intent_id, phrase)
            )
            if not c.fetchone():
                c.execute(
                    "INSERT INTO training_phrases (intent_id, phrase) VALUES (?, ?)",
                    (intent_id, phrase)
                )

    conn.commit()
    conn.close()
    print("[DB] Database initialised with all intents and training phrases.")

def get_all_training_data():
    """Return list of (phrase, intent_name) tuples for model training."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT tp.phrase, i.name
        FROM training_phrases tp
        JOIN intents i ON tp.intent_id = i.id
    ''')
    rows = c.fetchall()
    conn.close()
    return [(row["phrase"], row["name"]) for row in rows]

def get_response_for_intent(intent_name):
    """Return the response text for a given intent name."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT response FROM intents WHERE name = ?", (intent_name,))
    row = c.fetchone()
    conn.close()
    return row["response"] if row else None

if __name__ == "__main__":
    init_db()
