# -*- coding: utf-8 -*-
BS = chr(92)
pairs = [
    (u'Vytvoř funkční požadavek pro naskladnění nosiče',
     u'Create a functional requirement for container putaway'),
    (u'Zkontroluj konzistenci měřicí brány s procesní analýzou',
     u'Check measuring gate consistency against the process analysis'),
    (u'příjmu', u'prijmu'),
    (u'PICK_STATION_A2_LOAD', u''),
    (u'C:' + BS + 'Git' + BS + 'alzask' + BS + 'docs' + BS + 'fr' + BS + 'comp' + BS + 'wes' + BS, u''),
    (u'nosič, nosiče, nosiči, nosičem, nosičů, nosičům', u'container, containers'),
]
for a, b in pairs:
    print(u'CZ/ID: ' + a)
    print(u'       znaky=%d  UTF8_bajtu=%d  slova=%d' % (len(a), len(a.encode('utf-8')), len(a.split())))
    if b:
        print(u'EN   : ' + b)
        print(u'       znaky=%d  UTF8_bajtu=%d  slova=%d' % (len(b), len(b.encode('utf-8')), len(b.split())))
    print('')
