from tiếngViệt import LỗiHệThống, LỗiLạiThửLàm, mởĐiệnDữLiệu, nhậnĐiệnDữLiệu, đóngMạng, đọcTệp, ĐầuRa

điểmCuối = mởĐiệnDữLiệu(0)
try:
    try:
        nhậnĐiệnDữLiệu(điểmCuối)
        raise AssertionError("비어 있는 điệnDữLiệu 대기에서 예외가 필요합니다.")
    except LỗiHệThống as lỗi:
        assert lỗi.sốHiệu == LỗiLạiThửLàm
        assert lỗi.môTả == "HệĐiềuHành 작업에 실패했습니다."
        ĐầuRa("tiếngViệt điệnDữLiệu ngoạiLệ xácMinh")
finally:
    đóngMạng(điểmCuối)
try:
    đọcTệp("/없는파일")
except LỗiHệThống as lỗi:
    assert lỗi.sốHiệu == 2
    ĐầuRa("tiếngViệt Tệp ngoạiLệ xácMinh")
else:
    raise AssertionError("Tệp phươngThứcThiếu 예외가 필요합니다.")
