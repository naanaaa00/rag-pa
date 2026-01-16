import re

def extract_summary_metadata(text: str) -> dict:
    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    return {
        "title": find(r"Judul\s*:\s*(.+)"),
        "date": find(r"Tanggal\s*:\s*(.+)"),
        "participants": find(r"Peserta\s*Utama\s*:\s*(.+)"),
        "main_topic": find(r"Topik\s*Utama\s*:\s*(.+)"),
    }
