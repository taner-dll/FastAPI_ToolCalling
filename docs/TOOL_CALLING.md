# Tool Calling Rehberi

Bu belge, projedeki tool-calling akışının nasıl çalıştığını ve yeni bir aracın
nasıl ekleneceğini açıklar.

## Temel Kavramlar

- **Tool tanımı:** Modelin görebildiği ad, açıklama ve JSON parametre şemasıdır.
- **Tool fonksiyonu:** Uygulamanın gerçekten çalıştırdığı Python kodudur.
- **Function call:** Modelin bir aracı kullanma isteğidir.
- **Function call output:** Aracın ürettiği ve modele geri gönderilen sonuçtur.
- **Call ID:** Bir araç isteğiyle sonucunu eşleştiren kimliktir.

## Projedeki Sorumluluklar

### `tool_definitions.py`

Modele hangi araçların bulunduğunu anlatır. Örneğin:

```python
WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}
```

Bu tanım fonksiyonu çalıştırmaz. Yalnızca modele aracın nasıl çağrılacağını
öğretir.

### `tools.py`

Gerçek işi yapan Python fonksiyonlarını içerir:

```python
def get_weather(city: str) -> dict[str, object]:
    return {
        "city": city,
        "temperature": 22,
        "condition": "cloudy",
    }
```

### `main.py`

Tool şemalarını ve gerçek fonksiyonları iki ayrı kayıt içinde tutar:

```python
TOOLS = [WEATHER_TOOL, CITY_FOOD_TOOL]

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_city_food": get_city_food,
}
```

`TOOLS` modele gönderilir. `AVAILABLE_TOOLS`, modelin istediği aracın hangi
Python fonksiyonuna karşılık geldiğini bulmak için kullanılır.

## İstek Akışı

### 1. Kullanıcı mesajı gönderilir

```python
response = client.responses.create(
    model=MODEL,
    input=request.message,
    tools=TOOLS,
)
```

### 2. Function call öğeleri bulunur

```python
function_calls = [
    item for item in response.output
    if item.type == "function_call"
]
```

Model doğrudan cevap verdiyse liste boş olur ve `response.output_text`
kullanıcıya döndürülür.

### 3. Araçlar çalıştırılır

```python
tool_outputs = [
    execute_tool_call(item.name, item.arguments, item.call_id)
    for item in function_calls
]
```

`execute_tool_call` JSON argümanlarını okur, kayıtlı fonksiyonu bulur ve sonucu
JSON metnine dönüştürür.

### 4. Sonuçlar modele geri gönderilir

```python
response = client.responses.create(
    model=MODEL,
    tools=TOOLS,
    previous_response_id=response.id,
    input=tool_outputs,
)
```

`previous_response_id` önceki model yanıtıyla bağlantıyı korur. Her sonuçtaki
`call_id`, sonucu doğru tool çağrısıyla eşleştirir.

### 5. Döngü tamamlanır

Model yeni bir araç çağırabilir. Bu nedenle işlem en fazla
`MAX_TOOL_ROUNDS` kez tekrarlanır. Yeni çağrı yoksa nihai metin kullanıcıya
döner.

## Yeni Tool Ekleme

Örnek olarak `get_city_population` aracı eklenebilir.

### 1. Fonksiyonu oluşturun

```python
def get_city_population(city: str) -> dict[str, object]:
    populations = {"ankara": 5_800_000}
    population = populations.get(city.strip().casefold())
    return {"city": city, "population": population}
```

### 2. Tool şemasını oluşturun

```python
CITY_POPULATION_TOOL = {
    "type": "function",
    "name": "get_city_population",
    "description": "Get the example population for a city.",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "strict": True,
}
```

Şemadaki `name` ile Python kayıt anahtarı aynı olmalıdır.

### 3. Kayıtlara ekleyin

```python
TOOLS = [WEATHER_TOOL, CITY_FOOD_TOOL, CITY_POPULATION_TOOL]

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_city_food": get_city_food,
    "get_city_population": get_city_population,
}
```

### 4. Test yazın

En az şu durumları doğrulayın:

- Bilinen şehir için doğru sonuç
- Bilinmeyen şehir için kontrollü sonuç
- Tool adının doğru fonksiyona yönlenmesi
- Aynı model yanıtındaki birden fazla tool çağrısı

## Hata Davranışı

- Kayıtlı olmayan tool adı modele JSON hata sonucu olarak döner.
- Bozuk JSON veya yanlış argümanlar kontrollü hata sonucuna çevrilir.
- Model beş tur sonunda hâlâ tool çağırıyorsa API `502` yanıtı verir.
- API anahtarı yalnızca `OPENAI_API_KEY` ortam değişkeninden okunur.

## Resmi Kaynak

Akış, OpenAI Responses API function-calling yaklaşımını izler:

[OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
