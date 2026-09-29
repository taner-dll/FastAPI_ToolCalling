# Katkı Rehberi

Bu proje küçük ve eğitim odaklıdır. Değişiklikleri anlaşılır, test edilebilir ve
mevcut tool-calling yapısıyla uyumlu tutun.

## Geliştirme Ortamı

Bağımlılıkları kurun:

```bash
uv sync
```

`.env.example` dosyasını `.env` adıyla kopyalayın ve kendi API anahtarınızı
ekleyin:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

Uygulamayı geliştirme modunda çalıştırın:

```bash
uv run uvicorn main:app --reload
```

## Kod Düzeni

- Tool fonksiyonlarını `tools.py` içinde tutun.
- Modelin göreceği şemaları `tool_definitions.py` içinde tanımlayın.
- Tool şemalarını `TOOLS`, fonksiyonları `AVAILABLE_TOOLS` kaydına ekleyin.
- Tool fonksiyonlarından JSON'a çevrilebilen sözlükler döndürün.
- Kullanıcı girdilerini normalize edin ve bilinmeyen değerleri kontrollü biçimde
  ele alın.
- API anahtarlarını ve diğer sırları kaynak koda eklemeyin.

## Testler

Tüm testleri çalıştırın:

```bash
uv run python -m unittest discover -s tests -v
```

Yeni bir tool için en az bir başarılı ve bir başarısız veri senaryosu ekleyin.
Akış değişiyorsa doğrudan cevap, tek tool ve çoklu tool senaryolarını koruyun.
Testler mümkün olduğunda gerçek OpenAI isteği göndermemeli; SDK çağrıları mock
edilmelidir.

## Değişiklik Kontrol Listesi

- [ ] Tool adı, şemadaki `name` ve `AVAILABLE_TOOLS` anahtarıyla aynı.
- [ ] Şemada zorunlu alanlar ve `additionalProperties: False` tanımlı.
- [ ] Tool sonucu JSON'a dönüştürülebiliyor.
- [ ] Başarılı ve hatalı durumlar test edildi.
- [ ] README veya teknik rehber davranış değişikliği için güncellendi.
- [ ] `.env`, API anahtarı veya başka bir gizli bilgi commite eklenmedi.
