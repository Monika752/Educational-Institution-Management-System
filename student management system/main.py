from tkinter import *
from tkinter import messagebox
import ttkthemes
from tkinter import ttk
from datetime import datetime
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root",password="monikasql",database="managementsystem")

#clock function
def clock():
    current_date = datetime.now().strftime("%d/%m/%Y")
    dateLabel.config(text=f'Date: {current_date}')

def getCoursesFromDatabase():
    cur = conn.cursor()
    cur.execute("SELECT course_name FROM course")
    courses = cur.fetchall()
    course_names = [course[0] for course in courses]
    return course_names

#mysql connection function
def addstudent():
    def addData():
           Name = nameEntry.get()
           email = emailEntry.get()
           gender = genderEntry.get()
           course = courseEntry.get()
           joined_date = joinEntry.get()
           fees = int(feesEntry.get())
           amount_paid = int(paidEntry.get())
           feestopay = int(float(feesToPayEntry.get()))
           pending_fees = feestopay - amount_paid
           timing = batchEntry.get()
           status = statusEntry.get()
           completed = compEntry.get()
           contact = contactEntry.get()
           discount = discountEntry.get()
           if (Name=='' or email=='' or gender=='' or course=='' or joined_date=='' or fees=='' or amount_paid=='' or 
            timing=='' or status=='' or contact==''):
             messagebox.showerror("error","Fields should not be empty except Id")
           else:
             cur = conn.cursor()
             insert_query = "insert into student (Name, email, Gender, Course, Joined_Date, Fees,discount, feestopay, Amount_Paid, Pending_Fees, Batch_Timing, Course_Status, Contact) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
             record = (Name, email, gender, course, joined_date, fees ,discount, feestopay, amount_paid, pending_fees, timing, status, contact)
             cur.execute(insert_query, record)
             conn.commit()
             messagebox.showinfo("Success", "Details added successfully!")

             display = "select * from student"
             cur.execute(display)
             fetch = cur.fetchall()
             TopBar.delete(*TopBar.get_children())
             for data in fetch:
                datalist = list(data)
                TopBar.insert('',END,values=datalist)

             add_window.destroy()

    def updateFees(event):
        selected_course = courseEntry.get()
        cur = conn.cursor()
        cur.execute("SELECT fees FROM course WHERE course_name = %s", (selected_course,))
        course_fees = cur.fetchone()[0]
        feesEntry.delete(0,END)
        feesEntry.insert(0, course_fees)
        updateFeesToPay()  
    
    def updateFeesToPay():
        fees = int(feesEntry.get())
        discount = int(discountEntry.get().strip('%'))
        fees_to_pay = fees - (fees * discount / 100)
        feesToPayEntry.delete(0, END)
        feesToPayEntry.insert(0, fees_to_pay)
        pending_fees = fees_to_pay - int(paidEntry.get())
        pendingFeesEntry.delete(0, END)
        pendingFeesEntry.insert(0, pending_fees)

    add_window = Toplevel()
    add_window.resizable(False,False)
    add_window.grab_set()
    topicLabel = Label(add_window,text="Add Details",font=("arial",15),bg="#2b8783",fg="white",width=20)
    topicLabel.grid(row=0,columnspan=2,pady=10)
    idLabel = Label(add_window,text="Id",font=("arial",13),)
    idLabel.grid(row=1,column=0,padx=30,pady=10,sticky=W)
    idEntry = Entry(add_window,font=("arial",13),width=24,state='disabled')
    idEntry.grid(row=1,column=1,padx=10,pady=10)
    #Name
    nameLabel = Label(add_window,text="Name",font=("arial",13),)
    nameLabel.grid(row=1,column=2,padx=30,pady=10,sticky=W)
    nameEntry = Entry(add_window,font=("arial",13),width=24)
    nameEntry.grid(row=1,column=3,padx=10,pady=10)
    #email
    emailLabel = Label(add_window,text="email",font=("arial",13),)
    emailLabel.grid(row=2,column=0,padx=30,pady=10,sticky=W)
    emailEntry = Entry(add_window,font=("arial",13),width=24)
    emailEntry.grid(row=2,column=1,padx=10,pady=10)
    #gender
    genderLabel = Label(add_window,text="Gender",font=("arial",13),)
    genderLabel.grid(row=2,column=2,padx=30,pady=10,sticky=W)
    #dropdown change
    genderEntry = ttk.Combobox(add_window, font=("arial", 13), width=22, state='readonly')
    genderEntry['values'] = ("Male", "Female", "Other")
    genderEntry.grid(row=2, column=3, padx=10, pady=10)
    #course
    courseLabel = Label(add_window,text="Course",font=("arial",13),)
    courseLabel.grid(row=3,column=0,padx=30,pady=10,sticky=W)
    #course dropdown
    courseEntry = ttk.Combobox(add_window, font=("arial", 13), width=22, state='readonly')
    courseEntry['values'] = getCoursesFromDatabase() # This should fetch course names from the course table
    courseEntry.grid(row=3, column=1, padx=10, pady=10)
    courseEntry.bind("<<ComboboxSelected>>", updateFees)

    #joined date
    joinLabel = Label(add_window,text="Joined Date",font=("arial",13),)
    joinLabel.grid(row=3,column=2,padx=30,pady=10,sticky=W)
    joinEntry = Entry(add_window,font=("arial",13),width=24)
    joinEntry.grid(row=3,column=3,padx=10,pady=10)
    joinEntry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    #fees
    feesLabel = Label(add_window,text="Fees",font=("arial",13),)
    feesLabel.grid(row=4,column=0,padx=30,pady=10,sticky=W)
    feesEntry = Entry(add_window,font=("arial",13),width=24)
    feesEntry.grid(row=4,column=1,padx=10,pady=10)
     #discount

    discountLabel = Label(add_window, text="Discount", font=("arial", 13))
    discountLabel.grid(row=4, column=2, padx=30, pady=10, sticky=W)
    discountEntry = ttk.Combobox(add_window, font=("arial", 13), width=22, state='readonly')
    discountEntry['values'] = ("0%", "25%", "50%", "75%")
    discountEntry.grid(row=4, column=3, padx=10, pady=10)

