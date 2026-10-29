"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Nyckel_Layout = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {värde: 한쌍 for 한쌍,värde in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, skicka):
        자신.skicka = skicka
        자신.incheckning_komposition()

    def incheckning_komposition(자신):
        자신.kod_för_tillstånd = ('','','')
        자신.Historik = []

    def text(자신):
        첫소리,가운뎃소리,끝소리 = 자신.kod_för_tillstånd
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Historik:
            return False
        자신.kod_för_tillstånd = 자신.Historik.pop()
        자신.skicka(b'\x7f' + 자신.text().encode('utf-8'))
        return True

    def feed_Nyckel(자신, 누름값):
        teckendata = Nyckel_Layout.get(누름값, Nyckel_Layout.get(누름값.lower()))
        if teckendata is None:
            return False
        Föregående_objekt = 자신.text()
        첫소리,가운뎃소리,끝소리 = 자신.kod_för_tillstånd
        Historik = 자신.Historik + [자신.kod_för_tillstånd]
        확정글 = ''
        if teckendata in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and teckendata in 끝소리목록:
                끝소리 = teckendata
            elif 끝소리 and (끝소리,teckendata) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,teckendata]
            else:
                확정글 = Föregående_objekt
                첫소리,가운뎃소리,끝소리 = teckendata,'',''
                Historik = [('','','')]
        elif 끝소리:
            왼쪽,HÖGER = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.kod_för_tillstånd = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.text()
            첫소리,가운뎃소리,끝소리 = HÖGER,teckendata,''
            Historik = [('','',''),(HÖGER,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,teckendata) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,teckendata]
            else:
                확정글 = Föregående_objekt
                첫소리,가운뎃소리,끝소리 = '',teckendata,''
                Historik = [('','','')]
        else:
            가운뎃소리 = teckendata
        자신.kod_för_tillstånd = 첫소리,가운뎃소리,끝소리
        자신.Historik = Historik
        자신.skicka((b'\x7f' if Föregående_objekt else b'') + (확정글+자신.text()).encode('utf-8'))
        return True
