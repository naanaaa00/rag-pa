# import logging
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain.schema import Document
# from app.core.ollama import get_embedding
# from app.vectorstore.pgvector import get_vectorstore

# # Setup logger
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO) # Pastikan level log minimal INFO

# def ingest_transcript(text: str, summary_metadata: dict):
#     title = summary_metadata.get("title", "Unknown")
    
#     logger.info(f"=== Memulai Ingest Transkrip: {title} ===")
    
#     try:
#         # 1. Inisialisasi Embedding
#         logger.info("Mengambil model embedding...")
#         embeddings = get_embedding()
        
#         # 2. Proses Chunking
#         logger.info(f"Memulai proses Semantic Chunking (Threshold: Percentile)...")
#         splitter = SemanticChunker(
#             embeddings=embeddings,
#             breakpoint_threshold_type="percentile"
#         )
        
#         chunks = splitter.split_text(text)
#         chunk_count = len(chunks)
#         logger.info(f"Proses chunking selesai. Berhasil membagi menjadi {chunk_count} chunk.")

#         # 3. Pembuatan Dokumen & Metadata
#         logger.info("Menyusun dokumen dan menyisipkan metadata...")
#         docs = [
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     **summary_metadata,
#                     "content_type": "transcript",
#                     "chunk_index": i # Tambahan: index chunk untuk tracking
#                 }
#             )
#             for i, chunk in enumerate(chunks)
#         ]

#         # 4. Simpan ke Vector Store
#         logger.info(f"Menyimpan {chunk_count} dokumen ke PGVector...")
#         vector_store = get_vectorstore()
#         vector_store.add_documents(docs)
        
#         logger.info(f"=== Ingest Transkrip BERHASIL: {title} ===")
        
#     except Exception as e:
#         logger.error(f"!!! Gagal melakukan ingest transkrip '{title}': {str(e)}", exc_info=True)
#         raise e



import logging
from langchain_experimental.text_splitter import SemanticChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.ollama import get_embedding
from app.vectorstore.pgvector import get_vectorstore

# Setup logger agar kita bisa pantau progres di terminal
logger = logging.getLogger(__name__)

def ingest_transcript(text: str, summary_metadata: dict):
    """
    Memproses transkrip dengan Semantic Chunking dan menyimpannya ke PGVector.
    Metadata difilter agar tidak terjadi duplikasi isi summary.
    """
    # 1. Ambil metadata penting saja (Mencegah Double Summary)
    # Kita hanya butuh Judul dan ID untuk referensi, bukan isi teks summary-nya.
    minimal_metadata = {
        "title": summary_metadata.get("title", "Untitled"),
        "date": summary_metadata.get("date", "Unknown"),
        "content_type": "transcript" # Label pembeda dengan 'summary'
    }
    
    title = minimal_metadata["title"]
    logger.info(f"=== Memulai Ingest Transkrip: {title} ===")
    
    try:
        # 2. Inisialisasi Embedding (nomic-embed-text:v1.5)
        embeddings = get_embedding()
        
        # 3. Konfigurasi Splitter
        # Utama: Semantic (Memotong berdasarkan perubahan topik)
        semantic_splitter = SemanticChunker(
            embeddings=embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95 
        )
        
        # Cadangan: Jika ada chunk semantic yang kepanjangan (> 6000 char)
        safety_splitter = RecursiveCharacterTextSplitter(
            chunk_size=6000, 
            chunk_overlap=500,
            separators=["\n\n", "\n", ". ", " "]
        )

        # 4. Proses Chunking
        logger.info("Menganalisis teks secara semantic... (Sabar, Ollama sedang bekerja)")
        initial_chunks = semantic_splitter.split_text(text)
        
        final_docs = []
        for i, chunk in enumerate(initial_chunks):
            # Jika chunk terlalu besar, potong paksa agar tidak Error 500 di Ollama
            if len(chunk) > 6000:
                logger.warning(f"Chunk {i} terlalu besar ({len(chunk)} char). Membagi dengan safety net...")
                sub_chunks = safety_splitter.split_text(chunk)
                for j, sub_chunk in enumerate(sub_chunks):
                    final_docs.append(Document(
                        page_content=sub_chunk,
                        metadata={**minimal_metadata, "chunk_index": f"{i}_{j}", "is_semantic": False}
                    ))
            else:
                final_docs.append(Document(
                    page_content=chunk,
                    metadata={**minimal_metadata, "chunk_index": str(i), "is_semantic": True}
                ))

        chunk_count = len(final_docs)
        logger.info(f"Total: {chunk_count} chunk transkrip dihasilkan.")

        # 5. Simpan ke PGVector dengan Batching
        vector_store = get_vectorstore()
        
        # Gunakan batch kecil (5) agar koneksi tidak timeout saat mengirim ke database
        batch_size = 5
        for i in range(0, chunk_count, batch_size):
            batch = final_docs[i:i + batch_size]
            vector_store.add_documents(batch)
            logger.info(f"Sync Database: {min(i + batch_size, chunk_count)}/{chunk_count} tersimpan.")

        logger.info(f"=== SELESAI: Transkrip '{title}' berhasil di-ingest ===")
        
    except Exception as e:
        logger.error(f"!!! Gagal melakukan ingest transkrip '{title}': {str(e)}", exc_info=True)
        raise e