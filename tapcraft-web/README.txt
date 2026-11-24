TAPCRAFT -- PACZKA LOGO NA STRONĘ
================================

STRUKTURA
  svg/        logo wektorowe (zalecane, ostre w każdym rozmiarze, mała waga)
  png/        te same logo jako PNG z przezroczystym tłem + obraz OG 1200x630
  favicon/    favicony, ikony aplikacji, manifest, gotowy kod do <head>
  snippety/   dla KAŻDEGO logo osobny plik .html z gotowym kodem do skopiowania
  przyklad-strony.html   działająca przykładowa strona (otwórz w przeglądarce)
  gen.py, web.py         generatory (do zmian kolorów/proporcji)

KTÓRE LOGO GDZIE

  tapcraft-logo-pionowe-na-ciemnym
     co:      Znak nad nazwą
     gdzie:   hero, ekran ładowania, strona logowania/panelu
     tło:     ciemne tło   | viewBox 268x233 | proporcje 1.15:1
     kod:     snippety/tapcraft-logo-pionowe-na-ciemnym.html

  tapcraft-logo-pionowe-na-jasnym
     co:      Znak nad nazwą, wersja jasna
     gdzie:   jak wyżej, na jasnym
     tło:     jasne tło   | viewBox 268x233 | proporcje 1.15:1
     kod:     snippety/tapcraft-logo-pionowe-na-jasnym.html

  tapcraft-logo-poziome-na-ciemnym
     co:      Znak + nazwa obok siebie
     gdzie:   GŁÓWNE logo w nagłówku strony (navbar)
     tło:     ciemne tło   | viewBox 575x146 | proporcje 3.94:1
     kod:     snippety/tapcraft-logo-poziome-na-ciemnym.html

  tapcraft-logo-poziome-na-jasnym
     co:      Znak + nazwa obok siebie, wersja jasna
     gdzie:   nagłówek na jasnej stronie, faktury, e-maile
     tło:     jasne tło   | viewBox 575x146 | proporcje 3.94:1
     kod:     snippety/tapcraft-logo-poziome-na-jasnym.html

  tapcraft-nazwa-na-ciemnym
     co:      Sama nazwa TapCraft (Tap biały, Craft błękitny)
     gdzie:   tekstowy podpis, stopka, mały nagłówek
     tło:     ciemne tło   | viewBox 460x117 | proporcje 3.94:1
     kod:     snippety/tapcraft-nazwa-na-ciemnym.html

  tapcraft-nazwa-na-jasnym
     co:      Sama nazwa TapCraft (Tap granatowy, Craft niebieski)
     gdzie:   jak wyżej
     tło:     jasne tło   | viewBox 460x117 | proporcje 3.94:1
     kod:     snippety/tapcraft-nazwa-na-jasnym.html

  tapcraft-odznaka-ciemna-bez-napisu
     co:      Okrągła odznaka bez SCAN ME (granat)
     gdzie:   awatar, ikona okrągła, sekcje bez wezwania do skanowania
     tło:     okrągła, własne tło   | viewBox 350x350 | proporcje 1.00:1
     kod:     snippety/tapcraft-odznaka-ciemna-bez-napisu.html

  tapcraft-odznaka-ciemna-z-SCAN-ME
     co:      Okrągła odznaka z napisem SCAN ME (granat)
     gdzie:   sekcja o breloczkach, social media, wersja 1:1 jak na breloku
     tło:     okrągła, własne tło   | viewBox 350x350 | proporcje 1.00:1
     kod:     snippety/tapcraft-odznaka-ciemna-z-SCAN-ME.html

  tapcraft-odznaka-jasna-bez-napisu
     co:      Okrągła odznaka bez napisu (jasna)
     gdzie:   awatar, ikona okrągła
     tło:     okrągła, własne tło   | viewBox 350x350 | proporcje 1.00:1
     kod:     snippety/tapcraft-odznaka-jasna-bez-napisu.html

  tapcraft-odznaka-jasna-z-SCAN-ME
     co:      Okrągła odznaka z SCAN ME (jasna)
     gdzie:   jak wyżej, wariant dla ciemnych breloków
     tło:     okrągła, własne tło   | viewBox 350x350 | proporcje 1.00:1
     kod:     snippety/tapcraft-odznaka-jasna-z-SCAN-ME.html

  tapcraft-znak-jednokolorowe-biale
     co:      Znak w jednym kolorze (biały)
     gdzie:   stemple, grawer, druk 1 kolor, tło zdjęciowe
     tło:     dowolne ciemne/zdjęcie   | viewBox 210x138 | proporcje 1.52:1
     kod:     snippety/tapcraft-znak-jednokolorowe-biale.html

  tapcraft-znak-jednokolorowe-granatowe
     co:      Znak w jednym kolorze (granat)
     gdzie:   jak wyżej, na jasnym
     tło:     dowolne jasne   | viewBox 210x138 | proporcje 1.52:1
     kod:     snippety/tapcraft-znak-jednokolorowe-granatowe.html

  tapcraft-znak-na-ciemnym
     co:      Sam znak (kropla + fale), kolory pod ciemne tło
     gdzie:   awatar, ikona w sekcji, stopka, miejsca gdzie nazwa jest obok
     tło:     ciemne tło   | viewBox 210x138 | proporcje 1.52:1
     kod:     snippety/tapcraft-znak-na-ciemnym.html

  tapcraft-znak-na-jasnym
     co:      Sam znak, ciemniejsze fale pod jasne tło
     gdzie:   jak wyżej, na białym/jasnym tle
     tło:     jasne tło   | viewBox 210x138 | proporcje 1.52:1
     kod:     snippety/tapcraft-znak-na-jasnym.html

