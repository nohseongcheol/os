"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Chave_deseño = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {VALOR: 한쌍 for 한쌍,VALOR in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, enviar):
        자신.enviar = enviar
        자신.조합확정()

    def 조합확정(자신):
        자신.Estado_CÓDIGO = ('','','')
        자신.Historial = []

    def Texto(자신):
        첫소리,가운뎃소리,끝소리 = 자신.Estado_CÓDIGO
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Historial:
            return False
        자신.Estado_CÓDIGO = 자신.Historial.pop()
        자신.enviar(b'\x7f' + 자신.Texto().encode('utf-8'))
        return True

    def fonte_Chave(자신, 누름값):
        carácter_datos = Chave_deseño.get(누름값, Chave_deseño.get(누름값.lower()))
        if carácter_datos is None:
            return False
        이전 = 자신.Texto()
        첫소리,가운뎃소리,끝소리 = 자신.Estado_CÓDIGO
        Historial = 자신.Historial + [자신.Estado_CÓDIGO]
        확정글 = ''
        if carácter_datos in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and carácter_datos in 끝소리목록:
                끝소리 = carácter_datos
            elif 끝소리 and (끝소리,carácter_datos) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,carácter_datos]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = carácter_datos,'',''
                Historial = [('','','')]
        elif 끝소리:
            왼쪽,DEREITA = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.Estado_CÓDIGO = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.Texto()
            첫소리,가운뎃소리,끝소리 = DEREITA,carácter_datos,''
            Historial = [('','',''),(DEREITA,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,carácter_datos) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,carácter_datos]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = '',carácter_datos,''
                Historial = [('','','')]
        else:
            가운뎃소리 = carácter_datos
        자신.Estado_CÓDIGO = 첫소리,가운뎃소리,끝소리
        자신.Historial = Historial
        자신.enviar((b'\x7f' if 이전 else b'') + (확정글+자신.Texto()).encode('utf-8'))
        return True
