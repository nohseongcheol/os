"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

initialJamoTable = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
medialJamoTable = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
finalJamoTable = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
keyLayout = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
compoundMedialJamo = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
compoundFinalJamo = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
splitFinalJamo = {value: onePair for onePair,value in compoundFinalJamo.items()}


class composeHangul:
    def __init__(selfValue, send):
        selfValue.send = send
        selfValue.commitComposition()

    def commitComposition(selfValue):
        selfValue.stateCode = ('','','')
        selfValue.history = []

    def text(selfValue):
        initialJamo,medialJamo,finalJamo = selfValue.stateCode
        if initialJamo and medialJamo:
            return chr(0xac00 + (initialJamoTable.index(initialJamo)*21 + medialJamoTable.index(medialJamo))*28
                       + (finalJamoTable.index(finalJamo) if finalJamo else 0))
        return initialJamo or medialJamo

    def backspace(selfValue):
        if not selfValue.history:
            return False
        selfValue.stateCode = selfValue.history.pop()
        selfValue.send(b'\x7f' + selfValue.text().encode('utf-8'))
        return True

    def feedKey(selfValue, pressedValue):
        characterData = keyLayout.get(pressedValue, keyLayout.get(pressedValue.lower()))
        if characterData is None:
            return False
        previousItem = selfValue.text()
        initialJamo,medialJamo,finalJamo = selfValue.stateCode
        history = selfValue.history + [selfValue.stateCode]
        committed = ''
        if characterData in initialJamoTable:
            if initialJamo and medialJamo and not finalJamo and characterData in finalJamoTable:
                finalJamo = characterData
            elif finalJamo and (finalJamo,characterData) in compoundFinalJamo:
                finalJamo = compoundFinalJamo[finalJamo,characterData]
            else:
                committed = previousItem
                initialJamo,medialJamo,finalJamo = characterData,'',''
                history = [('','','')]
        elif finalJamo:
            leftSide,right = splitFinalJamo.get(finalJamo, ('',finalJamo))
            selfValue.stateCode = initialJamo,medialJamo,leftSide
            committed = selfValue.text()
            initialJamo,medialJamo,finalJamo = right,characterData,''
            history = [('','',''),(right,'','')]
        elif medialJamo:
            if (medialJamo,characterData) in compoundMedialJamo:
                medialJamo = compoundMedialJamo[medialJamo,characterData]
            else:
                committed = previousItem
                initialJamo,medialJamo,finalJamo = '',characterData,''
                history = [('','','')]
        else:
            medialJamo = characterData
        selfValue.stateCode = initialJamo,medialJamo,finalJamo
        selfValue.history = history
        selfValue.send((b'\x7f' if previousItem else b'') + (committed+selfValue.text()).encode('utf-8'))
        return True
