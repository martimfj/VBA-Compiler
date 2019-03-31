import re

class PrePro:
    @staticmethod
    def filtra(code):
        filter_comments = re.sub("'.*\n", "\n", code)#.replace("\n\n", "\n"))
        return re.sub("^(\s*(\r\n|\n|\r))", '', filter_comments)