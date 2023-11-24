import requests
import json
import html
from datetime import datetime

def show_question(question):
    global points

    print()
    print(html.unescape(question["question"]))

    for i, option in enumerate(question["answers"], start=1):
        print(f"{chr(96 + i)}:", html.unescape(option))

    print()

    answer_mapping = {chr(96 + i): question["answers"][i-1].lower() for i in range(1, len(question["answers"])+1)}

    while True:
        answer = input("Which answer do you choose? ").lower()

        try:
            if answer not in answer_mapping:
                raise ValueError("Give a letter from a-d.")

            
            if answer_mapping[answer] == question["correct_answer"].lower():
                points += 1
                print("That's the correct answer, bravo! You already have", points, "points.")
                break
            else:
                print(f"Unfortunately this is the wrong answer, the correct answer is {question['correct_answer']}.")
                break
        except ValueError as e:
            print(e)

def play_quiz():
    global points
    points = 0

    api_url = "https://opentdb.com/api.php?amount=10&type=multiple" 
    response = requests.get(api_url)
    questions_data = json.loads(response.text)

    questions = []
    for item in questions_data["results"]:
        question = {
            "question": item["question"],
            "answers": item["incorrect_answers"] + [item["correct_answer"]],
            "correct_answer": item["correct_answer"],
        }
        questions.append(question)

    for i in range(len(questions)):
        show_question(questions[i])

    print()
    print("This is the end of the game, the number of points scored is " + str(points) + ".")

    save_result()

def save_result():
    name = input("Enter your name: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    result = f"{name},{points},{date}\n"

    with open("ranking.txt", "a") as file:
        file.write(result)
    print("Your result has been saved.")

def show_ranking():
    try:
        with open("ranking.txt", "r") as file:
            lines = [line.strip().split(',') for line in file]
            sorted_lines = sorted(lines, key=lambda x: int(x[1]), reverse=True) 

            print("\nRanking of best results:\n")
            for i, (name, score, date) in enumerate(sorted_lines[:20], start=1):
                print(f"{i}. {name}: {score} points ({date})")
    except FileNotFoundError:
        print("No results available.")

while True:
    print("\nMenu:")
    print("1. Play Quiz")
    print("2. Ranking of best results")
    print("3. Exit the game")

    choice = input("Select the option: ")

    if choice == "1":
        play_quiz()
    elif choice == "2":
        show_ranking()
    elif choice == "3":
        print("Thank you for playing. Goodbye!")
        break
    else:
        print("Incorrect selection. Select option 1 to 3.")

