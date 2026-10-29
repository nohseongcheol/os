from Italiano import uscitaTesto, aperto_datagramma, inviare_esterno_datagramma, ricevere_datagramma, Chiudi_rete, 밀리초
from Italiano import errore_di_sistema, 다시시도오류, codificare_SMS, 명령인수, intero
endpoint = aperto_datagramma(0)
try:
    datagramma = codificare_SMS("PYTHON UDP it")
    inviare_esterno_datagramma(endpoint, "10.0.2.2", intero(명령인수[1]), datagramma)
    avvia = 밀리초()
    while True:
        try:
            replica, porta_VALORE = ricevere_datagramma(endpoint)
            break
        except errore_di_sistema as errore:
            if errore.INDICE != 다시시도오류 or 밀리초() - avvia >= 700:
                raise
    assert replica == datagramma
    uscitaTesto("PYTHON 네트워크 verificare: UDP it")
finally:
    Chiudi_rete(endpoint)