# Fees to Pay (auto-calculated based on discount)
    feesToPayLabel = Label(add_window, text="Fees to Pay", font=("arial", 13))
    feesToPayLabel.grid(row=5, column=0, padx=30, pady=10, sticky=W)
    feesToPayEntry = Entry(add_window, font=("arial", 13), width=24)
    feesToPayEntry.grid(row=5, column=1, padx=10, pady=10)
    discountEntry.bind("<<ComboboxSelected>>", lambda event: updateFeesToPay())

    #amount paid
    paidLabel = Label(add_window,text="Amount Paid",font=("arial",13),)
    paidLabel.grid(row=5,column=2,padx=30,pady=10,sticky=W)
    paidEntry = Entry(add_window,font=("arial",13),width=24)
    paidEntry.grid(row=5,column=3,padx=10,pady=10)
    #pending fees
    pendingFeesLabel = Label(add_window, text="Pending Fees", font=("arial", 13))
    pendingFeesLabel.grid(row=6, column=0, padx=30, pady=10, sticky=W)
    pendingFeesEntry = Entry(add_window, font=("arial", 13), width=24, state='readonly')
    pendingFeesEntry.grid(row=6, column=1, padx=10, pady=10)

    #batch timing
    batchLabel = Label(add_window,text="Batch",font=("arial",13),)
    batchLabel.grid(row=6,column=2,padx=30,pady=10,sticky=W)
    batchEntry = ttk.Combobox(add_window, font=("arial", 13), width=22, state='readonly')
    batchEntry['values'] = ("Morning 10-11", "Morning 11-12","Evening 3-4", "Evening 4-5", "Evening 5-6")
    batchEntry.grid(row=6, column=3, padx=10, pady=10)
    #course status
    statusLabel = Label(add_window,text="Course Status",font=("arial",13),)
    statusLabel.grid(row=7,column=0,padx=30,pady=10,sticky=W)
    statusEntry = ttk.Combobox(add_window, font=("arial", 13), width=22, state='readonly')
    statusEntry['values'] = ("Started", "In progress", "Completed")
    statusEntry.grid(row=7,column=1,padx=10,pady=10)
    #completed date
    compLabel = Label(add_window,text="Completed Date",font=("arial",13),)
    compLabel.grid(row=7,column=2,padx=30,pady=10,sticky=W)
    compEntry = Entry(add_window,font=("arial",13),width=24)
    compEntry.grid(row=7,column=3,padx=10,pady=10)
    #contact
    contactLabel = Label(add_window,text="Contact",font=("arial",13),)
    contactLabel.grid(row=8,column=0,padx=30,pady=10,sticky=W)
    contactEntry = Entry(add_window,font=("arial",13),width=24)
    contactEntry.grid(row=8,column=1,padx=10,pady=10)

    def updateFeesToPay():
        fees = int(feesEntry.get())
    
        discount_str = discountEntry.get().strip('%')
        if discount_str == '':
            discount = 0  # default to 0% if no discount is specified
        else:
            discount = int(discount_str)

        fees_to_pay = fees - (fees * discount / 100)
        feesToPayEntry.delete(0, END)
        feesToPayEntry.insert(0, fees_to_pay)

        paid_str = paidEntry.get()
        if paid_str == '':
            paid_amount = 0  # default to 0 if no amount is specified
        else:
            paid_amount = int(paid_str)

        pending_fees = fees_to_pay - paid_amount
        pendingFeesEntry.delete(0, END)
        pendingFeesEntry.insert(0, pending_fees)


    #Button
    addstudentButton = Button(add_window,text="ADD STUDENT",font=("arial",13),bg="orange",activebackground="lightgrey",command=addData)
    addstudentButton.grid(row=9,columnspan=2,pady=10)

