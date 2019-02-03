"""Declara a classe EmailNotification"""
import smtplib
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from notifications.BaseNotification import BaseNotification
except ModuleNotFoundError:  # For local execution
    from src.notifications.BaseNotification import BaseNotification


class EmailNotification(BaseNotification):
    """Classe usada para emitir uma notificacao em forma de email"""

    def __init__(self, host, credentials):
        self.host = host
        self.credentials = credentials

    def notificar(self, data, **kwargs):
        to_list = kwargs["to"]

        msg = MIMEMultipart()
        msg["From"] = self.credentials[0]
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = kwargs.get("subject", "SEM TITULO")

        msg.attach(MIMEText(data, "html"))

        with email_server(self.host, self.credentials) as server:
            server.send_message(msg)


@contextmanager
def email_server(host, credentials):
    """Inicia um servidor de email"""
    server = smtplib.SMTP(host)
    server.ehlo()
    server.starttls()
    server.login(credentials[0], credentials[1])

    try:
        yield server
    finally:
        server.quit()
