from Cymraeg import system_gwall, 다시시도오류, 전문통신열기, 전문받기, cau_Rhwydwaith, 파일읽기, Allbwn

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except system_gwall as Gwall:
        assert Gwall.INDEX == 다시시도오류
        assert Gwall.설명 == "system_weithredu 작업에 실패했습니다."
        Allbwn("Cymraeg 전문 eithriad dilysu")
finally:
    cau_Rhwydwaith(종단)
try:
    파일읽기("/없는파일")
except system_gwall as Gwall:
    assert Gwall.INDEX == 2
    Allbwn("Cymraeg Ffeil eithriad dilysu")
else:
    raise AssertionError("Ffeil 없음 예외가 필요합니다.")
