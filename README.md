# FastAPI Tool Calling

OpenAI Responses API ile function/tool calling akışını gösteren küçük bir FastAPI
projesi. Model, kullanıcının sorusuna göre uygun aracı seçer; uygulama aracı
yerel Python kodunda çalıştırır ve sonucu tekrar modele gönderir.

Projede iki örnek araç bulunur:

- `get_weather`: Şehir için örnek hava durumu döndürür.
- `get_city_food`: Şehirle özdeşleşen örnek bir yemek döndürür.

> Bu araçların kullandığı veriler eğitim amaçlı ve statiktir. Gerçek zamanlı
> hava durumu veya şehir verisi sağlamaz.

## Akış

```text
Kullanıcı
   ↓
POST /chat
   ↓
OpenAI modeli uygun tool'u seçer
   ↓
FastAPI yerel Python fonksiyonunu çalıştırır
   ↓
Tool sonucu modele gönderilir
   ↓
Modelin nihai cevabı kullanıcıya döner
```

Model tek bir istekte sıfır, bir veya birden fazla araç çağırabilir. Uygulama
çıkan tüm `function_call` öğelerini çalıştırır ve sonuçları ilgili `call_id`
değeriyle modele geri verir.

## Gereksinimler

- Python 3.14 veya üzeri
- [uv](https://docs.astral.sh/uv/)
- OpenAI API anahtarı

## Kurulum

Bağımlılıkları kurun:

```bash
uv sync
```

Örnek ortam dosyasını `.env` adıyla kopyalayın ve API anahtarınızı ekleyin:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

API anahtarını kaynak koda yazmayın veya Git'e göndermeyin. `.env` dosyası
`.gitignore` tarafından dışlanır.

## Çalıştırma

```bash
uv run uvicorn main:app --reload
```

Uygulama varsayılan olarak `http://127.0.0.1:8000` adresinde açılır. FastAPI
Swagger arayüzü:

```text
http://127.0.0.1:8000/docs
```

## API Kullanımı

### Sağlık kontrolü

```http
GET /
```

Örnek yanıt:

```json
{
  "message": "Welcome to the FastAPI Tool Calling Application!"
}
```

### Sohbet

```http
POST /chat
Content-Type: application/json
```

Tek araç kullanan örnek:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Ankara'da hava nasıl?\"}"
```

Birden fazla araç kullanabilen örnek:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"İzmir'in havası nasıl ve meşhur yemeği nedir?\"}"
```

Yanıt biçimi:

```json
{
  "response": "İzmir'de hava 27 derece ve güneşli. Meşhur yemeklerinden biri boyozdur."
}
```

## Testler

Testler gerçek OpenAI isteği göndermez; model yanıtları taklit edilir.

```bash
uv run python -m unittest discover -s tests -v
```

## Proje Yapısı

```text
.
├── main.py                    # FastAPI ve tool-calling döngüsü
├── tool_definitions.py        # Modele gönderilen JSON tool şemaları
├── tools.py                   # Yerel Python araçları
├── tests/
│   └── test_tool_calling.py   # Akış ve araç testleri
├── docs/
│   └── TOOL_CALLING.md        # Ayrıntılı teknik açıklama
├── AGENTS.md                   # Kodlama ajanları için proje talimatları
├── CONTRIBUTING.md            # Katkı ve geliştirme rehberi
├── pyproject.toml             # Proje ve bağımlılık tanımları
└── .env.example               # Ortam değişkeni şablonu
```

## Yeni Tool Eklemek

Yeni bir araç eklerken genel olarak dört adım izlenir:

1. Fonksiyonu `tools.py` içinde yazın.
2. JSON şemasını `tool_definitions.py` içinde tanımlayın.
3. Şemayı `TOOLS`, fonksiyonu `AVAILABLE_TOOLS` listesine ekleyin.
4. Başarılı, hatalı ve çoklu çağrı senaryoları için test yazın.

Ayrıntılı örnek için [Tool Calling Rehberi](docs/TOOL_CALLING.md) belgesine
bakın.

## Kaynaklar

- [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [uv Dokümantasyonu](https://docs.astral.sh/uv/)

## Katkı

Geliştirme kuralları ve kontrol listesi için [CONTRIBUTING.md](CONTRIBUTING.md)
dosyasını okuyun.
