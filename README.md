# Körmozgás
készítette: Forgács Péter

## Használati útmutató
Ez egy __Python 3__-ban írt program, tehát szükség van arra, hogy az eszközön, ahol a futtatásra sor kerülne, legyen telepítve __Python 3__.

Szükséges _Python csomagok_:
- mesa
- numpy

Ezeket a csomagokat parancssorban (pl. _Terminal, Windows PowerShell, Command Prompt_) a következő paranccsal lehet telepíteni:

```bash
pip install mesa numpy
```

Miután a csomagok telepítése befejeződött, annyi a teendő, hogy a parancssort abban a könyvtárban kell megnyitni, ahol a __run.py__ fájl is található, majd az alábbi parancs el is indítja a szimulációt:

```bash
mesa runserver
```

Ha az utóbbi parancs után a szimuláció nem nyílik meg automatikusan, az ehhez hasonló üzenetből a parancssorról ki kell másolni a címet, majd böngészőbe beírni: _Interface starting at http://127.0.0.1:8521_

A program futását parancssorban lehet megállítani a __Ctrl+C__ billentyűkombinációval.
