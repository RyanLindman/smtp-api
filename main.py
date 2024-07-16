import os
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# TODO: Add correct SMTP config


class ContactForm(BaseModel):
    name: str
    email: str
    message: str


def send_email(subject: str, body: str, to: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, [to], msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Email send fail")


@app.post("/contact")
async def contact_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    send_email(subject, body, os.getenv("EMAIL_USER"))
    return {"message": "Email sent successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/")
async def root():
    return {"message": "Hello World"}
