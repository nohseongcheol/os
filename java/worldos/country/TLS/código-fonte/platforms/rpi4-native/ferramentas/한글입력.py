"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Chave_Layout = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
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
        자신.commit_composição()

    def commit_composição(자신):
        자신.código_de_estado = ('','','')
        자신.Histórico = []

    def texto(자신):
        첫소리,가운뎃소리,끝소리 = 자신.código_de_estado
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Histórico:
            return False
        자신.código_de_estado = 자신.Histórico.pop()
        자신.enviar(b'\x7f' + 자신.texto().encode('utf-8'))
        return True

    def feed_Chave(자신, 누름값):
        dados_de_caractere = Chave_Layout.get(누름값, Chave_Layout.get(누름값.lower()))
        if dados_de_caractere is None:
            return False
        Anterior_item = 자신.texto()
        첫소리,가운뎃소리,끝소리 = 자신.código_de_estado
        Histórico = 자신.Histórico + [자신.código_de_estado]
        확정글 = ''
        if dados_de_caractere in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and dados_de_caractere in 끝소리목록:
                끝소리 = dados_de_caractere
            elif 끝소리 and (끝소리,dados_de_caractere) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,dados_de_caractere]
            else:
                확정글 = Anterior_item
                첫소리,가운뎃소리,끝소리 = dados_de_caractere,'',''
                Histórico = [('','','')]
        elif 끝소리:
            왼쪽,DIREITA = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.código_de_estado = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.texto()
            첫소리,가운뎃소리,끝소리 = DIREITA,dados_de_caractere,''
            Histórico = [('','',''),(DIREITA,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,dados_de_caractere) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,dados_de_caractere]
            else:
                확정글 = Anterior_item
                첫소리,가운뎃소리,끝소리 = '',dados_de_caractere,''
                Histórico = [('','','')]
        else:
            가운뎃소리 = dados_de_caractere
        자신.código_de_estado = 첫소리,가운뎃소리,끝소리
        자신.Histórico = Histórico
        자신.enviar((b'\x7f' if Anterior_item else b'') + (확정글+자신.texto()).encode('utf-8'))
        return True
