"""tựThân 커널의 Tệp·TruyềnThông·MànHình 호출과 tiếngViệt ngoạiLệ. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as HệĐiềuHành
import sys as MôiTrườngChạy

def ĐầuRa(*giáTrị, bộPhânCách=" ", phầnKết="\n", **cácĐốiSốKếThừa):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in cácĐốiSốKếThừa: cácĐốiSốKếThừa["sep"] = bộPhânCách
    if "end" not in cácĐốiSốKếThừa: cácĐốiSốKếThừa["end"] = phầnKết
    print(*giáTrị, **cácĐốiSốKếThừa)

SốNguyên = int
cácĐốiSốLệnh = MôiTrườngChạy.argv
LỗiLạiThửLàm = 11

class LỗiHệThống(OSError):
    def __init__(giáTrịBảnThân, sốHiệu, môTả="HệĐiềuHành 작업에 실패했습니다."):
        super().__init__(sốHiệu, môTả)
        giáTrịBảnThân.sốHiệu = sốHiệu
        giáTrịBảnThân.môTả = môTả

def gọiThựcHiệnHệThống(Hàm, *cácĐốiSố):
    try:
        return Hàm(*cácĐốiSố)
    except OSError as lỗi:
        sốHiệu = lỗi.args[0] if lỗi.args else 0
        raise LỗiHệThống(sốHiệu)

def mãHóaVănBản(vănBản):
    return vănBản.encode("utf-8")

def giảiMãVănBản(DữLiệu):
    return DữLiệu.decode("utf-8")

def đọcTệp(tên):
    return gọiThựcHiệnHệThống(HệĐiềuHành.read, tên)

def ghiTệp(tên, DữLiệu):
    return gọiThựcHiệnHệThống(HệĐiềuHành.write, tên, DữLiệu)

def gỡTệp(tên):
    return gọiThựcHiệnHệThống(HệĐiềuHành.remove, tên)

def mởĐiệnDữLiệu(sốCổng):
    return gọiThựcHiệnHệThống(HệĐiềuHành.udp_open, sốCổng)

def gửiĐiệnDữLiệu(điểmCuối, sốCổng, DữLiệu):
    return gọiThựcHiệnHệThống(HệĐiềuHành.udp_send, điểmCuối, sốCổng, DữLiệu)

def gửiĐiệnDữLiệuBênNgoài(điểmCuối, địaChỉ, sốCổng, DữLiệu):
    return gọiThựcHiệnHệThống(HệĐiềuHành.udp_sendto, điểmCuối, địaChỉ, sốCổng, DữLiệu)

def nhậnĐiệnDữLiệu(điểmCuối):
    return gọiThựcHiệnHệThống(HệĐiềuHành.udp_recv, điểmCuối)

def đóngMạng(điểmCuối):
    return gọiThựcHiệnHệThống(HệĐiềuHành.udp_close, điểmCuối)

def vẽHìnhChữNhật(*cácĐốiSố):
    return gọiThựcHiệnHệThống(HệĐiềuHành.rect, *cácĐốiSố)

def cỡMànHình():
    return gọiThựcHiệnHệThống(HệĐiềuHành.screen_size)

def chờBảnVẽCho():
    return gọiThựcHiệnHệThống(HệĐiềuHành.wait_key)

miliGiây = HệĐiềuHành.ticks_ms
