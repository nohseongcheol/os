"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Ključ_Raspored = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {VALUE: 한쌍 for 한쌍,VALUE in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, poslati):
        자신.poslati = poslati
        자신.조합확정()

    def 조합확정(자신):
        자신.Status_kôd = ('','','')
        자신.Istorija = []

    def SMS(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Status_kôd
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Istorija:
            return False
        자신.Status_kôd = 자신.Istorija.pop()
        자신.poslati(b'\x7f' + 자신.SMS().encode('utf-8'))
        return True

    def fid_Ključ(자신, 누름값):
        znakovni_podaci = Ključ_Raspored.get(누름값, Ključ_Raspored.get(누름값.lower()))
        if znakovni_podaci is None:
            return False
        이전 = 자신.SMS()
        첫소리,가운뎃소리,끝소리 = 자신.Status_kôd
        Istorija = 자신.Istorija + [자신.Status_kôd]
        izvršen = ''
        if znakovni_podaci in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and znakovni_podaci in 끝소리목록:
                끝소리 = znakovni_podaci
            elif 끝소리 and (끝소리,znakovni_podaci) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,znakovni_podaci]
            else:
                izvršen = 이전
                첫소리,가운뎃소리,끝소리 = znakovni_podaci,'',''
                Istorija = [('','','')]
        elif 끝소리:
            왼쪽,RIGHT = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Status_kôd = 첫소리,가운뎃소리,왼쪽
            izvršen = 자신.SMS()
            첫소리,가운뎃소리,끝소리 = RIGHT,znakovni_podaci,''
            Istorija = [('','',''),(RIGHT,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,znakovni_podaci) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,znakovni_podaci]
            else:
                izvršen = 이전
                첫소리,가운뎃소리,끝소리 = '',znakovni_podaci,''
                Istorija = [('','','')]
        else:
            가운뎃소리 = znakovni_podaci
        자신.Status_kôd = 첫소리,가운뎃소리,끝소리
        자신.Istorija = Istorija
        자신.poslati((b'\x7f' if 이전 else b'') + (izvršen+자신.SMS()).encode('utf-8'))
        return True
