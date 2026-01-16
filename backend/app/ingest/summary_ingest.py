from langchain.schema import Document
from app.ingest.summary_parser import parse_summary
from app.vectorstore.pgvector import get_vectorstore

def ingest_summary(text: str):
    """
    - Metadata TIDAK di-embed
    - Konten di-embed per section (##)
    """
    # 1. Pastikan input text tidak kosong
    if not text or not text.strip():
        print("Error: Input text kosong, proses dibatalkan.")
        return

    metadata, sections = parse_summary(text)

    # 2. Cek apakah parser menghasilkan sections
    if not sections:
        print("Warning: Tidak ada section yang ditemukan oleh parser. Periksa format ## Anda.")
        return

    docs = []

    for section_name, content in sections.items():
        # 3. Pastikan konten section tidak kosong sebelum dibuat jadi Document
        if content and content.strip():
            docs.append(
                Document(
                    page_content=content.strip(),
                    metadata={
                        **metadata,
                        "section": section_name,
                        "content_type": "summary",
                    }
                )
            )

    # 4. Validasi akhir: Hanya panggil database jika docs ada isinya
    if docs:
        print(f"Mengirim {len(docs)} dokumen ke Vector Store...")
        get_vectorstore().add_documents(docs)
        print("Ingest berhasil.")
    else:
        print("Error: List dokumen kosong setelah parsing. Tidak ada data yang dikirim ke DB.")