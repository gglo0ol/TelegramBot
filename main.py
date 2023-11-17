from PDF import PdfFile

path = 'A29-5697-2022_20231019_Postanovlenie_kassacionnoj_instancii.pdf'

f = PdfFile(path)

print(f.get_text())
