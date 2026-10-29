from Ikinyarwanda import sisitemu_ikosa, 다시시도오류, 전문통신열기, 전문받기, gufunga_Urusobemiyoboro, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except sisitemu_ikosa as IKOSA:
        assert IKOSA.umugerekashakiro == 다시시도오류
        assert IKOSA.설명 == "sisitemu_ngengamikorere 작업에 실패했습니다."
        출력("Ikinyarwanda 전문 예외 gusuzuma")
finally:
    gufunga_Urusobemiyoboro(종단)
try:
    파일읽기("/없는파일")
except sisitemu_ikosa as IKOSA:
    assert IKOSA.umugerekashakiro == 2
    출력("Ikinyarwanda Idosiye 예외 gusuzuma")
else:
    raise AssertionError("Idosiye 없음 예외가 필요합니다.")
