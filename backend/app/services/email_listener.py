from __future__ import annotations

import imaplib
import email
from email.header import decode_header


class EmailListener:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        mail = imaplib.IMAP4_SSL(self.host, self.port)
        mail.login(self.username, self.password)
        return mail

    def fetch_incoming_messages(self, mailbox: str = "INBOX") -> list[dict]:
        messages: list[dict] = []
        try:
            mail = self.connect()
            mail.select(mailbox)
            _, data = mail.search(None, "ALL")
            ids = data[0].split()
            for msg_id in ids[-5:]:
                _, payload = mail.fetch(msg_id, "(RFC822)")
                raw = payload[0][1]
                msg = email.message_from_bytes(raw)
                subject = self._decode_header(msg.get("Subject", ""))
                body = self._get_body(msg)
                messages.append({"subject": subject, "body": body})
            mail.close()
            mail.logout()
        except Exception:
            return []
        return messages

    @staticmethod
    def _decode_header(value: str) -> str:
        try:
            return "".join(part.decode(errors="replace") if isinstance(part, bytes) else part for part, _ in decode_header(value))
        except Exception:
            return value

    @staticmethod
    def _get_body(msg: email.message.Message) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(errors="replace")
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(errors="replace")
        return ""
