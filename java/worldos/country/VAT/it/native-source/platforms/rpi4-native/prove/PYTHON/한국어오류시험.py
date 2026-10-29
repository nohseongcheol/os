from Italiano import errore_di_sistema, 다시시도오류, aperto_datagramma, ricevere_datagramma, Chiudi_rete, 파일읽기, uscitaTesto

endpoint = aperto_datagramma(0)
try:
    try:
        ricevere_datagramma(endpoint)
        raise AssertionError("비어 있는 datagramma 대기에서 예외가 필요합니다.")
    except errore_di_sistema as errore:
        assert errore.INDICE == 다시시도오류
        assert errore.설명 == "sistema_operativo 작업에 실패했습니다."
        uscitaTesto("Italiano datagramma eccezione verificare")
finally:
    Chiudi_rete(endpoint)
try:
    파일읽기("/없는파일")
except errore_di_sistema as errore:
    assert errore.INDICE == 2
    uscitaTesto("Italiano file eccezione verificare")
else:
    raise AssertionError("file 없음 예외가 필요합니다.")
