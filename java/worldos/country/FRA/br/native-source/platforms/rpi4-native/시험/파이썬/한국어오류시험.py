from 한국어 import 운영체제오류, 다시시도오류, 전문통신열기, 전문받기, 통신닫기, 파일읽기, Ec_hankad

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except 운영체제오류 as Fazi:
        assert Fazi.번호 == 다시시도오류
        assert Fazi.설명 == "운영체제 작업에 실패했습니다."
        Ec_hankad("한국어 전문 예외 확인")
finally:
    통신닫기(종단)
try:
    파일읽기("/없는파일")
except 운영체제오류 as Fazi:
    assert Fazi.번호 == 2
    Ec_hankad("한국어 Restr 예외 확인")
else:
    raise AssertionError("Restr 없음 예외가 필요합니다.")