#search student function
def search():
    def searchData():
        cur = conn.cursor()
        query = "select * from student where (Id = %s or Name = %s or Gender = %s or Course = %s or Batch_Timing=%s or Course_Status = %s or Contact=%s)"
        cur.execute(query,(idEntry.get(),nameEntry.get(),genderEntry.get(),courseEntry.get(),batchEntry.get(),statusEntry.get(),contactEntry.get()))
        fetch = cur.fetchall()
        for item in TopBar.get_children():
            TopBar.delete(item)
        for data in fetch:
            datalist = list(data)
            TopBar.insert('',END,values=datalist)
        search_window.destroy()

    search_window = Toplevel()
    search_window.resizable(False,False)
    search_window.grab_set()
    topicLabel = Label(search_window,text="Search Student",font=("arial",15),bg="#2b8783",fg="white",width=20)
    topicLabel.grid(row=0,columnspan=2,pady=10)
    idLabel = Label(search_window,text="Id",font=("arial",13),)
    idLabel.grid(row=1,column=0,padx=30,pady=10,sticky=W)
    idEntry = Entry(search_window,font=("arial",13),width=24)
    idEntry.grid(row=1,column=1,padx=10,pady=10)
    #Name
    nameLabel = Label(search_window,text="Name",font=("arial",13),)
    nameLabel.grid(row=2,column=0,padx=30,pady=10,sticky=W)
    nameEntry = Entry(search_window,font=("arial",13),width=24)
    nameEntry.grid(row=2,column=1,padx=10,pady=10)
    #gender
    genderLabel = Label(search_window,text="Gender",font=("arial",13),)
    genderLabel.grid(row=4,column=0,padx=30,pady=10,sticky=W)
    genderEntry = ttk.Combobox(search_window, font=("arial", 13), width=22, state='readonly')
    genderEntry['values'] = ("Male", "Female", "Other")
    genderEntry.grid(row=4, column=1, padx=10, pady=10)
    #course
    courseLabel = Label(search_window,text="Course",font=("arial",13),)
    courseLabel.grid(row=5,column=0,padx=30,pady=10,sticky=W)
    courseEntry = ttk.Combobox(search_window, font=("arial", 13), width=22, state='readonly')
    courseEntry['values'] = getCoursesFromDatabase() # This should fetch course names from the course table
    courseEntry.grid(row=5, column=1, padx=10, pady=10)
    #batch timing
    batchLabel = Label(search_window,text="Batch",font=("arial",13),)
    batchLabel.grid(row=6,column=0,padx=30,pady=10,sticky=W)
    batchEntry = ttk.Combobox(search_window, font=("arial", 13), width=22, state='readonly')
    batchEntry['values'] = ("Morning 10-11", "Morning 11-12","Evening 3-4", "Evening 4-5", "Evening 5-6")
    batchEntry.grid(row=6, column=1, padx=10, pady=10)
    #course status
    statusLabel = Label(search_window,text="Course Status",font=("arial",13),)
    statusLabel.grid(row=7,column=0,padx=30,pady=10,sticky=W)
    statusEntry = ttk.Combobox(search_window, font=("arial", 13), width=22, state='readonly')
    statusEntry['values'] = ("Started", "In progress", "Completed")
    statusEntry.grid(row=7,column=1,padx=10,pady=10)
    #contact
    contactLabel = Label(search_window,text="Contact",font=("arial",13),)
    contactLabel.grid(row=8,column=0,padx=30,pady=10,sticky=W)
    contactEntry = Entry(search_window,font=("arial",13),width=24)
    contactEntry.grid(row=8,column=1,padx=10,pady=10)
    #Button
    searchstudentButton = Button(search_window,text="SEARCH STUDENT",font=("arial",13),bg="orange",activebackground="lightgrey",
    command=searchData)
    searchstudentButton.grid(row=9,columnspan=2,pady=10)

