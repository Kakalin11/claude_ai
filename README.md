# Görev API'si

API'lerin nasıl çalıştığını öğrenmek için hazırlanmış basit bir yapılacaklar listesi API'si (FastAPI ile).

## Kurulum ve çalıştırma

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Tarayıcıda **http://127.0.0.1:8000/docs** adresini aç. Her uç noktayı (endpoint) "Try it out" düğmesiyle oradan deneyebilirsin.

## Uç noktalar

| Yöntem | Adres | Ne yapar |
|---|---|---|
| GET | `/gorevler` | Tüm görevleri listeler (`?tamamlandi=true` ile süzülebilir) |
| GET | `/gorevler/{id}` | Tek bir görevi getirir |
| POST | `/gorevler` | Yeni görev ekler |
| PUT | `/gorevler/{id}` | Görevi günceller |
| DELETE | `/gorevler/{id}` | Görevi siler |

## Terminalden deneme (curl)

```bash
curl -X POST localhost:8000/gorevler -H "Content-Type: application/json" -d '{"baslik":"Faturaları kontrol et"}'
curl localhost:8000/gorevler
curl -X PUT localhost:8000/gorevler/1 -H "Content-Type: application/json" -d '{"baslik":"Faturaları kontrol et","tamamlandi":true}'
curl -X DELETE localhost:8000/gorevler/1
```

Veriler `gorevler.json` dosyasında saklanır.
