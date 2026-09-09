from pathlib import Path
import pypdfium2 as pdfium

source = Path(r"C:\rafiki\qa_word\enhanced.pdf")
output = Path(r"C:\rafiki\qa_word")
doc = pdfium.PdfDocument(source)
for index in range(len(doc)):
    page = doc[index]
    bitmap = page.render(scale=2.0)
    bitmap.to_pil().convert("RGB").save(output / f"page-{index + 1:02d}.png")
print(f"pages={len(doc)}")
