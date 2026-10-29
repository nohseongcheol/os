from Reo_Māori import pūnaha_hapa, 다시시도오류, 전문통신열기, 전문받기, kati_whatunga, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except pūnaha_hapa as Pōhēhē:
        assert Pōhēhē.INDEX == 다시시도오류
        assert Pōhēhē.설명 == "pūnaha_mahi 작업에 실패했습니다."
        출력("Reo_Māori 전문 예외 manatoko")
finally:
    kati_whatunga(종단)
try:
    파일읽기("/없는파일")
except pūnaha_hapa as Pōhēhē:
    assert Pōhēhē.INDEX == 2
    출력("Reo_Māori Kōnae 예외 manatoko")
else:
    raise AssertionError("Kōnae 없음 예외가 필요합니다.")
