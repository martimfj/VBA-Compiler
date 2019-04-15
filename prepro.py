import re

class PrePro:
    @staticmethod
    def filtra(code):
        return re.sub("'.*\n", "\n", code + "\n")