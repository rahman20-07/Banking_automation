from tkinter import Frame,Tk,Label,Entry,Button,messagebox, Scrollbar, VERTICAL, HORIZONTAL, END, LEFT, RIGHT, BOTTOM, BOTH, Y, X
from tkinter.ttk import Combobox, Treeview
from capcha_test import generate_captcha #For caotcha
from PIL import Image,ImageTk    #For image in our project

import time,random
from table_creation import generate
from email_test import send_openacn_akc , send_otp , send_otp_4_pass
import sqlite3
import re

generate()

def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt)  #ms (1 sec)

list_img=['images/logo.jpg','images/logo1.jpg','images/logo2.png','images/logo3.jpg','images/logo4.jpg']
def image_animation():
    index=random.randint(0,4)
    img=Image.open(list_img[index]).resize((250,115))
    imgtk=ImageTk.PhotoImage(img,master=root)
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)

    logo_lbl.image=imgtk
    logo_lbl.after(1000,image_animation)


root=Tk()
root.state('zoomed')
root.configure(bg="#DADAFC")

title_lbl=Label(root,text="Banking Automation",fg='black',bg="#DADAFC",font=('Arial',50,'bold','underline'))
title_lbl.pack()

dt_lbl=Label(root,font=('Arial',15,'bold'),bg="#DADAFC")
dt_lbl.pack(pady=5)
show_dt()

img=Image.open("images/logo.jpg").resize((250,115))
imgtk=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=imgtk)
logo_lbl.place(relx=0,rely=0)
image_animation()

footer_lbl=Label(root,font=('Arial',20,'bold'),bg='#DADAFC',text="Developed By\nIbrahim Rahman @6203864676")
footer_lbl.pack(side='bottom')

code_captcha=generate_captcha()


#Esse pahle ka sara  code Top level code tha 
#Ab hm function bna bna ke likhenge

