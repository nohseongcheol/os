from 한국어 import siostam_mearachd, 다시시도오류, 전문통신열기, 전문받기, dùin_lìonra, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except siostam_mearachd as Mearachd:
        assert Mearachd.INDEX == 다시시도오류
        assert Mearachd.설명 == "siostam_obrachaidh 작업에 실패했습니다."
        출력("한국어 전문 예외 dearbh")
finally:
    dùin_lìonra(종단)
try:
    파일읽기("/없는파일")
except siostam_mearachd as Mearachd:
    assert Mearachd.INDEX == 2
    출력("한국어 faidhle 예외 dearbh")
else:
    raise AssertionError("faidhle 없음 예외가 필요합니다.")
