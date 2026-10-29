"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
kelal_lelngo = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {njaru: 한쌍 for 한쌍,njaru in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, neldude):
        자신.neldude = neldude
        자신.조합확정()

    def 조합확정(자신):
        자신.상태값 = ('','','')
        자신.지난기록 = []

    def binndi(자신):
        첫소리,가운뎃소리,끝소리 = 자신.상태값
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.지난기록:
            return False
        자신.상태값 = 자신.지난기록.pop()
        자신.neldude(b'\x7f' + 자신.binndi().encode('utf-8'))
        return True

    def tummbitere_kelal(자신, 누름값):
        alkulal_keɓe = kelal_lelngo.get(누름값, kelal_lelngo.get(누름값.lower()))
        if alkulal_keɓe is None:
            return False
        이전 = 자신.binndi()
        첫소리,가운뎃소리,끝소리 = 자신.상태값
        지난기록 = 자신.지난기록 + [자신.상태값]
        확정글 = ''
        if alkulal_keɓe in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and alkulal_keɓe in 끝소리목록:
                끝소리 = alkulal_keɓe
            elif 끝소리 and (끝소리,alkulal_keɓe) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,alkulal_keɓe]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = alkulal_keɓe,'',''
                지난기록 = [('','','')]
        elif 끝소리:
            왼쪽,오른쪽 = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.상태값 = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.binndi()
            첫소리,가운뎃소리,끝소리 = 오른쪽,alkulal_keɓe,''
            지난기록 = [('','',''),(오른쪽,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,alkulal_keɓe) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,alkulal_keɓe]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = '',alkulal_keɓe,''
                지난기록 = [('','','')]
        else:
            가운뎃소리 = alkulal_keɓe
        자신.상태값 = 첫소리,가운뎃소리,끝소리
        자신.지난기록 = 지난기록
        자신.neldude((b'\x7f' if 이전 else b'') + (확정글+자신.binndi()).encode('utf-8'))
        return True
