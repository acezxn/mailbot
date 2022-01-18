import mail
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model")
parser.add_argument("--mail")
parser.add_argument("--password")

args = parser.parse_args()

mails = mail.read_email_from_gmail(args.user, args.password, 'ALL')
# print(mails)
with open(args.model) as file:
    data = json.load(file)

os.system('clear')


important = list(data['important'])
not_important = list(data['not important'])

while True:
    try:
        print(
        """
        Actions:
        1) Add important email
        2) Add not important email
        3) Save and exit
        """
        )
        actions = input("input actions >> ")
        if actions == '1':
            c = 0
            for m in mails:
                print(f"{c}\t{m[0]}: \t{m[1]}\n")
                c += 1
            while True:
                try:
                    idx = input("insert mail index (enter back to go back): ")
                    idx = int(idx)
                    if mails[idx][0] not in important:
                        data['important'].append(mails[idx][0])
                        important.append(mails[idx][0])
                    if mails[idx][1] not in important:
                        data['important'].append(mails[idx][1])
                        important.append(mails[idx][1])
                except:
                    if idx == 'back':
                        break

        elif actions == '2':
            c = 0
            for m in mails:
                print(f"{c}\t{m[0]}: \t{m[1]}\n")
                c += 1
            while True:
                try:
                    idx = input("insert mail index (enter back to go back): ")
                    idx = int(idx)
                    if mails[idx][0] not in not_important:
                        data['not important'].append(mails[idx][0])
                        not_important.append(mails[idx][0])
                    if mails[idx][1] not in not_important:
                        data['not important'].append(mails[idx][1])
                        not_important.append(mails[idx][1])
                except:
                    if idx == 'back':
                        break
        elif actions == '3':
            with open(args.model, 'w') as file:
                data = json.dump(data, file, indent=4, sort_keys=True)
            exit()
    except KeyboardInterrupt:
        print("exiting")