#delete function
def deletestudent():
    cur = conn.cursor()
    indexing = TopBar.focus()
    print(indexing)
    content = TopBar.item(indexing)
    cid = content['values'][0]
    query = "delete from student where Id=%s"
    cur.execute(query,(cid,))
    conn.commit()
    TopBar.delete(indexing)
    messagebox.showinfo("Deleted","Deleted successfully")

#show function
def show():
    cur = conn.cursor()
    query = "select * from student"
    cur.execute(query)
    fetch = cur.fetchall()
    TopBar.delete(*TopBar.get_children())
    for data in fetch:
        TopBar.insert('',END,values=data)

#update function
def update():
    def updatedata():
        Name = nameEntry.get()
        email = emailEntry.get()
        gender = genderEntry.get()
        course = courseEntry.get()
        joined_date = joinEntry.get()
        fees = int(feesEntry.get())
        amount_paid = int(paidEntry.get())
        feestopay = int(float(feesToPayEntry.get()))
        pending_fees = feestopay - amount_paid
        timing = batchEntry.get()
        status = statusEntry.get()
        completed = compEntry.get()
        contact = contactEntry.get()
        discount = discountEntry.get()
        Id = idEntry.get()
        cur = conn.cursor()
         
        if completed == "" or completed == "None":
           completed = None

        if amount_paid > feestopay:
            messagebox.showerror("Error", "Full Amount paid already")
            return
        if pending_fees <= 0:
            pendingFeesEntry.configure(state="readonly")
        else:
            pendingFeesEntry.configure(state="normal")

        query = "update student set Name=%s,email=%s,Gender=%s,Course=%s,Joined_Date=%s,Fees=%s,discount=%s,feestopay=%s,Amount_Paid=%s,Pending_Fees=%s,Batch_Timing=%s,Course_Status=%s,Completed_Date=%s,Contact=%s where Id=%s"
        record = (Name, email, gender, course, joined_date, fees,discount,feestopay, amount_paid, pending_fees, timing, status,completed,contact,Id)
        cur.execute(query, record)
        conn.commit()
        messagebox.showinfo("Success", "Details updated successfully!")

        # Clear the existing data in Treeview
        TopBar.delete(*TopBar.get_children())

        # Retrieve and display the updated record
        cur.execute("SELECT * FROM student WHERE Id=%s", (Id,))
        updated_record = cur.fetchone()
        
        if updated_record:
            datalist = list(updated_record)
            TopBar.insert('', 'end', values=datalist)

        update_window.destroy()

    update_window = Toplevel()
    update_window.resizable(False,False)
    update_window.grab_set()
    topicLabel = Label(update_window,text="Update Details",font=("arial",15),bg="#2b8783",fg="white",width=20)
    topicLabel.grid(row=0,columnspan=2,pady=10)
    idLabel = Label(update_window,text="Id",font=("arial",13),)
    idLabel.grid(row=1,column=0,padx=30,pady=10,sticky=W)
    idEntry = Entry(update_window,font=("arial",13),width=24,state='readonly')
    idEntry.grid(row=1,column=1,padx=10,pady=10)
    #Name
    nameLabel = Label(update_window,text="Name",font=("arial",13),)
    nameLabel.grid(row=1,column=2,padx=30,pady=10,sticky=W)
    nameEntry = Entry(update_window,font=("arial",13),width=24,state='readonly')
    nameEntry.grid(row=1,column=3,padx=10,pady=10)
    #email
    emailLabel = Label(update_window,text="email",font=("arial",13),)
    emailLabel.grid(row=2,column=0,padx=30,pady=10,sticky=W)
    emailEntry = Entry(update_window,font=("arial",13),width=24)
    emailEntry.grid(row=2,column=1,padx=10,pady=10)
    #gender
    genderLabel = Label(update_window,text="Gender",font=("arial",13),)
    genderLabel.grid(row=2,column=2,padx=30,pady=10,sticky=W)
    #dropdown change
    genderEntry = ttk.Combobox(update_window, font=("arial", 13), width=22,state='readonly')
    genderEntry['values'] = ("Male", "Female", "Other")
    genderEntry.grid(row=2, column=3, padx=10, pady=10)
    #course
    courseLabel = Label(update_window,text="Course",font=("arial",13))
    courseLabel.grid(row=3,column=0,padx=30,pady=10,sticky=W)
    #course dropdown
    courseEntry = ttk.Combobox(update_window, font=("arial", 13), width=22)
    courseEntry['values'] = getCoursesFromDatabase() # This should fetch course names from the course table
    courseEntry.grid(row=3, column=1, padx=10, pady=10)
    #courseEntry.bind("<<ComboboxSelected>>", updateFees)

    #joined date
    joinLabel = Label(update_window,text="Joined Date",font=("arial",13),)
    joinLabel.grid(row=3,column=2,padx=30,pady=10,sticky=W)
    joinEntry = Entry(update_window,font=("arial",13),width=24)
    joinEntry.grid(row=3,column=3,padx=10,pady=10)
    #fees
    feesLabel = Label(update_window,text="Fees",font=("arial",13))
    feesLabel.grid(row=4,column=0,padx=30,pady=10,sticky=W)
    feesEntry = Entry(update_window,font=("arial",13),width=24)
    feesEntry.grid(row=4,column=1,padx=10,pady=10)
    #discount

    discountLabel = Label(update_window, text="Discount", font=("arial", 13))
    discountLabel.grid(row=4, column=2, padx=30, pady=10, sticky=W)
    discountEntry = ttk.Combobox(update_window, font=("arial", 13), width=22)
    discountEntry['values'] = ("0%", "25%", "50%", "75%")
    discountEntry.grid(row=4, column=3, padx=10, pady=10)

