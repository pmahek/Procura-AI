from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    return "\n\n".join(pages)


if __name__ == "__main__":

    pdf_path = Path("data/documents/quotation_SUP001.pdf")

    try:
        text = extract_text_from_pdf(pdf_path)

        print("=" * 60)
        print("PROCURA AI — DOCUMENT EXTRACTION")
        print("=" * 60)

        print(f"\nDocument: {pdf_path}")
        print(f"Characters extracted: {len(text)}")

        print("\nExtracted text:")
        print(text)

        print("\n" + "=" * 60)

    except FileNotFoundError as error:
        print(f"ERROR: {error}")