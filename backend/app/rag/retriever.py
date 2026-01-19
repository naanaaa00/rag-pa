# from typing import Optional, Dict, Any, List
# from langchain.schema import Document
# from app.vectorstore.pgvector import get_vectorstore

# def retrieve_documents(
#     query: str,
#     metadata_filter: Dict[str, Any],
#     k: int = 5
# ) -> List[Document]:
#     """
#     Retrieve documents with metadata filtering + similarity search
#     """

#     vectorstore = get_vectorstore()

#     docs = vectorstore.similarity_search(
#         query=query,
#         k=k,
#         filter=metadata_filter
#     )

#     return docs


from typing import Optional, Dict, Any, List
from langchain.schema import Document
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_compressors import FlashrankRerank
from app.vectorstore.pgvector import get_vectorstore

def retrieve_documents(
    query: str,
    metadata_filter: Dict[str, Any],
    k: int = 6
) -> List[Document]:
    
    vectorstore = get_vectorstore()

    # 1. Dapatkan Retriever dari Vector Store (Semantic) dengan Filter
    vector_retriever = vectorstore.as_retriever(
        search_kwargs={
            "filter": metadata_filter,
            "k": k * 2 # Ambil lebih banyak untuk di-rerank nanti
        }
    )

    # 2. Buat Keyword Retriever (BM25)
    # Catatan: BM25 butuh daftar dokumen. Kita ambil dokumen yang sesuai metadata dulu.
    # Ini penting agar pencarian keyword tidak keluar dari konteks meeting_id/date.
    relevant_docs = vectorstore.similarity_search(
        query="", # Ambil semua yang cocok metadata
        k=100,    # Sesuaikan dengan jumlah dokumen per meeting
        filter=metadata_filter
    )
    
    # Jika tidak ada dokumen sama sekali, langsung return kosong
    if not relevant_docs:
        return []

    keyword_retriever = BM25Retriever.from_documents(relevant_docs)
    keyword_retriever.k = k * 2

    # 3. Gabungkan jadi Hybrid Search (Ensemble)
    # Weights [0.5, 0.5] artinya seimbang antara makna dan kata kunci
    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, keyword_retriever],
        weights=[0.5, 0.5]
    )

    # 4. Tambahkan Reranker (FlashRank)
    # Ini akan mengurutkan ulang hasil Hybrid agar yang paling relevan ada di Top-K
    compressor = FlashRankRerank()
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=ensemble_retriever
    )

    # Eksekusi pencarian
    final_docs = compression_retriever.get_relevant_documents(query)

    return final_docs[:k] # Kembalikan sebanyak k yang diminta