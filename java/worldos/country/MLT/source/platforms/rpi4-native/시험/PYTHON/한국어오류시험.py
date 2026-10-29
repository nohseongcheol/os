from Malti import sistema_żball, 다시시도오류, 전문통신열기, 전문받기, agħlaq_netwerk, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except sistema_żball as żball:
        assert żball.INDEX == 다시시도오류
        assert żball.설명 == "sistema_operattiva 작업에 실패했습니다."
        출력("Malti 전문 예외 vverifika")
finally:
    agħlaq_netwerk(종단)
try:
    파일읽기("/없는파일")
except sistema_żball as żball:
    assert żball.INDEX == 2
    출력("Malti fajl 예외 vverifika")
else:
    raise AssertionError("fajl 없음 예외가 필요합니다.")
