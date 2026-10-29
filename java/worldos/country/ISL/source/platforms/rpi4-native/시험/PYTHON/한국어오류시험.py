from Íslenska import kerfi_villa, 다시시도오류, 전문통신열기, 전문받기, loka_Net, 파일읽기, úttak

endastöð = 전문통신열기(0)
try:
    try:
        전문받기(endastöð)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except kerfi_villa as Villa:
        assert Villa.INDEX == 다시시도오류
        assert Villa.설명 == "stýrikerfi 작업에 실패했습니다."
        úttak("Íslenska 전문 undantekning sannprófa")
finally:
    loka_Net(endastöð)
try:
    파일읽기("/없는파일")
except kerfi_villa as Villa:
    assert Villa.INDEX == 2
    úttak("Íslenska Skrá undantekning sannprófa")
else:
    raise AssertionError("Skrá 없음 예외가 필요합니다.")
