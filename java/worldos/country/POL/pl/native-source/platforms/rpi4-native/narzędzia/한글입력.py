"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Klucz_Układ = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {WARTOŚĆ: 한쌍 for 한쌍,WARTOŚĆ in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, wysłać):
        자신.wysłać = wysłać
        자신.przekazywać_kompozycja()

    def przekazywać_kompozycja(자신):
        자신.Stan_KOD = ('','','')
        자신.Historia = []

    def tekst(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Stan_KOD
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Historia:
            return False
        자신.Stan_KOD = 자신.Historia.pop()
        자신.wysłać(b'\x7f' + 자신.tekst().encode('utf-8'))
        return True

    def kanał_Klucz(자신, 누름값):
        dane_znakowe = Klucz_Układ.get(누름값, Klucz_Układ.get(누름값.lower()))
        if dane_znakowe is None:
            return False
        Wstecz_towar = 자신.tekst()
        첫소리,가운뎃소리,끝소리 = 자신.Stan_KOD
        Historia = 자신.Historia + [자신.Stan_KOD]
        확정글 = ''
        if dane_znakowe in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and dane_znakowe in 끝소리목록:
                끝소리 = dane_znakowe
            elif 끝소리 and (끝소리,dane_znakowe) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,dane_znakowe]
            else:
                확정글 = Wstecz_towar
                첫소리,가운뎃소리,끝소리 = dane_znakowe,'',''
                Historia = [('','','')]
        elif 끝소리:
            왼쪽,PRAWY = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Stan_KOD = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.tekst()
            첫소리,가운뎃소리,끝소리 = PRAWY,dane_znakowe,''
            Historia = [('','',''),(PRAWY,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,dane_znakowe) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,dane_znakowe]
            else:
                확정글 = Wstecz_towar
                첫소리,가운뎃소리,끝소리 = '',dane_znakowe,''
                Historia = [('','','')]
        else:
            가운뎃소리 = dane_znakowe
        자신.Stan_KOD = 첫소리,가운뎃소리,끝소리
        자신.Historia = Historia
        자신.wysłać((b'\x7f' if Wstecz_towar else b'') + (확정글+자신.tekst()).encode('utf-8'))
        return True
