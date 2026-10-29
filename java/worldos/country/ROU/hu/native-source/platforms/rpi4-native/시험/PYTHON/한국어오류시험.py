from magyar import rendszerhiba, 다시시도오류, készít_datagram, fogad_datagram, bezár_hálózat, 파일읽기, Kimenet

végpont = készít_datagram(0)
try:
    try:
        fogad_datagram(végpont)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except rendszerhiba as HIBA:
        assert HIBA.INDEX == 다시시도오류
        assert HIBA.설명 == "operációs_rendszer 작업에 실패했습니다."
        Kimenet("magyar datagram kivétel igazol")
finally:
    bezár_hálózat(végpont)
try:
    파일읽기("/없는파일")
except rendszerhiba as HIBA:
    assert HIBA.INDEX == 2
    Kimenet("magyar Fájl kivétel igazol")
else:
    raise AssertionError("Fájl 없음 예외가 필요합니다.")
