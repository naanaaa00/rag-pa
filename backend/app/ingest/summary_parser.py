import re
from typing import Dict, Tuple, List

def clean(value: str) -> str:
    # Menghapus Markdown bold dan spasi di ujung
    return value.replace("**", "").strip()

def parse_summary(text: str) -> Tuple[Dict, Dict[str, str]]:
    # 1. Standarisasi baris baru (mengatasi masalah Windows \r\n)
    text = text.replace('\r\n', '\n')
    
    metadata = {}
    
    # Fungsi pembantu untuk ekstraksi metadata yang lebih fleksibel
    def extract_meta(pattern: str, default: str = "") -> str:
        match = re.search(pattern, text, re.IGNORECASE)
        return clean(match.group(1)) if match else default

    # 2. Ekstrak Metadata
    metadata["title"] = extract_meta(r"Judul:\s*(.*)")
    metadata["date"] = extract_meta(r"Tanggal:\s*(.*)")
    
    # Ekstrak & Split list (Peserta & Topik)
    participants_raw = extract_meta(r"Peserta Utama:\s*(.*)")
    metadata["participants"] = [p.strip() for p in participants_raw.split(",") if p.strip()]
    
    topics_raw = extract_meta(r"Topik Utama:\s*(.*)")
    metadata["main_topic"] = [t.strip() for t in topics_raw.split(",") if t.strip()]

    # 3. Ekstrak Sections secara Dinamis
    # Regex ini mencari baris yang dimulai dengan ## sampai ketemu ## berikutnya atau akhir dokumen
    sections: Dict[str, str] = {}
    
    # Mencari pola: ## Judul [newline] Isi
    # re.MULTILINE agar ^ cocok dengan awal baris
    # re.DOTALL agar . cocok dengan newline di bagian isi
    pattern = r"^##\s*(.*?)\s*\n(.*?)(?=\n##|\Z)"
    matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        if content:
            sections[title] = content

    return metadata, sections