import re

from PyPDF2 import PdfReader


class PdfFile:

    PATTERN = re.compile(r'\bп\s*о\s*с\s*т\s*а\s*н\s*о\s*в\s*и\s*л\s*:\s*(.*)', re.I)

    def __init__(self, filepath: str):
        self.reader = PdfReader(filepath)
        self.pages = self.reader.pages

    def get_text(self):
        result = ''
        flag = None
        for page in self.pages:
            text = self.text_by_page_without_headers(page)
            if flag:
                result += text.replace('  ', ' ')
            else:
                match = self.PATTERN.search(text)
                if match:
                    flag = True
                    result += match[1].replace('  ', ' ')
        pattern = re.compile(r"(.+)(\n +\n)", re.S)
        print(pattern.search(result)[1])
        return repr(result)


    def text_by_page_without_headers(self, page: PdfReader.pages, tmp=None):
        if tmp is None:
            tmp = []

        def visitor_body(text, cm, tm, fontDict, fontSize):
            y = tm[5]
            if y > 50 and y < 720:
                tmp.append(text)

        page.extract_text(visitor_text=visitor_body)
        text = ''.join(tmp)
        return text
