"""Two-set Hangul composition for the native VNC-to-UART input bridge.

The pending character is visible in the guest editor. Replacing it uses that
editor's UTF-8 Backspace, so commit before cursor motion, shortcuts or a click.
No host input-method daemon or third-party Python package is required.
"""

bảngTraJamoBanĐầu = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
bảngTraJamoỞGiữa = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
bảngTraJamoCuốiCùng = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
bốTríPhím = dict(zip('rRseEfaqQtTdwWczxvgkoiOjpuPhynbml',
                'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'))
jamoỞGiữaPhứcHợp = {('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',
          ('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ'}
jamoCuốiCùngPhứcHợp = {('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',
          ('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',
          ('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
táchJamoCuốiCùng = {giáTrị: cặpMột for cặpMột,giáTrị in jamoCuốiCùngPhứcHợp.items()}


class ghépHangul:
    def __init__(giáTrịBảnThân, gửi):
        giáTrịBảnThân.gửi = gửi
        giáTrịBảnThân.phépGhépChốt()

    def phépGhépChốt(giáTrịBảnThân):
        giáTrịBảnThân.mãTrạngThái = ('','','')
        giáTrịBảnThân.lịchSử = []

    def vănBản(giáTrịBảnThân):
        jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng = giáTrịBảnThân.mãTrạngThái
        if jamoBanĐầu and jamoỞGiữa:
            return chr(0xac00 + (bảngTraJamoBanĐầu.index(jamoBanĐầu)*21 + bảngTraJamoỞGiữa.index(jamoỞGiữa))*28
                       + (bảngTraJamoCuốiCùng.index(jamoCuốiCùng) if jamoCuốiCùng else 0))
        return jamoBanĐầu or jamoỞGiữa

    def xóaLùi(giáTrịBảnThân):
        if not giáTrịBảnThân.lịchSử:
            return False
        giáTrịBảnThân.mãTrạngThái = giáTrịBảnThân.lịchSử.pop()
        giáTrịBảnThân.gửi(b'\x7f' + giáTrịBảnThân.vănBản().encode('utf-8'))
        return True

    def phímCấp(giáTrịBảnThân, giáTrịĐãNhấn):
        dữLiệuKýTự = bốTríPhím.get(giáTrịĐãNhấn, bốTríPhím.get(giáTrịĐãNhấn.lower()))
        if dữLiệuKýTự is None:
            return False
        phầnMụcTrướcĐó = giáTrịBảnThân.vănBản()
        jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng = giáTrịBảnThân.mãTrạngThái
        lịchSử = giáTrịBảnThân.lịchSử + [giáTrịBảnThân.mãTrạngThái]
        đãChốt = ''
        if dữLiệuKýTự in bảngTraJamoBanĐầu:
            if jamoBanĐầu and jamoỞGiữa and not jamoCuốiCùng and dữLiệuKýTự in bảngTraJamoCuốiCùng:
                jamoCuốiCùng = dữLiệuKýTự
            elif jamoCuốiCùng and (jamoCuốiCùng,dữLiệuKýTự) in jamoCuốiCùngPhứcHợp:
                jamoCuốiCùng = jamoCuốiCùngPhứcHợp[jamoCuốiCùng,dữLiệuKýTự]
            else:
                đãChốt = phầnMụcTrướcĐó
                jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng = dữLiệuKýTự,'',''
                lịchSử = [('','','')]
        elif jamoCuốiCùng:
            bênTrái,phải = táchJamoCuốiCùng.get(jamoCuốiCùng, ('',jamoCuốiCùng))
            giáTrịBảnThân.mãTrạngThái = jamoBanĐầu,jamoỞGiữa,bênTrái
            đãChốt = giáTrịBảnThân.vănBản()
            jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng = phải,dữLiệuKýTự,''
            lịchSử = [('','',''),(phải,'','')]
        elif jamoỞGiữa:
            if (jamoỞGiữa,dữLiệuKýTự) in jamoỞGiữaPhứcHợp:
                jamoỞGiữa = jamoỞGiữaPhứcHợp[jamoỞGiữa,dữLiệuKýTự]
            else:
                đãChốt = phầnMụcTrướcĐó
                jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng = '',dữLiệuKýTự,''
                lịchSử = [('','','')]
        else:
            jamoỞGiữa = dữLiệuKýTự
        giáTrịBảnThân.mãTrạngThái = jamoBanĐầu,jamoỞGiữa,jamoCuốiCùng
        giáTrịBảnThân.lịchSử = lịchSử
        giáTrịBảnThân.gửi((b'\x7f' if phầnMụcTrướcĐó else b'') + (đãChốt+giáTrịBảnThân.vănBản()).encode('utf-8'))
        return True
