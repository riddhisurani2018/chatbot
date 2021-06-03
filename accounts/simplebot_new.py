import sqlite3
import random
from django.conf import settings
from nltk.corpus import stopwords
from text_keywords_processing import chat_bow

stop_words = set(stopwords.words('english'))
stop_words.add('please')
stop_words.add('provide')


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
    except sqlite3.Error as e:
        print(e)
    return conn


def select_about_us(conn):
    cur = conn.cursor()
    cur.execute("SELECT about_us_paragraph FROM accounts_about_us")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_about_us_arabic(conn):
    cur = conn.cursor()
    cur.execute("SELECT about_us_paragraph_arabic FROM accounts_about_us_arabic")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_link_by_keyword(conn, keyword):
    cur = conn.cursor()
    cur.execute("SELECT links FROM accounts_link_keyword WHERE keyword_values=?", (keyword,))
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_link_by_arabic_keyword(conn, keyword):
    cur = conn.cursor()
    cur.execute("SELECT links FROM accounts_link_keyword WHERE keyword_values_arabic=?", (keyword,))
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_text_by_keyword(conn, queryString):
    response = chat_bow(queryString)
    if response != 'Sorry, I don\'t have an answer for this right now..':
        print('\n' + response)
    else:
        cur = conn.cursor()
        print("Sorry, I don't have an answer for this right now..")
        u_email = input("Kindly provide an e-mail ID where we can provide you the response later : ")
        cur.execute("INSERT INTO accounts_manual_response(new_keyword, email_id) VALUES(?, ?)",
                    [queryString, u_email], )
        print("Our admins will reach out to you with the response shortly.. ")
        conn.commit()


def select_text_by_arabic_keyword(conn, keyword):
    cur = conn.cursor()
    cur.execute("SELECT desc_arabic FROM accounts_text_keyword_arabic WHERE keyword_value_arabic=?", (keyword,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        new_key_query = "SELECT new_keyword_arabic FROM accounts_manual_response_arabic"
        cur.execute(new_key_query)
        new_keys = cur.fetchall()
        if (keyword,) in new_keys:
            cur.execute("SELECT admin_data FROM accounts_manual_response WHERE new_keyword_arabic = ?", (keyword,))
            new_responses = cur.fetchall()
            for manual_row in new_responses:
                print(manual_row)
        else:
            print("آسف ، ليس لدي إجابة عن هذا الآن ..")
            u_email = input("يرجى تقديم معرف البريد الإلكتروني حيث يمكننا تزويدك بالرد لاحقًا ..\n")
            cur.execute(
                "INSERT INTO accounts_manual_response_arabic(new_keyword_arabic, email_id_arabic) VALUES(?, ?)",
                [keyword, u_email], )
            conn.commit()


def AskConsultant(conn, uname, file_no, u_inquiry):
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts_askconsultant VALUES(?,?,?)", [uname, file_no, u_inquiry])
    conn.commit()
    print("Your inquiry has been sent.")


def AskConsultant_arabic(conn, uname, file_no, u_inquiry):
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts_askconsultant_arabic VALUES(?,?,?)", [uname, file_no, u_inquiry])
    conn.commit()
    print("تم إرسال استفسارك")


def english_menu():
    print("\ta. About the Service \n\tb. Consult Me \n\tc. Gain Knowledge \n\td. Ask your consultant\n\te. Exit")


def arabic_menu():
    print("\t1. حول الخدمة \n\t2. استشرني \n\t3. اكتساب المعرفة \n\t4. اسأل مستشارك\n\t5. مخرج")


def main():
    database = "C:\\Users\\Riddhi\\Documents\\chatbot\\chatbot\\db.sqlite3"
    # create a database connection
    conn = create_connection(database)
    with conn:
        if not settings.configured:
            settings.configure()
            lang_choice = input("Press 1 for English or 2 for Arabic: ")
            if lang_choice == '2':
                greet_list = ["مرحبا", "تحية طيبة!"]
                ask_list = ["كيف يمكنني مساعدك؟", "كيف يمكنني مساعدتك؟"]
                random_greet = random.choice(greet_list)
                random_ask = random.choice(ask_list)
                print("روبوت الدردشة : " + random_greet + "," + random_ask)
                arabic_menu()
                while True:
                    try:
                        user_input = input('مستخدم: ')
                        if user_input == '1':
                            select_about_us_arabic(conn)
                        elif user_input == '2':
                            print("بماذا يمكنني مساعدتك؟")
                            print("(أدخل \"رجوع\" للعودة إلى القائمة الرئيسية)\n")
                            while True:
                                uquery = input("أدخل استفسارك : ")
                                if uquery.lower() == 'عودة':
                                    print("\nما الذي يمكنني مساعدتك به أيضًا؟")
                                    arabic_menu()
                                    break
                                select_text_by_arabic_keyword(conn, uquery)
                        elif user_input == '3':
                            uinput = input("أدخل الكلمة المفتاحية : ")
                            select_link_by_arabic_keyword(conn, uinput)
                        elif user_input == '4':
                            u_name = input("اسم : ")
                            FileNum = input("رقم الملف : ")
                            inquiry = input("سؤال : ")
                            AskConsultant_arabic(conn, u_name, FileNum, inquiry)
                        elif user_input == '5':
                            print("شكرا لك! يرجى تقديم ملاحظاتك على")
                            # Enter Feedback Form Link Here
                            exit()
                        else:
                            print("الرجاء إدخال خيار صالح!")
                    except(KeyboardInterrupt, EOFError, SystemExit):
                        break

            else:
                greet_list = ["Hi", "Hello", "Hey"]
                english_ask_list = ["How can I help you?", "How may I help you?"]
                random_greet = random.choice(greet_list)
                random_ask = random.choice(english_ask_list)
                print("Bot : " + random_greet + "," + random_ask)
                english_menu()
                while True:
                    try:
                        user_input = input('User: ')
                        if user_input == '1':
                            select_about_us(conn)
                        elif user_input == '2':
                            print("What can I help you with?")
                            print("(Enter 'back' to return to main menu)\n")
                            while True:
                                uquery = input("Enter your query : ")
                                if uquery.lower() == 'back':
                                    print("\nWhat else can I help you with?")
                                    english_menu()
                                    break
                                select_text_by_keyword(conn, uquery)
                        elif user_input == '3':
                            print("What can I help you with?")
                            uinput = input("Enter keyword : ")
                            select_link_by_keyword(conn, uinput)
                        elif user_input == '4':
                            u_name = input("Name : ")
                            FileNum = input("File number : ")
                            inquiry = input("Inquiry : ")
                            AskConsultant(conn, u_name, FileNum, inquiry)
                        elif user_input == '5':
                            print("Thank you! Kindly provide your feedback at [Enter Feedback Form Link Here]")
                            exit()
                        else:
                            print("Please enter valid option!")
                    except(KeyboardInterrupt, EOFError, SystemExit):
                        break


if __name__ == '__main__':
    main()
