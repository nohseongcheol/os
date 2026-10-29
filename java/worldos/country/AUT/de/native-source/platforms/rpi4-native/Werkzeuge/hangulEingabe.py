"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

anfänglichHangulBuchstabeTabelle = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
mittellautHangulBuchstabeTabelle = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
abschließendHangulBuchstabeTabelle = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
tasteAnordnung = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
zusammengesetztesWortMittellautHangulBuchstabe = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
zusammengesetztesWortAbschließendHangulBuchstabe = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
abschließendHangulBuchstabeAufteilen = {Wert: einsPaar for einsPaar,Wert in zusammengesetztesWortAbschließendHangulBuchstabe.items()}


class hangulZusammensetzen:
    def __init__(selbstWert, senden):
        selbstWert.senden = senden
        selbstWert.bestätigenZusammensetzung()

    def bestätigenZusammensetzung(selbstWert):
        selbstWert.statuswertKode = ('','','')
        selbstWert.verlauf = []

    def Text(selbstWert):
        anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe = selbstWert.statuswertKode
        if anfänglichHangulBuchstabe and mittellautHangulBuchstabe:
            return chr(0xac00 + (anfänglichHangulBuchstabeTabelle.index(anfänglichHangulBuchstabe)*21 + mittellautHangulBuchstabeTabelle.index(mittellautHangulBuchstabe))*28
                       + (abschließendHangulBuchstabeTabelle.index(abschließendHangulBuchstabe) if abschließendHangulBuchstabe else 0))
        return anfänglichHangulBuchstabe or mittellautHangulBuchstabe

    def rückschritt(selbstWert):
        if not selbstWert.verlauf:
            return False
        selbstWert.statuswertKode = selbstWert.verlauf.pop()
        selbstWert.senden(b'\x7f' + selbstWert.Text().encode('utf-8'))
        return True

    def zuführenTaste(selbstWert, gedrücktWert):
        zeichenDaten = tasteAnordnung.get(gedrücktWert, tasteAnordnung.get(gedrücktWert.lower()))
        if zeichenDaten is None:
            return False
        vorherigElementeintrag = selbstWert.Text()
        anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe = selbstWert.statuswertKode
        verlauf = selbstWert.verlauf + [selbstWert.statuswertKode]
        bestätigt = ''
        if zeichenDaten in anfänglichHangulBuchstabeTabelle:
            if anfänglichHangulBuchstabe and mittellautHangulBuchstabe and not abschließendHangulBuchstabe and zeichenDaten in abschließendHangulBuchstabeTabelle:
                abschließendHangulBuchstabe = zeichenDaten
            elif abschließendHangulBuchstabe and (abschließendHangulBuchstabe,zeichenDaten) in zusammengesetztesWortAbschließendHangulBuchstabe:
                abschließendHangulBuchstabe = zusammengesetztesWortAbschließendHangulBuchstabe[abschließendHangulBuchstabe,zeichenDaten]
            else:
                bestätigt = vorherigElementeintrag
                anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe = zeichenDaten,'',''
                verlauf = [('','','')]
        elif abschließendHangulBuchstabe:
            linksSeiteRand,rechts = abschließendHangulBuchstabeAufteilen.get(abschließendHangulBuchstabe, ('',abschließendHangulBuchstabe))
            selbstWert.statuswertKode = anfänglichHangulBuchstabe,mittellautHangulBuchstabe,linksSeiteRand
            bestätigt = selbstWert.Text()
            anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe = rechts,zeichenDaten,''
            verlauf = [('','',''),(rechts,'','')]
        elif mittellautHangulBuchstabe:
            if (mittellautHangulBuchstabe,zeichenDaten) in zusammengesetztesWortMittellautHangulBuchstabe:
                mittellautHangulBuchstabe = zusammengesetztesWortMittellautHangulBuchstabe[mittellautHangulBuchstabe,zeichenDaten]
            else:
                bestätigt = vorherigElementeintrag
                anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe = '',zeichenDaten,''
                verlauf = [('','','')]
        else:
            mittellautHangulBuchstabe = zeichenDaten
        selbstWert.statuswertKode = anfänglichHangulBuchstabe,mittellautHangulBuchstabe,abschließendHangulBuchstabe
        selbstWert.verlauf = verlauf
        selbstWert.senden((b'\x7f' if vorherigElementeintrag else b'') + (bestätigt+selbstWert.Text()).encode('utf-8'))
        return True
