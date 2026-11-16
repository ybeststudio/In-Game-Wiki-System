# In-Game Wiki System

Oyun içi ansiklopedi. Eşya, canavar, zindan, sistem ve rehber sayfaları; 3D önizleme, arama, kategori ağacı ve çok dilli içerik.

![Önizleme](preview2.png)

---

## Ne var?

- Wiki penceresi (`uiwiki.py`, `wikiui.py`, `wikipages.py`)
- İçerik ve işaretleme (`wikicontent.py`, `wikimarkup.py`)
- `PythonWiki` C++ modülü (eşya / canavar verisi, efekt önizleme)
- Dil başına içerik: `locale/<dil>/wiki/`, ortak: `locale/common/wiki/`

## Paket yapısı

```
01. Svn/          → Client & Game source (Ara / Altına ekle / Bul / Değiştir patch dosyaları + yeni dosyalar)
02. Client/       → root, uiscript, locale, d_/ymir work assetleri
Added/            → Değişikliklerin uygulanmış hali (tam dosyalar, karşılaştırma için)
```

## Flagler

**Client** (`Locale_inc.h`):
- `ENABLE_WIKI_SYSTEM`

## Kurulum (kısaca)

1. `01. Svn` altındaki patch dosyalarını kendi source ağacına uygula. Her blokta `// Ara:` satırlarını bul, `// Altına ekle:` kısmını altına ekle; `// Bul:` / `// Degistir:` bloklarında bulduğun satırları verilen blokla değiştir.
2. Yeni dosyaları (`PythonWiki.cpp`, `PythonWiki.h`) ilgili klasöre kopyala; game için `Makefile`, client için `vcxproj.txt` notuna göre projeye ekle.
3. `02. Client/root` ve `02. Client/uiscript` içindeki tam dosyaları pack'e kopyala, patch dosyalarını (`# Ara:` / `# Altına ekle:`) kendi dosyalarına uygula.
4. `02. Client/locale/<dil>/` satırlarını kendi locale dosyalarının sonuna ekle.
5. `02. Client/d_/ymir work/` görsellerini pack'e ekle (`d:/ymir work/...`).
6. Client + game + db rebuild, pack güncelle.

## Bağımlılıklar

- Render Target sistemi
- `uibattlepass.py` patch'i yalnızca **Battlepass System** paketi kuruluysa gerekli.
- `uibiologist.py` patch'i yalnızca **Biologist System Renewal** paketi kuruluysa gerekli.
- `uicompanion.py` patch'i yalnızca **Companion System (Pet - Buffi - Mount)** paketi kuruluysa gerekli.
- `uicompanionmount.py` patch'i yalnızca **Companion System (Pet - Buffi - Mount)** paketi kuruluysa gerekli.
- `uicostumeshop.py` patch'i yalnızca **Wardrobe & Costume Shop System** paketi kuruluysa gerekli.
- `uidungeontrack.py` patch'i yalnızca **Dungeon & Teleport Window** paketi kuruluysa gerekli.
- `uienergycrystal.py` patch'i yalnızca **Energy Crystal System** paketi kuruluysa gerekli.
- `uiguildrenewal.py` patch'i yalnızca **Guild Window Renewal** paketi kuruluysa gerekli.
- `uiwardrobe.py` patch'i yalnızca **Wardrobe & Costume Shop System** paketi kuruluysa gerekli.

## Notlar

- Veri dosyaları: `locale/<lang>/wiki/guides/faq.txt`, `locale/<lang>/wiki/guides/the_start.txt`, `locale/common/wiki/systems/biologist.txt`, `locale/<lang>/wiki/systems/biologist.txt`, `locale/<lang>/wiki/systems/alchemy.txt`, `locale/<lang>/wiki/systems/bonus67.txt`, `locale/<lang>/wiki/systems/costume.txt`, `locale/<lang>/wiki/systems/talismane.txt`, `locale/<lang>/wiki/systems/boosters.txt`, `locale/<lang>/wiki/dungeon/devil.txt`, `locale/<lang>/wiki/dungeon/spider.txt`, `locale/<lang>/wiki/dungeon/dragon.txt` ...
- Locale dosyalarında yalnızca bu sisteme ait anahtarlar var; `new_locale_*` kendi eklediğimiz, `locale_game` / `locale_interface` resmi istemcide olmayan anahtarlar. Türkçe dosyalar cp1254.
- Patch'lerde başka sistemlere ait satırlar görürsen (farklı `#ifdef`), o sistem sende yoksa yok say.
- Fork farklıysa paket header / struct sıralamasını kontrol et.

---

## İletişim

Sorular için Discord'dan yazabilirsin.

| | |
|---|---|
| GitHub | [github.com/ybeststudio](https://github.com/ybeststudio) |
| Discord | [discord.gg/NXmc6JrwYr](https://discord.gg/NXmc6JrwYr) |
| Discord ID | `beststudio` |
| Web | [bestpro.dev](https://bestpro.dev) |
| TurkMMO | [Best Studio](https://forum.turkmmo.com/uye/2104546-best-studio/) |
| YouTube | [@ybeststudio](https://www.youtube.com/@ybeststudiotr) |
| Instagram | [@ybeststudio](https://www.instagram.com/ybeststudio) |
| Facebook | [ybeststudio](https://www.facebook.com/ybeststudio/) |
| Twitter | [@ybeststudio](https://twitter.com/ybeststudio) |
| TikTok | [@ybeststudio](https://tiktok.com/@ybeststudio) |

---

**Best Studio** — Metin2 private server çözümleri
