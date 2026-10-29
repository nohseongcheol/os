from Dansk import systemfejl, 다시시도오류, åben_datagram, modtage_datagram, Luk_netværk, 파일읽기, Udgang

slutpunkt = åben_datagram(0)
try:
    try:
        modtage_datagram(slutpunkt)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except systemfejl as fejl:
        assert fejl.INDEKS == 다시시도오류
        assert fejl.설명 == "operativsystem 작업에 실패했습니다."
        Udgang("Dansk datagram undtagelse bekræfte")
finally:
    Luk_netværk(slutpunkt)
try:
    파일읽기("/없는파일")
except systemfejl as fejl:
    assert fejl.INDEKS == 2
    Udgang("Dansk Fil undtagelse bekræfte")
else:
    raise AssertionError("Fil 없음 예외가 필요합니다.")
