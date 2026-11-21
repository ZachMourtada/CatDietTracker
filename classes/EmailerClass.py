import smtplib
import ssl
import mimetypes
from email.message import EmailMessage


subject = "PI IMAGE"
body = ""

class EmailerClass:
    def __init__(self, param_sender, param_password):
        self._sender = param_sender
        self._password = param_password
    
    def make_msg(self, subject, body, file_path):
        msg = EmailMessage()
        msg['Subject'] = subject

        msg.set_content(body)
    
        mime_type,_ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        main_type, sub_type = mime_type.split('/', 1)
    
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        
        msg.add_attachment(file_data, maintype = main_type, subtype=sub_type, filename=file_name)
        return msg
    
    
    def mail_msg(self, receiver, msg):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.starttls()
                server.login(self._sender, self._password)
            
                server.send_message(msg, from_addr=self._sender, to_addrs=receiver)

        except Exception as e:
            print(f"Error: {e}")
            
