# HUNZALA MUSHTAQ CS-20052 OEL
# Searching using Binary search
# Sorting using Merge Sort
import sqlite3
db = sqlite3.connect("test.db")

class Book :
    def create_table(self):
        try:
            cur = db.cursor()
            cur.execute('''CREATE TABLE books (
            bookID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT (20) NOT NULL,
            author TEXT(20) , 
            pub_date TEXT(20) , 
            subject TEXT(50) , 
            price  REAL);''')

            print('table created successfully')
        except :
            print("Error Occurred during  Creating the Table ")
            db.rollback()

    def add_book(self,title , price ,author ,pub_date , subject ):
        query = """insert into books (title , author , pub_date , subject , price ) values (?,?,?,?,?)"""
        try:
            cur = db.cursor()
            cur.execute(query,(title ,author,pub_date,subject , price))
            db.commit()
            print("Record Inserted Succesfully  ")
        except Exception as e:
            print("Error Occured Inserting an Book  " , e)
            db.rollback()
    def delete_book(self,title):
        query = "DELETE from student where name=?"
        try :
            cur = db.cursor()
            cur.execute(query ,(title,))
        except Exception as e :
            print("Error Occurred in deleting a Reacord :" , e )
    def show_all_book(self):
        query = "SELECT * FROM books"
        data = None
        try :
            cur = db.cursor()
            cur.execute(query)
            data = cur.fetchall()

        except Exception as e :
            print("Error Occurred during fetch ",e)
        return data
    def return_date(self, date ):
        self.date_to_return = date

    def print_all_book(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM books")
        result = cur.fetchall()
        for book in result :
            print(book[0] ,". -->", book[1])
    def sort_by_name(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM books")
        raw_result = cur.fetchall()
        result = [data[1] for data in raw_result]
        def mergeSort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2
                L = arr[:mid]
                R = arr[mid:]
                mergeSort(L)
                mergeSort(R)
                i = j = k = 0
                while i < len(L) and j < len(R):
                    if L[i] < R[j]:
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                    k += 1
                while i < len(L):
                    arr[k] = L[i]
                    i += 1
                    k += 1
                while j < len(R):
                    arr[k] = R[j]
                    j += 1
                    k += 1
        mergeSort(result)
        # print("sorted ",result)
        for book in result :
            for data  in raw_result:
                if book in data :
                    print(data[0] , "-->" , data[1])



class user:
    def __init__(self):
        self.username = None
        self.have_book = False
        self.is_admin = False
        self.reserved_book = False #b_b 2. history 3.reservedbook
        self.borrowed_book = []
        self.transaction_history = []
        self.cart = {}
    def login(self,username,password) :
        query = """SELECT * FROM users WHERE username = ? AND password = ?"""
        exist = False

        cur = db.cursor()
        try :
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cur.fetchall()
            if len(result) == 0:
                print('Not found')
            else:
                print('Found')
                self.username= username
                exist = True
        except Exception as e :
            print("Error Occurred:", e)
        return exist
    def create_table(self):
        try:
            cur = db.cursor()
            cur.execute('''CREATE TABLE users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT (20)  NOT NULL,
            password TEXT (20) NOT NULL ,  
            roll_no INTEGER , 
            borrowed_book TEXT(500) , 
            reserved_book INTEGER , 
            transaction_history TEXT(500) , 
            
            is_admin INTEGER);''')

            print('table created successfully')
        except Exception as e:
            print("Error Occurred during  Creating the Table ",e)
            db.rollback()
    def check_admin(self):
        return 1 if self.is_admin== True else False
    def save_all_data(self):
        cur = db.cursor()
        try :
            cur.execute("SELECT * FROM users WHERE username = ? ", (self.username,))
            result = cur.fetchall()
            print("all data in db",result)
            borrowed_book = (result[0][4])
            reserved_book = (result[0][5])
            transaction_history = (result[0][6])
            print("------" , borrowed_book,reserved_book,transaction_history)
            if borrowed_book is None or reserved_book is None or transaction_history is None:
                cur2 = db.cursor()

                borrowed_book = str(self.borrowed_book)
                reserved_book = str(self.reserved_book)
                transaction_history = str(self.transaction_history)
                statement = "UPDATE users SET  borrowed_book = ?, reserved_book = ?, transaction_history = ? WHERE username = ? "
                print(self.borrowed_book , self.username)
                cur2.execute(statement , (borrowed_book, self.reserved_book , transaction_history,self.username))
                db.commit()
                print("Done")
            else:
                borrowed_book = eval(result[0][4])
                transaction_history = eval(result[0][6])
                for data in self.borrowed_book :
                    borrowed_book.append(data)
                for data in self.transaction_history:
                    transaction_history.append(data)
                cur2 = db.cursor()
                # borrowed_book.append(self.borrowed_book)
                reserved_book = str(self.reserved_book)
                # transaction_history.append(self.transaction_history)
                print("************", borrowed_book, reserved_book, transaction_history)

                statement = "UPDATE users SET  borrowed_book = ?, reserved_book = ?, transaction_history = ? WHERE username = ? "

                cur2.execute(statement , (str(borrowed_book),str(reserved_book),str(transaction_history),self.username))
                db.commit()
                print("Done by else")
        except Exception as e :
            print("Error Occurred:", e)
    def logout(self):
        self.username = None
        self.have_book = False
        self.is_admin = False
        self.reserved_book = False
        self.borrowed_book = []
        self.transaction_history = []
        self.cart = {}

    def create_user(self,name,password,roll_no):
        query = """insert into users (username , password , roll_no , is_admin) values (?,?,?,?)"""
        try:
            cur = db.cursor()
            cur.execute(query,(name ,password,roll_no,self.check_admin()))
            db.commit()
            print("Record Inserted Succesfully  ")
        except Exception as e:
            print("Error Occured Inserting an user  " , e)
            db.rollback()
    def checkout(self):
        # print("Do You Want To Check Out ")
        self.transaction_history.append(self.cart)
        for book in self.cart.keys() :
            self.borrowed_book.append(book)
        self.reserved_book = True
        self.save_all_data()
        self.cart = {}
        # self.transaction_historyy = []
        # self.borrowed_book =[]

    def return_book(self):
        self.borrowed_book = []
        self.have_book = False
        cur = db.cursor()
        try :
            statement = "UPDATE users SET  borrowed_book = ?, reserved_book = ? WHERE username = ? "
            cur.execute(statement , (None , False,self.username))
            db.commit()
            print("Booked returned To library ")
        except Exception as e :
            print("Error Occured During returning book " , e)

    def reserve_book(self):
        pass
    def check_balance(self):
        pass
    def reborrow_book(self):
        pass
    def borrow_book(self,id):
        found = False
        all_books= Book().show_all_book()
        low = 0
        high = len(all_books) - 1
        mid = 0
        while low <= high:
            mid = (high + low) // 2

            if all_books[mid][0] < id:
                low = mid + 1

            elif all_books[mid][0] > id:
                high = mid - 1
            else :
                print(all_books[mid])
                self.cart[all_books[mid][1]] = (all_books[mid][5])
                found = True
                self.have_book = True
                break
        return  found
class admin(user):
    def __init__(self):
        super().__init__()
        self.is_admin = True

    def delete_user(self,username):
        try :
            cur = db.cursor()
            query = """DELETE from users where username = ?"""
            cur.execute(query , (username,))
            print("User Deleted")
            db.commit()
        except Exception as e :
            print("Error occured in Deleting User" , e)
    def delete_book(self,title):
        try :
            cur = db.cursor()
            query = """DELETE from books where title = ?"""
            cur.execute(query , (title,))
            print("Book Deleted")
            db.commit()
        except Exception as e :
            print("Error occured in Deleting Book" , e)
    def insert_book(self,title , price ,author ,pub_date , subject ):
        b1 = Book()
        b1.add_book(title , price ,author ,pub_date , subject )


#
print("Welcome To The Library ")
# print("""1.Login \n2.Admin Login\n3.Exit""")
while True :
    print("""1.Login \n2.Admin Login\n3.Sign Up\n4.Exit""")
    response = int(input("Enter Option : "))
    if response == 1 :
        u = user()
        username = input("Enter Username :" )
        pas= input("Enter password :")
        userlogged = u.login(username,pas)
        if userlogged == True :
            while True :
                print("Username",u.username,'\n')
                print("""1.Show Books\n2.Show Book Alphabatically \n3.Cart\n4.Transaction History\n5.Do You i have any Book ? \n6.Borrow Book \n7.Return all Books \n8.Checkout \n9.Borrowed Book\n10.Logout""")
                inp = int(input("Enter Options :"))
                if inp==1 :
                    b= Book()
                    b.print_all_book()
                elif inp==2:
                    b=Book()
                    b.sort_by_name()

                elif inp == 3:
                    print(u.cart)
                elif inp == 4:
                    print(u.transaction_history)

                elif inp == 5:
                    print(u.have_book)
                elif inp == 6:
                    b=Book()
                    b.print_all_book()

                    try:
                        book_inp = int(input("Enter Book ID"))
                        u.borrow_book(book_inp)
                    except Exception as e :
                        print("Give valid id of book")

                elif inp == 7:
                    u.return_book()
                elif inp == 8:
                    u.checkout()
                elif inp == 9:
                    print(u.borrowed_book)
                elif inp == 10:
                    u.logout()
                    break
                else:
                    print("invalid Input")

    if response == 2:
        a =admin()

        while True :
            print("""Admin \n1.SignUp \n2.LogIn\n3.Back to UserMode """)
            inp = int(input("Enter Option (admin) :"))
            if inp ==1 :
                name = input("Enter username")
                pas = input("Enter password")
                roll_no = input("Enter roll No : ")
                a.create_user(name,pas,roll_no)
            elif inp == 3  :
                break
            elif inp == 2 :
                name = input("Enter username :")
                pas = input("Enter password :")
                a.login(name , pas)
                while True :
                    print("""\n4.Delete Book \n5.Delete User\n6.Insert Book\n7.Logout""")
                    if a.is_admin ==True :
                        inp = input("Enter option :")

                        if int(inp) == 4:
                            bookname = input("Enter Book Name :")
                            a.delete_book(bookname)
                        elif int(inp) == 5:
                            username = input("Enter User Name :")
                            a.delete_user(username)

                        elif int(inp) == 6:
                            title= input("Enter Title :")
                            price= input("Enter price :")
                            author= input("Enter author  :")
                            pubdate= input("Enter date :")
                            sub= input("Enter subject :")
                            a.insert_book(title,price,author,pubdate,sub)
                        elif int(inp) == 7 :
                            break
                        else:
                            print("invalid Input")
            else:
                print("invalid Input")

    if response == 3:
        u = user()
        username = input("Enter Username :")
        pas = input("Enter password :")
        roll_no = input("Enter Rollno :")
        u.create_user(username,pas,roll_no)

    elif response == 3 :
        break
    else:
        print("invalid Input")
