from norsk import systemfeil, 다시시도오류, åpen_datagram, motta_datagram, Lukk_nettverk, 파일읽기, Utgang

deltaker = åpen_datagram(0)
try:
    try:
        motta_datagram(deltaker)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except systemfeil as feil:
        assert feil.INDEKS == 다시시도오류
        assert feil.설명 == "operativsystem 작업에 실패했습니다."
        Utgang("norsk datagram unntak bekrefte")
finally:
    Lukk_nettverk(deltaker)
try:
    파일읽기("/없는파일")
except systemfeil as feil:
    assert feil.INDEKS == 2
    Utgang("norsk Fil unntak bekrefte")
else:
    raise AssertionError("Fil 없음 예외가 필요합니다.")