# Fees to Pay (auto-calculated based on discount)
    feesToPayLabel = Label(update_window, text="Fees to Pay", font=("arial", 13))
    feesToPayLabel.grid(row=5, column=0, padx=30, pady=10, sticky=W)
    feesToPayEntry = Entry(update_window, font=("arial", 13), width=24)
    feesToPayEntry.grid(row=5, column=1, padx=10, pady=10)
    #discountEntry.bind("<<ComboboxSelected>>", lambda event: updateFeesToPay())
    #amount paid
    paidLabel = Label(update_window,text="Amount Paid",font=("arial",13),)
    paidLabel.grid(row=5,column=2,padx=30,pady=10,sticky=W)
    paidEntry = Entry(update_window,font=("arial",13),width=24)
    paidEntry.grid(row=5,column=3,padx=10,pady=10)
    #pending fees
    pendingFeesLabel = Label(update_window, text="Pending Fees", font=("arial", 13))
    pendingFeesLabel.grid(row=6, column=0, padx=30, pady=10, sticky=W)
    pendingFeesEntry = Entry(update_window, font=("arial", 13), width=24)
    pendingFeesEntry.grid(row=6, column=1, padx=10, pady=10)
    #batch timing
    batchLabel = Label(update_window,text="Batch",font=("arial",13),)
    batchLabel.grid(row=6,column=2,padx=30,pady=10,sticky=W)
    batchEntry = ttk.Combobox(update_window, font=("arial", 13), width=22)
    batchEntry['values'] = ("Morning 10-11", "Morning 11-12","Evening 3-4", "Evening 4-5", "Evening 5-6")
    batchEntry.grid(row=6, column=3, padx=10, pady=10)
    #course status
    statusLabel = Label(update_window,text="Course Status",font=("arial",13),)
    statusLabel.grid(row=7,column=0,padx=30,pady=10,sticky=W)
    statusEntry = ttk.Combobox(update_window, font=("arial", 13), width=22)
    statusEntry['values'] = ("Started", "In progress", "Completed")
    statusEntry.grid(row=7,column=1,padx=10,pady=10)
    #completed date
    compLabel = Label(update_window,text="Completed Date",font=("arial",13),)
    compLabel.grid(row=7,column=2,padx=30,pady=10,sticky=W)
    compEntry = Entry(update_window,font=("arial",13),width=24)
    compEntry.grid(row=7,column=3,padx=10,pady=10)
    #contact
    contactLabel = Label(update_window,text="Contact",font=("arial",13),)
    contactLabel.grid(row=8,column=0,padx=30,pady=10,sticky=W)
    contactEntry = Entry(update_window,font=("arial",13),width=24)
    contactEntry.grid(row=8,column=1,padx=10,pady=10)
        #Button
    updatestudentButton = Button(update_window,text="UPDATE STUDENT",font=("arial",13),bg="orange",activebackground="lightgrey",
    command=updatedata)
    updatestudentButton.grid(row=9,columnspan=2,pady=10)

    #geting from selecting
    indexing = TopBar.focus()
    content = TopBar.item(indexing)
    listdata = content["values"]
    #id number 
    idEntry.configure(state='normal')
    idEntry.insert(0, listdata[0])
    idEntry.configure(state='readonly')
    #name
    nameEntry.configure(state="normal")
    nameEntry.insert(0,listdata[1])
    nameEntry.configure(state="readonly")
    #email
    emailEntry.insert(0,listdata[2])
    #gender
    genderEntry.configure(state="normal")
    genderEntry.set(listdata[3])
    genderEntry.configure(state="disabled")
    #course
    courseEntry.configure(state="normal")
    courseEntry.insert(0,listdata[4])
    courseEntry.configure(state="disabled")
    #joinEntry
    joinEntry.configure(state="normal")
    joinEntry.insert(0,listdata[5])
    joinEntry.configure(state="disabled")
    #fees
    feesEntry.configure(state="normal")
    feesEntry.insert(0,listdata[6])
    feesEntry.configure(state="readonly")
    #discount
    discountEntry.insert(0,listdata[7])
    discountEntry.configure(state="disabled")
    #fees to pay
    feesToPayEntry.configure(state="normal")
    feesToPayEntry.insert(0,listdata[8])
    feesToPayEntry.configure(state="readonly")
    #paid
    paidEntry.insert(0,listdata[9])
    #pending
    pendingFeesEntry.configure(state="normal")
    pendingFeesEntry.insert(0,listdata[10])
    pendingFeesEntry.configure(state="readonly")
    #batch timing
    batchEntry.insert(0,listdata[11])
    #status
    statusEntry.insert(0,listdata[12])
    #completion date
    compEntry.configure(state="normal")
    compEntry.insert(0,listdata[13])
    #contact
    contactEntry.configure(state="normal")
    contactEntry.insert(0,listdata[14])
    contactEntry.configure(state="readonly")

