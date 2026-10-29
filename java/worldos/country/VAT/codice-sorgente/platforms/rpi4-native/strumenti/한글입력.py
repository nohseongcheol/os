"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
tasto_Layout = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {VALORE: 한쌍 for 한쌍,VALORE in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, inviare):
        자신.inviare = inviare
        자신.commit_composizione()

    def commit_composizione(자신):
        자신.codice_di_stato = ('','','')
        자신.Cronologia = []

    def testo(자신):
        첫소리,가운뎃소리,끝소리 = 자신.codice_di_stato
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Cronologia:
            return False
        자신.codice_di_stato = 자신.Cronologia.pop()
        자신.inviare(b'\x7f' + 자신.testo().encode('utf-8'))
        return True

    def feed_tasto(자신, 누름값):
        dati_di_tipo_carattere = tasto_Layout.get(누름값, tasto_Layout.get(누름값.lower()))
        if dati_di_tipo_carattere is None:
            return False
        Indietro_articolo = 자신.testo()
        첫소리,가운뎃소리,끝소리 = 자신.codice_di_stato
        Cronologia = 자신.Cronologia + [자신.codice_di_stato]
        확정글 = ''
        if dati_di_tipo_carattere in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and dati_di_tipo_carattere in 끝소리목록:
                끝소리 = dati_di_tipo_carattere
            elif 끝소리 and (끝소리,dati_di_tipo_carattere) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,dati_di_tipo_carattere]
            else:
                확정글 = Indietro_articolo
                첫소리,가운뎃소리,끝소리 = dati_di_tipo_carattere,'',''
                Cronologia = [('','','')]
        elif 끝소리:
            왼쪽,DESTRA = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.codice_di_stato = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.testo()
            첫소리,가운뎃소리,끝소리 = DESTRA,dati_di_tipo_carattere,''
            Cronologia = [('','',''),(DESTRA,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,dati_di_tipo_carattere) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,dati_di_tipo_carattere]
            else:
                확정글 = Indietro_articolo
                첫소리,가운뎃소리,끝소리 = '',dati_di_tipo_carattere,''
                Cronologia = [('','','')]
        else:
            가운뎃소리 = dati_di_tipo_carattere
        자신.codice_di_stato = 첫소리,가운뎃소리,끝소리
        자신.Cronologia = Cronologia
        자신.inviare((b'\x7f' if Indietro_articolo else b'') + (확정글+자신.testo()).encode('utf-8'))
        return True
