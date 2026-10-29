from tiếngViệt import ĐầuRa, mởĐiệnDữLiệu, gửiĐiệnDữLiệuBênNgoài, nhậnĐiệnDữLiệu, đóngMạng, miliGiây
from tiếngViệt import LỗiHệThống, LỗiLạiThửLàm, mãHóaVănBản, cácĐốiSốLệnh, SốNguyên
điểmCuối = mởĐiệnDữLiệu(0)
try:
    điệnDữLiệu = mãHóaVănBản("PYTHON UDP vi")
    gửiĐiệnDữLiệuBênNgoài(điểmCuối, "10.0.2.2", SốNguyên(cácĐốiSốLệnh[1]), điệnDữLiệu)
    chạy = miliGiây()
    while True:
        try:
            lờiĐáp, giáTrịCổng = nhậnĐiệnDữLiệu(điểmCuối)
            break
        except LỗiHệThống as lỗi:
            if lỗi.sốHiệu != LỗiLạiThửLàm or miliGiây() - chạy >= 700:
                raise
    assert lờiĐáp == điệnDữLiệu
    ĐầuRa("PYTHON 네트워크 xácMinh: UDP vi")
finally:
    đóngMạng(điểmCuối)
