import re

class PrePro:
    @staticmethod
    def filtra(code):
        filter_comments = re.sub("'.*\n", "\n", code.replace("\\n", "\n"))
        return re.sub("\n\s*\n", '', filter_comments)