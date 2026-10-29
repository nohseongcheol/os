from Galego import sistema_erro, 다시시도오류, 전문통신열기, 전문받기, peche_Rede, 파일읽기, Saída

extremo = 전문통신열기(0)
try:
    try:
        전문받기(extremo)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except sistema_erro as ERRO:
        assert ERRO.ÍNDICE == 다시시도오류
        assert ERRO.설명 == "sistema_operativo 작업에 실패했습니다."
        Saída("Galego 전문 excepción verificar")
finally:
    peche_Rede(extremo)
try:
    파일읽기("/없는파일")
except sistema_erro as ERRO:
    assert ERRO.ÍNDICE == 2
    Saída("Galego Ficheiro excepción verificar")
else:
    raise AssertionError("Ficheiro 없음 예외가 필요합니다.")
