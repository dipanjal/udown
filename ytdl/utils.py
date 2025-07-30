import re


class Utils:
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Sanitize a string to be a valid filename."""
        return re.sub(r'[\\/*?:"<>|]', "", name)
