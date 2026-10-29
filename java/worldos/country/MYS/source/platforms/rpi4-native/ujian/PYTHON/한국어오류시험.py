from Melayu import sistem_ralat, 다시시도오류, 전문통신열기, 전문받기, Tutup_rangkaian, 파일읽기, 출력

peserta = 전문통신열기(0)
try:
    try:
        전문받기(peserta)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except sistem_ralat as RALAT:
        assert RALAT.INDEX == 다시시도오류
        assert RALAT.설명 == "sistem_pengendalian 작업에 실패했습니다."
        출력("Melayu 전문 pengecualian tentu_sahkan")
finally:
    Tutup_rangkaian(peserta)
try:
    파일읽기("/없는파일")
except sistem_ralat as RALAT:
    assert RALAT.INDEX == 2
    출력("Melayu Fail pengecualian tentu_sahkan")
else:
    raise AssertionError("Fail 없음 예외가 필요합니다.")
