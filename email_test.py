# from gmail import GMail,Message
# email_id="ibrahimrahmancsework@gmail.com"
# app_pass="qsvn wmty yuiy uqou"

# def send_openacn_akc(uemail,uname,uacn,upass):
#     con=GMail(email_id,app_pass)
#     sub="Congrates 😊,Account opend successfully"
#     utext=f'''Hello,{uname}
#     welcme to 7R Bank
#     Your Acc No is {uacn}
#     Your Pass is {upass}
#     Kindly change your password when you login first

#     Thanks
#     7R Bank
#     Delhi
#     '''
#     msg=Message(to=uemail,subject=sub,text=utext)
#     con.send(msg)


import yagmail
#Replace with your email_id & App_password
email_id = "ibrahimrahmancsework@gmail.com"
app_pass = "qsvn wmty yuiy uqou"

def send_openacn_akc(uemail, uname, uacn, upass):
    try:
        # Initialize yagmail
        con = yagmail.SMTP(email_id, app_pass)
        
        sub = "Congrates 😊, Account opened successfully"
        utext = f'''Hello {uname},

Welcome to 7R Bank!

Your Account Details:
- Account Number: {uacn}
- Password: {upass}

Kindly change your password when you login first time.

Thanks,
7R Bank
Delhi
'''
        # Send email
        con.send(to=uemail, subject=sub, contents=utext)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")


def send_otp(uemail,otp,amt):
    try:
        # Initialize yagmail
        con = yagmail.SMTP(email_id, app_pass)
        
        sub = "OTP for fund transfer"
        utext = f'''Your {otp} to transfer amount {amt}
        Kindly use this otp to complete transfer
        please don't share to anyone
        Thanks,
        7R Bank
        Delhi
        '''
        # Send email
        con.send(to=uemail, subject=sub, contents=utext)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")

def send_otp_4_pass(uemail,otp):
    try:
        # Initialize yagmail
        con = yagmail.SMTP(email_id, app_pass)
        
        sub = "OTP for Password recovery"
        utext = f'''Your {otp} to recover password
        please don't share to anyone
        Thanks,
        7R Bank
        Delhi
        '''
        # Send email
        con.send(to=uemail, subject=sub, contents=utext)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")