"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Avain_Asettelu = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {ARVO: 한쌍 for 한쌍,ARVO in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, lähettää):
        자신.lähettää = lähettää
        자신.vahvistaa_muutokset_kokoonpano()

    def vahvistaa_muutokset_kokoonpano(자신):
        자신.Tila_KOODI = ('','','')
        자신.Historia = []

    def teksti(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Tila_KOODI
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Historia:
            return False
        자신.Tila_KOODI = 자신.Historia.pop()
        자신.lähettää(b'\x7f' + 자신.teksti().encode('utf-8'))
        return True

    def syöte_Avain(자신, 누름값):
        merkkitiedot = Avain_Asettelu.get(누름값, Avain_Asettelu.get(누름값.lower()))
        if merkkitiedot is None:
            return False
        Edellinen_kohde = 자신.teksti()
        첫소리,가운뎃소리,끝소리 = 자신.Tila_KOODI
        Historia = 자신.Historia + [자신.Tila_KOODI]
        확정글 = ''
        if merkkitiedot in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and merkkitiedot in 끝소리목록:
                끝소리 = merkkitiedot
            elif 끝소리 and (끝소리,merkkitiedot) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,merkkitiedot]
            else:
                확정글 = Edellinen_kohde
                첫소리,가운뎃소리,끝소리 = merkkitiedot,'',''
                Historia = [('','','')]
        elif 끝소리:
            왼쪽,OIKEA = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Tila_KOODI = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.teksti()
            첫소리,가운뎃소리,끝소리 = OIKEA,merkkitiedot,''
            Historia = [('','',''),(OIKEA,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,merkkitiedot) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,merkkitiedot]
            else:
                확정글 = Edellinen_kohde
                첫소리,가운뎃소리,끝소리 = '',merkkitiedot,''
                Historia = [('','','')]
        else:
            가운뎃소리 = merkkitiedot
        자신.Tila_KOODI = 첫소리,가운뎃소리,끝소리
        자신.Historia = Historia
        자신.lähettää((b'\x7f' if Edellinen_kohde else b'') + (확정글+자신.teksti()).encode('utf-8'))
        return True
