"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Klíč_Navigace = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {HODNOTA: 한쌍 for 한쌍,HODNOTA in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, poslat):
        자신.poslat = poslat
        자신.zápis_složení()

    def zápis_složení(자신):
        자신.Stav_KÓD = ('','','')
        자신.Historie = []

    def text(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Stav_KÓD
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Historie:
            return False
        자신.Stav_KÓD = 자신.Historie.pop()
        자신.poslat(b'\x7f' + 자신.text().encode('utf-8'))
        return True

    def novinky_Klíč(자신, 누름값):
        textová_data = Klíč_Navigace.get(누름값, Klíč_Navigace.get(누름값.lower()))
        if textová_data is None:
            return False
        Předchozí_zboží = 자신.text()
        첫소리,가운뎃소리,끝소리 = 자신.Stav_KÓD
        Historie = 자신.Historie + [자신.Stav_KÓD]
        확정글 = ''
        if textová_data in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and textová_data in 끝소리목록:
                끝소리 = textová_data
            elif 끝소리 and (끝소리,textová_data) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,textová_data]
            else:
                확정글 = Předchozí_zboží
                첫소리,가운뎃소리,끝소리 = textová_data,'',''
                Historie = [('','','')]
        elif 끝소리:
            왼쪽,právo = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Stav_KÓD = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.text()
            첫소리,가운뎃소리,끝소리 = právo,textová_data,''
            Historie = [('','',''),(právo,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,textová_data) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,textová_data]
            else:
                확정글 = Předchozí_zboží
                첫소리,가운뎃소리,끝소리 = '',textová_data,''
                Historie = [('','','')]
        else:
            가운뎃소리 = textová_data
        자신.Stav_KÓD = 첫소리,가운뎃소리,끝소리
        자신.Historie = Historie
        자신.poslat((b'\x7f' if Předchozí_zboží else b'') + (확정글+자신.text()).encode('utf-8'))
        return True
