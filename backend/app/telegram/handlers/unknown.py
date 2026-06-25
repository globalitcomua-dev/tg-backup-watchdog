from app.telegram.update import TelegramMessage


class UnknownMessageHandler:
    def handle(self, message: TelegramMessage) -> None:
        print(
            f"Unknown telegram message chat_id={message.chat_id} "
            f"message_id={message.message_id}",
            flush=True,
        )