KOLORY MARKI
  granat #0F172A   błękit #38BDF8   niebieski #2563EB   jasny błękit #7DD3FC
  czcionka: Poppins Bold (w logo jest już zamieniona na krzywe, nie trzeba jej ładować)

NAJCZĘSTSZE UŻYCIA (kod)

1) Nagłówek strony (ciemny):
   <a href="/"><img src="svg/tapcraft-logo-poziome-na-ciemnym.svg" alt="TapCraft" height="40"></a>

2) Automatyczna zmiana logo w trybie jasnym/ciemnym przeglądarki:
   <picture>
     <source srcset="svg/tapcraft-logo-poziome-na-ciemnym.svg" media="(prefers-color-scheme: dark)">
     <img src="svg/tapcraft-logo-poziome-na-jasnym.svg" alt="TapCraft" height="40">
   </picture>

3) Odznaka w sekcji o breloczkach:
   <img src="svg/tapcraft-odznaka-ciemna-z-SCAN-ME.svg" alt="TapCraft SCAN ME" width="220" height="220">

4) Logo jako tło/CSS:
   .logo { background: url("svg/tapcraft-logo-poziome-na-ciemnym.svg") no-repeat center / contain; width: 220px; height: 48px; }

5) Favicon + podgląd linku (wklej do <head>, zawartość favicon/WKLEJ-DO-HEAD.html;
   pliki z folderu favicon/ wrzuć do głównego katalogu strony; w og:image wpisz swoją domenę):
   <link rel="icon" href="/favicon.ico" sizes="48x48">
   <link rel="icon" href="/favicon.svg" type="image/svg+xml">
   <link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
   <link rel="manifest" href="/site.webmanifest">
   <meta name="theme-color" content="#0F172A">
   <meta property="og:image" content="https://TWOJA-DOMENA/tapcraft-og-image-1200x630.png">

ZASADY
  - Używaj SVG, PNG tylko tam, gdzie SVG nie działa (e-mail, social media, Facebook/OG).
  - Ustawiaj tylko height ALBO width, drugi wymiar się policzy sam.
  - Minimalna wysokość logo poziomego: 28 px. Wokół logo zostaw wolne pole o szerokości ok. wysokości kropli.
  - Wersji "na-ciemnym" nie kładź na jasnym tle i odwrotnie (zniknie biała/granatowa część nazwy).
  - Inline SVG (opcja C w snippetach) tylko raz na stronie, bo powtarzają się identyfikatory gradientów.
  - Pliki z folderu favicon/ muszą leżeć w głównym katalogu domeny, jeśli zostawiasz ścieżki z "/".
