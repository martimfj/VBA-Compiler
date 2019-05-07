import re

class PrePro:
    @staticmethod
    def filtra(code):
        filter_comments = re.sub("'.*\n", "\n", code)
        return re.sub("^(\s*(\r\n|\n|\r))", '', filter_comments) 