#exit function
def exit():
    window.destroy()

#course function
#course components
def fetch_courses():
            cur = conn.cursor()
            cur.execute("SELECT * FROM course")
            fetch = cur.fetchall()
            TopBar.delete(*TopBar.get_children())
            for data in fetch:
                datalist = list(data)
                TopBar.insert("", END, values=datalist)
            cur.close()

def coursefunction():
    #clear Treeview
    def clear_treeview():
        TopBar.delete(*TopBar.get_children())
    for col in TopBar['columns']:
        clear_treeview()
        TopBar["columns"] = ("course_id", "course_name", "no_of_slots", "slots_available" ,"fees", "course_duration")
        TopBar.heading("course_id", text="Course ID")
        TopBar.heading("course_name", text="Course Name")
        TopBar.heading("no_of_slots", text="No. of Slots")
        TopBar.heading("slots_available", text="Slots Available")
        TopBar.heading("fees", text="Fees")
        TopBar.heading("course_duration", text="Course Duration")
        fetch_courses()

#add course window
def add_course_window():
    def add_course():
        course_name = course_name_entry.get()
        no_of_slots = int(no_of_slots_entry.get())
        fees = int(feesentry.get())
        course_duration = course_duration_entry.get()
        
        cur = conn.cursor()
        cur.execute("INSERT INTO course (course_name, no_of_slots, slots_available,fees,course_duration) VALUES (%s, %s, %s, %s,%s)", 
                       (course_name, no_of_slots, no_of_slots,fees, course_duration))
        conn.commit()
        cur.close()

        fetch_courses()
        course_window.destroy()

    course_window = Toplevel()
    course_window.title("Add Course")

    Course_Label = Label(course_window,text="Add Course Details",font=("arial",15),bg="#2b8783",fg="white",width=20)
    Course_Label.grid(row=0,columnspan=2,pady=10)
   
    Course_Name = Label(course_window, text="Course Name",font=("arial",13))
    Course_Name.grid(row=1,column=0,padx=30,pady=10,sticky=W)
    course_name_entry = Entry(course_window,font=("arial",13),width=24)
    course_name_entry.grid(row=1,column=1,padx=10,pady=10)
    
    No_of_slots = Label(course_window, text="No. of Slots",font=("arial",13))
    No_of_slots.grid(row=2,column=0,padx=30,pady=10,sticky=W)
    no_of_slots_entry = Entry(course_window,font=("arial",13),width=24)
    no_of_slots_entry.grid(row=2,column=1,padx=10,pady=10)

    fees = Label(course_window, text="Fees",font=("arial",13))
    fees.grid(row=3,column=0,padx=30,pady=10,sticky=W)
    feesentry = Entry(course_window,font=("arial",13),width=24)
    feesentry.grid(row=3,column=1,padx=10,pady=10)
    
    course_duration = Label(course_window, text="Course Duration",font=("arial",13))
    course_duration.grid(row=4,column=0,padx=30,pady=10,sticky=W)
    course_duration_entry = ttk.Combobox(course_window, font=("arial", 13), width=24)
    course_duration_entry['values'] = ("2 Months","4 Months", "6 Months", "8 Months", "1 Year")
    course_duration_entry.grid(row=4, column=1, padx=10, pady=10)
    #course_duration_entry = Entry(course_window,font=("arial",13),width=24)
    #course_duration_entry.grid(row=4,column=1,padx=10,pady=10)

    #addstudent button to add it in the course window
    addstudent = Button(course_window, text="Add Course", font=("arial",13),bg="orange",activebackground="lightgrey",
    command=add_course)
    addstudent.grid(row=5,columnspan=2,pady=10)

