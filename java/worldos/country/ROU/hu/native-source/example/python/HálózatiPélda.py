from magyar import Kimenet, készít_datagram, küld_külső_datagram, fogad_datagram, bezár_hálózat, 밀리초
from magyar import rendszerhiba, 다시시도오류, kódolás_SMS, 명령인수, egész_szám
végpont = készít_datagram(0)
try:
    datagram = kódolás_SMS("PYTHON UDP hu")
    küld_külső_datagram(végpont, "10.0.2.2", egész_szám(명령인수[1]), datagram)
    Futtatás = 밀리초()
    while True:
        try:
            válasz, port_ÉRTÉK = fogad_datagram(végpont)
            break
        except rendszerhiba as HIBA:
            if HIBA.INDEX != 다시시도오류 or 밀리초() - Futtatás >= 700:
                raise
    assert válasz == datagram
    Kimenet("PYTHON 네트워크 igazol: UDP hu")
finally:
    bezár_hálózat(végpont)
