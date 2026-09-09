import os

p = 'C:/tmp/workshop-namety/NAMETY.md'
with open(p, encoding='utf-8') as f:
    t = f.read()

BT = chr(96)
a = '**Co ukážu na obrazovce:** dvě různé chyby, dvě různé návratové hodnoty, dvě různé reakce.'
b = ('**Co ukážu na obrazovce:** spustím kontrolu nad evidencí, ve které jsou otevřené dotazy\n'
     'čekající na odpověď dodavatele — vrátí nenulový kód a výpis „je tu otevřená práce",\n'
     'ale proces to nezastaví. Pak v té evidenci porušim invariant (dva záznamy se stejným\n'
     'identifikátorem) a spustím totéž — vrátí jiný kód a jinou hlášku, a tenhle stav\n'
     'proces zastavit má. Publikum vidí, že to nejsou dvě hlasitosti téhož signálu,\n'
     'ale dva různé signály, na které se reaguje jinak.')

if a not in t:
    raise SystemExit('vzor M-08 nenalezen')
t = t.replace(a, b, 1)
with open(p, 'w', encoding='utf-8') as f:
    f.write(t)
print('M-08 doplneno |', round(os.path.getsize(p) / 1024, 1), 'KB')
