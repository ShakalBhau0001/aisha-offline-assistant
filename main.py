import random
import time
import sys
import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def save_chat(history):
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        for speaker, message in history:
            f.write(f"{speaker}: {message}\n")


def display_message(role, message, color="magenta"):
    if role == "user":
        panel = Panel(
            message,
            title="[bold cyan]You[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    else:
        panel = Panel(
            message,
            title=f"[bold {color}]Aisha[/bold {color}]",
            border_style=color,
            box=box.ROUNDED,
        )
    console.print(panel)


def show_welcome():
    console.clear()
    title = Text("🤖 AISHA AI BOT", style="bold magenta")
    console.print(
        Panel(
            title,
            subtitle="Offline • Smart Memory • Beginner Friendly",
            border_style="magenta",
            box=box.DOUBLE,
        )
    )
    console.print("[bold green]Type 'help' to see commands[/bold green]\n")


def help_table():
    table = Table(title="Available Commands", box=box.ROUNDED)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("hello / hi", "Greet Aisha")
    table.add_row("my name is ___", "Store your name")
    table.add_row("what is my name", "Recall your name")
    table.add_row("joke", "Hear a joke")
    table.add_row("quote", "Motivation quote")
    table.add_row("weather", "Offline weather")
    table.add_row("time", "Current time")
    table.add_row("date", "Today's date")
    table.add_row("color", "Change theme color")
    table.add_row("help", "Show help menu")
    table.add_row("bye / exit", "Exit & save chat")

    return table


#  AI Core Logic (Offline Mode) - Simple Pattern Matching and Random Responses


def offline_ai(user_input, memory):
    text = user_input.lower().strip()

    # Storing Name
    name_match = re.search(r"my name is ([a-zA-Z ]+)", text)
    if name_match:
        name = name_match.group(1).strip().title()
        memory["name"] = name
        return f"Nice to meet you {name}. I will remember your name."

    # Recalling Name
    if "what is my name" in text or "do you remember my name" in text:
        if memory.get("name"):
            return f"Your name is {memory['name']}."
        else:
            return "You haven't told me your name yet."

    # Knowledge Base
    knowledge = {
        "python": "Python is a powerful and beginner-friendly programming language.",
        "ai": "Artificial Intelligence enables machines to simulate human intelligence.",
        "future": "The future belongs to those who work consistently.",
        "motivation": "Discipline is more powerful than motivation.",
        "security": "Always use strong passwords and enable 2FA.",
    }

    for key in knowledge:
        if key in text:
            return knowledge[key]

    # Emotion Detection
    if "sad" in text:
        return "It's okay to feel sad sometimes. Things will improve."
    if "happy" in text:
        return "Glad to hear that. Keep smiling."

    # Default Responses
    generic = [
        "Interesting. Tell me more.",
        "I'm running in offline mode.",
        "Can you explain that more clearly?",
        "That’s something to think about.",
    ]

    return random.choice(generic)


def get_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!",
    ]
    return random.choice(jokes)


def get_quote():
    quotes = [
        "Believe you can and you're halfway there.",
        "Dream big. Start small. Act now.",
        "Push yourself, because no one else will do it for you.",
    ]
    return random.choice(quotes)


def local_weather():
    conditions = ["Sunny ☀️", "Cloudy ☁️", "Windy 🌬️", "Rainy 🌧️"]
    temp = random.randint(18, 35)
    humidity = random.randint(30, 80)
    return f"{random.choice(conditions)}, {temp}°C, Humidity {humidity}%"


def chatbot():
    show_welcome()

    history = []
    memory = {}
    colors = ["magenta", "green", "cyan", "yellow", "blue"]
    current_color = "magenta"

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            history.append(("You", user_input))

            text = user_input.lower()

            # Exit
            if text in ["bye", "exit", "quit", "goodbye", "see you"]:
                response = "Goodbye. Chat history saved locally."
                display_message("bot", response, current_color)
                history.append(("Aisha", response))
                save_chat(history)
                console.print(f"\nTotal messages: {len(history)}")
                break

            # Help
            elif text == "help":
                console.print(help_table())
                continue

            # Greeting
            elif text in ["hello", "hi", "hey"]:
                response = "Hello! How can I help you today?"
                display_message("bot", response, current_color)

            # Joke
            elif "joke" in text:
                response = get_joke()
                display_message("bot", response, current_color)

            # Quote
            elif "quote" in text:
                response = get_quote()
                display_message("bot", response, current_color)

            # Weather
            elif text == "weather":
                response = local_weather()
                display_message("bot", response, current_color)

            # Time
            elif text == "time":
                now = datetime.now().strftime("%I:%M %p")
                response = f"Current time is {now}."
                display_message("bot", response, current_color)

            # Date
            elif text == "date":
                today = datetime.now().strftime("%d %B %Y")
                response = f"Today's date is {today}."
                display_message("bot", response, current_color)

            # Change Color
            elif text == "color":
                new_color = random.choice([c for c in colors if c != current_color])
                current_color = new_color
                response = f"Theme changed to {new_color}."
                display_message("bot", response, current_color)

            # AI Core
            else:
                response = offline_ai(user_input, memory)
                display_message("bot", response, current_color)

            history.append(("Aisha", response))

        except KeyboardInterrupt:
            console.print("\n[bold red]Chat interrupted.[/bold red]")
            break


if __name__ == "__main__":
    try:
        chatbot()
    except ImportError:
        console.print("Install required library: pip install rich")
        sys.exit(1)
