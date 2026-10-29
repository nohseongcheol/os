from Nederlands import tekstuitvoer, open_datagram, e_mailen_extern_datagram, ontvangen_datagram, Sluiten_net, 밀리초
from Nederlands import systeemfout, 다시시도오류, coderen_sms, 명령인수, geheel_getal
eindpunt = open_datagram(0)
try:
    datagram = coderen_sms("PYTHON UDP nl")
    e_mailen_extern_datagram(eindpunt, "10.0.2.2", geheel_getal(명령인수[1]), datagram)
    starten = 밀리초()
    while True:
        try:
            reactie, poort_WAARDE = ontvangen_datagram(eindpunt)
            break
        except systeemfout as fout:
            if fout.INDEX != 다시시도오류 or 밀리초() - starten >= 700:
                raise
    assert reactie == datagram
    tekstuitvoer("PYTHON 네트워크 bevestigen: UDP nl")
finally:
    Sluiten_net(eindpunt)
