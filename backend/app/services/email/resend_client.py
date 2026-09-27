import resend


class EmailSender:
    def __init__(self, api_key: str, from_address: str) -> None:
        resend.api_key = api_key
        self._from_address = from_address

    def send(self, to: str, subject: str, body: str) -> str:
        response = resend.Emails.send(
            {
                "from": self._from_address,
                "to": [to],
                "subject": subject,
                "text": body,
            }
        )
        return response["id"]
