#!/usr/bin/env python3
"""90-Day Income Generation Tracker — $100 budget, $1000 goal."""

import json
import os
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "tracker_data.json")

STREAMS = ["freelance", "pod", "digital"]
BUDGET = 100.00
GOAL = 1000.00
DAYS = 90


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "budget_remaining": BUDGET,
        "expenses": [],
        "income": [],
    }


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_income(data, stream, amount, description):
    if stream not in STREAMS:
        print(f"Invalid stream. Choose from: {STREAMS}")
        return
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "stream": stream,
        "amount": float(amount),
        "description": description,
    }
    data["income"].append(entry)
    save_data(data)
    print(f"Added ${amount:.2f} income from {stream}: {description}")


def add_expense(data, category, amount, description):
    amount = float(amount)
    if amount > data["budget_remaining"]:
        print(f"Warning: Over budget! Remaining: ${data['budget_remaining']:.2f}")
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "amount": amount,
        "description": description,
    }
    data["expenses"].append(entry)
    data["budget_remaining"] -= amount
    save_data(data)
    print(f"Expense: ${amount:.2f} for {description}. Budget remaining: ${data['budget_remaining']:.2f}")


def dashboard(data):
    start = datetime.strptime(data["start_date"], "%Y-%m-%d")
    today = datetime.now()
    day = (today - start).days + 1
    week = (day - 1) // 7 + 1

    total_income = sum(e["amount"] for e in data["income"])
    total_expenses = sum(e["amount"] for e in data["expenses"])

    stream_totals = {s: 0 for s in STREAMS}
    for e in data["income"]:
        stream_totals[e["stream"]] += e["amount"]

    progress = total_income / GOAL * 100
    bar_len = 30
    filled = int(bar_len * min(progress, 100) / 100)

    print("\n" + "=" * 50)
    print("   90-DAY INCOME TRACKER DASHBOARD")
    print("=" * 50)
    print(f"  Day {day}/90  |  Week {week}/13")
    print(f"  Days remaining: {max(90 - day, 0)}")
    print("-" * 50)
    print(f"  TOTAL INCOME:  ${total_income:>8.2f} / $1,000.00")
    print(f"  [{'#' * filled}{'.' * (bar_len - filled)}] {progress:.1f}%")
    print("-" * 50)
    print("  INCOME BY STREAM:")
    for s in STREAMS:
        print(f"    {s:>10}: ${stream_totals[s]:>8.2f}")
    print("-" * 50)
    print(f"  BUDGET SPENT:  ${total_expenses:>8.2f} / $100.00")
    print(f"  BUDGET LEFT:   ${data['budget_remaining']:>8.2f}")
    print(f"  NET PROFIT:    ${total_income - total_expenses:>8.2f}")
    print("-" * 50)

    if day > 0:
        daily_rate = total_income / day
        remaining_needed = GOAL - total_income
        if daily_rate > 0:
            days_to_goal = remaining_needed / daily_rate
            print(f"  Daily avg:     ${daily_rate:.2f}/day")
            print(f"  Est. days to goal: {days_to_goal:.0f}")
        else:
            needed_daily = remaining_needed / max(90 - day, 1)
            print(f"  Need ${needed_daily:.2f}/day to hit goal")

    print("=" * 50 + "\n")


def show_log(data):
    print("\n--- Income Log ---")
    for e in data["income"]:
        print(f"  {e['date']}  ${e['amount']:>7.2f}  [{e['stream']}]  {e['description']}")
    print(f"\n--- Expense Log ---")
    for e in data["expenses"]:
        print(f"  {e['date']}  ${e['amount']:>7.2f}  [{e['category']}]  {e['description']}")


def main():
    data = load_data()

    import sys
    if len(sys.argv) < 2:
        dashboard(data)
        return

    cmd = sys.argv[1]

    if cmd == "dashboard":
        dashboard(data)
    elif cmd == "income" and len(sys.argv) >= 5:
        add_income(data, sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "expense" and len(sys.argv) >= 5:
        add_expense(data, sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "log":
        show_log(data)
    else:
        print("Usage:")
        print("  python tracker.py                              # Show dashboard")
        print("  python tracker.py income <stream> <amt> <desc>  # Add income")
        print("  python tracker.py expense <cat> <amt> <desc>    # Add expense")
        print("  python tracker.py log                           # Show all entries")
        print(f"\nStreams: {', '.join(STREAMS)}")


if __name__ == "__main__":
    main()
