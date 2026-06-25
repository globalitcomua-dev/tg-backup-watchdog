import re


def strip_telegram_prefix(text: str) -> str:
    return re.sub(
        r"^\[\d{2}\.\d{2}\.\d{4}\s+\d{1,2}:\d{2}\]\s*backup:\s*",
        "",
        text.strip(),
    ).strip()


def parse_english_duration(text: str) -> int | None:
    match = re.search(
        r"Time elapsed:\s*(\d+)\s*hours?,\s*(\d+)\s*minutes?,\s*(\d+)\s*seconds?",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    hours, minutes, seconds = map(int, match.groups())

    return hours * 3600 + minutes * 60 + seconds


def parse_ukrainian_duration(text: str) -> int | None:
    match = re.search(
        r"Витрачено часу:\s*(\d+)\s*год,\s*(\d+)\s*хв,\s*(\d+)\s*сек",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    hours, minutes, seconds = map(int, match.groups())

    return hours * 3600 + minutes * 60 + seconds