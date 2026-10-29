from Gaeilge import córas_earráid, 다시시도오류, 전문통신열기, 전문받기, dún_Líonra, 파일읽기, Aschur

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except córas_earráid as ERREÁID:
        assert ERREÁID.INDEX == 다시시도오류
        assert ERREÁID.설명 == "córas_oibriúcháin 작업에 실패했습니다."
        Aschur("Gaeilge 전문 eisceacht fíoraigh")
finally:
    dún_Líonra(종단)
try:
    파일읽기("/없는파일")
except córas_earráid as ERREÁID:
    assert ERREÁID.INDEX == 2
    Aschur("Gaeilge Comhad eisceacht fíoraigh")
else:
    raise AssertionError("Comhad 없음 예외가 필요합니다.")
