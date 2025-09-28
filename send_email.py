import smtplib
from email.message import EmailMessage

SENDER = "wesleyzhengca@gmail.com"
APP_PASS = "swor efes yird ompg"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

partners = [
    ("Nahal Ghaznavi", "nahalghaznavi@berkeley.edu", "Angela X Ye", "angela_ye@berkeley.edu"),
    ("Stefanie Sandra Barrios Lara", "stefaniebl@berkeley.edu", "Alicia Rosaline Rodriguez Lopez", "ali_rodriguez86@berkeley.edu"),
    ("Katelyn Pech", "katelynpech@berkeley.edu", "Kaiyue Li", "likaiyue@berkeley.edu"),
    ("Aaron Isaac Rome", "aaron_rome@berkeley.edu", "Shrihan Reddy Nomula", "shrihanrn@berkeley.edu"),
    ("Claire Wang", "claire-wang@berkeley.edu", "Elise Madeline Swarts", "elise.swarts@berkeley.edu"),
    ("Calista Rose Cantu", "can2calirose@berkeley.edu", "Dan Gotesdyner", "dan_gotesdyner@berkeley.edu"),
    ("Ahdil Arif Khan", "ahdil_khan@berkeley.edu", "Sagar Niranjan Bhatia", "sagarbhatia@berkeley.edu"),
    ("Isabella Zhao", "isabellazhao@berkeley.edu", "Kyla Lee Kuo", "kyla_kuo@berkeley.edu"),
    ("Imanol Torrero Santiago", "imanolts@berkeley.edu", "Nick Dmitry Vengerov", "nickvengerov@berkeley.edu"),
    ("Vinayak Nikhil Prathikanti", "vinayakp@berkeley.edu", "Tu-Anh Huynh Bui", "tuabui541@berkeley.edu"),
    ("Celeste Esmelia Morales", "cmorales19@berkeley.edu", "Kate Ting Lin", "kate.t.lin@berkeley.edu"),
    ("Victoria Hernandez Padilla", "vherna0@berkeley.edu", "Nomar Nunez", "nn1209@berkeley.edu"),
    ("Eric Drew Schneider", "ericschneider@berkeley.edu", "Randon Rea", "rrea.cal@berkeley.edu"),
    ("Evan Zhong", "evanzhong@berkeley.edu", "Mia Soon Sweeny", "miasweeny@berkeley.edu")
]

random_partners = [
    ("Coco Fan", "sc.fan@berkeley.edu", "Aiyanna Brown", "aiyanna-brown@berkeley.edu")
]

left_overs = [
    ("Thomas Matthew Hoppner", "thomas22@berkeley.edu"),
]

independents = [
    ("Michael Li", "mickle.li@berkeley.edu"),
    ("Khushi Madan", "khushi_madan@berkeley.edu"),
    ("Joel Pena Oritz", "jp46686@berkeley.edu"),
    ("Christina Chuang", "chuangchristina27@berkeley.edu"),
    ("Morgan Alexis Venable", "morgnn@berkeley.edu"),
    ("Sasha Brown", "sbrown_5@berkeley.edu"),
]


def send_partner_email(name1, email1, name2, email2):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = ", ".join([email1, email2])
    msg["Subject"] = "[Data 8] Project 1 Partner Confirmation"

    body = f"""
Hi {name1.strip().split()[0]} and {name2.strip().split()[0]}! 

Thank you so much for filling out the project partner matching form. This is a confirmation that you will be working as project partners. It will be released on the course website soon. Please feel free to use this email thread to do the initial reaching out to each other if you have not yet.

As I have mentioned, please feel free to use all the class resources at your disposal. We are always here to help you whether that be during office hours, on Ed Discussion, or in section. Please reach out if you ever have questions, and good luck!

Best,
Wesley
"""
    msg.set_content(body)
    return msg


def send_pairing_email(name1, email1, name2, email2):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = ", ".join([email1, email2])
    msg["Subject"] = "[Data 8] Project Partner Match"

    body = f"""
Hi {name1.strip().split()[0]} and {name2.strip().split()[0]},

I’m happy to let you know that you have been matched as project partners based on your similar preferences for the upcoming Data 8 project.

Please coordinate your schedules and preferences, and start planning your collaboration. If you have any questions or need support, feel free to reach out.

Best of luck working together!

Best,
Wesley
"""
    msg.set_content(body)
    return msg

def send_independent_email(independents):
    emails = [email for _, email in independents]

    msg = EmailMessage()
    msg["From"] = SENDER
    msg["Bcc"] = ", ".join(emails)
    msg["Subject"] = "[Data 8] Project 1 Solo Confirmation"

    body = """
Hi,

Thank you for filling out the project partnership form. This is a quick confirmation that you’ve opted to work independently on the project. You are all set to proceed solo—no further action is needed regarding partner matching.

If your plans change and you'd like to be matched with someone after all, feel free to reach out to me ASAP.

Best of luck with your project!

Best,
Wesley
"""
    msg.set_content(body)
    return msg

def send_leftover_email(name, email):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = email
    msg["Subject"] = "[Data 8] Project Partner Update"

    body = f"""
Hi {name.strip().split()[0]},

Thank you for filling out the project partnership form. At the moment, we don’t have another student available to match you with as a project partner. For now, you’ll be working solo on the project.

If another student reaches out or a new match becomes available, I’ll notify you right away so you can pair up.

In the meantime, you’re all set to move forward independently.

Best of luck with your project!

Best,
Wesley
"""
    msg.set_content(body)
    return msg



with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(SENDER, APP_PASS)

    for n1, e1, n2, e2 in partners:
        smtp.send_message(send_partner_email(n1, e1, n2, e2))

    for n1, e1, n2, e2 in random_partners:
        smtp.send_message(send_pairing_email(n1, e1, n2, e2))
    
    for n, e in left_overs:
        smtp.send_message(send_leftover_email(n, e))

    smtp.send_message(send_independent_email(independents))

print("✅ All partner, random pool, and independent emails sent.")
