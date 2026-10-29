"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Kulcs_Navigáció = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {ÉRTÉK: 한쌍 for 한쌍,ÉRTÉK in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, küld):
        자신.küld = küld
        자신.véglegesít_rész_egész()

    def véglegesít_rész_egész(자신):
        자신.Állapot_KÓD = ('','','')
        자신.Előzmények = []

    def Szöveg(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Állapot_KÓD
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Előzmények:
            return False
        자신.Állapot_KÓD = 자신.Előzmények.pop()
        자신.küld(b'\x7f' + 자신.Szöveg().encode('utf-8'))
        return True

    def csatorna_Kulcs(자신, 누름값):
        karakteres_adat = Kulcs_Navigáció.get(누름값, Kulcs_Navigáció.get(누름값.lower()))
        if karakteres_adat is None:
            return False
        Előző_cikk = 자신.Szöveg()
        첫소리,가운뎃소리,끝소리 = 자신.Állapot_KÓD
        Előzmények = 자신.Előzmények + [자신.Állapot_KÓD]
        확정글 = ''
        if karakteres_adat in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and karakteres_adat in 끝소리목록:
                끝소리 = karakteres_adat
            elif 끝소리 and (끝소리,karakteres_adat) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,karakteres_adat]
            else:
                확정글 = Előző_cikk
                첫소리,가운뎃소리,끝소리 = karakteres_adat,'',''
                Előzmények = [('','','')]
        elif 끝소리:
            왼쪽,jog = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Állapot_KÓD = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.Szöveg()
            첫소리,가운뎃소리,끝소리 = jog,karakteres_adat,''
            Előzmények = [('','',''),(jog,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,karakteres_adat) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,karakteres_adat]
            else:
                확정글 = Előző_cikk
                첫소리,가운뎃소리,끝소리 = '',karakteres_adat,''
                Előzmények = [('','','')]
        else:
            가운뎃소리 = karakteres_adat
        자신.Állapot_KÓD = 첫소리,가운뎃소리,끝소리
        자신.Előzmények = Előzmények
        자신.küld((b'\x7f' if Előző_cikk else b'') + (확정글+자신.Szöveg()).encode('utf-8'))
        return True
