"""
Basit bir Görev (Yapılacaklar) API'si.

Çalıştırmak için:
    uvicorn main:app --reload

Sonra tarayıcıda http://127.0.0.1:8000/docs adresini aç.
"""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Görev API'si", description="API öğrenmek için basit bir yapılacaklar listesi.")

# Veriler bu dosyada saklanır, böylece sunucu kapanınca kaybolmaz.
VERI_DOSYASI = Path(__file__).parent / "gorevler.json"


class GorevGirdi(BaseModel):
    """Kullanıcının gönderdiği veri (id'yi sunucu verir)."""
    baslik: str
    tamamlandi: bool = False


class Gorev(GorevGirdi):
    """Sunucunun döndürdüğü veri."""
    id: int


def oku() -> list[dict]:
    if VERI_DOSYASI.exists():
        return json.loads(VERI_DOSYASI.read_text(encoding="utf-8"))
    return []


def kaydet(gorevler: list[dict]) -> None:
    VERI_DOSYASI.write_text(json.dumps(gorevler, ensure_ascii=False, indent=2), encoding="utf-8")


def bul(gorevler: list[dict], gorev_id: int) -> dict:
    for g in gorevler:
        if g["id"] == gorev_id:
            return g
    raise HTTPException(status_code=404, detail="Görev bulunamadı")


@app.get("/")
def ana_sayfa():
    return {"mesaj": "Görev API'sine hoş geldin! Denemek için /docs adresine git."}


# GET: veri okuma
@app.get("/gorevler", response_model=list[Gorev])
def gorevleri_listele(tamamlandi: bool | None = None):
    gorevler = oku()
    if tamamlandi is not None:
        gorevler = [g for g in gorevler if g["tamamlandi"] == tamamlandi]
    return gorevler


@app.get("/gorevler/{gorev_id}", response_model=Gorev)
def gorev_getir(gorev_id: int):
    return bul(oku(), gorev_id)


# POST: yeni veri ekleme
@app.post("/gorevler", response_model=Gorev, status_code=201)
def gorev_ekle(girdi: GorevGirdi):
    gorevler = oku()
    yeni_id = max((g["id"] for g in gorevler), default=0) + 1
    gorev = {"id": yeni_id, **girdi.model_dump()}
    gorevler.append(gorev)
    kaydet(gorevler)
    return gorev


# PUT: var olan veriyi güncelleme
@app.put("/gorevler/{gorev_id}", response_model=Gorev)
def gorev_guncelle(gorev_id: int, girdi: GorevGirdi):
    gorevler = oku()
    gorev = bul(gorevler, gorev_id)
    gorev.update(girdi.model_dump())
    kaydet(gorevler)
    return gorev


# DELETE: veri silme
@app.delete("/gorevler/{gorev_id}", status_code=204)
def gorev_sil(gorev_id: int):
    gorevler = oku()
    gorevler.remove(bul(gorevler, gorev_id))
    kaydet(gorevler)
