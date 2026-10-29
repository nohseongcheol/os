"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
tuş_Düzen = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {değer: 한쌍 for 한쌍,değer in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, göndermek):
        자신.göndermek = göndermek
        자신.조합확정()

    def 조합확정(자신):
        자신.Durum_KOD = ('','','')
        자신.Geçmiş = []

    def metin(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Durum_KOD
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Geçmiş:
            return False
        자신.Durum_KOD = 자신.Geçmiş.pop()
        자신.göndermek(b'\x7f' + 자신.metin().encode('utf-8'))
        return True

    def akış_tuş(자신, 누름값):
        karakter_verileri = tuş_Düzen.get(누름값, tuş_Düzen.get(누름값.lower()))
        if karakter_verileri is None:
            return False
        Önceki_öğe = 자신.metin()
        첫소리,가운뎃소리,끝소리 = 자신.Durum_KOD
        Geçmiş = 자신.Geçmiş + [자신.Durum_KOD]
        확정글 = ''
        if karakter_verileri in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and karakter_verileri in 끝소리목록:
                끝소리 = karakter_verileri
            elif 끝소리 and (끝소리,karakter_verileri) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,karakter_verileri]
            else:
                확정글 = Önceki_öğe
                첫소리,가운뎃소리,끝소리 = karakter_verileri,'',''
                Geçmiş = [('','','')]
        elif 끝소리:
            왼쪽,hak = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Durum_KOD = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.metin()
            첫소리,가운뎃소리,끝소리 = hak,karakter_verileri,''
            Geçmiş = [('','',''),(hak,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,karakter_verileri) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,karakter_verileri]
            else:
                확정글 = Önceki_öğe
                첫소리,가운뎃소리,끝소리 = '',karakter_verileri,''
                Geçmiş = [('','','')]
        else:
            가운뎃소리 = karakter_verileri
        자신.Durum_KOD = 첫소리,가운뎃소리,끝소리
        자신.Geçmiş = Geçmiş
        자신.göndermek((b'\x7f' if Önceki_öğe else b'') + (확정글+자신.metin()).encode('utf-8'))
        return True
