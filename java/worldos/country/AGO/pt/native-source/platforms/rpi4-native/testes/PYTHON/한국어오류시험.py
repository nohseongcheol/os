from Português import erro_do_sistema, 다시시도오류, abrir_datagrama, receber_datagrama, Close_rede, leitura_Arquivo, saídaTexto

empresa = abrir_datagrama(0)
try:
    try:
        receber_datagrama(empresa)
        raise AssertionError("비어 있는 datagrama 대기에서 예외가 필요합니다.")
    except erro_do_sistema as erro:
        assert erro.ÍNDICE == 다시시도오류
        assert erro.설명 == "SO 작업에 실패했습니다."
        saídaTexto("Português datagrama exceção verificar")
finally:
    Close_rede(empresa)
try:
    leitura_Arquivo("/없는파일")
except erro_do_sistema as erro:
    assert erro.ÍNDICE == 2
    saídaTexto("Português ficheiro exceção verificar")
else:
    raise AssertionError("ficheiro 없음 예외가 필요합니다.")
