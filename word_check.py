import csv
import json
import os
import time
import re
import requests


def korrektor_json():
    url = "http://korrektor.manu.uz/spellcheck"
    with open('data/correct_data/new_data.csv', 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for txt_id, row in enumerate(reader):
            print(f"Checking sentence >> {row[2]}")
            payload = {'alphabet': 'latin', 'text': str(row[2])}
            time.sleep(2)
            headers = {}
            files = []
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.json()  # Convert the response to JSON

            # Store the JSON data in a file
            with open("data/words.json", "w") as file:
                json.dump(data, file)
                time.sleep(1)


korrektor_json()


def korrektor_check():
    url = "http://korrektor.manu.uz/spellcheck"

    with open('data/correct_data/new_data.csv', 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for txt_id, row in enumerate(reader):
            payload = {'alphabet': 'latin', 'text': str(row[2])}
            time.sleep(2)
            headers = {}
            files = []
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            time.sleep(1)
            if not os.path.exists('data/check_spell.csv'):
                with open('data/check_spell.csv', 'w', newline='') as spell:
                    headers = ['text id', 'sentence', 'results', 'status']
                    writer = csv.DictWriter(spell, headers, delimiter='|')
                    writer.writeheader()
                    if response.json()['code'] == 200:
                        writer.writerow({'text id': txt_id, 'sentence': row[2], 'results': "200", 'status': 'correct'})
                        print(f"in book {row[0]} >> sentence >> {row[2]} is correct\n")
                    elif response.json()['code'] == 418:
                        try:
                            writer.writerow(
                                {'text id': txt_id, 'sentence': row[2], 'results': "", 'status': 'incorrect'})
                            for i in response.json()['result']:
                                writer.writerow({'text id': txt_id, 'sentence': "-",
                                                 'results': f"{i} -> {response.json()['result'][i][0]['suggestions']}",
                                                 'status': 'incorrect'})
                                print(
                                    f"in book {row[0]} >> sentence >> {row[2]}:\n {i}>>{response.json()['result'][i][0]['suggestions']}\n")
                        except KeyError:
                            writer.writerow(
                                {'text id': txt_id, 'sentence': row[2], 'results': "", 'status': 'incorrect'})
                            writer.writerow(
                                {'text id': txt_id, 'sentence': "-", 'results': "KeyError", 'status': 'incorrect'})
                            print(f"KeyError in sentence {row[2]}\n")
                            continue
            else:
                with open('data/check_spell.csv', 'a', newline='') as spell:
                    headers = ['text id', 'sentence', 'results', 'status']
                    writer = csv.DictWriter(spell, headers, delimiter='|')
                    if response.json()['code'] == 200:
                        writer.writerow({'text id': txt_id, 'sentence': row[2], 'results': "200", 'status': 'correct'})
                        print(f"in book {row[0]} >> sentence >> {row[2]} is correct\n")
                    elif response.json()['code'] == 418:
                        try:
                            writer.writerow(
                                {'text id': txt_id, 'sentence': row[2], 'results': "", 'status': 'incorrect'})
                            for i in response.json()['result']:
                                writer.writerow({'text id': txt_id, 'sentence': "-",
                                                 'results': f"{i} -> {response.json()['result'][i][0]['suggestions']}",
                                                 'status': 'incorrect'})
                                print(
                                    f"in book {row[0]} >> sentence >> {row[2]}:\n {i}>>{response.json()['result'][i][0]['suggestions']}\n")
                        except KeyError:
                            writer.writerow(
                                {'text id': txt_id, 'sentence': row[2], 'results': "", 'status': 'incorrect'})
                            writer.writerow(
                                {'text id': txt_id, 'sentence': "-", 'results': "KeyError", 'status': 'incorrect'})
                            print(f"KeyError in sentence {row[2]}\n")
                            continue


# korrektor_check()

def check_symbol(txt_str):
    regex = r"ê|ë|é|è|е"

    matches = re.finditer(regex, txt_str, re.UNICODE)

    for matchNum, match in enumerate(matches, start=1):

        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                            end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                            start=match.start(groupNum),
                                                                            end=match.end(groupNum),
                                                                            group=match.group(groupNum)))

        text_repl = re.sub(match.group(), "e", txt_str)
        return text_repl


# print(check_symbol("Konan Doyl Xolms haqida hikoyalar MALLALAR UYUSHMASI Bu voqеa oʻtgan yili kuzda bo’lgan edi"))

# read csv file, check symbols and replace them if they are wrong
def check_csv_file(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        # iterate to each row in csv file and check symbols in sentence column and replace them if they are wrong and replace to new csv file with correct symbols
        for row in reader:
            # check symbols in sentence column and replace them if they are wrong and replace to new csv file with correct symbols
            with open('data/correct_data/new_data.csv', 'a', newline='') as correct:
                headers = ['Asar_nomi', 'Muallif', 'Matn']
                writer = csv.DictWriter(correct, headers, delimiter='|')
                if check_symbol(row[2]):
                    writer.writerow({'Asar_nomi': row[0], 'Muallif': row[1], 'Matn': check_symbol(row[2])})
                    print(f"Corrected sentence: {check_symbol(row[2])}\n")
                else:
                    writer.writerow({'Asar_nomi': row[0], 'Muallif': row[1], 'Matn': row[2]})
                    print(f"Corrected sentence: {row[2]}\n")

# check_csv_file('data/correct_data/e-book.csv')
