"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

첫소리목록 = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
가운뎃소리목록 = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
끝소리목록 = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
Kunci_Navigasi = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
겹가운뎃소리 = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
겹끝소리 = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
끝소리가르기 = {VALUE: 한쌍 for 한쌍,VALUE in 겹끝소리.items()}


class 한글조합:
    def __init__(자신, e_mel_9aee63bd):
        자신.e_mel_9aee63bd = e_mel_9aee63bd
        자신.조합확정()

    def 조합확정(자신):
        자신.status_kod = ('','','')
        자신.Sejarah = []

    def Teks(자신):
        첫소리,가운뎃소리,끝소리 = 자신.status_kod
        if 첫소리 and 가운뎃소리:
            return chr(0xac00 + (첫소리목록.index(첫소리)*21 + 가운뎃소리목록.index(가운뎃소리))*28
                       + (끝소리목록.index(끝소리) if 끝소리 else 0))
        return 첫소리 or 가운뎃소리

    def 앞글자지우기(자신):
        if not 자신.Sejarah:
            return False
        자신.status_kod = 자신.Sejarah.pop()
        자신.e_mel_9aee63bd(b'\x7f' + 자신.Teks().encode('utf-8'))
        return True

    def suapan_Kunci(자신, 누름값):
        data_aksara = Kunci_Navigasi.get(누름값, Kunci_Navigasi.get(누름값.lower()))
        if data_aksara is None:
            return False
        이전 = 자신.Teks()
        첫소리,가운뎃소리,끝소리 = 자신.status_kod
        Sejarah = 자신.Sejarah + [자신.status_kod]
        확정글 = ''
        if data_aksara in 첫소리목록:
            if 첫소리 and 가운뎃소리 and not 끝소리 and data_aksara in 끝소리목록:
                끝소리 = data_aksara
            elif 끝소리 and (끝소리,data_aksara) in 겹끝소리:
                끝소리 = 겹끝소리[끝소리,data_aksara]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = data_aksara,'',''
                Sejarah = [('','','')]
        elif 끝소리:
            왼쪽,RIGHT = 끝소리가르기.get(끝소리, ('',끝소리))
            자신.status_kod = 첫소리,가운뎃소리,왼쪽
            확정글 = 자신.Teks()
            첫소리,가운뎃소리,끝소리 = RIGHT,data_aksara,''
            Sejarah = [('','',''),(RIGHT,'','')]
        elif 가운뎃소리:
            if (가운뎃소리,data_aksara) in 겹가운뎃소리:
                가운뎃소리 = 겹가운뎃소리[가운뎃소리,data_aksara]
            else:
                확정글 = 이전
                첫소리,가운뎃소리,끝소리 = '',data_aksara,''
                Sejarah = [('','','')]
        else:
            가운뎃소리 = data_aksara
        자신.status_kod = 첫소리,가운뎃소리,끝소리
        자신.Sejarah = Sejarah
        자신.e_mel_9aee63bd((b'\x7f' if 이전 else b'') + (확정글+자신.Teks()).encode('utf-8'))
        return True
