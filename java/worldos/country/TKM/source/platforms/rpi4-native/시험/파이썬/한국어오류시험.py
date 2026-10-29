from 한국어 import ulgam_säwlik, 다시시도오류, 전문통신열기, 전문받기, ýap_Tor, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except ulgam_säwlik as Hata:
        assert Hata.indeks == 다시시도오류
        assert Hata.설명 == "operasiýa_ulgamy 작업에 실패했습니다."
        출력("한국어 전문 예외 barla")
finally:
    ýap_Tor(종단)
try:
    파일읽기("/없는파일")
except ulgam_säwlik as Hata:
    assert Hata.indeks == 2
    출력("한국어 Faýl 예외 barla")
else:
    raise AssertionError("Faýl 없음 예외가 필요합니다.")
