import requests


class TelegramClient:
    def __init__(self, bot_token: str):
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def get_updates(self, offset: int | None = None, timeout: int = 30) -> list[dict]:
        params = {
            "timeout": timeout,
            "allowed_updates": ["message", "channel_post"],
        }

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
            timeout=timeout + 10,
        )
        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error: {data}")

        return data.get("result", [])

    def send_message(self, chat_id: str, text: str) -> dict:
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error: {data}")

        return data.get("result", {})
