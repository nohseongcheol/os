from Català import sistema_error, 다시시도오류, 전문통신열기, 전문받기, Tanca_xarxa, tancar_arxiu, Sortida

extrem = 전문통신열기(0)
try:
    try:
        전문받기(extrem)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except sistema_error as s_ha_produït_un_error:
        assert s_ha_produït_un_error.INDEX == 다시시도오류
        assert s_ha_produït_un_error.설명 == "sistema_operatiu 작업에 실패했습니다."
        Sortida("Català 전문 excepció verificar")
finally:
    Tanca_xarxa(extrem)
try:
    tancar_arxiu("/없는파일")
except sistema_error as s_ha_produït_un_error:
    assert s_ha_produït_un_error.INDEX == 2
    Sortida("Català Fitxer excepció verificar")
else:
    raise AssertionError("Fitxer 없음 예외가 필요합니다.")
