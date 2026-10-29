"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
toets_Indeling = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {WAARDE: 한쌍 for 한쌍,WAARDE in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, e_mailen):
        자신.e_mailen = e_mailen
        자신.doorvoeren_samenstelling()

    def doorvoeren_samenstelling(자신):
        자신.Status_CODE = ('','','')
        자신.Geschiedenis = []

    def tekst(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Status_CODE
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Geschiedenis:
            return False
        자신.Status_CODE = 자신.Geschiedenis.pop()
        자신.e_mailen(b'\x7f' + 자신.tekst().encode('utf-8'))
        return True

    def feed_toets(자신, 누름값):
        tekengegevens = toets_Indeling.get(누름값, toets_Indeling.get(누름값.lower()))
        if tekengegevens is None:
            return False
        Vorige_item = 자신.tekst()
        첫소리,가운뎃소리,끝소리 = 자신.Status_CODE
        Geschiedenis = 자신.Geschiedenis + [자신.Status_CODE]
        확정글 = ''
        if tekengegevens in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and tekengegevens in 끝소리목록:
                끝소리 = tekengegevens
            elif 끝소리 and (끝소리,tekengegevens) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,tekengegevens]
            else:
                확정글 = Vorige_item
                첫소리,가운뎃소리,끝소리 = tekengegevens,'',''
                Geschiedenis = [('','','')]
        elif 끝소리:
            왼쪽,recht = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Status_CODE = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.tekst()
            첫소리,가운뎃소리,끝소리 = recht,tekengegevens,''
            Geschiedenis = [('','',''),(recht,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,tekengegevens) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,tekengegevens]
            else:
                확정글 = Vorige_item
                첫소리,가운뎃소리,끝소리 = '',tekengegevens,''
                Geschiedenis = [('','','')]
        else:
            가운뎃소리 = tekengegevens
        자신.Status_CODE = 첫소리,가운뎃소리,끝소리
        자신.Geschiedenis = Geschiedenis
        자신.e_mailen((b'\x7f' if Vorige_item else b'') + (확정글+자신.tekst()).encode('utf-8'))
        return True
