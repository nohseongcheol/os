from 한국어 import ètò_àṣìṣe, 다시시도오류, 전문통신열기, 전문받기, pa_dé_Alásopọ̀, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except ètò_àṣìṣe as àṣìṣe:
        assert àṣìṣe.wá_atọ̀ka_àkóónú == 다시시도오류
        assert àṣìṣe.설명 == "OS 작업에 실패했습니다."
        출력("한국어 전문 예외 ridájú")
finally:
    pa_dé_Alásopọ̀(종단)
try:
    파일읽기("/없는파일")
except ètò_àṣìṣe as àṣìṣe:
    assert àṣìṣe.wá_atọ̀ka_àkóónú == 2
    출력("한국어 Fáìlì 예외 ridájú")
else:
    raise AssertionError("Fáìlì 없음 예외가 필요합니다.")