#Main window
window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('smog')
window.title("Educational Institution Management System")
window.geometry("1500x700+0+0")

#date label
dateLabel = Label(window,text="hello",font=("arial",18),bg="lightgrey",width=17,height=1,pady=10)
dateLabel.place(x=5,y=10)
clock()

#Header
Topic = Label(window,text="Educational Institution Management System",font=("arial",20),bg="#2b8783",width=68,height=1,pady=7,fg="white")
Topic.place(x=255,y=10)

#Left Frame
sidebar = Frame(window,bg="#2b8783",height=625,width=245)
sidebar.place(x=5,y=70)

#Logo
Logo = PhotoImage(file="menuicon.png")
logo_label = Label(sidebar,image=Logo)
logo_label.place(x=75,y=20)

#add button
addButton = Button(sidebar,text="Add student",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=addstudent)
addButton.place(x=25,y=150)
#search Button
searchButton = Button(sidebar,text="Search student",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=search)
searchButton.place(x=25,y=210)
#update Button
updateButton = Button(sidebar,text="Update Details",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=update)
updateButton.place(x=25,y=270)
#show Button
ShowButton = Button(sidebar,text="Show student",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=show)
ShowButton.place(x=25,y=330)
#delete Button
deleteButton = Button(sidebar,text="Delete student",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=deletestudent)
deleteButton.place(x=25,y=390)
#export Button
courseButton = Button(sidebar,text="Course Details",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=coursefunction)
courseButton.place(x=25,y=450)
#Add course Button
add_course_button = Button(sidebar, text="Add Course",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=add_course_window)
add_course_button.place(x=25,y=510)
#exit
ExitButton = Button(sidebar,text="Exit",height=1,width=20,font=("arial",13),activebackground="cornflowerblue",
cursor="hand2",command=exit)
ExitButton.place(x=25,y=570)

