import json
import matplotlib.pyplot as plt

# ================= USERS =================
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def register():
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/student): ")

    users[username] = {"password": password, "role": role}
    save_users(users)
    print("User registered successfully!")

def login():
    users = load_users()
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == password:
        print("Login successful!")
        return users[username]["role"], username
    else:
        print("Invalid credentials!")
        return None, None

# ================= QUESTIONS =================
def load_questions():
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_questions(questions):
    with open("questions.json", "w") as f:
        json.dump(questions, f)

def add_question():
    questions = load_questions()
    q = input("Enter question: ")
    options = {
        "A": input("Option A: "),
        "B": input("Option B: "),
        "C": input("Option C: "),
        "D": input("Option D: ")
    }
    answer = input("Correct option (A/B/C/D): ").upper()

    questions.append({"question": q, "options": options, "answer": answer})
    save_questions(questions)
    print("Question added!")

def view_questions():
    questions = load_questions()

    if not questions:
        print("No Questions Available")
        return

    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['question']}")
        for key, val in q["options"].items():
            print(f"   {key}: {val}")
        print("Answer:", q["answer"])

# ================= QUIZ =================
def attempt_quiz():
    questions = load_questions()

    if not questions:
        print("No Quiz Available")
        return []

    answers = []

    for q in questions:
        print("\n", q["question"])
        for key, val in q["options"].items():
            print(f"{key}: {val}")
        ans = input("Your answer: ").upper()
        answers.append(ans)

    return answers

def evaluate(answers):
    questions = load_questions()
    score = 0

    for i in range(len(questions)):
        if answers[i] == questions[i]["answer"]:
            score += 1

    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    return score, percentage

# ================= RESULTS =================
def load_results():
    try:
        with open("results.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f)

def store_result(username, score):
    results = load_results()
    results[username] = score
    save_results(results)

# ================= ANALYTICS =================
def analytics():
    results = load_results()
    scores = list(results.values())

    if not scores:
        print("No data available")
        return

    avg = sum(scores) / len(scores)
    print("Average Score:", avg)
    print("Highest Score:", max(scores))
    print("Lowest Score:", min(scores))

# ================= GRAPHS =================
def plot_scores():
    results = load_results()

    if not results:
        print("No data to plot")
        return

    names = list(results.keys())
    scores = list(results.values())

    plt.figure()
    plt.bar(names, scores)
    plt.title("Student Scores")
    plt.xlabel("Students")
    plt.ylabel("Scores")
    plt.show()

def plot_pass_fail():
    results = load_results()

    if not results:
        print("No data")
        return

    pass_count = 0
    fail_count = 0
    total_questions = 5

    for score in results.values():
        percentage = (score / total_questions) * 100
        if percentage >= 40:
            pass_count += 1
        else:
            fail_count += 1

    plt.figure()
    plt.pie([pass_count, fail_count], labels=["Pass", "Fail"], autopct='%1.1f%%')
    plt.title("Pass vs Fail")
    plt.show()

def plot_trend():
    results = load_results()

    if not results:
        print("No data")
        return

    scores = list(results.values())

    plt.figure()
    plt.plot(scores, marker='o')
    plt.title("Performance Trend")
    plt.xlabel("Attempts")
    plt.ylabel("Scores")
    plt.show()

# ================= REPORT =================
def generate_report(username, score, percentage):
    print("\n===== REPORT =====")
    print("Student:", username)
    print("Score:", score)
    print("Percentage:", percentage)

    if percentage >= 40:
        print("Status: PASS")
    else:
        print("Status: FAIL")

# ================= MAIN =================
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            register()

        elif choice == "2":
            role, username = login()

            if role == "admin":
                while True:
                    print("\n1. Add Question\n2. View Questions\n3. Analytics + Graphs\n4. Logout")
                    admin_choice = input("Choose option: ")

                    if admin_choice == "1":
                        add_question()
                    elif admin_choice == "2":
                        view_questions()
                    elif admin_choice == "3":
                        analytics()
                        plot_scores()
                        plot_pass_fail()
                        plot_trend()
                    elif admin_choice == "4":
                        break

            elif role == "student":
                answers = attempt_quiz()
                if answers:
                    score, percentage = evaluate(answers)
                    generate_report(username, score, percentage)
                    store_result(username, score)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
