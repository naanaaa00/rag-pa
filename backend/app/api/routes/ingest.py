from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.ingest.summary_ingest import ingest_summary
from app.ingest.transcript_ingest import ingest_transcript
from app.ingest.utils import extract_summary_metadata
from app.ingest.file_storage import save_both_files

router = APIRouter(prefix="/api/ingest", tags=["Ingest"])

@router.post("/upload")
async def upload_files(
    background_tasks: BackgroundTasks,
    transcript_file: UploadFile = File(...),
    summary_file: UploadFile = File(...)
):
    # 1. Baca isi kedua file
    try:
        t_content = (await transcript_file.read()).decode("utf-8")
        s_content = (await summary_file.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal membaca file: {str(e)}")

    # 2. Ekstraksi Metadata dari Summary
    full_metadata = extract_summary_metadata(s_content)
    
    # 3. Buat metadata minimal untuk transkrip (agar tidak duplikasi isi summary)
    # Gunakan fallback jika judul tidak ditemukan di dalam teks
    final_title = full_metadata.get("title") or summary_file.filename.rsplit('.', 1)[0]
    final_date = full_metadata.get("date", "Unknown")

    minimal_metadata = {
        "title": final_title,
        "date": final_date,
    }

    # 4. Daftarkan tugas ke Background Tasks
    # Proses berat dijalankan di belakang layar agar user tidak menunggu/timeout
    background_tasks.add_task(ingest_summary, s_content)
    background_tasks.add_task(ingest_transcript, t_content, minimal_metadata)
    background_tasks.add_task(
        save_both_files, 
        t_content, 
        s_content, 
        transcript_file.filename
    )

    # 5. Berikan respons sukses (Variabel di sini sudah diperbaiki)
    return {
        "status": "processing",
        "message": "File diterima. Proses embedding sedang berjalan di latar belakang.",
        "data_info": {
            "title": final_title,
            "date": final_date,
            "transcript_file": transcript_file.filename,
            "summary_file": summary_file.filename
        }
    }