#Right Frame
mainbar = Frame(window,)
mainbar.place(x=255,y=70,height=625,width=1090)

#scrollbar
ScrollbarX = Scrollbar(mainbar,orient=HORIZONTAL)
ScrollbarY = Scrollbar(mainbar,orient=VERTICAL)
ScrollbarX.pack(side=BOTTOM,fill=X)
ScrollbarY.pack(side=RIGHT,fill=Y)

#Treeview styling #ebedc7
style = ttk.Style()
style.configure("Treeview", background="lightgrey", 
foreground="black", rowheight=25, fieldbackground="#ebedc7",font=("arial",12))
style.configure("Treeview.Heading",background="#2d9c97",font=("arial",15),foreground="white")
style.map("Treeview", background=[('selected', 'cornflowerblue')], foreground=[('selected', 'white')])

#Top bar
TopBar = ttk.Treeview(mainbar,style="Treeview",columns=("Id","Name","email","Gender","Course","Joined Date","Fees","discount","feestopay",
"Amount Paid","Pending Fees","Batch Timing","Course status","Completed Date","Contact"),
xscrollcommand=ScrollbarX.set,yscrollcommand=ScrollbarY.set)

#scrollbar function
ScrollbarX.config(command=TopBar.xview)
ScrollbarY.config(command=TopBar.yview)
TopBar.pack(fill="both",expand=1)

#adding text to treeview
TopBar.heading("Id",text="Id")
TopBar.heading("Name",text="Name")
TopBar.heading("email",text="email")
TopBar.heading("Gender",text="Gender")
TopBar.heading("Course",text="Course")
TopBar.heading("Joined Date",text="Joined Date")
TopBar.heading("Fees",text="Fees")
TopBar.heading("discount",text="Discount")
TopBar.heading("feestopay",text="FeesToPay")
TopBar.heading("Amount Paid",text="Amount Paid")
TopBar.heading("Pending Fees",text="Pending Fees")
TopBar.heading("Batch Timing",text="Batch Timing")
TopBar.heading("Course status",text="Course status")
TopBar.heading("Completed Date",text="Completed Date")
TopBar.heading("Contact",text="Contact")

TopBar.config(show="headings")

window.mainloop()