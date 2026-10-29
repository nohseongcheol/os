"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

tableLettreHangulInitialValeur = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
tableLettreHangulVoyelleMédiane = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
tableLettreHangulFinal = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
dispositionTouche = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
lettreHangulVoyelleMédianeComposéMot = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
lettreHangulFinalComposéMot = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
séparerLettreHangulFinal = {valeur: paireUn for paireUn,valeur in lettreHangulFinalComposéMot.items()}


class composerHangul:
    def __init__(valeurSoi, envoyer):
        valeurSoi.envoyer = envoyer
        valeurSoi.compositionConfirmer()

    def compositionConfirmer(valeurSoi):
        valeurSoi.codeÉtatValeur = ('','','')
        valeurSoi.historique = []

    def texte(valeurSoi):
        lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal = valeurSoi.codeÉtatValeur
        if lettreHangulInitialValeur and lettreHangulVoyelleMédiane:
            return chr(0xac00 + (tableLettreHangulInitialValeur.index(lettreHangulInitialValeur)*21 + tableLettreHangulVoyelleMédiane.index(lettreHangulVoyelleMédiane))*28
                       + (tableLettreHangulFinal.index(lettreHangulFinal) if lettreHangulFinal else 0))
        return lettreHangulInitialValeur or lettreHangulVoyelleMédiane

    def retourArrière(valeurSoi):
        if not valeurSoi.historique:
            return False
        valeurSoi.codeÉtatValeur = valeurSoi.historique.pop()
        valeurSoi.envoyer(b'\x7f' + valeurSoi.texte().encode('utf-8'))
        return True

    def toucheAlimenter(valeurSoi, valeurEnfoncé):
        donnéesCaractère = dispositionTouche.get(valeurEnfoncé, dispositionTouche.get(valeurEnfoncé.lower()))
        if donnéesCaractère is None:
            return False
        élémentListePrécédentÉlément = valeurSoi.texte()
        lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal = valeurSoi.codeÉtatValeur
        historique = valeurSoi.historique + [valeurSoi.codeÉtatValeur]
        validé = ''
        if donnéesCaractère in tableLettreHangulInitialValeur:
            if lettreHangulInitialValeur and lettreHangulVoyelleMédiane and not lettreHangulFinal and donnéesCaractère in tableLettreHangulFinal:
                lettreHangulFinal = donnéesCaractère
            elif lettreHangulFinal and (lettreHangulFinal,donnéesCaractère) in lettreHangulFinalComposéMot:
                lettreHangulFinal = lettreHangulFinalComposéMot[lettreHangulFinal,donnéesCaractère]
            else:
                validé = élémentListePrécédentÉlément
                lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal = donnéesCaractère,'',''
                historique = [('','','')]
        elif lettreHangulFinal:
            côtéGauche,droit = séparerLettreHangulFinal.get(lettreHangulFinal, ('',lettreHangulFinal))
            valeurSoi.codeÉtatValeur = lettreHangulInitialValeur,lettreHangulVoyelleMédiane,côtéGauche
            validé = valeurSoi.texte()
            lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal = droit,donnéesCaractère,''
            historique = [('','',''),(droit,'','')]
        elif lettreHangulVoyelleMédiane:
            if (lettreHangulVoyelleMédiane,donnéesCaractère) in lettreHangulVoyelleMédianeComposéMot:
                lettreHangulVoyelleMédiane = lettreHangulVoyelleMédianeComposéMot[lettreHangulVoyelleMédiane,donnéesCaractère]
            else:
                validé = élémentListePrécédentÉlément
                lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal = '',donnéesCaractère,''
                historique = [('','','')]
        else:
            lettreHangulVoyelleMédiane = donnéesCaractère
        valeurSoi.codeÉtatValeur = lettreHangulInitialValeur,lettreHangulVoyelleMédiane,lettreHangulFinal
        valeurSoi.historique = historique
        valeurSoi.envoyer((b'\x7f' if élémentListePrécédentÉlément else b'') + (validé+valeurSoi.texte()).encode('utf-8'))
        return True
