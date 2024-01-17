import re

emails = [
    "fake_email.com",
    "fake_email@",
    "fake_email@fake",
    "real_email@example.com",
    "real.email123@example.co.in",
    "another_real.email@example.co.uk",
    "email_with_numbers123@example.com",
    "email_with_symbols$%^&@example.com",
    "noname@domain.co",
    "email_fashion@example.net",
    "fake_email@fake",
    "real.email@example.com",
    "anotherReal.email@example.co.in",
    "email_with_numbers1234@example.com",
    "email_with_symbols@!example.com",
    "Bounces-Back@whereIhe.live",
    "Jack.Maybe@ex-citing.co.uk",
    "real-email@example.uk",
    "Yoda@jedimaster.co.uk",
    "no_service@example"
]
pattern = r"^[^\d]\S+@[a-zA-Z]+\.\S{2,3}"

for email in emails:
    if re.match(pattern, email):
        print(f"The email address {email} is valid")
    else:
        print(f"The email address {email} is invalid")