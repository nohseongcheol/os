from Română import Rezultat, crea_diagramă_informații, trimite_extern_diagramă_informații, primi_diagramă_informații, închide_rețea, 밀리초
from Română import sistem_eroare, 다시시도오류, codifica_SMS, 명령인수, întreg
participant = crea_diagramă_informații(0)
try:
    diagramă_informații = codifica_SMS("PYTHON UDP ro")
    trimite_extern_diagramă_informații(participant, "10.0.2.2", întreg(명령인수[1]), diagramă_informații)
    Pornește = 밀리초()
    while True:
        try:
            replică, muta_VALUE = primi_diagramă_informații(participant)
            break
        except sistem_eroare as eroare:
            if eroare.INDEX != 다시시도오류 or 밀리초() - Pornește >= 700:
                raise
    assert replică == diagramă_informații
    Rezultat("PYTHON 네트워크 verifica: UDP ro")
finally:
    închide_rețea(participant)
