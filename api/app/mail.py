import ssl
from dataclasses import asdict
from email.message import EmailMessage

import aiosmtplib

from .config import Config


class Mail:
    def __init__(self, config: Config):
        self.name = config.mail.username
        self.smtp = aiosmtplib.SMTP(
            tls_context=ssl.create_default_context(),
            use_tls=True,
            **asdict(config.mail),
        )
        self.connect = self.smtp.connect

    async def send(
            self,
            to: str,
            subject: str,
            content: str
    ):
        try:
            message = EmailMessage()
            message["From"] = self.name
            message["To"] = to
            message["Subject"] = subject
            message.set_content(content)
            await self.smtp.send_message(message)
            return True
        except aiosmtplib.errors.SMTPServerDisconnected as e:
            return False