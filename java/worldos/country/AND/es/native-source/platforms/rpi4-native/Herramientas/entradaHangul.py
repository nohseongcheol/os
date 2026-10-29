"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No Anfitrión input-method daemon or third-party Python package is required.
"""

tablaLetraHangulInicialValor = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
tablaLetraHangulVocalMedial = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
tablaLetraHangulFinal = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
disposiciónTecla = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
letraHangulVocalMedialPalabraCompuesta = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
letraHangulFinalPalabraCompuesta = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
separarLetraHangulFinal = {valor: parUno for parUno,valor in letraHangulFinalPalabraCompuesta.items()}


class componerHangul:
    def __init__(valorPropio, enviar):
        valorPropio.enviar = enviar
        valorPropio.composiciónConfirmar()

    def composiciónConfirmar(valorPropio):
        valorPropio.códigoEstadoValor = ('','','')
        valorPropio.historial = []

    def texto(valorPropio):
        letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal = valorPropio.códigoEstadoValor
        if letraHangulInicialValor and letraHangulVocalMedial:
            return chr(0xac00 + (tablaLetraHangulInicialValor.index(letraHangulInicialValor)*21 + tablaLetraHangulVocalMedial.index(letraHangulVocalMedial))*28
                       + (tablaLetraHangulFinal.index(letraHangulFinal) if letraHangulFinal else 0))
        return letraHangulInicialValor or letraHangulVocalMedial

    def retroceso(valorPropio):
        if not valorPropio.historial:
            return False
        valorPropio.códigoEstadoValor = valorPropio.historial.pop()
        valorPropio.enviar(b'\x7f' + valorPropio.texto().encode('utf-8'))
        return True

    def teclaAlimentar(valorPropio, valorPulsado):
        datosCarácter = disposiciónTecla.get(valorPulsado, disposiciónTecla.get(valorPulsado.lower()))
        if datosCarácter is None:
            return False
        elementoListaElementoPrevio = valorPropio.texto()
        letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal = valorPropio.códigoEstadoValor
        historial = valorPropio.historial + [valorPropio.códigoEstadoValor]
        confirmado = ''
        if datosCarácter in tablaLetraHangulInicialValor:
            if letraHangulInicialValor and letraHangulVocalMedial and not letraHangulFinal and datosCarácter in tablaLetraHangulFinal:
                letraHangulFinal = datosCarácter
            elif letraHangulFinal and (letraHangulFinal,datosCarácter) in letraHangulFinalPalabraCompuesta:
                letraHangulFinal = letraHangulFinalPalabraCompuesta[letraHangulFinal,datosCarácter]
            else:
                confirmado = elementoListaElementoPrevio
                letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal = datosCarácter,'',''
                historial = [('','','')]
        elif letraHangulFinal:
            ladoIzquierdo,derecho = separarLetraHangulFinal.get(letraHangulFinal, ('',letraHangulFinal))
            valorPropio.códigoEstadoValor = letraHangulInicialValor,letraHangulVocalMedial,ladoIzquierdo
            confirmado = valorPropio.texto()
            letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal = derecho,datosCarácter,''
            historial = [('','',''),(derecho,'','')]
        elif letraHangulVocalMedial:
            if (letraHangulVocalMedial,datosCarácter) in letraHangulVocalMedialPalabraCompuesta:
                letraHangulVocalMedial = letraHangulVocalMedialPalabraCompuesta[letraHangulVocalMedial,datosCarácter]
            else:
                confirmado = elementoListaElementoPrevio
                letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal = '',datosCarácter,''
                historial = [('','','')]
        else:
            letraHangulVocalMedial = datosCarácter
        valorPropio.códigoEstadoValor = letraHangulInicialValor,letraHangulVocalMedial,letraHangulFinal
        valorPropio.historial = historial
        valorPropio.enviar((b'\x7f' if elementoListaElementoPrevio else b'') + (confirmado+valorPropio.texto()).encode('utf-8'))
        return True