#ye function chiled windo keliye h
def main_screen():
    def referesh_captcha():
        global code_captcha
        code_captcha=generate_captcha()
        captcha_value_lbl.configure(text=code_captcha)    

    frm=Frame(root,highlightbackground='black',highlightthickness=2 )
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.78)

    def forgot():
        frm.destroy()
        fb_screen()


    def login():
        utype=acntype_cb.get()
        uacn=acnno_e.get()
        upass=pass_e.get()


        ucaptcha=captcha_e.get()
        global code_captcha
        code_captcha=code_captcha.replace(' ','')

        if utype=="Admin":
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid Captcha")
            else:
                messagebox.showerror("Login",'You are not Admin!')
        else:
            if code_captcha==ucaptcha:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacn,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])
            else:
                messagebox.showerror("Login","Invalid Captcha")

    acntype_lbl=Label(frm,text="ACN Type",font=('Arial',20,'bold'),bg='powder blue')
    acntype_lbl.place(relx=.35,rely=.1)


    acntype_cb=Combobox(frm,values=['User','Admin'],font=('Arial',20,'bold'))
    acntype_cb.current(0)
    acntype_cb.place(relx=.45,rely=.1)

    acnno_lbl=Label(frm,text="👤 ACN",font=('Arial',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.35,rely=.2)

    acnno_e=Entry(frm,font=('Arial',20,'bold'),bd=4)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()

    pass_lbl=Label(frm,text="🔒 Pass",font=('Arial',20,'bold'),bg='powder blue')
    pass_lbl.place(relx=.35,rely=.3)

    pass_e=Entry(frm,font=('Arial',20,'bold'),bd=4,show='*')
    pass_e.place(relx=.45,rely=.3)

    capcha_lbl=Label(frm,text="Capcha",font=('Arial',20,'bold'),bg='powder blue')
    capcha_lbl.place(relx=.35,rely=.4)

    captcha_value_lbl=Label(frm,text=code_captcha,fg='green',font=('Arial',20,'bold'))
    captcha_value_lbl.place(relx=.45,rely=.4)

    referesh_btn=Button(frm,text="referesh 🔄",command=referesh_captcha)
    referesh_btn.place(relx=.6,rely=.4)

    captcha_e=Entry(frm,font=('Arial',20,'bold'),bd=4,)
    captcha_e.place(relx=.45,rely=.5)

    submit_btn=Button(frm,text="Login",command=login,width=23,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    submit_btn.place(relx=.461,rely=.6)

    fp_btn=Button(frm,text="Forgot Pass",command=forgot,width=23,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    fp_btn.place(relx=.461,rely=.7)

    # new_btn=Button(frm,text="New User",bg='#DADAFC',bd=4,font=('Arial',16,'bold'))
    # new_btn.place(relx=.57,rely=.7)


def fb_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2 )
    frm.configure(bg='sky blue')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.78)

    def back():
        frm.destroy()
        main_screen()

    def fp_pass():
        uemail=email_e.get()
        uacn=acnno_e.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))
        torow=curobj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Pass","To ACN does not exist")
        else:
            if uemail==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_4_pass(uemail,otp)
                messagebox.showinfo("Forgot Passworf","OTP sent to registered email,kindly veryfy")

                def verify_otp():
                    uotp=int(otp_e.get())
                    if otp==uotp:
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='select acn_pass from accounts where acn_acno=?'    
                        curobj.execute(query,(uacn,))
                        messagebox.showinfo("Forgot Password",f"Your Password is {curobj.fetchone()[0]}")
                        conobj.close() 
                        frm.destroy()
                        main_screen()
                        
                    else:
                         messagebox.showerror("Forgot Password","Invalid OTP")
                    
                otp_e=Entry(frm,font=('Arial',15,'bold'),bd=3)
                otp_e.place(relx=.7,rely=.41)
                otp_e.focus()

                verify_btn=Button(frm,text="Verify",width=15,command=verify_otp,bg='#DADAFC',bd=3,font=('Arial',15,'bold'))
                verify_btn.place(relx=.73,rely=.55)
            else:
                        messagebox.showerror("Forgot Password","Email is not matched")


    back_btn=Button(frm,text="Back",bg='#DADAFC',bd=4,font=('Arial',15,'bold'),command=back)
    back_btn.place(relx=0,rely=0)

    acnno_lbl=Label(frm,text="👤 ACN",font=('Arial',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.35,rely=.2)

    acnno_e=Entry(frm,font=('Arial',20,'bold'),bd=4)
    acnno_e.place(relx=.45,rely=.2)
    acnno_e.focus()


    email_lbl=Label(frm,text="📧 Email",font=('Arial',20,'bold'),bg='powder blue')
    email_lbl.place(relx=.35,rely=.3)

    email_e=Entry(frm,font=('Arial',20,'bold'),bd=4)
    email_e.place(relx=.45,rely=.3)

    sub_btn=Button(frm,command=fp_pass,text="Submit",width=23,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    sub_btn.place(relx=.457,rely=.4)


def admin_screen():
    frm=Frame(root,highlightbackground='black',highlightthickness=2 )
    frm.configure(bg="#e9e4d3")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.78)

    def logout():
        frm.destroy()
        main_screen()

    logout_btn=Button(frm,text="Logout",bg='#DADAFC',bd=4,font=('Arial',15,'bold'),command=logout)
    logout_btn.place(relx=.9,rely=.01)

    def open():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.1,rely=.1,relwidth=.8,relheight=.8 )

        t_lbl=Label(ifrm,text="Account open screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()

        def openac():
             uname=name_e.get()
             uemail=email_e.get()  
             umob=mob_e.get()
             uadhar=adhar_e.get()   
             uadr=adr_e.get()
             udob=dob_e.get()
             upass=generate_captcha()
             upass=upass.replace(" ",'')
             ubal=0
             uopendate=time.strftime("%A %d-%b-%Y") 

             #empty validation
             if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0:
                 messagebox.showerror("Open Account","Empty fields are not allowed")
                 return

             #email validater 
             match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
             if match==None:
                 messagebox.showerror("Open Account","Kindly check format of Email")
                 return
             
             #mon validation
             match=re.fullmatch("[6-9][0-9]{9}",umob)
             if match==None:
                 messagebox.showerror("Open Account","Kindly check format of mob")
                 return
             
             #adhar validation
             match=re.fullmatch("[6-9]{12}",uadhar)
             if match==None:
                 messagebox.showerror("Open Account","Kindly check format of Adhar")
                 return

             conobj=sqlite3.connect(database='bank.sqlite')
             curobj=conobj.cursor()
             query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)' 
             curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendate))
             conobj.commit()
             conobj.close()

             conobj=sqlite3.connect(database='bank.sqlite')
             curobj=conobj.cursor()
             curobj.execute("select max(acn_acno) from accounts")
             uacn=curobj.fetchone()[0]
             conobj.close() 

             send_openacn_akc(uemail,uname,uacn,upass)
             messagebox.showinfo("Account","Account opened and details sent to email")
             frm.destroy()
             admin_screen()



        name_lbl=Label(ifrm,text="Name",font=('Arial',20,'bold'),bg='#dededc')
        name_lbl.place(relx=.09,rely=.2)

        name_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        name_e.place(relx=.19,rely=.2)
        name_e.focus()

        email_lbl=Label(ifrm,text="Email",font=('Arial',20,'bold'),bg='#dededc')
        email_lbl.place(relx=.09,rely=.4)

        email_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        email_e.place(relx=.19,rely=.4)

        mob_lbl=Label(ifrm,text="Mob",font=('Arial',20,'bold'),bg='#dededc')
        mob_lbl.place(relx=.09,rely=.6)

        mob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        mob_e.place(relx=.19,rely=.6)

        adhar_lbl=Label(ifrm,text="Adhar",font=('Arial',20,'bold'),bg='#dededc')
        adhar_lbl.place(relx=.52,rely=.2)

        adhar_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        adhar_e.place(relx=.62,rely=.2)

        adr_lbl=Label(ifrm,text="Adress",font=('Arial',20,'bold'),bg='#dededc')
        adr_lbl.place(relx=.52,rely=.4)

        adr_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        adr_e.place(relx=.62,rely=.4)

        dob_lbl=Label(ifrm,text="DOB",font=('Arial',20,'bold'),bg='#dededc')
        dob_lbl.place(relx=.52,rely=.6)

        dob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        dob_e.place(relx=.62,rely=.6)

        open_btn=Button(frm,command=openac,text="Open ACN",bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
        open_btn.place(relx=.72,rely=.75)



    def close():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.1,rely=.1,relwidth=.8,relheight=.8 )

        t_lbl=Label(ifrm,text="Account close screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()

        def sent_close_otp():
            uacn=acnno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Close Account","Account does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_4_pass(torow[3],otp)
                messagebox.showinfo("Close Account","OTP sent to registered email,kindly veryfy")

                def verify_otp():
                    uotp=int(otp_e.get())
                    if otp==uotp:
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from accounts where acn_acno=?'    
                        curobj.execute(query,(uacn,))
                        messagebox.showinfo("Close Account","Account Closed")
                        conobj.commit()
                        conobj.close() 
                        frm.destroy()
                        admin_screen()
                        
                    else:
                        messagebox.showerror("Close Account","Invalid OTP")
                        
                otp_e=Entry(frm,font=('Arial',15,'bold'),bd=3)
                otp_e.place(relx=.7,rely=.41)
                otp_e.focus()

                verify_btn=Button(frm,text="Verify",width=15,command=verify_otp,bg='#DADAFC',bd=3,font=('Arial',15,'bold'))
                verify_btn.place(relx=.73,rely=.55)

    

        acnno_lbl=Label(ifrm,text="👤ACN",font=('Arial',20,'bold'),bg='powder blue')
        acnno_lbl.place(relx=.35,rely=.2)

        acnno_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        acnno_e.place(relx=.45,rely=.2)
        acnno_e.focus()

        otp_btn=Button(ifrm,command=sent_close_otp,text="Send OTP",bd=4,font=('Arial',15,'bold'))
        otp_btn.place(relx=.6,rely=.3)

    #Ye function use view window keliye h
    def view():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.1,rely=.1,relwidth=.8,relheight=.8 )

        
        t_lbl=Label(ifrm,text="Account view screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()

        # Creating Treeview frame
        tree_frame = Frame(ifrm)
        tree_frame.place(relx=.05,rely=.1,relwidth=.9,relheight=.75)

        # Creating scrollbars
        v_scroll = Scrollbar(tree_frame, orient=VERTICAL)
        h_scroll = Scrollbar(tree_frame, orient=HORIZONTAL)


        # Creating Treeview
        tree = Treeview(tree_frame, 
                   columns=("ACNO", "NAME", "Email", "MOB", "OPEN DATE", "BALANCE"),
                   show='headings',
                   yscrollcommand=v_scroll.set,
                   xscrollcommand=h_scroll.set)
        
        # Configure scrollbars
        v_scroll.config(command=tree.yview)
        #h_scroll.config(command=tree.xview)

        # Define headings
        tree.heading("ACNO", text="ACCOUNT NO")
        tree.heading("NAME", text="NAME")
        tree.heading("Email", text="EMAIL")
        tree.heading("MOB", text="MOBILE")
        tree.heading("OPEN DATE", text="OPEN DATE")
        tree.heading("BALANCE", text="BALANCE")

        # Configure column widths
        tree.column("ACNO", width=100, anchor='center')
        tree.column("NAME", width=150, anchor='center')
        tree.column("Email", width=200, anchor='center')
        tree.column("MOB", width=120, anchor='center')
        tree.column("OPEN DATE", width=150, anchor='center')
        tree.column("BALANCE", width=100, anchor='center')


        # Pack treeview and scrollbars
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        v_scroll.pack(side=RIGHT, fill=Y)
        #h_scroll.pack(side=BOTTOM, fill=X)

        # Fetch data from database
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        curobj.execute(query)
        
        # Insert data into treeview
        for row in curobj.fetchall():
            tree.insert("", END, values=row)


        # table_headers= ("ACNO","NAME","Email","MOB","OPEN DATE","BALANCE")
        # mytable = Table(ifrm, table_headers,headings_bold=True)
        # mytable.place(relx=.1,rely=.1,relwidth=.8,relheight=.8)

        # conobj=sqlite3.connect(database='bank.sqlite')
        # curobj=conobj.cursor()
        # query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        # curobj.execute(query)
        # for tup in curobj.fetchall():
        #     mytable.insert_row(tup)

        conobj.close()

    open_btn=Button(frm,text="Open ACN",width=10,command=open,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    open_btn.place(relx=.25,rely=.01)

    close_btn=Button(frm,text="Close ACN",width=10,command=close,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    close_btn.place(relx=.4,rely=.01)

    view_btn=Button(frm,text="View ACN",width=10,command=view,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    view_btn.place(relx=.55,rely=.01) 

def user_screen(uacn,uname):
    frm=Frame(root,highlightbackground='black',highlightthickness=2 )
    frm.configure(bg='#DADAFC')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.78)


    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacn,))
    row=curobj.fetchone()
    conobj.close()

    def logout():
        frm.destroy()
        main_screen()


    def check():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.15,rely=.13,relwidth=.75,relheight=.79 )

        t_lbl=Label(ifrm,text="This is check details screen",font=('Arial',20,'bold'),bg="#e9e2ff",fg='black')
        t_lbl.pack() 

        acn_lbl=Label(ifrm,text=f"Account No\t=\t{row[0]}",font=('Arial',20),bg='white',fg='black')
        acn_lbl.place(relx=.15,rely=.15) 

        bal_lbl=Label(ifrm,text=f"Account Bal\t=\t{row[8]}",font=('Arial',20),bg='white',fg='black')
        bal_lbl.place(relx=.15,rely=.3)

        dob_lbl=Label(ifrm,text=f"Date of birth\t=\t{row[7]}",font=('Arial',20),bg='white',fg='black')
        dob_lbl.place(relx=.15,rely=.6)

        adhar_lbl=Label(ifrm,text=f"ADHAR No\t=\t{row[5]}",font=('Arial',20),bg='white',fg='black')
        adhar_lbl.place(relx=.15,rely=.75)

        bal_lbl=Label(ifrm,text=f"Open Date\t=\t{row[9]}",font=('Arial',20),bg='white',fg='black')
        bal_lbl.place(relx=.15,rely=.45)


    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.15,rely=.13,relwidth=.75,relheight=.79 )

        t_lbl=Label(ifrm,text="This is update screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()


        def update_details():
            uname=name_e.get()
            upass=pass_e.get()
            uemail=email_e.get()
            umob=mob_e.get()


            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")
            frm.destroy()
            user_screen(uacn,None)


        name_lbl=Label(ifrm,text="Name",font=('Arial',20,'bold'),bg='#dededc')
        name_lbl.place(relx=.09,rely=.24)

        name_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        name_e.place(relx=.19,rely=.24)
        name_e.focus()
        name_e.insert(0,row[1])

        pass_lbl=Label(ifrm,text="Pass",font=('Arial',20,'bold'),bg='#dededc')
        pass_lbl.place(relx=.52,rely=.24)

        pass_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        pass_e.place(relx=.62,rely=.24)
        pass_e.insert(0,row[2])

        email_lbl=Label(ifrm,text="Email",font=('Arial',20,'bold'),bg='#dededc')
        email_lbl.place(relx=.09,rely=.46)

        email_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        email_e.place(relx=.19,rely=.46)
        email_e.insert(0,row[3])

        mob_lbl=Label(ifrm,text="Mob",font=('Arial',20,'bold'),bg='#dededc')
        mob_lbl.place(relx=.52,rely=.46)

        mob_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        mob_e.place(relx=.62,rely=.46)
        mob_e.insert(0,row[4])


        update_btn=Button(ifrm,text="Update Details",width=15,command=update_details,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
        update_btn.place(relx=.47,rely=.72)

    
    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.15,rely=.13,relwidth=.75,relheight=.79 )

        t_lbl=Label(ifrm,text="This is deposit screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()

        def deposit_amt():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn,None)
            

        amt_lbl=Label(ifrm,text="Amount",font=('Arial',20,'bold'),bg='#dededc')
        amt_lbl.place(relx=.25,rely=.35)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        amt_e.place(relx=.36,rely=.35)
        amt_e.focus()

        amt_btn=Button(ifrm,text="Deposit",width=15,command=deposit_amt,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
        amt_btn.place(relx=.46,rely=.55)


    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.15,rely=.13,relwidth=.75,relheight=.79 )

        t_lbl=Label(ifrm,text="This is withdra screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()


        def withdraw_amt():
            uamt=float(amt_e.get())
            if row[8]>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn,None)
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")


        amt_lbl=Label(ifrm,text="Amount",font=('Arial',20,'bold'),bg='#dededc')
        amt_lbl.place(relx=.25,rely=.35)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        amt_e.place(relx=.36,rely=.35)
        amt_e.focus()

        amt_btn=Button(ifrm,text="Withdraw",width=15,command=withdraw_amt,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
        amt_btn.place(relx=.46,rely=.55)


    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg="#dededc")
        ifrm.place(relx=.15,rely=.13,relwidth=.75,relheight=.79 )

        t_lbl=Label(ifrm,text="This is transfer screen",font=('Arial',20,'bold'),bg='#dededc',fg='black')
        t_lbl.pack()

        def transfer_amt():
            toacn=to_e.get()
            uamt=float(amt_e.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(toacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showerror("Transfer","To ACN does not exist")
            else:
                if row[8]>=uamt:
                    otp=random.randint(1000,9999)
                    send_otp(row[3],otp,uamt)
                    messagebox.showinfo("Transfer","OTP sent to registered email,kindly veryfy")

                    def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()
                            query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                            query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'

                            curobj.execute(query1,(uamt,uacn))
                            curobj.execute(query2,(uamt,toacn))
                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo("Transfer",f"{uamt} Amount Transfered")
                            frm.destroy()
                            user_screen(uacn,None)
                        else:
                            messagebox.showerror("Transfer","Invalid OTP")
                    
                    otp_e=Entry(ifrm,font=('Arial',15,'bold'),bd=3)
                    otp_e.place(relx=.7,rely=.41)
                    otp_e.focus()

                    verify_btn=Button(ifrm,text="Verify",width=15,command=verify_otp,bg='#DADAFC',bd=3,font=('Arial',15,'bold'))
                    verify_btn.place(relx=.73,rely=.55)
                else:
                    messagebox.showerror("Transfer","Insufficient Bal")


        to_lbl=Label(ifrm,text="To ACN",font=('Arial',20,'bold'),bg='#dededc')
        to_lbl.place(relx=.25,rely=.25)

        to_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        to_e.place(relx=.36,rely=.25)
        to_e.focus()


        amt_lbl=Label(ifrm,text="Amount",font=('Arial',20,'bold'),bg='#dededc')
        amt_lbl.place(relx=.25,rely=.4)

        amt_e=Entry(ifrm,font=('Arial',20,'bold'),bd=4)
        amt_e.place(relx=.36,rely=.4)

        transfer_btn=Button(ifrm,text="Transfer",width=15,command=transfer_amt,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
        transfer_btn.place(relx=.46,rely=.55)



    logout_btn=Button(frm,text="Logout",bg='#DADAFC',bd=4,font=('Arial',15,'bold'),command=logout)
    logout_btn.place(relx=.9,rely=.01)


    wel_lbl=Label(frm,text=f"Welcom {row[1]}",font=('Arial',20,'bold'),bg='#DADAFC',fg='black')
    wel_lbl.place(relx=0,rely=0)


    check_btn=Button(frm,text="User Details",width=15,command=check,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    check_btn.place(relx=.001,rely=.17)

    update_btn=Button(frm,text="Update Details",width=15,command=update,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    update_btn.place(relx=.001,rely=.32)

    deposit_btn=Button(frm,text="Deposit",width=15,command=deposit,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    deposit_btn.place(relx=.001,rely=.47)

    withdraw_btn=Button(frm,text="Withdraw",width=15,command=withdraw,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    withdraw_btn.place(relx=.001,rely=.62)

    transfer_btn=Button(frm,text="Transfer",width=15,command=transfer,bg='#DADAFC',bd=4,font=('Arial',15,'bold'))
    transfer_btn.place(relx=.001,rely=.77)

main_screen()
root.mainloop()