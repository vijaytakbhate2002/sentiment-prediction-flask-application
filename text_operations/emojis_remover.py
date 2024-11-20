import re

def remove_emojis(text):
    """
    Remove emojis from the input text.

    :param text: The input string potentially containing emojis.
    :return: The text with emojis removed.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\u2600-\u26FF"          # Miscellaneous Symbols
        "\u2700-\u27BF"          # Dingbats
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

