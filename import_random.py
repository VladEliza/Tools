# vietlott_power655_checker.py

import requests
from bs4 import BeautifulSoup
import secrets
import re

VIETLOTT_URL = "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655.html"

def fetch_latest_draw():
    response = requests.get(VIETLOTT_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the draw number and date
    draw_number = None
    draw_date = None
    for text in soup.stripped_strings:
        match = re.search(r"Kỳ quay thưởng\s*#(\d+)\s*ngày\s*(\d{2}/\d{2}/\d{4})", text)
        if match:
            draw_number = match.group(1)
            draw_date = match.group(2)
            break

    # Find the winning numbers (usually in bold or with 'O O O O O O')
    winning_numbers = []
    for tag in soup.find_all(['strong', 'b', 'span', 'div']):
        nums = re.findall(r"\b\d{2}\b", tag.get_text())
        if len(nums) == 6:
            winning_numbers = [int(n) for n in nums]
            break

    # Find bonus number (if present)
    bonus_number = None
    bonus_match = re.search(r"\|\s*(\d{2})", soup.text)
    if bonus_match:
        bonus_number = int(bonus_match.group(1))

    return {
        "draw_number": draw_number,
        "draw_date": draw_date,
        "winning_numbers": winning_numbers,
        "bonus_number": bonus_number
    }

def generate_power655_rows(num_rows=5, num_numbers=6, min_num=1, max_num=55):
    rows = []
    for _ in range(num_rows):
        row = secrets.SystemRandom().sample(range(min_num, max_num + 1), num_numbers)
        row.sort()
        rows.append(row)
    return rows

def compare_rows_to_draw(rows, winning_numbers, bonus_number):
    print("\nComparison to latest draw:")
    for idx, row in enumerate(rows, 1):
        match_count = len(set(row) & set(winning_numbers))
        bonus_hit = bonus_number in row if bonus_number else False
        result = ""
        if match_count == 6:
            result = "Jackpot 1!"
        elif match_count == 5 and bonus_hit:
            result = "Jackpot 2!"
        elif match_count == 5:
            result = "First Prize"
        elif match_count == 4:
            result = "Second Prize"
        elif match_count == 3:
            result = "Third Prize"
        else:
            result = "No prize"
        print(f"Row {idx}: {' '.join(f'{num:02d}' for num in row)} | Matches: {match_count} | Bonus: {'Yes' if bonus_hit else 'No'} | Result: {result}")

def main():
    print("Fetching latest Power 6/55 draw from Vietlott.vn...")
    draw = fetch_latest_draw()
    print(f"Draw #{draw['draw_number']} on {draw['draw_date']}")
    print(f"Winning numbers: {' '.join(f'{n:02d}' for n in draw['winning_numbers'])}")
    if draw['bonus_number']:
        print(f"Bonus number: {draw['bonus_number']:02d}")

    rows = generate_power655_rows()
    print("\nYour 5 random rows:")
    for idx, row in enumerate(rows, 1):
        print(f"Row {idx}: {' '.join(f'{num:02d}' for num in row)}")

    compare_rows_to_draw(rows, draw['winning_numbers'], draw['bonus_number'])

if __name__ == "__main__":
    main()
